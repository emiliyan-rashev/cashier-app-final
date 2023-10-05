from django import forms

from cashier.households.models import HouseholdProfile


class HouseholdProfileForm(forms.ModelForm):
    class Meta:
        model = HouseholdProfile
        fields = ("apartment_percent_ideal_parts",)


class UserApproveForm(forms.Form):
    CHOICES = [("Approve", "Approve"), ("Reject", "Reject")]
    approval = forms.ChoiceField(label="", choices=CHOICES, widget=forms.RadioSelect)
