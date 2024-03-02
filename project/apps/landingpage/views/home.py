from django.shortcuts import render, redirect, HttpResponse





# =====================================================================================================
#                                               LOAD PAGE
# =====================================================================================================

def error_404(request, exception):
  return render(request,'landingpage/error_404.html')

def home(request):
  return render(request, 'landingpage/index.html')