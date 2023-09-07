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

# 감가상각비명세서
def depreciationViews(request):

    return render(request, "finance/depreciation-reg-sheet.html")

def dptViews_search(request):
    yymm = request.POST.get('yymm')
    yymm = yymm + '00'

    with connection.cursor() as cursor:
        cursor.execute(" SELECT IFNULL(A.FIX_NO, ''), IFNULL(A.FIX_NME, ''), IFNULL(A.FIX_GRD, ''), IFNULL(A.FIX_QTY, 0)"
                       "    , IFNULL(A.FIX_GDATE, ''), IFNULL(A.FIX_YEARS, ''), IFNULL(A.FIX_GAMTS, 0) "
                       "    , IFNULL(B.FIX_FUND, 0), IFNULL(B.FIX_REPAY, 0), IFNULL(B.FIX_TAXC, 0) "
                       "    FROM OSREPAY A "
                       "    LEFT OUTER JOIN OSREPAY_D B "
                       "    ON A.FIX_NO = B.FIX_NO "
                       "    WHERE B.FIX_YYMM = '" + yymm + "' ")
        mainresult = cursor.fetchall()

    return JsonResponse({"mainList": mainresult})