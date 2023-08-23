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

# 월별 자금 유동 현황
def receiptPaymentViews(request):

    return render(request, "currentstate/receipts-payments-sheet.html")

def receiptPaymentViews_search(request):
    date = request.POST.get('date')
    act = request.POST.get('act')
    cust = request.POST.get('cust')

    with connection.cursor() as cursor:
        cursor.execute(" SELECT CUST_NBR, CUST_NME FROM MIS1TB003 ORDER BY CUST_NBR ")
    cboCust = cursor.fetchall()

    with connection.cursor() as cursor:
        cursor.execute(" SELECT ACNUMBER FROM ACNUMBER ORDER BY ACNUMBER ")
    cboAct = cursor.fetchall()

    return JsonResponse({'cboCust': cboCust, 'cboAct': cboAct})