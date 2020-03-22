from django.contrib.auth.models import User
from socshare.models import Society
from django import forms

class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = ('username', 'email', 'password',)
        

class SocietyForm(forms.ModelForm):
    class Meta:
        model = Society
        fields = ('name', 'acronym',)
