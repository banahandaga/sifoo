from django.urls import path, include
from django.contrib.auth.decorators import login_required
from apps.adminpage.views import (
    services,
    profile,
    account,
    dashboard,
    category,
)

app_name = 'adminpage'

urlpatterns = [
  path('dashboard',                             login_required(dashboard.index),            name='dashboard'),
  path('service/setprofilesync',                login_required(services.setprofilesync),    name='setprofilesync'),
  path('profile',                               login_required(profile.index),              name='profile'),


  path('account/', include([
      # =================================================[ LOAD PAGE ]=================================================
      path('table',                             login_required(account.table),              name='account_table'),
      path('role',                              login_required(account.role),               name='account_role'),
      path('add',                               login_required(account.add),                name='account_add'),        
      path('edit/<int:id>',                     login_required(account.edit),               name='account_edit'),
      path('edit_group/<int:id>',               login_required(account.edit_group),         name='account_edit_group'),
      
      # ==================================================[ SERVICE ]==================================================
      path('delrole/<int:userid>/<int:groupid>',login_required(account.delrole),            name='account_delrole'),
      path('deletelist',                        login_required(account.deletelist),         name='account_deletelist'),
      path('setisactive/<str:mode>',            login_required(account.setisactive),        name='account_setisactive'),
  ])), 


  path('category/', include([
      # =================================================[ LOAD PAGE ]=================================================
      path('table',                             login_required(category.table),             name='category_table'),
      path('add',                               login_required(category.add),               name='category_add'),
      path('edit/<int:id>',                     login_required(category.edit),              name='category_edit'),

      # ==================================================[ SERVICE ]==================================================
      path('deletelist',                        login_required(category.deletelist),        name='category_deletelist'),
  ])),    
]