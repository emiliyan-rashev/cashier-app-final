import datetime
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import UpdateView
from django.views.generic.base import View
from django.forms import models as model_forms
from cashier.payments.models import PaymentsAdmin, IndividualPayment
from cashier.profiles.models import UserProfile


class PaymentsAdminView(UpdateView):
    model = PaymentsAdmin
    fields = ('individual_monthly_tax', 'salaries')
    template_name = 'admin_payments.html'
    def get_object(self, queryset=None):
        return self.model.objects.first()

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
    template_name = 'make_payment.html'
    success_url = reverse_lazy('home_view')

class UserPaymentsView(View):
    def get(self, request):
        context = {

        }
        return render(request=self.request, template_name='view_user_payments.html', context=context)