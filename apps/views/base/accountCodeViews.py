from django.shortcuts import render, redirect
from django import template
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from django.urls import reverse
from django.http import JsonResponse
from django.db import connection

def accountCodeViews(request):

    return render(request, "base/base-accountCode.html")

def accountCodeViews_search(request):
    mainCode = request.POST.get('mainCode')
    mainCode2 = request.POST.get('mainCode2')

    if mainCode != '' and mainCode is not None:
        with connection.cursor() as cursor:
            cursor.execute(" SELECT MCODE, MCODENM, MDESC FROM OSCODEM WHERE MCODE = '" + mainCode + "' ")
            mresult = cursor.fetchall()

        return JsonResponse({"subMList": mresult})

    elif mainCode2 != '' and mainCode2 is not None:
        with connection.cursor() as cursor:
            cursor.execute(" SELECT ACODE, ACODENM, ADESC FROM OSCODEA WHERE ACODE = '" + mainCode2 + "' ")
            aresult = cursor.fetchall()

        return JsonResponse({'subAList': aresult})

    else:
        with connection.cursor() as cursor:
            cursor.execute(" SELECT MCODE, MCODENM FROM OSCODEM ORDER BY MCODE ")
            mresult = cursor.fetchall()

        with connection.cursor() as cursor:
            cursor.execute(" SELECT ACODE, ACODENM FROM OSCODEA ORDER BY ACODE ")
            aresult = cursor.fetchall()

        return JsonResponse({"mList": mresult, 'aList': aresult})