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
def approvalViews(request):

    return render(request, "finance/approval-reg.html")

def approvalViews_search(request):
    empNbr = request.POST.get('empNbr')
    gbn = request.POST.get('gbn')
    iCust = request.POST.get('iCust')
    ioDate = request.POST.get('ioDate')
    acSeqn = request.POST.get('acSeqn')

    with connection.cursor() as cursor:
        cursor.execute(" SELECT EMP_NBR, EMP_NME, ICUST FROM PIS1TB001 WHERE EMP_NBR = '" + empNbr + "' AND ICUST = '" + iCust + "' ")
        empresult = cursor.fetchall()

    if gbn:
        with connection.cursor() as cursor:
            cursor.execute(" SELECT IFNULL(A.MCODE_M, ''), IFNULL(D.RESNAM, ''), IFNULL(A.MCODE, ''), IFNULL(A.MCODENM, ''), IFNULL(A.MDESC, ''), IFNULL(A.MSEQ, '')"
                           "    , IFNULL(A.GBN, ''), IFNULL(B.RESNAM, ''), IFNULL(A.GBN2, ''), IFNULL(C.RESNAM, ''), IFNULL(A.ACODE, ''), IFNULL(E.RESNAM, '') "
                           "    FROM OSCODEM A "
                           "    LEFT OUTER JOIN OSREFCP B "
                           "    ON A.GBN = B.RESKEY "
                           "    AND B.RECODE = 'CGB' "
                           "    LEFT OUTER JOIN OSREFCP C "
                           "    ON A.GBN2 = C.RESKEY "
                           "    AND C.RECODE = 'AGB' "
                           "    LEFT OUTER JOIN OSREFCP D "
                           "    ON A.MCODE_M = D.RESKEY "
                           "    AND D.RECODE = 'MCD' "
                           "    LEFT OUTER JOIN OSREFCP E "
                           "    ON A.ACODE = E.RESKEY "
                           "    AND E.RECODE = 'ACD' "
                           "    WHERE MCODE = '" + gbn + "' ")
            mainresult = cursor.fetchall()

        return JsonResponse({"mainList": mainresult})

    if ioDate and acSeqn:
        with connection.cursor() as cursor:
            cursor.execute(" SELECT A.SEQ, A.EMP_NBR, B.EMP_NME, B.EMP_FOLDER "
                           " FROM OSSIGN A "
                           " LEFT OUTER JOIN PIS1TB001 B "
                           " ON A.EMP_NBR = B.EMP_NBR "
                           " WHERE A.ACDATE = '" + str(ioDate) + "' "
                           " AND A.ACSEQN = '" + str(acSeqn) + "' "
                           " ORDER BY SEQ ASC ")
            subresult = cursor.fetchall()

        return JsonResponse({"subList": subresult})