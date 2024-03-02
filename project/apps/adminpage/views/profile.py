from django.shortcuts import render, redirect, HttpResponse
from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.models import User
from django.conf import settings

from apps.authentication.forms.profile import FormProfile, FormChangePassword, FormChangePasswordNew
from apps.authentication.models import Profile
from apps.services.session import setsession

import os





# =====================================================================================================
#                                               LOAD PAGE
# =====================================================================================================

def index(request):
    context = {}
    # ===[Load a CSS And JS File]===
    context['datatables']       = False
    context['tinydatepicker']   = False
    context['datetimepicker']   = False
    context['select2']          = False
    context['chosen']           = False
    context['dropzone']         = False
    context['summernote']       = False
    context['fullcalendar']     = False
    context['photoswipe']       = False
    context['maxlength']        = False
    context['inputmask']        = False
    context['moment']           = False
    context['duallistbox']      = False
    context['daterange']        = False
    context['countdown']        = False
    
    # ===[Fetch Data]===
    getprofile = Profile.objects.get(user=request.user)
    context['dataprofile'] = getprofile

    # ===[Load Form]===
    context['formprofile']      = FormProfile(request.POST or None, request.FILES or None, instance=getprofile)

    
    if request.user.password:
        # if the user already has a password
        context['formpassword']     = FormChangePassword(request.user, request.POST or None)
    else:
        # if the user doesn't have a password yet
        context['formpassword']     = FormChangePasswordNew(request.POST or None, instance=request.user)

    oldimage = str(getprofile.image)

    if request.POST:

        form = request.POST.get('form')
        if form in ['profile','password'] :
            if form == 'profile':
                if context['formprofile'].is_valid():
                    formprofile = context['formprofile'].save(commit=False)
                    formprofile.save()
                    newimage = str(formprofile.image)

                    oldpath = os.path.join(settings.MEDIA_ROOT, oldimage)
                    newpath = os.path.join(settings.MEDIA_ROOT, newimage)
                    if (oldimage != newimage and os.path.exists(oldpath)) or (request.POST.get('_setprofile_') and os.path.exists(oldpath)):
                        if os.path.isfile(oldpath):
                            os.remove(oldpath)
                            
                        if request.POST.get('_setprofile_'):
                            formprofile.image = ''
                            formprofile.save()
                            if os.path.isfile(newpath):
                                os.remove(newpath)
                    
                    setsession(request, request.user)
                    messages.success(request, 'Data has been saved')
                else:
                    messages.error(request, context['formprofile'].errors)

            else:          
                if context['formpassword'].is_valid():
                    # ===[If there is already a password]===
                    if request.user.password:
                        user = context['formpassword'].save()
                        update_session_auth_hash(request, user)
                        messages.success(request, 'Your password was successfully updated!')

                    # ===[if you log in using "cas" then there is no password]===
                    else:
                        if request.POST.get('password1') != request.POST.get('password2'):
                            messages.error(request, 'Confirm password is not the same.')
                        
                        elif len(request.POST.get('password1')) < 8:
                            messages.error(request, 'Your password must contain at least 8 characters.')

                        elif request.POST.get('password1').isnumeric():
                            messages.error(request, 'Your password cannot be entirely numeric.')
                        
                        else:
                            getuser = User.objects.get(username=request.user.username)
                            getuser.set_password(request.POST.get('password1'))
                            getuser.save()
                            messages.success(request, 'Your password was successfully updated!')

                else:
                    messages.error(request, context['formpassword'].errors)

        else:
            messages.success(request, 'There is an error')

        return redirect('adminpage:profile')
        
    # ===[Render Template]===
    return render(request, 'adminpage/profile.html', context)
