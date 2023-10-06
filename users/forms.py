from django.contrib.auth.forms import UserCreationForm
from users.models import CashierUser


class UserForm(UserCreationForm):
    class Meta:
        model = CashierUser
        fields = [
            "username",
        ]
