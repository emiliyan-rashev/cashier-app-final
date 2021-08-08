from django.urls import path

from cashier.payments.views import PaymentsAdminView, PaymentTypes, MakePaymentView, PaySalaries

urlpatterns = [
    path('admin/', PaymentsAdminView.as_view(), name = 'payments_admin'),
    path('view/', PaymentTypes.as_view(), name = 'payment_types'),
    path('pay/', MakePaymentView.as_view(), name = 'make_payment'),
    path('salaries/', PaySalaries.as_view(), name = 'salaries_payment'),
]

import cashier.payments.signals