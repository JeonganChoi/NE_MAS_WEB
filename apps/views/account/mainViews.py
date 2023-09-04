from django.shortcuts import render, redirect
from django import template
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from django.urls import reverse


def index(request):

    return render(request, "home/index.html")

def redirectToMain(request):

    return redirect("home")

# def redirectToLogin(request):
#
#     return redirect("login")
#
# def login(request):
#
#     return render(request, "account/login.html")