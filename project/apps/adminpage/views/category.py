from django.shortcuts import render, redirect
from django.contrib import messages
from django.urls import reverse
from django.db import transaction

from apps.services.decorators import group_required
from apps.adminpage.models import Category
from apps.adminpage.forms import FormCategory

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
    context['datacategory']     = Category.objects.all()

    # ===[Render Template]===
    return render(request, 'adminpage/category/table.html', context)



@group_required('admin')
def add(request):
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

    # ===[Load Form]===
    context['formcategory']     = FormCategory(request.POST or None, request.FILES or None)


    # ===[Insert Logic]===
    if request.POST:
        if context['formcategory'].is_valid():
            context['formcategory'].save()
            messages.success(request, 'Data Added Successfully', extra_tags=dumps({
                'redirect'      : reverse('adminpage:category_table'), 
                'confbtntxt'    : 'Check Data',
                'cnclbtntxt'    : 'Cancel',
            }))
            return redirect('adminpage:category_add')
        else:
            messages.error(request, context['formcategory'].errors)
    
    
    # ===[Render Template]===
    return render(request, 'adminpage/category/add.html', context)



@group_required('admin')
def edit(request, id):
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
        getcategory = Category.objects.get(id=id)
    except Category.DoesNotExist:
        messages.error(request, 'Data Not Found!')
        return redirect('adminpage:category_table')


    # ===[Load Form]===
    context['formcategory']     = FormCategory(request.POST or None, instance=getcategory)


    # ===[Edit Logic]===
    if request.POST:
        if context['formcategory'].is_valid():
            context['formcategory'].save()

            messages.success(request, 'Data Edited Successfully', extra_tags=dumps({
                'redirect'      : reverse('adminpage:category_table'), 
                'confbtntxt'    : 'Check Data',
                'cnclbtntxt'    : 'Cancel',
            }))
            return redirect('adminpage:category_edit', id=id)
        else:
            messages.error(request, context['formcategory'].errors)


    # ===[Render Template]===
    return render(request, 'adminpage/category/edit.html', context)





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
                    Category.objects.get(id=id).delete()
                messages.success(request, 'Data Deleted Successfully')

        except Category.DoesNotExist:
            messages.error(request, 'There is an error')
    else:
        messages.error(request, 'Invalid request!')

    # ===[Redirect]===
    return redirect('adminpage:category_table')