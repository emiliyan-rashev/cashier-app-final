from django import template

from cashier.payments.models import PaymentsAdmin

register = template.Library()

@register.inclusion_tag('payments/current_tax.html')
def tax_admin():
    tax_admin = PaymentsAdmin.objects.first()
    return {
            'tax_admin' : tax_admin
        }
