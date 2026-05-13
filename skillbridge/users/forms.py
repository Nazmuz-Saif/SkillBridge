from django import forms

from .models import FreelancerProfile
from .models import ClientProfile


class SignupForm(forms.Form):
    rolechoices = (('freelancer', 'Freelancer'),('client', 'Client'),)
    name = forms.CharField()
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput)
    role = forms.ChoiceField(choices=rolechoices)


class FreelancerProfileForm(forms.ModelForm):
    class Meta:
        model = FreelancerProfile
        fields = '__all__'


class ClientProfileForm(forms.ModelForm):
    class Meta:
        model = ClientProfile
        fields = '__all__'