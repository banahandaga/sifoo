from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.utils.translation import gettext_lazy as _

class FormSignUp(UserCreationForm):
    first_name  = forms.CharField(max_length=30, required=False, help_text='Optional')
    last_name   = forms.CharField(max_length=30, required=False, help_text='Optional')
    email       = forms.CharField(max_length=100, help_text='Enter a valid email address')

    class Meta:
        model   = User
        fields  = ['username','first_name','last_name','email','password1','password2']


class FormSignIn(AuthenticationForm):
    error_messages = {
        "invalid_login": _(
            "Please enter a correct %(username)s and password. Note that both "
            "fields may be case-sensitive."
        ),
        "inactive": _("This account is inactive. Please check your email for account verification or contact admin!"),
    }
    class Meta:
        model   = User
        fields  = ['username','password']

  
class FormUserEdit(forms.ModelForm):
    username    = forms.CharField(max_length=30, required=False, help_text='Optional')
    first_name  = forms.CharField(max_length=30, required=False, help_text='Optional')
    last_name   = forms.CharField(max_length=30, required=False, help_text='Optional')
    email       = forms.CharField(max_length=100, required=False, help_text='Enter a valid email address')
    password1   = forms.CharField(max_length=30, required=False, help_text='Optional')
    password2   = forms.CharField(max_length=30, required=False, help_text='Optional')

    class Meta:
        model   = User
        fields  = ['username','first_name','last_name','email','password1','password2']