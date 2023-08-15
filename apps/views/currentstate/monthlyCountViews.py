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

# 월별집계
def montlyCountViews(request):

    return render(request, "currentstate/monthly-countReport.html")

def montlyCountViews_search(request):
    strDate = request.POST.get('startDate')
    endDate = request.POST.get('endDate')

    # 매입/매출
    with connection.cursor() as cursor:
        cursor.execute(" SELECT RESKEY, RESNAM FROM OSREFCP WHERE RECODE = 'AGB' ")
        headerresult = cursor.fetchall()

    with connection.cursor() as cursor:
        cursor.execute(" SELECT A.OPT, B.MCODENM FROM OSBILL A LEFT OUTER JOIN OSCODEM B ON A.OPT = B.MCODE GROUP BY A.OPT, B.MCODENM ")
        headresult = cursor.fetchall()

    # 입금/출금
    with connection.cursor() as cursor:
        cursor.execute(" SELECT A.MCODE, B.MCODENM FROM SISACCTT A LEFT OUTER JOIN OSCODEM B ON A.MCODE = B.MCODE GROUP BY A.MCODE, B.MCODENM ")
        headresult2 = cursor.fetchall()

    return JsonResponse({"headerList": headerresult, "headList": headresult, 'headList2': headresult2})