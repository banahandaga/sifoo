from django.urls import path, include
from apps.authentication.views import auth
from apps.services import djangocas
import django_cas_ng.views

app_name = 'authentication'

urlpatterns = [
  path('signin',      auth.signin,                               name='signin'),
  path('signout',     django_cas_ng.views.LogoutView.as_view(),  name='signout'),
  path('signup',      auth.signup,                               name='signup'),
  path('forgot',      auth.forgot,                               name='forgot'),
  path('verify',      auth.verify,                               name='verify'),

  path('login_cas',   djangocas.APILoginView.as_view(),           name='cas_ng_login'), # Custom Django CAS LOGIN
  # path('login_cas', django_cas_ng.views.LoginView.as_view(),    name='cas_ng_login'), # Default Django CAS Login
  path('logout_cas',  django_cas_ng.views.LogoutView.as_view(),   name='cas_ng_logout'),
  path('callback',    django_cas_ng.views.CallbackView.as_view(), name='cas_ng_proxy_callback'),
]