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
    Year = request.POST.get('Year')

    with connection.cursor() as cursor:
        cursor.execute(" SELECT IFNULL(A.ITEM, ''), IFNULL(A.UP_CODE, ''), IFNULL(B.CUST_NME, '')"
                       "    , IFNULL(A.GUBUN, ''), IFNULL(A.DANGA, ''), IFNULL(SUM(A.QTY), 0)"
                       "    , IFNULL(SUM(A.SUPPLY), 0), IFNULL(SUM(A.AMTS), 0), IFNULL(DATE_FORMAT(BAL_DD, '%Y%m'), '')"
                       "    , IFNULL(SUM(ACAMTS), 0), IFNULL(ACIOGB, '') "
                       "    FROM OSBILL A  "
                       "    LEFT OUTER JOIN MIS1TB003 B "
                       "    ON A.UP_CODE = B.CUST_NBR "
                       "    WHERE GUBUN = '2' "
                       "    AND YEAR(BAL_DD) = '" + Year + "' "
                       "    GROUP BY A.ITEM, A.UP_CODE, A.DANGA, A.GUBUN, DATE_FORMAT(BAL_DD, '%Y%m') "
                       "    ORDER BY A.ITEM, A.UP_CODE, A.DANGA, A.GUBUN, DATE_FORMAT(BAL_DD, '%Y%m') ")

        mainresult = cursor.fetchall()

    return JsonResponse({"mainList": mainresult})


def custLedgerViews(request):

    return render(request, "finance/custledger-report.html")

def custLedgerViews_search(request):
    Year = request.POST.get('Year')

    with connection.cursor() as cursor:
        cursor.execute(" SELECT IFNULL(A.ITEM, ''), IFNULL(A.UP_CODE, ''), IFNULL(B.CUST_NME, '')"
                       "    , IFNULL(A.GUBUN, ''), IFNULL(A.DANGA, ''), IFNULL(SUM(A.QTY), 0)"
                       "    , IFNULL(SUM(A.SUPPLY), 0), IFNULL(SUM(A.AMTS), 0), IFNULL(DATE_FORMAT(BAL_DD, '%Y%m'), '')"
                       "    , IFNULL(SUM(ACAMTS), 0), IFNULL(ACIOGB, '') "
                       "    FROM OSBILL A  "
                       "    LEFT OUTER JOIN MIS1TB003 B "
                       "    ON A.UP_CODE = B.CUST_NBR "
                       "    WHERE GUBUN = '2' "
                       "    AND YEAR(BAL_DD) = '" + Year + "' "
                       "    GROUP BY A.ITEM, A.UP_CODE, A.DANGA, A.GUBUN, DATE_FORMAT(BAL_DD, '%Y%m') "
                       "    ORDER BY A.ITEM, A.UP_CODE, A.DANGA, A.GUBUN, DATE_FORMAT(BAL_DD, '%Y%m') ")

        mainresult = cursor.fetchall()

    return JsonResponse({"mainList": mainresult})