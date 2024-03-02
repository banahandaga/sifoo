from django.http.response import JsonResponse, HttpResponseBadRequest
from django.shortcuts import render, redirect, HttpResponse
from django.contrib import messages
from django.contrib.auth.models import User, Group
from django.urls import reverse
from django.db import transaction

from apps.services.decorators import group_required
from apps.authentication.models import Profile, GroupDetails
from apps.authentication.forms.auth import FormSignUp, FormUserEdit
from apps.authentication.forms.groupdetails import FormGroupDetails
from apps.authentication.forms.profile import FormProfile

from json import dumps





# =====================================================================================================
#                                               LOAD PAGE
# =====================================================================================================

@group_required('admin')
def table(request):
    context = {}
    # ===[Load a CSS And JS File]===
    context['datatables']       = True
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
    context['dataaccounts']    = User.objects.all().exclude(is_superuser=True).exclude(is_staff=True).order_by('id')
    
    
    # ===[Render Template]===
    return render(request, 'adminpage/account/table.html', context)



@group_required('admin')
def role(request):
    context = {}
    # ===[Load a CSS And JS File]===
    context['datatables']       = True
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


    # ===[Load Form]===
    context['datagroup']        = Group.objects.all()

    # ===[Fetch Data]===
    context['datauser']         = {}
    context['datagrouplist']    = {}
    getalluser                  = User.objects.all().exclude(is_staff=True).exclude(is_superuser=True)

    for user in getalluser:
        for group in user.groups.all():
            try:
                context['datagrouplist'][group.name] = group.groupdetails.alias
                context['datauser'][group.name].append({'user':user, 'group':group})
            except Exception as e:
                context['datagrouplist'][group.name] = group.groupdetails.alias
                context['datauser'][group.name] = [{'user':user, 'group':group}]

    # ===[Render Template]===
    return render(request, 'adminpage/account/role.html', context)



@group_required('admin')
def edit_group(request, id):
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

    # ===[Check ID IsValid]===
    try:
        getgroupdetails = GroupDetails.objects.get(group_id=id)
    except GroupDetails.DoesNotExist:
        messages.error(request, 'Data Not Found!')
        return redirect('adminpage:account_role')


    # ===[Load Form]===
    context['formgroupdetails']     = FormGroupDetails(request.POST or None, instance=getgroupdetails)


    # ===[Editt Logic]===
    if request.POST:
        if context['formgroupdetails'].is_valid():
            context['formgroupdetails'].save()

            messages.success(request, 'Data Edited Successfully', extra_tags=dumps({
                'redirect'      : reverse('adminpage:account_role'), 
                'confbtntxt'    : 'Check Data',
                'cnclbtntxt'    : 'Cancel',
            }))
            return redirect('adminpage:account_edit_group', id=id)
        else:
            messages.error(request, context['formgroupdetails'].errors)


    # ===[Render Template]===
    return render(request, 'adminpage/account/edit_group.html', context)



@group_required('admin')
def add(request):
    context = {}
    # ===[Load a CSS And JS File]===
    context['datatables']       = False
    context['tinydatepicker']   = False
    context['datetimepicker']   = False
    context['select2']          = True
    context['chosen']           = False
    context['dropzone']         = False
    context['summernote']       = False
    context['fullcalendar']     = False
    context['photoswipe']       = False
    context['maxlength']        = False
    context['inputmask']        = True
    context['moment']           = False
    context['duallistbox']      = True
    context['daterange']        = False
    context['countdown']        = False

    # ===[Load Form]===
    context['formsignup']       = FormSignUp(request.POST or None)
    context['formprofile']      = FormProfile(request.POST or None, request.FILES or None)

    # ===[Fetch Data]===
    context['groups']           = Group.objects.all()

    if request.POST:
        if context['formsignup'].is_valid():
            if context['formprofile'].is_valid():
                user = context['formsignup'].save()
                usergroups = request.POST.getlist('groups[]')
                user.groups.clear()
                user.groups.set(usergroups)
                user.save()

                profile = context['formprofile'].save(commit=False)
                profile.user = user
                profile.save()
                
                messages.success(request, 'Data Added Successfully', extra_tags=dumps({
                    'redirect'      : reverse('adminpage:account_table'), 
                    'confbtntxt'    : 'Check Data',
                    'cnclbtntxt'    : 'Cancel',
                }))
                return redirect('adminpage:account_add')
            else:
                messages.error(request, context['formprofile'].errors)
        else:
            messages.error(request, context['formsignup'].errors)
    
    
    # ===[Render Template]===
    return render(request, 'adminpage/account/add.html', context)



