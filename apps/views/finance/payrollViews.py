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

# 임금대장
def payrollViews(request):

    return render(request, "finance/payroll-reg-sheet.html")

def payrollViews_search(request):
    modal = request.POST.get('modal')

    if modal:
        with connection.cursor() as cursor:
            cursor.execute(" SELECT ACNUMBER FROM ACNUMBER ORDER BY ACNUMBER ")
            cboAct = cursor.fetchall()

        with connection.cursor() as cursor:
            cursor.execute(" SELECT MCODE, MCODENM FROM OSCODEM ORDER BY MCODE ASC ")
            cboMCode = cursor.fetchall()

        return JsonResponse({"cboAct": cboAct, "cboMCode": cboMCode})

    else:
        with connection.cursor() as cursor:
            cursor.execute(" SELECT RESKEY, RESNAM FROM OSREFCP WHERE RECODE = 'PNM' ORDER BY CAST(RESKEY AS UNSIGNED ) ASC ")
            headresult = cursor.fetchall()

        with connection.cursor() as cursor:
            cursor.execute(" SELECT EMP_NBR, EMP_NME FROM PIS1TB001 WHERE EMP_TESA IS NULL OR EMP_TESA = ''; ")
            empresult = cursor.fetchall()

        return JsonResponse({"headList": headresult, "empList": empresult})