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


def custBalRegViews(request):

    return render(request, "finance/custBalance-reg.html")

def custBalRegViews_search(request):
    startDate = request.POST.get('startDate')
    endDate = request.POST.get('endDate')
    custCode = request.POST.get('custCode')

    with connection.cursor() as cursor:
        cursor.execute(
            " SELECT IFNULL(A.MOdate,''), IFNULL(A.MOCUST, ''), IFNULL(B.CUST_NME,'') "
            "    , IFNULL(A.MOIWOL, 0), IFNULL(A.MOIWOL2, 0), IFNULL(A.MODESC, ''), IFNULL(B.CUST_GBN, '')"
            "    FROM SIOMONTT A "
            "    LEFT OUTER JOIN MIS1TB003 B "
            "    ON A.MOCUST = B.CUST_NBR "
            "    WHERE CUST_GBN = '1' OR CUST_GBN = '2' OR CUST_GBN = '3' "
            "    AND MOdate BETWEEN '" + startDate + "' AND '" + endDate + "' "
            "    AND MOCUST LIKE '%" + custCode + "%'"
            "    ORDER BY A.MOdate ")

        custBalresult = cursor.fetchall()

    # 거래처 - 콤보박스
    with connection.cursor() as cursor:
        cursor.execute(" SELECT CUST_NBR, CUST_NME, CUST_GBN FROM MIS1TB003 "
                       "        WHERE CUST_GBN = '1' "
                       "        OR CUST_GBN = '2' "
                       "        OR CUST_GBN = '3' ")
        inputCustType = cursor.fetchall()

    return JsonResponse({"inputCustType": inputCustType, "custBalList": custBalresult})