@group_required('admin')
def edit(request, id):
    context = {}
    # ===[Load a CSS And JS File]===
    context['datatables']       = False
    context['tinydatepicker']   = False
    context['datetimepicker']   = False
    context['select2']          = True
    context['chosen']           = False
    context['dropzone']         = False
    context['summernote']       = False
    context['fullcalendar']     = False
    context['photoswipe']       = False
    context['maxlength']        = False
    context['inputmask']        = True
    context['moment']           = False
    context['duallistbox']      = True
    context['daterange']        = False
    context['countdown']        = False
    

    # ===[Check ID IsValid]===
    try:
        user = User.objects.get(id=id)
        context['usergroups'] = user.groups.values_list('id',flat=True)
    except User.DoesNotExist:
        messages.error(request, 'Data Not Found!')
        return redirect('adminpage:account_table')

    # ===[Load Form]===
    context['formsignup']       = FormUserEdit(request.POST or None, instance=user)
    context['formprofile']      = FormProfile(request.POST or None, request.FILES or None, instance=user.profile)


    # ===[Fetch Data]===
    context['groups']           = Group.objects.all()


    # ===[Editt Logic]===
    if request.POST:

        if context['formsignup'].is_valid():
            if context['formprofile'].is_valid():
                user = context['formsignup'].save()
                profile = context['formprofile'].save(commit=False)
                profile.user = user
                profile.save()

                if request.POST.get('password1') and request.POST.get('password2'):
                    if request.POST.get('password1') != request.POST.get('password2'):
                        messages.error(request, 'Confirm password is not the same.')
                        return redirect('adminpage:account_edit', id=id)
                    
                    elif len(request.POST.get('password1')) < 8:
                        messages.error(request, 'Your password must contain at least 8 characters.')
                        return redirect('adminpage:account_edit', id=id)

                    elif request.POST.get('password1').isnumeric():
                        messages.error(request, 'Your password cannot be entirely numeric.')
                        return redirect('adminpage:account_edit', id=id)
                    
                    else:
                        user.set_password(request.POST.get('password1'))
                        user.save()



                usergroups = request.POST.getlist('groups[]')
                user.groups.clear()
                user.groups.set(usergroups)


                messages.success(request, 'Data Updated Successfully', extra_tags=dumps({
                    'redirect'      : reverse('adminpage:account_table'), 
                    'confbtntxt'    : 'Check Data',
                    'cnclbtntxt'    : 'Cancel',
                }))
                return redirect('adminpage:account_edit', id=id)
                
            else:
                messages.error(request, context['formprofile'].errors)
        else:
            messages.error(request, context['formsignup'].errors)

    # ===[Render Template]===
    return render(request, 'adminpage/account/edit.html', context)





# =====================================================================================================
#                                                SERVICE
# =====================================================================================================

@group_required('admin')
def deletelist(request):
    if request.POST and request.POST.getlist('list_id'):
        list_id = request.POST.getlist('list_id')
        try:
            with transaction.atomic():
                for id in list_id:
                    getprofile = Profile.objects.get(user__id=id)
                    getprofile.image.delete()
                    getprofile.user.delete()
                messages.success(request, 'Data Deleted Successfully')

        except User.DoesNotExist:
            messages.error(request, 'There is an error')

    else:
        messages.error(request, 'Invalid request!')

    # ===[Redirect]===
    return redirect('adminpage:account_table')



@group_required('admin')
def delrole(request, userid, groupid):
    try:
        user = User.objects.get(id=userid)
        user.groups.remove(groupid)
        messages.success(request, 'Data Updated Successfully')
        return redirect('adminpage:account_role')
    except User.DoesNotExist:
        messages.error(request, 'Data Not Found!')
        return redirect('adminpage:account_role')



@group_required('admin')
def setisactive(request, mode):
    if request.POST and request.POST.getlist('list_id'):
        list_id = request.POST.getlist('list_id')
        try:
            with transaction.atomic():
                for id in list_id:
                    getuser = User.objects.get(id=id)
                    if mode == 'active':
                        getuser.is_active = True
                    else:
                        getuser.is_active = False
                    getuser.save()
                messages.success(request, 'Data Updated Successfully')

        except User.DoesNotExist:
            messages.error(request, 'Data Not Found!')

    else:
        messages.error(request, 'Invalid request!')

    # ===[Redirect]===
    return redirect('adminpage:account_table')