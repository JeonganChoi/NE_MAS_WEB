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

# 내역별
def nonPaymentView(request):

    return render(request, "currentstate/non-pay-get-sheet.html")

def nonPaymentView_search(request):
    strDate = request.POST.get('strDate').replace("-", "")
    endDate = request.POST.get('endDate').replace("-", "")
    creUser = request.session.get("userId")
    iCust = request.session.get("USER_ICUST")

    with connection.cursor() as cursor:
        cursor.execute(" SELECT IFNULL(AA.ACCUST, ''), IFNULL(AA.CUST_NME, ''), IFNULL(CASH, 0), IFNULL(INCASH, 0) FROM( "
                       " SELECT A.ACCUST, B.CUST_NME, SUM(IFNULL(A.ACAMTS, 0)) AS CASH, 0 AS INCASH FROM SISACCTT A "
                       " LEFT OUTER JOIN MIS1TB003 B ON A.ACCUST = B.CUST_NBR "
                       " WHERE A.MCODE LIKE '51%' AND A.ACGUBN = '2' AND A.ACDATE BETWEEN '" + str(strDate) + "' AND '" + str(endDate) + "' AND A.ICUST = '" + str(iCust) + "' "
                       " GROUP BY A.ACCUST, B.CUST_NME "
                       " UNION ALL "
                       " SELECT A.ACCUST, B.CUST_NME, 0 AS CASH, SUM(IFNULL(A.ACAMTS, 0)) AS INCASH FROM SISACCTT A "
                       " LEFT OUTER JOIN MIS1TB003 B ON A.ACCUST = B.CUST_NBR "
                       " WHERE A.MCODE LIKE '53%' AND A.ACDATE BETWEEN '" + str(strDate) + "' AND '" + str(endDate) + "' AND A.ICUST = '" + str(iCust) + "' "
                       " GROUP BY A.ACCUST, B.CUST_NME) AA GROUP BY AA.ACCUST, AA.CUST_NME, CASH, INCASH ")
        inresult = cursor.fetchall()

    with connection.cursor() as cursor:
        cursor.execute(" SELECT IFNULL(AA.ACCUST, ''), IFNULL(AA.CUST_NME, ''), IFNULL(CASH, 0), IFNULL(INCASH, 0) FROM( "
                       " SELECT A.ACCUST, B.CUST_NME, SUM(IFNULL(A.ACAMTS, 0)) AS CASH, 0 AS INCASH FROM SISACCTT A "
                       " LEFT OUTER JOIN MIS1TB003 B ON A.ACCUST = B.CUST_NBR "
                       " WHERE A.MCODE LIKE '41%' AND A.ACGUBN = '2' AND A.ACDATE BETWEEN '" + str(strDate) + "' AND '" + str(endDate) + "' AND A.ICUST = '" + str(iCust) + "' "
                       " GROUP BY A.ACCUST, B.CUST_NME "
                       " UNION ALL "
                       " SELECT A.ACCUST, B.CUST_NME, 0 AS CASH, SUM(IFNULL(A.ACAMTS, 0)) AS INCASH FROM SISACCTT A "
                       " LEFT OUTER JOIN MIS1TB003 B ON A.ACCUST = B.CUST_NBR "
                       " WHERE A.MCODE LIKE '43%' AND A.ACDATE BETWEEN '" + str(strDate) + "' AND '" + str(endDate) + "' AND A.ICUST = '" + str(iCust) + "' "
                       " GROUP BY A.ACCUST, B.CUST_NME) AA GROUP BY AA.ACCUST, AA.CUST_NME, CASH, INCASH ")
        outresult = cursor.fetchall()


    return JsonResponse({"inList": inresult, "outList": outresult})