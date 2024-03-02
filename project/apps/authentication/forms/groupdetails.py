from django import forms
from apps.authentication.models import GroupDetails
from django.utils.translation import gettext_lazy as _

class FormGroupDetails(forms.ModelForm):
    class Meta:
        model   = GroupDetails
        fields  = ['alias','description']
        labels  = {
            'alias'       : _('Alias'),
            'description' : _('Deskripsi'),
        }
