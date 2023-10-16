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
def permitViews(request):

    return render(request, "finance/permit-reg.html")


def permitViews_search(request):
    perDate = request.POST.get('perDate')
    custCode = request.POST.get('custCode')
    offSet = request.POST.get('offSet')
    user = request.session.get('userId')
    iCust = request.session.get('USER_ICUST')

    if offSet and custCode:
        with connection.cursor() as cursor:
            cursor.execute("  SELECT IFNULL(A.IODATE, ''), IFNULL(A.ACTITLE, ''), IFNULL(A.ACAMTS, '') "
                           "        , IFNULL(A.CRE_USER, ''), IFNULL(C.EMP_NME, ''), IFNULL(A.ACSEQN, ''), IFNULL(A.ACIOGB, '')"
                           "        , IFNULL(A.MCODE, ''), IFNULL(D.MCODENM, '') "
                           " FROM SISACCTT A "
                           " LEFT OUTER JOIN OSSIGN B "
                           " ON A.IODATE = B.ACDATE "
                           " AND A.ACSEQN = B.ACSEQN "
                           " AND A.ICUST = B.ICUST "
                           " AND NOT EXISTS (SELECT OPT FROM OSSIGN WHERE OPT = 'N') "
                           " LEFT OUTER JOIN PIS1TB001 C "
                           " ON A.CRE_USER = C.EMP_NBR "
                           " LEFT OUTER JOIN OSCODEM D "
                           " ON A.MCODE = D.MCODE "
                           " WHERE B.EMP_NBR = '" + user + "' "
                           " AND B.ACDATE <= '" + perDate + "' "
                           " AND A.ACCUST = '" + custCode + "' "
                           " AND A.OFF_GBN = 'off'"
                           " AND A.ICUST = '" + iCust + "' "
                           " ORDER BY A.ACSEQN ASC ")
            mainresult = cursor.fetchall()

        return JsonResponse({"mainList": mainresult})

    elif custCode:
        with connection.cursor() as cursor:
            cursor.execute("  SELECT IFNULL(A.IODATE, ''), IFNULL(A.ACTITLE, ''), IFNULL(A.ACAMTS, '') "
                           "        , IFNULL(A.CRE_USER, ''), IFNULL(C.EMP_NME, ''), IFNULL(A.ACSEQN, ''), IFNULL(A.ACIOGB, '')"
                           "        , IFNULL(A.MCODE, ''), IFNULL(D.MCODENM, '') "
                           " FROM SISACCTT A "
                           " LEFT OUTER JOIN OSSIGN B "
                           " ON A.IODATE = B.ACDATE "
                           " AND A.ACSEQN = B.ACSEQN "
                           " AND A.ICUST = B.ICUST "
                           " AND NOT EXISTS (SELECT OPT FROM OSSIGN WHERE OPT = 'N') "
                           " LEFT OUTER JOIN PIS1TB001 C "
                           " ON A.CRE_USER = C.EMP_NBR "
                           " LEFT OUTER JOIN OSCODEM D "
                           " ON A.MCODE = D.MCODE "
                           " WHERE B.EMP_NBR = '" + user + "' "
                           " AND B.ACDATE <= '" + perDate + "' "
                           " AND A.ACCUST = '" + custCode + "' "
                           " AND A.ICUST = '" + iCust + "' "
                           " ORDER BY A.ACSEQN ASC ")
            mainresult = cursor.fetchall()

        return JsonResponse({"mainList": mainresult})

    elif offSet:
        with connection.cursor() as cursor:
            cursor.execute("  SELECT IFNULL(A.IODATE, ''), IFNULL(A.ACTITLE, ''), IFNULL(A.ACAMTS, '') "
                           "        , IFNULL(A.CRE_USER, ''), IFNULL(C.EMP_NME, ''), IFNULL(A.ACSEQN, ''), IFNULL(A.ACIOGB, '')"
                           "        , IFNULL(A.MCODE, ''), IFNULL(D.MCODENM, '') "
                           " FROM SISACCTT A "
                           " LEFT OUTER JOIN OSSIGN B "
                           " ON A.IODATE = B.ACDATE "
                           " AND A.ACSEQN = B.ACSEQN "
                           " AND A.ICUST = B.ICUST "
                           " AND NOT EXISTS (SELECT OPT FROM OSSIGN WHERE OPT = 'N') "
                           " LEFT OUTER JOIN PIS1TB001 C "
                           " ON A.CRE_USER = C.EMP_NBR "
                           " LEFT OUTER JOIN OSCODEM D "
                           " ON A.MCODE = D.MCODE "
                           " WHERE B.EMP_NBR = '" + user + "' "
                           " AND B.ACDATE <= '" + perDate + "' "
                           " AND A.OFF_GBN = 'off'"
                           " AND A.ICUST = '" + iCust + "' "
                           " ORDER BY A.ACSEQN ASC ")
            mainresult = cursor.fetchall()

        return JsonResponse({"mainList": mainresult})

    else:
        with connection.cursor() as cursor:
            cursor.execute("  SELECT IFNULL(A.IODATE, ''), IFNULL(A.ACTITLE, ''), IFNULL(A.ACAMTS, '') "
                           "        , IFNULL(A.CRE_USER, ''), IFNULL(C.EMP_NME, ''), IFNULL(A.ACSEQN, ''), IFNULL(A.ACIOGB, '')"
                           "        , IFNULL(A.MCODE, ''), IFNULL(D.MCODENM, '') "
                           " FROM SISACCTT A "
                           " LEFT OUTER JOIN OSSIGN B "
                           " ON A.IODATE = B.ACDATE "
                           " AND A.ACSEQN = B.ACSEQN "
                           " AND A.ICUST = B.ICUST "
                           " AND NOT EXISTS (SELECT OPT FROM OSSIGN WHERE OPT = 'N') "
                           " LEFT OUTER JOIN PIS1TB001 C "
                           " ON A.CRE_USER = C.EMP_NBR "
                           " LEFT OUTER JOIN OSCODEM D "
                           " ON A.MCODE = D.MCODE "
                           " WHERE B.EMP_NBR = '" + user + "' "
                           " AND B.ACDATE <= '" + perDate + "' "
                           " AND A.ICUST = '" + iCust + "' "
                           " ORDER BY A.ACSEQN ASC ")
            mainresult = cursor.fetchall()

        with connection.cursor() as cursor:
            cursor.execute(" SELECT CUST_NBR, CUST_NME FROM MIS1TB003 WHERE ICUST = '" + iCust + "'")
            cboCust = cursor.fetchall()

        with connection.cursor() as cursor:
            cursor.execute(" SELECT ACNUMBER FROM ACNUMBER WHERE ICUST = '" + iCust + "'")
            cboAct = cursor.fetchall()

        return JsonResponse({"mainList": mainresult, "cboCust": cboCust, "cboAct": cboAct})


