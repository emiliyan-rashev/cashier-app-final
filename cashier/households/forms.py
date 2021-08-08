from django import forms

from cashier.households.models import HouseholdProfile

class HouseholdProfileForm(forms.ModelForm):
    class Meta:
        model = HouseholdProfile
        fields = ('apartment_percent_ideal_parts',)

class UserApproveForm(forms.Form):
    approve = forms.BooleanField(required=False)

