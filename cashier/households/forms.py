from django import forms

from cashier.households.models import HouseholdProfile

class HouseholdProfileForm(forms.ModelForm):
    class Meta:
        model = HouseholdProfile
        fields = ('apartment_percent_ideal_parts',)


