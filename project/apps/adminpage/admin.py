from django.contrib import admin
from apps.adminpage.models import *

# Register your models here.

class AdminCategory(admin.ModelAdmin):
    list_display = ('id', 'name', 'description')

admin.site.register(Category, AdminCategory)