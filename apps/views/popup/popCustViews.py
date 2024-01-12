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

def pop_base_cust(request):
    iCust = request.session.get('USER_ICUST')

    return render(request, "popup/pop_base_cust.html")


def pop_base_cust_search(request):
    custCode = request.POST.get('custCode')
    iCust = request.session.get('USER_ICUST')

    if custCode != '':
        with connection.cursor() as cursor:
            cursor.execute(" SELECT IFNULL(A.CUST_NBR, ''), IFNULL(A.CUST_NME, ''), IFNULL(A.CUST_GBN, ''), IFNULL(D.RESNAM, '') "
                           "   FROM MIS1TB003 A "
                           "   LEFT OUTER JOIN OSREFCP D "
                           "   ON A.CUST_GBN = D.RESKEY "
                           "   AND D.RECODE = 'BGB' "
                           "   WHERE A.ICUST = '" + str(iCust) + "' "
                           "     AND A.CUST_NBR LIKE '%" + str(custCode) + "%' "
                           "      OR A.CUST_NME LIKE '%" + str(custCode) + "%'")
            custresult = cursor.fetchall()

        return JsonResponse({"custList": custresult})