from django import template

from payments.models import PaymentsAdmin

register = template.Library()


@register.inclusion_tag("payments/current_tax.html")
def tax_admin():
    return {"tax_admin": PaymentsAdmin.objects.first()}
