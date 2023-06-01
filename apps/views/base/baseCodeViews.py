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


def baseCodeViews(request):

    return render(request, "base/base-code.html")

def baseCodeViews_search(request):
    mainCode = request.POST.get('mainCode')

    if mainCode is not None and mainCode != '':
        with connection.cursor() as cursor:
            cursor.execute(" SELECT RECODE, RECNAM, RESKEY, RESNAM FROM OSREFCP "
                           "        WHERE RECODE LIKE '%" + mainCode + "%'")
            subresult = cursor.fetchall()

        return JsonResponse({"subList": subresult})

    else:
        with connection.cursor() as cursor:
            cursor.execute(" SELECT RECODE, RECNAM FROM OSREFCP "
                           "        GROUP BY RECODE, RECNAM "
                           "        ORDER BY RECODE ")
            mainresult = cursor.fetchall()

        return JsonResponse({"mainList": mainresult})