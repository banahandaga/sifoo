from django.http.response import JsonResponse, HttpResponseBadRequest
from django.shortcuts import render, redirect
from django.contrib import messages

from apps.services.utils import profilesync
from apps.services.session import setsession


def setprofilesync(request):
    if request.POST:
        user, is_success = profilesync(request.user)
        if is_success:
            setsession(request, user)
            # return JsonResponse({ 'status' : 'success', 'message' : 'Profile sync successful' })
            messages.success(request, 'Profile sync successful') 
        else:
            # return JsonResponse({ 'status' : 'error', 'message' : 'Failed to sync profile' }) 
            messages.error(request, 'Failed to sync profile')            
    else:        
        # return JsonResponse({ 'status' : 'error', 'message' : 'Failed to sync profile' })  
        messages.error(request, 'Failed to sync profile')      

    # ===[Redirect]===
    return redirect(request.META.get('HTTP_REFERER', 'adminpage:dashboard'))

