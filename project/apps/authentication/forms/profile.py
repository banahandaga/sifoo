from django import forms
from apps.authentication.models import Profile
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.models import User

class FormProfile(forms.ModelForm):
    nip         = forms.CharField(max_length=20, required=False, help_text='Optional')
    nidn        = forms.CharField(max_length=50, required=False, help_text='Optional')
    surelluar   = forms.CharField(max_length=100, required=False, help_text='Optional')
    nomorhp     = forms.CharField(max_length=15, required=False, help_text='Optional')
    image       = forms.ImageField(max_length=255, required=False, help_text='Optional')

    class Meta:
        model   = Profile
        fields  = ['nip', 'nidn', 'surelluar', 'nomorhp', 'image']
        labels  = {
            'nip'       : _('NIP'),
            'nidn'      : _('NIDN'),
            'surelluar' : _('SURELLUAR'),
            'nomorhp'   : _('NOMORHP'),
            'image'     : _('IMAGE'),
        }

class FormChangePassword(PasswordChangeForm):
    def __init__(self, *args, **kwargs):
        super(FormChangePassword, self).__init__(*args, **kwargs)
        for field in ('old_password', 'new_password1', 'new_password2'):
            self.fields[field].widget.attrs = {'class': 'form-control'}


class FormChangePasswordNew(forms.ModelForm):
    password1 = forms.CharField(label='Password', widget=forms.PasswordInput, max_length=20)
    password2 = forms.CharField(label='Repeat Password', widget=forms.PasswordInput, max_length=20)

    class Meta:
        model   = User
        fields  = ('password1', 'password2')
        labels  = {
            'password1' : _('Password'),
            'password2' : _('Password confirmation'),
        }