from django.shortcuts import render, redirect
from django import template
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from django.urls import reverse
from django.contrib import messages
from django.http import JsonResponse
from django.db import connection

def pop_base_mCode(request):
    iCust = request.session.get('USER_ICUST')

    return render(request, "popup/pop_base_mCode.html")

def pop_base_mCode_search(request):
    mCode = request.POST.get('mCode')
    iCust = request.session.get('USER_ICUST')

    if mCode != '':
        with connection.cursor() as cursor:
            cursor.execute(" SELECT A.MCODE_M, B.RESNAM, A.ACODE, C.RESNAM, A.MCODE, A.MCODENM, A.MDESC "
                           " FROM OSCODEM A "
                           " LEFT OUTER JOIN OSREFCP B "
                           " ON A.MCODE_M = B.RESKEY "
                           " AND B.RECODE = 'MCD' "
                           " LEFT OUTER JOIN OSREFCP C "
                           " ON A.ACODE = C.RESKEY "
                           " AND C.RECODE = 'ACD' "
                           " WHERE A.ICUST = '" + str(iCust) + "' "
                           " AND A.MCODENM LIKE '%" + str(mCode) + "%' "
                           " ORDER BY A.MCODENM; ")
            coderesult = cursor.fetchall()

        return JsonResponse({"codeList": coderesult})

    if mCode == '':
        with connection.cursor() as cursor:
            cursor.execute(" SELECT A.MCODE_M, B.RESNAM, A.ACODE, C.RESNAM, A.MCODE, A.MCODENM, A.MDESC "
                           " FROM OSCODEM A "
                           " LEFT OUTER JOIN OSREFCP B "
                           " ON A.MCODE_M = B.RESKEY "
                           " AND B.RECODE = 'MCD' "
                           " LEFT OUTER JOIN OSREFCP C "
                           " ON A.ACODE = C.RESKEY "
                           " AND C.RECODE = 'ACD' "
                           " WHERE A.ICUST = '" + str(iCust) + "' "
                           " ORDER BY A.MCODENM; ")
            coderesult = cursor.fetchall()

        return JsonResponse({"codeList": coderesult})