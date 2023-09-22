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
    empNbr = request.session.get('userId')
    gbn = request.POST.get('gbn')
    iCust = request.session.get('USER_ICUST')
    ioDate = request.POST.get('ioDate')
    acSeqn = request.POST.get('acSeqn')
    acIogb = request.POST.get('acIogb')

    if ioDate and acSeqn:
        with connection.cursor() as cursor:
            cursor.execute(" SELECT A.SEQ, A.EMP_NBR, B.EMP_NME, B.EMP_FOLDER, A.ACDATE, A.ACSEQN, A.ACIOGB "
                           " FROM OSSIGN A "
                           " LEFT OUTER JOIN PIS1TB001 B "
                           " ON A.EMP_NBR = B.EMP_NBR "
                           " WHERE A.ACDATE = '" + str(ioDate) + "' "
                           " AND A.ACSEQN = '" + str(acSeqn) + "' "
                           " AND A.ACIOGB = '" + str(acIogb) + "' "
                           " ORDER BY SEQ ASC ")
            subresult = cursor.fetchall()

        with connection.cursor() as cursor:
            cursor.execute(" SELECT IFNULL(A.ACIOGB, ''), IFNULL(A.ACTITLE, ''), IFNULL(A.ACCUST, ''), IFNULL(A.IODATE, ''), IFNULL(A.MCODE, '') "
                           "        , IFNULL(A.EXDATE, ''), IFNULL(A.ACAMTS, ''), IFNULL(A.ACACNUMBER, ''), IFNULL(A.ACGUBN, ''), IFNULL(A.ACCARD, '') "
                           "        , IFNULL(A.ACDESC, ''), IFNULL(A.ACSEQN, '') "
                           " FROM SISACCTT A "
                           " WHERE A.IODATE = '" + str(ioDate) + "' "
                           " AND A.ACSEQN = '" + str(acSeqn) + "' "
                           " AND A.ACIOGB = '" + str(acIogb) + "' ")
            mainresult = cursor.fetchall()

            # 거래처
        with connection.cursor() as cursor:
            cursor.execute(" SELECT CUST_NBR, CUST_NME FROM MIS1TB003 ")
            cboCust = cursor.fetchall()

            # 입출금구분
        with connection.cursor() as cursor:
            cursor.execute(" SELECT RESKEY, RESNAM FROM OSREFCP WHERE RECODE = 'OUA' ORDER BY RESKEY ")
            cboGgn = cursor.fetchall()

            # 관리계정
        with connection.cursor() as cursor:
            cursor.execute(" SELECT MCODE, MCODENM FROM OSCODEM ORDER BY MCODE ASC ")
            cboMCode = cursor.fetchall()

            # 결제방법
        with connection.cursor() as cursor:
            cursor.execute(" SELECT RESKEY, RESNAM FROM OSREFCP WHERE RECODE = 'PGB' ORDER BY RESNAM ")
            cboPay = cursor.fetchall()

            # 계좌번호
        with connection.cursor() as cursor:
            cursor.execute(" SELECT ACNUMBER FROM ACNUMBER ")
            cboAcnumber = cursor.fetchall()

        return JsonResponse({"subList": subresult, "mainList": mainresult, "cboCust": cboCust, "cboGgn": cboGgn, "cboMCode": cboMCode, "cboPay": cboPay, "cboAcnumber": cboAcnumber})

    else:
        with connection.cursor() as cursor:
            cursor.execute(" SELECT IFNULL(A.IODATE, ''), IFNULL(A.ACTITLE, ''), IFNULL(A.ACAMTS, '')"
                           "        , IFNULL(A.CRE_USER, ''), IFNULL(C.EMP_NME, ''), IFNULL(A.ACSEQN, ''), IFNULL(A.ACIOGB, '')  "
                           " FROM SISACCTT A "
                           " LEFT OUTER JOIN OSSIGN B "
                           " ON A.IODATE = B.ACDATE "
                           " AND A.ACSEQN = B.ACSEQN "
                           " AND A.ICUST = B.ICUST "
                           " LEFT OUTER JOIN PIS1TB001 C "
                           " ON A.CRE_USER = C.EMP_NBR "
                           " WHERE B.EMP_NBR = '" + empNbr + "' "
                           " AND B.ACDATE <= '" + str(ioDate) + "' ")
            mainresult = cursor.fetchall()

        return JsonResponse({"mainList": mainresult})

def approvalViews_save(request):
    seq = request.POST.get("seq")
    empNbr = request.POST.get("empNbr")
    folder = request.POST.get("folder")
    reason = request.POST.get("reason")
    ioDate = request.POST.get("empNbr")
    acSeqn = request.POST.get("acSeqn")
    acIogb = request.POST.get("acIogb")
    iCust = request.session.get('USER_ICUST')
    gbn = request.POST.get('gbn')
    opt = 'Y'

    if gbn == '1':
        with connection.cursor() as cursor:
            cursor.execute("    UPDATE OSSIGN SET "
                               "     OPT = '" + str(opt) + "' "
                               "   , GBN = '" + str(gbn) + "' "
                               "     WHERE ACDATE = '" + str(ioDate) + "' "
                               "     AND ACSEQN = '" + str(acSeqn) + "' "
                               "     AND SEQ = '" + str(seq) + "' "
                               "     AND EMP_NBR = '" + str(empNbr) + "' "
                               "     AND ACIOGB = '" + str(acIogb) + "' "
                               "     AND ICUST = '" + str(iCust) + "'"
                               )
            connection.commit()

        return JsonResponse({'sucYn': "Y"})

    elif gbn == '2':
        with connection.cursor() as cursor:
            cursor.execute("    UPDATE OSSIGN SET "
                               "     OPT = '" + str(opt) + "' "
                               "   , GBN = '" + str(gbn) + "' "
                               "     WHERE ACDATE = '" + str(ioDate) + "' "
                               "     AND ACSEQN = '" + str(acSeqn) + "' "
                               "     AND SEQ = '" + str(seq) + "' "
                               "     AND EMP_NBR = '" + str(empNbr) + "' "
                               "     AND ACIOGB = '" + str(acIogb) + "' "
                               "     AND ICUST = '" + str(iCust) + "'"
                               )
            connection.commit()

        return JsonResponse({'sucYn': "Y"})

    elif gbn == '3':
        with connection.cursor() as cursor:
            cursor.execute("    UPDATE OSSIGN SET "
                               "     RETURN = '" + str(reason) + "' "
                               "   , OPT = '" + str(opt) + "' "
                               "   , GBN = '" + str(gbn) + "' "
                               "     WHERE ACDATE = '" + str(ioDate) + "' "
                               "     AND ACSEQN = '" + str(acSeqn) + "' "
                               "     AND SEQ = '" + str(seq) + "' "
                               "     AND EMP_NBR = '" + str(empNbr) + "' "
                               "     AND ACIOGB = '" + str(acIogb) + "' "
                               "     AND ICUST = '" + str(iCust) + "'"
                               )
            connection.commit()

        return JsonResponse({'sucYn': "Y"})