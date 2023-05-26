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


def purchaseRegViews(request):

    return render(request, "finance/purchases-reg.html")

def purchaseRegViews_search(request):
    strDate = request.POST.get('strDate')
    endDate = request.POST.get('endDate')

    with connection.cursor() as cursor:
        cursor.execute(" SELECT A.TRDATE, A.TRSEQN, A.TRRECN, A.TRITEM, C.ITNAME, A.TRRCID, D.RESNAM"
                       "    , A.TROTP, E.RESNAM, A.TRPRCE, A.TRQTYS, A.TRAMTS"
                       "    , A.TRVATS, A.TRDESC, A.TRCUST, B.CUST_NME "
                       "    FROM OSTRNSP A "
                       "    LEFT OUTER JOIN MIS1TB003 B "
                       "    ON A.TRCUST = B.CUST_NBR "
                       "    LEFT OUTER JOIN OSITITEM C "
                       "    ON A.TRITEM = C.ITITEM"
                       "    LEFT OUTER JOIN OSREFCP D "
                       "    ON A.TRRCID = D.RESKEY "
                       "    AND D.RECODE = 'IPG' "
                       "    LEFT OUTER JOIN OSREFCP E "
                       "    ON A.TROTP = E.RESKEY "
                       "    AND E.RECODE = 'OUB'"
                       "    WHERE TRDATE BETWEEN '" + strDate + "' AND '" + endDate + "' "
                       "    ORDER BY TRDATE "
                       )

        buyresult = cursor.fetchall()
    return JsonResponse({"buyList": buyresult})