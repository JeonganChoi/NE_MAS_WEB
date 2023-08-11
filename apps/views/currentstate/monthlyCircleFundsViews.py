import json
from django.shortcuts import render, redirect
from django import template
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from django.urls import reverse
from django.contrib import messages
from django.http import JsonResponse
from django.db import connection

# 은행내역서
def montlyCircleFundsViews(request):

    return render(request, "currentstate/monthly-circulate-fundsReport.html")