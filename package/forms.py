from django.contrib.auth.models import User
from django import forms
from .models import Package


class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['username', 'email', 'password']


class PackageForm(forms.ModelForm):

    class Meta:
        model = Package
        fields = ['tracking_num', 'package_type', 'package_company', 'staff_company', 'staff_price']

