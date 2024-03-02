from django.shortcuts import render
from apps.services.decorators import group_required
from django.contrib import messages
from django.urls import reverse
from json import dumps





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


    # Example Notification
    # extra_tags is optional, used in the notif function located in -> (apps\adminpage\templates\adminpage\layout\javascript.html)

    # messages.success(request, 'Welcome to Dashboard', extra_tags=dumps({
    #     'redirect'      : reverse('adminpage:dashboard'), 
    #     'confbtntxt'    : 'Check Data',
    #     'cnclbtntxt'    : 'Cancel',
    #     'title'         : 'Welcome',
    # }))


    # ===[Render Template]===
    return render(request, 'adminpage/index.html', context)
