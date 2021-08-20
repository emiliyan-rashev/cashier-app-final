from django.core.exceptions import ValidationError


def validate_integer(value):
    if not value.isdigit():
        raise ValidationError(
            _('%(value)s is not a number'),
            params={'value': value},
        )