from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import UpdateView
from django.views.generic.base import View
from django.forms import models as model_forms
from cashier.payments.models import PaymentsAdmin, IndividualPayment, TaxesPerMonth, SalariesPayment, SalariesPerMonth, \
    IndividualTaxesPayed
from cashier.profiles.models import UserProfile

class PaymentsAdminView(UpdateView):
    model = PaymentsAdmin
    fields = ('individual_monthly_tax', 'salaries')
    template_name = 'admin_payments.html'
    def get_object(self, queryset=None):
        return self.model.objects.first()
    success_url = reverse_lazy('home_view')

class PaySalaries(UpdateView):
    model = SalariesPayment
    def get_object(self, queryset=None):
        return self.model.objects.get(pk=1)
    def get_form_class(self):
        self.fields = [str(curr_field.name) for curr_field in self.model._meta.get_fields() if not curr_field.value_from_object(self.model.objects.get(pk=1))]
        return model_forms.modelform_factory(self.model, fields=self.fields)
    def get_context_data(self, **kwargs):
        if 'form' not in kwargs:
            kwargs['form'] = self.get_form()
        tax_object = SalariesPerMonth.objects.first()
        tax_info = [(curr_field.name, curr_field.value_from_object(tax_object), curr_field.name not in self.fields) for curr_field in tax_object._meta.get_fields() if curr_field.name != 'id']
        if 'tax_info' not in kwargs:
            kwargs['tax_info'] = tax_info
        return super().get_context_data(**kwargs)
    template_name = 'salaries_payment.html'
    success_url = reverse_lazy('home_view')

class PaymentTypes(View):
    def get(self, request):
        is_hh_admin = UserProfile.objects.get(pk=self.request.user.id).is_household_admin
        context = {
            'is_hh_admin' : is_hh_admin,
        }
        return render(request=self.request, template_name='view_payments.html', context=context)

class MakePaymentView(UpdateView):
    model = IndividualPayment
    def get_object(self, queryset=None):
        return self.model.objects.get(pk=self.request.user.id)
    def get_form_class(self):
        self.fields = [str(curr_field.name) for curr_field in self.model._meta.get_fields() if not curr_field.value_from_object(self.model.objects.get(pk=self.request.user.pk))]
        return model_forms.modelform_factory(self.model, fields=self.fields)
    def get_context_data(self, **kwargs):
        if 'form' not in kwargs:
            kwargs['form'] = self.get_form()
        tax_object = TaxesPerMonth.objects.first()
        month_keys = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']
        payed_object = IndividualTaxesPayed.objects.get(pk=self.request.user.pk)
        taxes_payed_per_month = {curr_field.name: curr_field.value_from_object(payed_object) for curr_field in payed_object._meta.get_fields() if curr_field.name in month_keys}
        tax_info = [(curr_field.name, curr_field.value_from_object(tax_object), taxes_payed_per_month[curr_field.name]) for curr_field in tax_object._meta.get_fields() if curr_field.name in month_keys]
        tax_info.append(['Total', sum([curr_value[1] for curr_value in tax_info]), sum([curr_value[2] for curr_value in tax_info])])
        if 'tax_info' not in kwargs:
            kwargs['tax_info'] = tax_info
        return super().get_context_data(**kwargs)
    template_name = 'make_payment.html'
    success_url = reverse_lazy('home_view')