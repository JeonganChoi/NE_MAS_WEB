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

# 매입
def purTransSearchViews(request):

    return render(request, "finance/purchases-trans-report.html")

# 매출
def saleTransSearchViews(request):

    return render(request, "finance/sales-trans-report.html")


def purTransSearchViews_search(request):
    with connection.cursor() as cursor:
        cursor.execute(" SELECT IFNULL(ACDATE, ''), IFNULL(DAY(ACDATE), '') "
                       "    , IFNULL(SUM(ACAMTS), 0), IFNULL(ACIOGB, '') "
                       "    FROM OSBILL  "
                       "    WHERE ACIOGB = '2' "
                       "    GROUP BY DAY(ACDATE) ")
        mainresult = cursor.fetchall()

    return JsonResponse({"mainList": mainresult})

def saleTransSearchViews_search(request):
    with connection.cursor() as cursor:
        cursor.execute(" SELECT IFNULL(ACDATE, ''), IFNULL(DAY(ACDATE), '') "
                       "    , IFNULL(SUM(ACAMTS), 0), IFNULL(ACIOGB, '') "
                       "    FROM OSBILL  "
                       "    WHERE ACIOGB = '2' "
                       "    GROUP BY DAY(ACDATE) ")
        mainresult = cursor.fetchall()

    return JsonResponse({"mainList": mainresult})