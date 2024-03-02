# =========================================
# Created by Ridwan Renaldi, S.Kom. (rr867)
# =========================================
from django.contrib.auth.models import User

def setsession(request, user: User) -> User:
    request.session.set_expiry(7200)
    request.session['user'] = {
        'username'      : user.username,
        'first_name'    : user.first_name,
        'last_name'     : user.last_name,
        'email'         : user.email,
        'is_superuser'  : user.is_superuser,
        'is_staff'      : user.is_staff,
        'date_joined'   : user.date_joined.strftime("%Y:%m:%d %H:M:S") if user.date_joined else user.date_joined,
        'last_login'    : user.last_login.strftime("%Y:%m:%d %H:M:S") if user.last_login else user.last_login,
        'image'         : user.profile.image_url(),
        'fullname'      : user.get_full_name(),
        'groups'        : list(user.groups.values_list('groupdetails__alias',flat=True)),
    }

    if request.session['user']['fullname'] == '':
        request.session['user']['fullname'] = user.username

    return user