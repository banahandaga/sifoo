# =========================================
# Created by Ridwan Renaldi, S.Kom. (rr867)
# =========================================
from django.conf import settings
from django.contrib.auth.models import User
from django.core.mail import send_mail, EmailMessage
from django.utils.crypto import get_random_string
from django.template.loader import render_to_string

from apps.services.apigateway import apigateway
from apps.services.apistar import apistar
from django.urls import reverse



def profilesync(user) -> User:
    try:
        username = user.username
    except:
        username = user
    

    user, created   = User.objects.get_or_create(username = username)
    if created:
        print('Create a new user {}'.format(username))
    profile         = apigateway.get('umar/v3/profil?uniid=%s' % (username))
    is_success      = False # If successful in getting data from the API


    # check if he is an employee
    if profile['status'] and profile['data'] :
        is_success = True
        
        if type(profile['data']) == list:
            data = profile['data'][0]
        else:
            data = profile['data']

        if data['nip']:
            user.profile.nip        = data['nip']

        if data['nidn']:
            user.profile.nidn       = data['nidn']

        if data['nomorhp']:
            user.profile.nomorhp    = data['nomorhp']

        if data['is_dosen']:
            user.profile.is_dosen   = data['is_dosen']

        if data['home_id']:
            user.profile.home_id    = data['home_id']

        if data['homebase']:
            user.profile.homebase   = data['homebase']

        if data['fname']:
            user.first_name         = data['fname']

        if data['lname']:    
            user.last_name          = data['lname']   

        if data['surelluar']:        
            user.email              = data['surelluar']



    # otherwise it means he is a student
    else :
        is_success = False

        # use apistar to check if he is a student here
        if hasattr(settings,'API_STAR_URL') and hasattr(settings,'API_STAR_USERNAME') and hasattr(settings,'API_STAR_PASSWORD') and settings.API_STAR_URL and settings.API_STAR_USERNAME and settings.API_STAR_PASSWORD:
            getmhs = apistar.getMhsProfile(username)
            if getmhs and getmhs['success'] and str(getmhs['success']).lower() != 'false':
                is_success = True
            else:
                getmhs = False

        else:
            # ===[GET DATA MAHASISWA WITHOUT AUTH]===
            getmhs = apistar.getMhsProfileWithoutAuth(username)
            if getmhs and getmhs['success'] and str(getmhs['success']).lower() != 'false':
                is_success = True
            else:
                getmhs = False
        

        # If successful in getting student data from the API
        if getmhs:
            name            = getmhs['Nama']
            namelist        = name.split(' ')

            if len(namelist) == 0 :
                first_name = None
                last_name = None
            else:
                first_name = namelist[0]
                last_name = namelist[1:len(namelist)]

                if len(last_name) == 0 :
                    last_name = None
                else:
                    last_name = ' '.join(last_name)

            user.first_name = first_name
            user.last_name = last_name


    user.save()
    user.profile.save()
    return user, is_success



def send_otp_by_email(user: User, viewname) -> User:
    user.profile.otp = get_random_string(16)
    user.save()

    data = {                
        'name'                      : user.username,    
        'url'                       : settings.APP_BASE_URL+reverse(viewname)+'?email='+user.email+'&otp='+user.profile.otp,          
        # 'url'                       : settings.APP_BASE_URL+'/authentication/verify?email='+user.email+'&otp='+user.profile.otp,
        'staticurl'                 : settings.APP_BASE_URL+settings.STATIC_URL,
        'APP_SHORT_NAME'            : settings.APP_SHORT_NAME,
        'APP_COMPANY_SHORT_NAME'    : settings.APP_COMPANY_SHORT_NAME,
        'APP_YEAR'                  : settings.APP_YEAR,
    }

    message = render_to_string('authentication/verify_email.html', data)

    return send_mail(
        subject = 'Your email needs to be verified', 
        message = message, 
        from_email = settings.EMAIL_HOST_USER, 
        recipient_list = [user.email], 
        fail_silently=False, 
        html_message = message
    )



def username_in_cas(username:str) -> bool:
    '''
    Check if the username has been registered in the cas account
    return TRUE if the username is already registered in cas
    return FALSE if the username has not been registered with cas
    '''

    getuser = apigateway.get('umar/v3/profil?uniid=%s' % (username))
    if getuser['status'] :
        return True
    else :
        if hasattr(settings,'API_STAR_URL') and hasattr(settings,'API_STAR_USERNAME') and hasattr(settings,'API_STAR_PASSWORD') and settings.API_STAR_URL and settings.API_STAR_USERNAME and settings.API_STAR_PASSWORD:
            getuser = apistar.getMhsProfile(username)
            if getuser and getuser['success'] and str(getuser['success']).lower() != 'false':
                return True
            else:
                return False
            
        else:
            getuser = apistar.getMhsProfileWithoutAuth(username)
            if getuser and getuser['success'] and str(getuser['success']).lower() != 'false':
                return True
            else:
                return False