from django import forms
from apps.adminpage.models import Category
from django.utils.translation import gettext_lazy as _

class FormCategory(forms.ModelForm):
  class Meta:
    model   = Category
    fields  = '__all__'
    labels  = {
      'name'        : _('Name'),
      'description' : _('Description'),
    }