def cboActNum_search(request):
    user = request.session.get('userId')
    iCust = request.session.get('USER_ICUST')

    with connection.cursor() as cursor:
        cursor.execute(" SELECT ACNUMBER, ACNUM_NAME FROM ACNUMBER WHERE ICUST = '" + iCust + "' ORDER BY ACNUMBER ")
        cboActNum = cursor.fetchall()

        return JsonResponse({'cboActNum': cboActNum})

def permitViews_save(request):
    pmtArray = json.loads(request.POST.get('pmtArrList'))
    iCust = request.session.get('USER_ICUST')
    permit = 'Y'


    pmtArrayLists = list(filter(len, pmtArray))
    for data in range(len(pmtArrayLists)):
        with connection.cursor() as cursor:
            cursor.execute(" UPDATE SISACCTT SET "
                           "    ACDATE = '" + pmtArrayLists[data]["ioDate"] + "'"
                           "  , FIN_OPT = '" + permit + "' "
                           "  , ACACNUMBER = '" + pmtArrayLists[data]["acNum"] + "' "
                           "     WHERE IODATE = '" + pmtArrayLists[data]["ioDate"] + "' "
                           "     AND ACIOGB = '" + pmtArrayLists[data]["acIogb"] + "' "
                           "     AND ACSEQN = '" + pmtArrayLists[data]["acSeqn"] + "' "
                           "     AND ICUST = '" + iCust + "' "
            )
            connection.commit()

    return JsonResponse({'sucYn': "Y"})