from django.shortcuts import render
from django.shortcuts import redirect



def root_redirect(request):
    return redirect("accounts:login")