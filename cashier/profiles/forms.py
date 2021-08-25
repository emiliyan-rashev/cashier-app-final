from django import forms
from cashier.profiles.models import UserProfile


class EditProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = '__all__'
        exclude = ['user','is_household_admin','household']


class DeleteProfileForm(forms.Form):
    CHOICES = [('Delete', 'Delete'),
               ('Cancel', 'Cancel')]
    result = forms.ChoiceField(label="", choices=CHOICES, widget=forms.RadioSelect)