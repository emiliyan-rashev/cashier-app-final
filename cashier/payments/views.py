from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import UpdateView
from django.views.generic.base import View
from django.forms import models as model_forms

from cashier.mixins.form_bootstrap import BootStrapFormMixin
from cashier.mixins.mixins import OwnerOrHouseholdAdminOrSuperUserRequiredMixin, SuperUserRequiredMixin
from cashier.payments.models import PaymentsAdmin, IndividualPayment, TaxesPerMonth, SalariesPayment, SalariesPerMonth, \
    IndividualTaxesPayed, SalariesPayedPerMonth
from cashier.profiles.models import UserProfile


class PaymentsAdminView(SuperUserRequiredMixin, BootStrapFormMixin, UpdateView):
    model = PaymentsAdmin
    fields = ('individual_monthly_tax', 'salaries')
    template_name = 'payments/admin_payments.html'
    def get_object(self, queryset=None):
        return self.model.objects.first()
    success_url = reverse_lazy('payment_types')

class PaySalaries(SuperUserRequiredMixin, BootStrapFormMixin, UpdateView):
    model = SalariesPayment
    template_name = 'payments/salaries_payment.html'
    success_url = reverse_lazy('salaries_payment')

    def get_object(self, queryset=None):
        return self.model.objects.get(pk=1)
    def get_form_class(self):
        self.object = self.get_object()
        self.fields = [str(curr_field.name) for curr_field in self.model._meta.get_fields() if not curr_field.value_from_object(self.model.objects.get(pk=1))]
        return model_forms.modelform_factory(self.model, fields=self.fields)
    def get_context_data(self, **kwargs):
        if 'form' not in kwargs:
            kwargs['form'] = self.get_form()
        tax_object = SalariesPerMonth.objects.first()
        month_keys = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']
        payed_object = SalariesPayedPerMonth.objects.get(pk=1)
        taxes_payed_per_month = {curr_field.name: curr_field.value_from_object(payed_object) for curr_field in payed_object._meta.get_fields() if curr_field.name in month_keys}
        tax_info = [(curr_field.name, curr_field.value_from_object(tax_object), taxes_payed_per_month[curr_field.name]) for curr_field in tax_object._meta.get_fields() if curr_field.name in month_keys]

        if 'tax_info' not in kwargs:
            kwargs['tax_info'] = tax_info
        if 'total_taxes_needed' not in kwargs:
            kwargs['total_taxes_needed'] = sum([curr_value[1] for curr_value in tax_info])
        if 'total_taxes_paid' not in kwargs:
            kwargs['total_taxes_paid'] = sum([curr_value[2] for curr_value in tax_info])

        return super().get_context_data(**kwargs)


class PaymentTypes(LoginRequiredMixin, View):
    def get(self, request):
        is_hh_admin = UserProfile.objects.get(pk=self.request.user.id).is_household_admin
        apartment = UserProfile.objects.get(pk=self.request.user.id).apartment
        context = {
            'is_hh_admin' : is_hh_admin,
            'apartment' : apartment,
        }
        return render(request=self.request, template_name='payments/view_payments.html', context=context)

class MakePaymentView(OwnerOrHouseholdAdminOrSuperUserRequiredMixin, BootStrapFormMixin, UpdateView):
    model = IndividualPayment
    def get_form_class(self):
        #get the object again, because the pre_init signal wouldn't work... very very sad (with FBV it was working properly)
        self.object = self.get_object()
        self.fields = [str(curr_field.name) for curr_field in self.model._meta.get_fields() if not (curr_field.value_from_object(self.object))]
        return model_forms.modelform_factory(self.model, fields=self.fields)
    def get_context_data(self, **kwargs):
        pk = self.kwargs.get(self.pk_url_kwarg)
        if 'form' not in kwargs:
            kwargs['form'] = self.get_form()
        tax_object = TaxesPerMonth.objects.first()
        month_keys = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']
        payed_object = IndividualTaxesPayed.objects.get(pk=pk)
        taxes_payed_per_month = {curr_field.name: curr_field.value_from_object(payed_object) for curr_field in payed_object._meta.get_fields() if curr_field.name in month_keys}
        tax_info = [(curr_field.name, curr_field.value_from_object(tax_object), taxes_payed_per_month[curr_field.name]) for curr_field in tax_object._meta.get_fields() if curr_field.name in month_keys]
        tax_info.append(['Total', sum([curr_value[1] for curr_value in tax_info]), sum([curr_value[2] for curr_value in tax_info])])
        if 'tax_info' not in kwargs:
            kwargs['tax_info'] = tax_info
        if 'profile_owner' not in kwargs:
            kwargs['profile_owner'] = UserProfile.objects.get(pk=pk).user
        return super().get_context_data(**kwargs)
    template_name = 'payments/make_payment.html'
    def get_success_url(self):
        return reverse_lazy('make_payment', kwargs={'pk': self.kwargs.get(self.pk_url_kwarg)})