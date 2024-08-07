import json
import os
from wsgiref.util import FileWrapper
import zipfile
from django.shortcuts import render, redirect
from django import template
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect, FileResponse
from django.template import loader
from django.urls import reverse
from django.contrib import messages
from django.http import JsonResponse
from django.db import connection
from django.core.files.storage import FileSystemStorage
from urllib.parse import quote
from django.conf import settings


# 출금-수불장
def withRegNewViews(request):
    userId = request.session.get('userId')
    if userId == '' or userId is None:
        return redirect("/page-404/")
    else:
        return render(request, "finance/withdraw-reg-sheet.html")

def chkDate(request):
    method = request.POST.get('method')
    cardNum = request.POST.get('cardNum')
    custCode = request.POST.get('custCode')
    creUser = request.session.get("userId")
    iCust = request.session.get("USER_ICUST")

    if method == '2' and custCode != '':
        with connection.cursor() as cursor:
            cursor.execute(" SELECT CUST_PAY_DAY, CUST_PAY FROM MIS1TB003 WHERE CUST_NBR = '" + str(custCode) + "' AND ICUST = '" + str(iCust) + "'")
        chkDate = cursor.fetchall()

        with connection.cursor() as cursor:
            cursor.execute(" SELECT CUST_BKCD FROM MIS1TB003_D WHERE CUST_NBR = '" + str(custCode) + "' AND ICUST = '" + str(iCust) + "' ")
        chkBank = cursor.fetchall()

        with connection.cursor() as cursor:
            cursor.execute(" SELECT CUST_ACNUM FROM MIS1TB003_D WHERE CUST_NBR = '" + str(custCode) + "' AND ICUST = '" + str(iCust) + "' ")
        chkAct = cursor.fetchall()

        return JsonResponse({'chkDate': chkDate, "chkBank": chkBank, "chkAct": chkAct})

    if method == '3' and cardNum != '' or method == '4' and cardNum != '':
        with connection.cursor() as cursor:
            cursor.execute(" SELECT ACPAYDTE FROM ACCARD WHERE CARDNUM = '" + str(cardNum) + "' AND ICUST = '" + str(iCust) + "'")
        chkDate = cursor.fetchall()
        return JsonResponse({'chkDate': chkDate})


def cboBank_search(request):
    inputBank = request.POST.get('inputBank')
    creUser = request.session.get("userId")
    iCust = request.session.get("USER_ICUST")

    with connection.cursor() as cursor:
        cursor.execute(" SELECT ACNUMBER FROM ACNUMBER WHERE ACBKCD = '" + str(inputBank) + "' AND ICUST = '" + str(iCust) + "'")
    cboAct = cursor.fetchall()

    return JsonResponse({'cboAct': cboAct})

def chkEmp_Sign(request):
    acDate = request.POST.get('acDate')
    acIogb = request.POST.get('acIogb')
    acSeqn = request.POST.get('acSeqn')
    creUser = request.session.get("userId")
    iCust = request.session.get("USER_ICUST")

    if acDate != '':
        with connection.cursor() as cursor:
            cursor.execute(" SELECT A.EMP_NBR, B.EMP_NME FROM OSSIGN A LEFT OUTER JOIN PIS1TB001 B ON A.EMP_NBR = B.EMP_NBR "
                           "     WHERE A.ICUST = '" + str(iCust) + "' AND A.ACDATE = '" + str(acDate) + "' AND A.ACSEQN = '" + str(acSeqn) + "' AND A.ACIOGB = '" + str(acIogb) + "'  "
                           "     AND A.SEQ = (SELECT IFNULL(MAX(SEQ), '') FROM OSSIGN WHERE ICUST = '" + str(iCust) + "' AND ACDATE = '" + str(acDate) + "' AND ACSEQN = '" + str(acSeqn) + "' AND ACIOGB = '" + str(acIogb) + "' AND OPT = 'Y'); ")
            chkEmp = cursor.fetchall()

            return JsonResponse({'chkEmp': chkEmp})



def chkCustYn(request):
    txtCustName = request.POST.get('txtCustName')
    iCust = request.session.get("USER_ICUST")

    if txtCustName != '':
        with connection.cursor() as cursor:
            cursor.execute(" SELECT COUNT(CUST_NBR) AS COUNTED FROM MIS1TB003 WHERE ICUST = '" + str(iCust) + "' AND CUST_NME LIKE '%" + str(txtCustName) + "%';")
            result = cursor.fetchall()
            count = result[0][0]
        # 여러개의 거래처가 조회되었을때.
        if count > 1:
            custYn = 'N'
            return JsonResponse({'custYn': custYn})

        # 여러개의 1개만 조회되었을때.
        elif count == 1:
            with connection.cursor() as cursor:
                cursor.execute(" SELECT CUST_NBR AS COUNTED FROM MIS1TB003 WHERE ICUST = '" + str(iCust) + "' AND CUST_NME LIKE '%" + str(txtCustName) + "%'; ")
                result2 = cursor.fetchall()
                custYn = result2[0][0]
            return JsonResponse({'custYn': custYn})

        else:
            custYn = 'N'
            return JsonResponse({'custYn': custYn})

# def receivePayByGbn(request):
#     strDate = request.POST.get('sDate')
#     endDate = request.POST.get('eDate')
#     inputGbn = request.POST.get('inputGbn')
#     creUser = request.session.get("userId")
#     iCust = request.session.get("USER_ICUST")
#
#     if inputGbn != '':
#         # 시행
#         if inputGbn == '0':
#             with connection.cursor() as cursor:
#                 cursor.execute(" SELECT IFNULL(SUM(BAL), 0), IFNULL(SUM(INTOTAL), 0), IFNULL(SUM(OUTTOTAL), 0), IFNULL(SUM(BAL + INTOTAL - OUTTOTAL), 0) FROM "
#                                " ("
#                                " SELECT SUM(IFNULL(ACAMTS, 0)) AS BAL, 0 AS INTOTAL, 0 AS OUTTOTAL FROM ACBALANCE WHERE ACDATE < '" + str(strDate) + "' AND ICUST = '" + str(iCust) + "' "
#                                " UNION ALL "
#                                " SELECT 0 AS BAL, SUM(IFNULL(ACAMTS, 0)) AS INTOTAL, 0 AS OUTTOTAL FROM SISACCTT "
#                                "        WHERE ACIOGB = '2' AND ACDATE < '" + str(strDate) + "' AND ICUST = '" + str(iCust) + "' AND FIN_OPT = 'Y' "
#                                " UNION ALL "
#                                " SELECT 0 AS BAL, 0 AS INTOTAL, SUM(IFNULL(ACAMTS, 0)) AS OUTTOTAL FROM SISACCTT "
#                                "        WHERE ACIOGB = '1' AND ACDATE < '" + str(strDate) + "' AND ICUST = '" + str(iCust) + "' AND FIN_OPT = 'Y' "
#                                " ) AA ")
#                 balresult = cursor.fetchall()
#             with connection.cursor() as cursor:
#                 cursor.execute("  SELECT IFNULL(AA.ACIOGB, ''), IFNULL(AA.IODATE, ''), IFNULL(AA.IN_ACAMTS, 0), IFNULL(AA.OUT_ACAMTS, 0)"
#                                "        , IFNULL(AA.ACCUST, ''), IFNULL(AA.CUST_NME, ''), IFNULL(AA.ACACNUMBER, ''), IFNULL(AA.ACNUM_NAME, '')"
#                                "        , IFNULL(AA.MCODE, ''), IFNULL(AA.FIN_OPT, ''), IFNULL(AA.MCODENM, ''), IFNULL(AA.ACTITLE, '')"
#                                "        , IFNULL(AA.ACSEQN, ''), IFNULL(AA.ACODE, ''), IFNULL(AA.ACODENM, ''), IFNULL(AA.GBN, ''), IFNULL(AA.GBNNM, ''), IFNULL(AA.APPLYDT, '')"
#                                "        , IFNULL(AA.ACGUBN, ''), IFNULL(AA.GBN, ''), IFNULL(AA.FIN_OPT, ''), IFNULL(AA.MID_OPT, ''), IFNULL(AA.ACUSE, ''), IFNULL(AA.ACGUBN, ''), IFNULL(AA.NME, '') FROM "
#                                " ( "
#                                "     SELECT A.ACIOGB, A.IODATE, A.ACAMTS AS IN_ACAMTS, 0 AS OUT_ACAMTS, A.ACCUST, B.CUST_NME"
#                                "            , A.ACACNUMBER, C.ACNUM_NAME, A.MCODE, A.FIN_OPT, D.MCODENM, A.ACTITLE, A.ACSEQN"
#                                "            , A.ACODE, E.RESNAM AS ACODENM, F.GBN, G.RESNAM AS GBNNM, A.APPLYDT, A.ACGUBN, A.MID_OPT, A.ACUSE "
#                                "            , IFNULL((SELECT X.EMP_NME FROM OSSIGN Y "
#                                "                LEFT OUTER JOIN PIS1TB001 X ON Y.EMP_NBR = X.EMP_NBR "
#                                "                WHERE Y.ICUST = A.ICUST AND Y.ACDATE = A.ACDATE AND Y.ACSEQN = A.ACSEQN AND Y.ACIOGB = A.ACIOGB "
#                                "                AND Y.SEQ = (SELECT IFNULL(MAX(SEQ), '') FROM OSSIGN WHERE ICUST = A.ICUST AND ACDATE = A.ACDATE AND ACSEQN = A.ACSEQN AND ACIOGB = A.ACIOGB AND OPT = 'Y')), '') AS NME "
#                                "     FROM SISACCTT A "
#                                "     LEFT OUTER JOIN MIS1TB003 B "
#                                "     ON A.ACCUST = B.CUST_NBR "
#                                "     LEFT OUTER JOIN ACNUMBER C "
#                                "     ON A.ACACNUMBER = C.ACNUMBER "
#                                "     LEFT OUTER JOIN OSCODEM D "
#                                "     ON A.MCODE = D.MCODE "
#                                "    LEFT OUTER JOIN OSREFCP E "
#                                "    ON A.ACODE = E.RESKEY "
#                                "    AND E.RECODE = 'ACD' "
#                                "    LEFT OUTER JOIN OSCODEM F "
#                                "    ON A.MCODE = F.MCODE "
#                                "    LEFT OUTER JOIN OSREFCP G "
#                                "    ON F.GBN = G.RESKEY "
#                                "    AND G.RECODE = 'CGB' "
#                                "     WHERE A.ACIOGB = '2' "
#                                "     AND A.ICUST = '" + str(iCust) + "'"
#                                "     UNION ALL "
#                                "     SELECT A.ACIOGB, A.IODATE, 0 AS IN_ACAMTS, A.ACAMTS AS OUT_ACAMTS, A.ACCUST, B.CUST_NME"
#                                "            , A.ACACNUMBER, C.ACNUM_NAME, A.MCODE, A.FIN_OPT, D.MCODENM, A.ACTITLE, A.ACSEQN"
#                                "            , A.ACODE, E.RESNAM AS ACODENM, F.GBN, G.RESNAM AS GBNNM, A.APPLYDT, A.ACGUBN, A.MID_OPT, A.ACUSE "
#                                "            , IFNULL((SELECT X.EMP_NME FROM OSSIGN Y "
#                                "                LEFT OUTER JOIN PIS1TB001 X ON Y.EMP_NBR = X.EMP_NBR "
#                                "                WHERE Y.ICUST = A.ICUST AND Y.ACDATE = A.ACDATE AND Y.ACSEQN = A.ACSEQN AND Y.ACIOGB = A.ACIOGB "
#                                "                AND Y.SEQ = (SELECT IFNULL(MAX(SEQ), '') FROM OSSIGN WHERE ICUST = A.ICUST AND ACDATE = A.ACDATE AND ACSEQN = A.ACSEQN AND ACIOGB = A.ACIOGB AND OPT = 'Y')), '') AS NME "
#                                "     FROM SISACCTT A "
#                                "     LEFT OUTER JOIN MIS1TB003 B "
#                                "     ON A.ACCUST = B.CUST_NBR "
#                                "     LEFT OUTER JOIN ACNUMBER C "
#                                "     ON A.ACACNUMBER = C.ACNUMBER "
#                                "     LEFT OUTER JOIN OSCODEM D "
#                                "     ON A.MCODE = D.MCODE "
#                                "    LEFT OUTER JOIN OSREFCP E "
#                                "    ON A.ACODE = E.RESKEY "
#                                "    AND E.RECODE = 'ACD' "
#                                "    LEFT OUTER JOIN OSCODEM F "
#                                "    ON A.MCODE = F.MCODE "
#                                "    LEFT OUTER JOIN OSREFCP G "
#                                "    ON F.GBN = G.RESKEY "
#                                "    AND G.RECODE = 'CGB' "
#                                "     WHERE A.ACIOGB = '1' "
#                                "     AND A.ICUST = '" + str(iCust) + "'"
#                                " ) AA "
#                                " WHERE AA.IODATE BETWEEN '" + strDate + "' AND '" + endDate + "' "
#                                " ORDER BY AA.IODATE ")
#                 mainresult = cursor.fetchall()
#         # 미시행
#         if inputGbn == '1':
#             with connection.cursor() as cursor:
#                 cursor.execute(" SELECT EMP_CLS FROM PIS1TB001 WHERE EMP_NBR = '" + str(creUser) + "' ")
#                 chkEmp = cursor.fetchall()
#
#         return JsonResponse({'balList': balresult, 'mainList': mainresult})


def receivePay_search(request):
    strDate = request.POST.get('strDate')
    endDate = request.POST.get('endDate')
    cboAct = request.POST.get('cboAct')
    cboCust = request.POST.get('cboCust')
    creUser = request.session.get("userId")
    iCust = request.session.get("USER_ICUST")
    inputBank = request.POST.get('inputBank')
    empName = request.POST.get('empName')
    payGbn = request.POST.get('payGbn')
    Gbn = request.POST.get('Gbn')
    inputCard = request.POST.get('inputCard')
    inputCardNum = request.POST.get('inputCardNum')


    with connection.cursor() as cursor:
        cursor.execute(" SELECT EMP_CLS FROM PIS1TB001 WHERE EMP_NBR = '" + str(creUser) + "' ")
        chkEmp = cursor.fetchall()


    if chkEmp[0][0] != '':
        if int(chkEmp[0][0]) < 2:
            if Gbn != '':
                if Gbn == '1' or Gbn == '4':
                    with connection.cursor() as cursor:
                        cursor.execute(" SELECT IFNULL(SUM(BAL), 0), IFNULL(SUM(INTOTAL), 0), IFNULL(SUM(OUTTOTAL), 0), IFNULL(SUM(BAL + INTOTAL - OUTTOTAL), 0) FROM "
                                       " ("
                                       " SELECT SUM(IFNULL(ACAMTS, 0)) AS BAL, 0 AS INTOTAL, 0 AS OUTTOTAL FROM ACBALANCE WHERE ACDATE < '" + str(strDate) + "' AND ICUST = '" + str(iCust) + "' "
                                       " UNION ALL "
                                       " SELECT 0 AS BAL, SUM(IFNULL(ACAMTS, 0)) AS INTOTAL, 0 AS OUTTOTAL FROM SISACCTT "
                                       "        WHERE ACIOGB = '2' AND ACDATE < '" + str(strDate) + "' AND ICUST = '" + str(iCust) + "' AND FIN_OPT = 'Y' "
                                       " UNION ALL "
                                       " SELECT 0 AS BAL, 0 AS INTOTAL, SUM(IFNULL(ACAMTS, 0)) AS OUTTOTAL FROM SISACCTT "
                                       "        WHERE ACIOGB = '1' AND ACDATE < '" + str(strDate) + "' AND ICUST = '" + str(iCust) + "' AND FIN_OPT = 'Y' "
                                       " ) AA ")
                        balresult = cursor.fetchall()

                    with connection.cursor() as cursor:
                        cursor.execute("  SELECT IFNULL(AA.ACIOGB, ''), IFNULL(AA.IODATE, ''), IFNULL(AA.IN_ACAMTS, 0), IFNULL(AA.OUT_ACAMTS, 0)"
                                       "        , IFNULL(AA.ACCUST, ''), IFNULL(AA.CUST_NME, ''), IFNULL(AA.ACACNUMBER, ''), IFNULL(AA.ACNUM_NAME, '')"
                                       "        , IFNULL(AA.MCODE, ''), IFNULL(AA.FIN_OPT, ''), IFNULL(AA.MCODENM, ''), IFNULL(AA.ACTITLE, '')"
                                       "        , IFNULL(AA.ACSEQN, ''), IFNULL(AA.ACODE, ''), IFNULL(AA.ACODENM, ''), IFNULL(AA.GBN, '')"
                                       "        , IFNULL(AA.GBNNM, ''), IFNULL(AA.APPLYDT, ''), IFNULL(AA.ACGUBN, ''), IFNULL(AA.GBN, '')" 
                                       "        , IFNULL(AA.FIN_OPT, ''), IFNULL(AA.MID_OPT, ''), IFNULL(AA.ACUSE, ''), IFNULL(AA.ACGUBN, ''), IFNULL(AA.NME, '') FROM "
                                       " ( "
                                       "     SELECT A.ACIOGB, A.IODATE, A.ACAMTS AS IN_ACAMTS, 0 AS OUT_ACAMTS, A.ACCUST, B.CUST_NME"
                                       "            , A.ACACNUMBER, C.ACNUM_NAME, A.MCODE, A.FIN_OPT, D.MCODENM, A.ACTITLE, A.ACSEQN"
                                       "            , A.ACODE, E.RESNAM AS ACODENM, F.GBN, G.RESNAM AS GBNNM, A.APPLYDT, A.ACGUBN, A.MID_OPT, A.ACUSE "
                                       "            , IFNULL((SELECT X.EMP_NME FROM OSSIGN Y "
                                       "                LEFT OUTER JOIN PIS1TB001 X ON Y.EMP_NBR = X.EMP_NBR "
                                       "                WHERE Y.ICUST = A.ICUST AND Y.ACDATE = A.IODATE AND Y.ACSEQN = A.ACSEQN AND Y.ACIOGB = A.ACIOGB "
                                       "                AND Y.SEQ = (SELECT IFNULL(MAX(SEQ), '') FROM OSSIGN WHERE ICUST = A.ICUST AND ACDATE = A.IODATE AND ACSEQN = A.ACSEQN AND ACIOGB = A.ACIOGB AND OPT = 'Y')), '') AS NME"
                                       "     FROM SISACCTT A "
                                       "     LEFT OUTER JOIN MIS1TB003 B "
                                       "     ON A.ACCUST = B.CUST_NBR "
                                       "     LEFT OUTER JOIN ACNUMBER C "
                                       "     ON A.ACACNUMBER = C.ACNUMBER "
                                       "     LEFT OUTER JOIN OSCODEM D "
                                       "     ON A.MCODE = D.MCODE "
                                       "    LEFT OUTER JOIN OSREFCP E "
                                       "    ON A.ACODE = E.RESKEY "
                                       "    AND E.RECODE = 'ACD' "
                                       "    LEFT OUTER JOIN OSCODEM F "
                                       "    ON A.MCODE = F.MCODE "
                                       "    LEFT OUTER JOIN OSREFCP G "
                                       "    ON F.GBN = G.RESKEY "
                                       "    AND G.RECODE = 'CGB' "
                                       "     WHERE A.ACIOGB = '2' "
                                       "     AND A.ICUST = '" + str(iCust) + "'"
                                       "    AND A.MID_OPT = 'Y'"
                                       "    AND A.FIN_OPT = 'N'"
                                       "     UNION ALL "
                                       "     SELECT A.ACIOGB, A.IODATE, 0 AS IN_ACAMTS, A.ACAMTS AS OUT_ACAMTS, A.ACCUST, B.CUST_NME"
                                       "            , A.ACACNUMBER, C.ACNUM_NAME, A.MCODE, A.FIN_OPT, D.MCODENM, A.ACTITLE, A.ACSEQN"
                                       "            , A.ACODE, E.RESNAM AS ACODENM, F.GBN, G.RESNAM AS GBNNM, A.APPLYDT, A.ACGUBN, A.MID_OPT, A.ACUSE "
                                       "            , IFNULL((SELECT X.EMP_NME FROM OSSIGN Y "
                                       "                LEFT OUTER JOIN PIS1TB001 X ON Y.EMP_NBR = X.EMP_NBR "
                                       "                WHERE Y.ICUST = A.ICUST AND Y.ACDATE = A.IODATE AND Y.ACSEQN = A.ACSEQN AND Y.ACIOGB = A.ACIOGB "
                                       "                AND Y.SEQ = (SELECT IFNULL(MAX(SEQ), '') FROM OSSIGN WHERE ICUST = A.ICUST AND ACDATE = A.IODATE AND ACSEQN = A.ACSEQN AND ACIOGB = A.ACIOGB AND OPT = 'Y')), '') AS NME "
                                       "     FROM SISACCTT A "
                                       "     LEFT OUTER JOIN MIS1TB003 B "
                                       "     ON A.ACCUST = B.CUST_NBR "
                                       "     LEFT OUTER JOIN ACNUMBER C "
                                       "     ON A.ACACNUMBER = C.ACNUMBER "
                                       "     LEFT OUTER JOIN OSCODEM D "
                                       "     ON A.MCODE = D.MCODE "
                                       "    LEFT OUTER JOIN OSREFCP E "
                                       "    ON A.ACODE = E.RESKEY "
                                       "    AND E.RECODE = 'ACD' "
                                       "    LEFT OUTER JOIN OSCODEM F "
                                       "    ON A.MCODE = F.MCODE "
                                       "    LEFT OUTER JOIN OSREFCP G "
                                       "    ON F.GBN = G.RESKEY "
                                       "    AND G.RECODE = 'CGB' "                                   
                                       "     WHERE A.ACIOGB = '1' "
                                       "     AND A.ICUST = '" + str(iCust) + "'"
                                       "    AND A.MID_OPT = 'Y'"
                                       "    AND A.FIN_OPT = 'N'"
                                       " ) AA "
                                       " WHERE AA.IODATE BETWEEN '" + str(strDate) + "' AND '" + str(endDate) + "' "
                                       " ORDER BY AA.IODATE ")
                        mainresult = cursor.fetchall()

                        return JsonResponse({'balList': balresult, 'mainList': mainresult})

                if Gbn == '2':
                    with connection.cursor() as cursor:
                        cursor.execute(" SELECT IFNULL(SUM(BAL), 0), IFNULL(SUM(INTOTAL), 0), IFNULL(SUM(OUTTOTAL), 0), IFNULL(SUM(BAL + INTOTAL - OUTTOTAL), 0) FROM "
                                       " ("
                                       " SELECT SUM(IFNULL(ACAMTS, 0)) AS BAL, 0 AS INTOTAL, 0 AS OUTTOTAL FROM ACBALANCE WHERE ACDATE < '" + str(strDate) + "' AND ICUST = '" + str(iCust) + "' "
                                       " UNION ALL "
                                       " SELECT 0 AS BAL, SUM(IFNULL(ACAMTS, 0)) AS INTOTAL, 0 AS OUTTOTAL FROM SISACCTT "
                                       "        WHERE ACIOGB = '2' AND ACDATE < '" + str(strDate) + "' AND ICUST = '" + str(iCust) + "' AND FIN_OPT = 'Y' "
                                       " UNION ALL "
                                       " SELECT 0 AS BAL, 0 AS INTOTAL, SUM(IFNULL(ACAMTS, 0)) AS OUTTOTAL FROM SISACCTT "
                                       "        WHERE ACIOGB = '1' AND ACDATE < '" + str(strDate) + "' AND ICUST = '" + str(iCust) + "' AND FIN_OPT = 'Y' "
                                       " ) AA ")
                        balresult = cursor.fetchall()

                    with connection.cursor() as cursor:
                        cursor.execute("  SELECT IFNULL(AA.ACIOGB, ''), IFNULL(AA.IODATE, ''), IFNULL(AA.IN_ACAMTS, 0), IFNULL(AA.OUT_ACAMTS, 0)"
                                       "        , IFNULL(AA.ACCUST, ''), IFNULL(AA.CUST_NME, ''), IFNULL(AA.ACACNUMBER, ''), IFNULL(AA.ACNUM_NAME, '')"
                                       "        , IFNULL(AA.MCODE, ''), IFNULL(AA.FIN_OPT, ''), IFNULL(AA.MCODENM, ''), IFNULL(AA.ACTITLE, '')"
                                       "        , IFNULL(AA.ACSEQN, ''), IFNULL(AA.ACODE, ''), IFNULL(AA.ACODENM, ''), IFNULL(AA.GBN, '')"
                                       "        , IFNULL(AA.GBNNM, ''), IFNULL(AA.APPLYDT, ''), IFNULL(AA.ACGUBN, ''), IFNULL(AA.GBN, '')" 
                                       "        , IFNULL(AA.FIN_OPT, ''), IFNULL(AA.MID_OPT, ''), IFNULL(AA.ACUSE, ''), IFNULL(AA.ACGUBN, ''), IFNULL(AA.NME, '') FROM "
                                       " ( "
                                       "     SELECT A.ACIOGB, A.IODATE, A.ACAMTS AS IN_ACAMTS, 0 AS OUT_ACAMTS, A.ACCUST, B.CUST_NME"
                                       "            , A.ACACNUMBER, C.ACNUM_NAME, A.MCODE, A.FIN_OPT, D.MCODENM, A.ACTITLE, A.ACSEQN"
                                       "            , A.ACODE, E.RESNAM AS ACODENM, F.GBN, G.RESNAM AS GBNNM, A.APPLYDT, A.ACGUBN, A.MID_OPT, A.ACUSE "
                                       "            , IFNULL((SELECT X.EMP_NME FROM OSSIGN Y "
                                       "                LEFT OUTER JOIN PIS1TB001 X ON Y.EMP_NBR = X.EMP_NBR "
                                       "                WHERE Y.ICUST = A.ICUST AND Y.ACDATE = A.IODATE AND Y.ACSEQN = A.ACSEQN AND Y.ACIOGB = A.ACIOGB "
                                       "                AND Y.SEQ = (SELECT IFNULL(MAX(SEQ), '') FROM OSSIGN WHERE ICUST = A.ICUST AND ACDATE = A.IODATE AND ACSEQN = A.ACSEQN AND ACIOGB = A.ACIOGB AND OPT = 'Y')), '') AS NME"
                                       "     FROM SISACCTT A "
                                       "     LEFT OUTER JOIN MIS1TB003 B "
                                       "     ON A.ACCUST = B.CUST_NBR "
                                       "     LEFT OUTER JOIN ACNUMBER C "
                                       "     ON A.ACACNUMBER = C.ACNUMBER "
                                       "     LEFT OUTER JOIN OSCODEM D "
                                       "     ON A.MCODE = D.MCODE "
                                       "    LEFT OUTER JOIN OSREFCP E "
                                       "    ON A.ACODE = E.RESKEY "
                                       "    AND E.RECODE = 'ACD' "
                                       "    LEFT OUTER JOIN OSCODEM F "
                                       "    ON A.MCODE = F.MCODE "
                                       "    LEFT OUTER JOIN OSREFCP G "
                                       "    ON F.GBN = G.RESKEY "
                                       "    AND G.RECODE = 'CGB' "
                                       "     WHERE A.ACIOGB = '2' "
                                       "     AND A.ICUST = '" + str(iCust) + "'"
                                       "    AND A.MID_OPT = 'N'"
                                       "    AND A.FIN_OPT = 'N'"
                                       "     UNION ALL "
                                       "     SELECT A.ACIOGB, A.IODATE, 0 AS IN_ACAMTS, A.ACAMTS AS OUT_ACAMTS, A.ACCUST, B.CUST_NME"
                                       "            , A.ACACNUMBER, C.ACNUM_NAME, A.MCODE, A.FIN_OPT, D.MCODENM, A.ACTITLE, A.ACSEQN"
                                       "            , A.ACODE, E.RESNAM AS ACODENM, F.GBN, G.RESNAM AS GBNNM, A.APPLYDT, A.ACGUBN, A.MID_OPT, A.ACUSE "
                                       "            , IFNULL((SELECT X.EMP_NME FROM OSSIGN Y "
                                       "                LEFT OUTER JOIN PIS1TB001 X ON Y.EMP_NBR = X.EMP_NBR "
                                       "                WHERE Y.ICUST = A.ICUST AND Y.ACDATE = A.IODATE AND Y.ACSEQN = A.ACSEQN AND Y.ACIOGB = A.ACIOGB "
                                       "                AND Y.SEQ = (SELECT IFNULL(MAX(SEQ), '') FROM OSSIGN WHERE ICUST = A.ICUST AND ACDATE = A.IODATE AND ACSEQN = A.ACSEQN AND ACIOGB = A.ACIOGB AND OPT = 'Y')), '') AS NME "
                                       "     FROM SISACCTT A "
                                       "     LEFT OUTER JOIN MIS1TB003 B "
                                       "     ON A.ACCUST = B.CUST_NBR "
                                       "     LEFT OUTER JOIN ACNUMBER C "
                                       "     ON A.ACACNUMBER = C.ACNUMBER "
                                       "     LEFT OUTER JOIN OSCODEM D "
                                       "     ON A.MCODE = D.MCODE "
                                       "    LEFT OUTER JOIN OSREFCP E "
                                       "    ON A.ACODE = E.RESKEY "
                                       "    AND E.RECODE = 'ACD' "
                                       "    LEFT OUTER JOIN OSCODEM F "
                                       "    ON A.MCODE = F.MCODE "
                                       "    LEFT OUTER JOIN OSREFCP G "
                                       "    ON F.GBN = G.RESKEY "
                                       "    AND G.RECODE = 'CGB' "                                   
                                       "     WHERE A.ACIOGB = '1' "
                                       "     AND A.ICUST = '" + str(iCust) + "'"
                                       "    AND A.MID_OPT = 'N'"
                                       "    AND A.FIN_OPT = 'N'"
                                       " ) AA "
                                       " WHERE AA.IODATE BETWEEN '" + str(strDate) + "' AND '" + str(endDate) + "' "
                                       " ORDER BY AA.IODATE ")
                        mainresult = cursor.fetchall()

                        return JsonResponse({'balList': balresult, 'mainList': mainresult})
                if Gbn == '3':
                    with connection.cursor() as cursor:
                        cursor.execute(" SELECT IFNULL(SUM(BAL), 0), IFNULL(SUM(INTOTAL), 0), IFNULL(SUM(OUTTOTAL), 0), IFNULL(SUM(BAL + INTOTAL - OUTTOTAL), 0) FROM "
                                       " ("
                                       " SELECT SUM(IFNULL(ACAMTS, 0)) AS BAL, 0 AS INTOTAL, 0 AS OUTTOTAL FROM ACBALANCE WHERE ACDATE < '" + str(strDate) + "' AND ICUST = '" + str(iCust) + "' "
                                       " UNION ALL "
                                       " SELECT 0 AS BAL, SUM(IFNULL(ACAMTS, 0)) AS INTOTAL, 0 AS OUTTOTAL FROM SISACCTT "
                                       "        WHERE ACIOGB = '2' AND ACDATE < '" + str(strDate) + "' AND ICUST = '" + str(iCust) + "' AND FIN_OPT = 'Y' "
                                       " UNION ALL "
                                       " SELECT 0 AS BAL, 0 AS INTOTAL, SUM(IFNULL(ACAMTS, 0)) AS OUTTOTAL FROM SISACCTT "
                                       "        WHERE ACIOGB = '1' AND ACDATE < '" + str(strDate) + "' AND ICUST = '" + str(iCust) + "' AND FIN_OPT = 'Y' "
                                       " ) AA ")
                        balresult = cursor.fetchall()

                    with connection.cursor() as cursor:
                        cursor.execute("  SELECT IFNULL(AA.ACIOGB, ''), IFNULL(AA.IODATE, ''), IFNULL(AA.IN_ACAMTS, 0), IFNULL(AA.OUT_ACAMTS, 0)"
                                       "        , IFNULL(AA.ACCUST, ''), IFNULL(AA.CUST_NME, ''), IFNULL(AA.ACACNUMBER, ''), IFNULL(AA.ACNUM_NAME, '')"
                                       "        , IFNULL(AA.MCODE, ''), IFNULL(AA.FIN_OPT, ''), IFNULL(AA.MCODENM, ''), IFNULL(AA.ACTITLE, '')"
                                       "        , IFNULL(AA.ACSEQN, ''), IFNULL(AA.ACODE, ''), IFNULL(AA.ACODENM, ''), IFNULL(AA.GBN, '')"
                                       "        , IFNULL(AA.GBNNM, ''), IFNULL(AA.APPLYDT, ''), IFNULL(AA.ACGUBN, ''), IFNULL(AA.GBN, '')" 
                                       "        , IFNULL(AA.FIN_OPT, ''), IFNULL(AA.MID_OPT, ''), IFNULL(AA.ACUSE, ''), IFNULL(AA.ACGUBN, ''), IFNULL(AA.NME, '') FROM "
                                       " ( "
                                       "     SELECT A.ACIOGB, A.IODATE, A.ACAMTS AS IN_ACAMTS, 0 AS OUT_ACAMTS, A.ACCUST, B.CUST_NME"
                                       "            , A.ACACNUMBER, C.ACNUM_NAME, A.MCODE, A.FIN_OPT, D.MCODENM, A.ACTITLE, A.ACSEQN"
                                       "            , A.ACODE, E.RESNAM AS ACODENM, F.GBN, G.RESNAM AS GBNNM, A.APPLYDT, A.ACGUBN, A.MID_OPT, A.ACUSE "
                                       "            , IFNULL((SELECT X.EMP_NME FROM OSSIGN Y "
                                       "                LEFT OUTER JOIN PIS1TB001 X ON Y.EMP_NBR = X.EMP_NBR "
                                       "                WHERE Y.ICUST = A.ICUST AND Y.ACDATE = A.IODATE AND Y.ACSEQN = A.ACSEQN AND Y.ACIOGB = A.ACIOGB "
                                       "                AND Y.SEQ = (SELECT IFNULL(MAX(SEQ), '') FROM OSSIGN WHERE ICUST = A.ICUST AND ACDATE = A.IODATE AND ACSEQN = A.ACSEQN AND ACIOGB = A.ACIOGB AND OPT = 'Y')), '') AS NME"
                                       "     FROM SISACCTT A "
                                       "     LEFT OUTER JOIN MIS1TB003 B "
                                       "     ON A.ACCUST = B.CUST_NBR "
                                       "     LEFT OUTER JOIN ACNUMBER C "
                                       "     ON A.ACACNUMBER = C.ACNUMBER "
                                       "     LEFT OUTER JOIN OSCODEM D "
                                       "     ON A.MCODE = D.MCODE "
                                       "    LEFT OUTER JOIN OSREFCP E "
                                       "    ON A.ACODE = E.RESKEY "
                                       "    AND E.RECODE = 'ACD' "
                                       "    LEFT OUTER JOIN OSCODEM F "
                                       "    ON A.MCODE = F.MCODE "
                                       "    LEFT OUTER JOIN OSREFCP G "
                                       "    ON F.GBN = G.RESKEY "
                                       "    AND G.RECODE = 'CGB' "
                                       "     WHERE A.ACIOGB = '2' "
                                       "     AND A.ICUST = '" + str(iCust) + "'"
                                       "    AND A.MID_OPT = 'Y'"
                                       "    AND A.FIN_OPT = 'Y'"
                                       "     UNION ALL "
                                       "     SELECT A.ACIOGB, A.IODATE, 0 AS IN_ACAMTS, A.ACAMTS AS OUT_ACAMTS, A.ACCUST, B.CUST_NME"
                                       "            , A.ACACNUMBER, C.ACNUM_NAME, A.MCODE, A.FIN_OPT, D.MCODENM, A.ACTITLE, A.ACSEQN"
                                       "            , A.ACODE, E.RESNAM AS ACODENM, F.GBN, G.RESNAM AS GBNNM, A.APPLYDT, A.ACGUBN, A.MID_OPT, A.ACUSE "
                                       "            , IFNULL((SELECT X.EMP_NME FROM OSSIGN Y "
                                       "                LEFT OUTER JOIN PIS1TB001 X ON Y.EMP_NBR = X.EMP_NBR "
                                       "                WHERE Y.ICUST = A.ICUST AND Y.ACDATE = A.IODATE AND Y.ACSEQN = A.ACSEQN AND Y.ACIOGB = A.ACIOGB "
                                       "                AND Y.SEQ = (SELECT IFNULL(MAX(SEQ), '') FROM OSSIGN WHERE ICUST = A.ICUST AND ACDATE = A.IODATE AND ACSEQN = A.ACSEQN AND ACIOGB = A.ACIOGB AND OPT = 'Y')), '') AS NME "
                                       "     FROM SISACCTT A "
                                       "     LEFT OUTER JOIN MIS1TB003 B "
                                       "     ON A.ACCUST = B.CUST_NBR "
                                       "     LEFT OUTER JOIN ACNUMBER C "
                                       "     ON A.ACACNUMBER = C.ACNUMBER "
                                       "     LEFT OUTER JOIN OSCODEM D "
                                       "     ON A.MCODE = D.MCODE "
                                       "    LEFT OUTER JOIN OSREFCP E "
                                       "    ON A.ACODE = E.RESKEY "
                                       "    AND E.RECODE = 'ACD' "
                                       "    LEFT OUTER JOIN OSCODEM F "
                                       "    ON A.MCODE = F.MCODE "
                                       "    LEFT OUTER JOIN OSREFCP G "
                                       "    ON F.GBN = G.RESKEY "
                                       "    AND G.RECODE = 'CGB' "                                   
                                       "     WHERE A.ACIOGB = '1' "
                                       "     AND A.ICUST = '" + str(iCust) + "'"
                                       "    AND A.MID_OPT = 'Y'"
                                       "    AND A.FIN_OPT = 'Y'"
                                       " ) AA "
                                       " WHERE AA.IODATE BETWEEN '" + str(strDate) + "' AND '" + str(endDate) + "' "
                                       " ORDER BY AA.IODATE ")
                        mainresult = cursor.fetchall()

                        return JsonResponse({'balList': balresult, 'mainList': mainresult})

            if empName != '':
                with connection.cursor() as cursor:
                    cursor.execute(" SELECT EMP_NBR FROM PIS1TB001 WHERE EMP_NME LIKE '%" + str(empName) + "%' ")
                    result = cursor.fetchall()
                    empCode = result[0][0]

                with connection.cursor() as cursor:
                    cursor.execute(" SELECT IFNULL(SUM(BAL), 0), IFNULL(SUM(INTOTAL), 0), IFNULL(SUM(OUTTOTAL), 0), IFNULL(SUM(BAL + INTOTAL - OUTTOTAL), 0) FROM "
                                   " ("
                                   " SELECT SUM(IFNULL(ACAMTS, 0)) AS BAL, 0 AS INTOTAL, 0 AS OUTTOTAL FROM ACBALANCE WHERE ACDATE < '" + str(strDate) + "' AND ICUST = '" + str(iCust) + "' "
                                   " UNION ALL "
                                   " SELECT 0 AS BAL, SUM(IFNULL(ACAMTS, 0)) AS INTOTAL, 0 AS OUTTOTAL FROM SISACCTT "
                                   "        WHERE ACIOGB = '2' AND ACDATE < '" + str(strDate) + "' AND ICUST = '" + str(iCust) + "' AND FIN_OPT = 'Y' "
                                   " UNION ALL "
                                   " SELECT 0 AS BAL, 0 AS INTOTAL, SUM(IFNULL(ACAMTS, 0)) AS OUTTOTAL FROM SISACCTT "
                                   "        WHERE ACIOGB = '1' AND ACDATE < '" + str(strDate) + "' AND ICUST = '" + str(iCust) + "' AND FIN_OPT = 'Y' "
                                   " ) AA ")
                    balresult = cursor.fetchall()

                with connection.cursor() as cursor:
                    cursor.execute("  SELECT IFNULL(AA.ACIOGB, ''), IFNULL(AA.IODATE, ''), IFNULL(AA.IN_ACAMTS, 0), IFNULL(AA.OUT_ACAMTS, 0)"
                                   "        , IFNULL(AA.ACCUST, ''), IFNULL(AA.CUST_NME, ''), IFNULL(AA.ACACNUMBER, ''), IFNULL(AA.ACNUM_NAME, '')"
                                   "        , IFNULL(AA.MCODE, ''), IFNULL(AA.FIN_OPT, ''), IFNULL(AA.MCODENM, ''), IFNULL(AA.ACTITLE, '')"
                                   "        , IFNULL(AA.ACSEQN, ''), IFNULL(AA.ACODE, ''), IFNULL(AA.ACODENM, ''), IFNULL(AA.GBN, '')"
                                   "        , IFNULL(AA.GBNNM, ''), IFNULL(AA.APPLYDT, ''), IFNULL(AA.ACGUBN, ''), IFNULL(AA.GBN, '')" 
                                   "        , IFNULL(AA.FIN_OPT, ''), IFNULL(AA.MID_OPT, ''), IFNULL(AA.ACUSE, ''), IFNULL(AA.ACGUBN, ''), IFNULL(AA.NME, '') FROM "
                                   " ( "
                                   "     SELECT A.ACIOGB, A.IODATE, A.ACAMTS AS IN_ACAMTS, 0 AS OUT_ACAMTS, A.ACCUST, B.CUST_NME"
                                   "            , A.ACACNUMBER, C.ACNUM_NAME, A.MCODE, A.FIN_OPT, D.MCODENM, A.ACTITLE, A.ACSEQN"
                                   "            , A.ACODE, E.RESNAM AS ACODENM, F.GBN, G.RESNAM AS GBNNM, A.APPLYDT, A.ACGUBN, A.MID_OPT, A.ACUSE "
                                   "            , IFNULL((SELECT X.EMP_NME FROM OSSIGN Y "
                                   "                LEFT OUTER JOIN PIS1TB001 X ON Y.EMP_NBR = X.EMP_NBR "
                                   "                WHERE Y.ICUST = A.ICUST AND Y.ACDATE = A.IODATE AND Y.ACSEQN = A.ACSEQN AND Y.ACIOGB = A.ACIOGB "
                                   "                AND Y.SEQ = (SELECT IFNULL(MAX(SEQ), '') FROM OSSIGN WHERE ICUST = A.ICUST AND ACDATE = A.IODATE AND ACSEQN = A.ACSEQN AND ACIOGB = A.ACIOGB AND OPT = 'Y')), '') AS NME"
                                   "     FROM SISACCTT A "
                                   "     LEFT OUTER JOIN MIS1TB003 B "
                                   "     ON A.ACCUST = B.CUST_NBR "
                                   "     LEFT OUTER JOIN ACNUMBER C "
                                   "     ON A.ACACNUMBER = C.ACNUMBER "
                                   "     LEFT OUTER JOIN OSCODEM D "
                                   "     ON A.MCODE = D.MCODE "
                                   "    LEFT OUTER JOIN OSREFCP E "
                                   "    ON A.ACODE = E.RESKEY "
                                   "    AND E.RECODE = 'ACD' "
                                   "    LEFT OUTER JOIN OSCODEM F "
                                   "    ON A.MCODE = F.MCODE "
                                   "    LEFT OUTER JOIN OSREFCP G "
                                   "    ON F.GBN = G.RESKEY "
                                   "    AND G.RECODE = 'CGB' "
                                   "     WHERE A.ACIOGB = '2' "
                                   "     AND A.ICUST = '" + str(iCust) + "'"
                                   "     AND A.CRE_USER = '" + str(empCode) + "'"
                                   "     UNION ALL "
                                   "     SELECT A.ACIOGB, A.IODATE, 0 AS IN_ACAMTS, A.ACAMTS AS OUT_ACAMTS, A.ACCUST, B.CUST_NME"
                                   "            , A.ACACNUMBER, C.ACNUM_NAME, A.MCODE, A.FIN_OPT, D.MCODENM, A.ACTITLE, A.ACSEQN"
                                   "            , A.ACODE, E.RESNAM AS ACODENM, F.GBN, G.RESNAM AS GBNNM, A.APPLYDT, A.ACGUBN, A.MID_OPT, A.ACUSE "
                                   "            , IFNULL((SELECT X.EMP_NME FROM OSSIGN Y "
                                   "                LEFT OUTER JOIN PIS1TB001 X ON Y.EMP_NBR = X.EMP_NBR "
                                   "                WHERE Y.ICUST = A.ICUST AND Y.ACDATE = A.IODATE AND Y.ACSEQN = A.ACSEQN AND Y.ACIOGB = A.ACIOGB "
                                   "                AND Y.SEQ = (SELECT IFNULL(MAX(SEQ), '') FROM OSSIGN WHERE ICUST = A.ICUST AND ACDATE = A.IODATE AND ACSEQN = A.ACSEQN AND ACIOGB = A.ACIOGB AND OPT = 'Y')), '') AS NME "
                                   "     FROM SISACCTT A "
                                   "     LEFT OUTER JOIN MIS1TB003 B "
                                   "     ON A.ACCUST = B.CUST_NBR "
                                   "     LEFT OUTER JOIN ACNUMBER C "
                                   "     ON A.ACACNUMBER = C.ACNUMBER "
                                   "     LEFT OUTER JOIN OSCODEM D "
                                   "     ON A.MCODE = D.MCODE "
                                   "    LEFT OUTER JOIN OSREFCP E "
                                   "    ON A.ACODE = E.RESKEY "
                                   "    AND E.RECODE = 'ACD' "
                                   "    LEFT OUTER JOIN OSCODEM F "
                                   "    ON A.MCODE = F.MCODE "
                                   "    LEFT OUTER JOIN OSREFCP G "
                                   "    ON F.GBN = G.RESKEY "
                                   "    AND G.RECODE = 'CGB' "                                   
                                   "     WHERE A.ACIOGB = '1' "
                                   "     AND A.ICUST = '" + str(iCust) + "'"
                                   "     AND A.CRE_USER = '" + str(empCode) + "'"
                                   " ) AA "
                                   " WHERE AA.IODATE BETWEEN '" + str(strDate) + "' AND '" + str(endDate) + "' "
                                   " ORDER BY AA.IODATE ")
                    mainresult = cursor.fetchall()

                    return JsonResponse({'balList': balresult, 'mainList': mainresult})

            if payGbn != '':
                with connection.cursor() as cursor:
                    cursor.execute(" SELECT IFNULL(SUM(BAL), 0), IFNULL(SUM(INTOTAL), 0), IFNULL(SUM(OUTTOTAL), 0), IFNULL(SUM(BAL + INTOTAL - OUTTOTAL), 0) FROM "
                                   " ("
                                   " SELECT SUM(IFNULL(ACAMTS, 0)) AS BAL, 0 AS INTOTAL, 0 AS OUTTOTAL FROM ACBALANCE WHERE ACDATE < '" + str(strDate) + "' AND ICUST = '" + str(iCust) + "' "
                                   " UNION ALL "
                                   " SELECT 0 AS BAL, SUM(IFNULL(ACAMTS, 0)) AS INTOTAL, 0 AS OUTTOTAL FROM SISACCTT "
                                   "        WHERE ACIOGB = '2' AND ACDATE < '" + str(strDate) + "' AND ICUST = '" + str(iCust) + "' AND FIN_OPT = 'Y' "
                                   " UNION ALL "
                                   " SELECT 0 AS BAL, 0 AS INTOTAL, SUM(IFNULL(ACAMTS, 0)) AS OUTTOTAL FROM SISACCTT "
                                   "        WHERE ACIOGB = '1' AND ACDATE < '" + str(strDate) + "' AND ICUST = '" + str(iCust) + "' AND FIN_OPT = 'Y' "
                                   " ) AA ")
                    balresult = cursor.fetchall()

                with connection.cursor() as cursor:
                    cursor.execute("  SELECT IFNULL(AA.ACIOGB, ''), IFNULL(AA.IODATE, ''), IFNULL(AA.IN_ACAMTS, 0), IFNULL(AA.OUT_ACAMTS, 0)"
                                   "        , IFNULL(AA.ACCUST, ''), IFNULL(AA.CUST_NME, ''), IFNULL(AA.ACACNUMBER, ''), IFNULL(AA.ACNUM_NAME, '')"
                                   "        , IFNULL(AA.MCODE, ''), IFNULL(AA.FIN_OPT, ''), IFNULL(AA.MCODENM, ''), IFNULL(AA.ACTITLE, '')"
                                   "        , IFNULL(AA.ACSEQN, ''), IFNULL(AA.ACODE, ''), IFNULL(AA.ACODENM, ''), IFNULL(AA.GBN, '')"
                                   "        , IFNULL(AA.GBNNM, ''), IFNULL(AA.APPLYDT, ''), IFNULL(AA.ACGUBN, ''), IFNULL(AA.GBN, '')" 
                                   "        , IFNULL(AA.FIN_OPT, ''), IFNULL(AA.MID_OPT, ''), IFNULL(AA.ACUSE, ''), IFNULL(AA.ACGUBN, ''), IFNULL(AA.NME, '') FROM "
                                   " ( "
                                   "     SELECT A.ACIOGB, A.IODATE, A.ACAMTS AS IN_ACAMTS, 0 AS OUT_ACAMTS, A.ACCUST, B.CUST_NME"
                                   "            , A.ACACNUMBER, C.ACNUM_NAME, A.MCODE, A.FIN_OPT, D.MCODENM, A.ACTITLE, A.ACSEQN"
                                   "            , A.ACODE, E.RESNAM AS ACODENM, F.GBN, G.RESNAM AS GBNNM, A.APPLYDT, A.ACGUBN, A.MID_OPT, A.ACUSE "
                                   "            , IFNULL((SELECT X.EMP_NME FROM OSSIGN Y "
                                   "                LEFT OUTER JOIN PIS1TB001 X ON Y.EMP_NBR = X.EMP_NBR "
                                   "                WHERE Y.ICUST = A.ICUST AND Y.ACDATE = A.IODATE AND Y.ACSEQN = A.ACSEQN AND Y.ACIOGB = A.ACIOGB "
                                   "                AND Y.SEQ = (SELECT IFNULL(MAX(SEQ), '') FROM OSSIGN WHERE ICUST = A.ICUST AND ACDATE = A.IODATE AND ACSEQN = A.ACSEQN AND ACIOGB = A.ACIOGB AND OPT = 'Y')), '') AS NME"
                                   "     FROM SISACCTT A "
                                   "     LEFT OUTER JOIN MIS1TB003 B "
                                   "     ON A.ACCUST = B.CUST_NBR "
                                   "     LEFT OUTER JOIN ACNUMBER C "
                                   "     ON A.ACACNUMBER = C.ACNUMBER "
                                   "     LEFT OUTER JOIN OSCODEM D "
                                   "     ON A.MCODE = D.MCODE "
                                   "    LEFT OUTER JOIN OSREFCP E "
                                   "    ON A.ACODE = E.RESKEY "
                                   "    AND E.RECODE = 'ACD' "
                                   "    LEFT OUTER JOIN OSCODEM F "
                                   "    ON A.MCODE = F.MCODE "
                                   "    LEFT OUTER JOIN OSREFCP G "
                                   "    ON F.GBN = G.RESKEY "
                                   "    AND G.RECODE = 'CGB' "
                                   "     WHERE A.ACIOGB = '2' "
                                   "     AND A.ICUST = '" + str(iCust) + "'"
                                   "     AND A.ACGUBN = '" + str(payGbn) + "'"
                                   "     UNION ALL "
                                   "     SELECT A.ACIOGB, A.IODATE, 0 AS IN_ACAMTS, A.ACAMTS AS OUT_ACAMTS, A.ACCUST, B.CUST_NME"
                                   "            , A.ACACNUMBER, C.ACNUM_NAME, A.MCODE, A.FIN_OPT, D.MCODENM, A.ACTITLE, A.ACSEQN"
                                   "            , A.ACODE, E.RESNAM AS ACODENM, F.GBN, G.RESNAM AS GBNNM, A.APPLYDT, A.ACGUBN, A.MID_OPT, A.ACUSE "
                                   "            , IFNULL((SELECT X.EMP_NME FROM OSSIGN Y "
                                   "                LEFT OUTER JOIN PIS1TB001 X ON Y.EMP_NBR = X.EMP_NBR "
                                   "                WHERE Y.ICUST = A.ICUST AND Y.ACDATE = A.IODATE AND Y.ACSEQN = A.ACSEQN AND Y.ACIOGB = A.ACIOGB "
                                   "                AND Y.SEQ = (SELECT IFNULL(MAX(SEQ), '') FROM OSSIGN WHERE ICUST = A.ICUST AND ACDATE = A.IODATE AND ACSEQN = A.ACSEQN AND ACIOGB = A.ACIOGB AND OPT = 'Y')), '') AS NME "
                                   "     FROM SISACCTT A "
                                   "     LEFT OUTER JOIN MIS1TB003 B "
                                   "     ON A.ACCUST = B.CUST_NBR "
                                   "     LEFT OUTER JOIN ACNUMBER C "
                                   "     ON A.ACACNUMBER = C.ACNUMBER "
                                   "     LEFT OUTER JOIN OSCODEM D "
                                   "     ON A.MCODE = D.MCODE "
                                   "    LEFT OUTER JOIN OSREFCP E "
                                   "    ON A.ACODE = E.RESKEY "
                                   "    AND E.RECODE = 'ACD' "
                                   "    LEFT OUTER JOIN OSCODEM F "
                                   "    ON A.MCODE = F.MCODE "
                                   "    LEFT OUTER JOIN OSREFCP G "
                                   "    ON F.GBN = G.RESKEY "
                                   "    AND G.RECODE = 'CGB' "                                   
                                   "     WHERE A.ACIOGB = '1' "
                                   "     AND A.ICUST = '" + str(iCust) + "'"
                                   "     AND A.ACGUBN = '" + str(payGbn) + "'"
                                   " ) AA "
                                   " WHERE AA.IODATE BETWEEN '" + str(strDate) + "' AND '" + str(endDate) + "' "
                                   " ORDER BY AA.IODATE ")
                    mainresult = cursor.fetchall()

                    return JsonResponse({'balList': balresult, 'mainList': mainresult})

            if strDate != '' and endDate != '' and cboAct == '' and cboCust == '':
                with connection.cursor() as cursor:
                    cursor.execute(" SELECT IFNULL(SUM(BAL), 0), IFNULL(SUM(INTOTAL), 0), IFNULL(SUM(OUTTOTAL), 0), IFNULL(SUM(BAL + INTOTAL - OUTTOTAL), 0) FROM "
                                   " ("
                                   " SELECT SUM(IFNULL(ACAMTS, 0)) AS BAL, 0 AS INTOTAL, 0 AS OUTTOTAL FROM ACBALANCE WHERE ACDATE < '" + str(strDate) + "' AND ICUST = '" + str(iCust) + "' "
                                   " UNION ALL "
                                   " SELECT 0 AS BAL, SUM(IFNULL(ACAMTS, 0)) AS INTOTAL, 0 AS OUTTOTAL FROM SISACCTT "
                                   "        WHERE ACIOGB = '2' AND ACDATE < '" + str(strDate) + "' AND ICUST = '" + str(iCust) + "' AND FIN_OPT = 'Y' "
                                   " UNION ALL "
                                   " SELECT 0 AS BAL, 0 AS INTOTAL, SUM(IFNULL(ACAMTS, 0)) AS OUTTOTAL FROM SISACCTT "
                                   "        WHERE ACIOGB = '1' AND ACDATE < '" + str(strDate) + "' AND ICUST = '" + str(iCust) + "' AND FIN_OPT = 'Y' "
                                   " ) AA ")
                    balresult = cursor.fetchall()
                with connection.cursor() as cursor:
                    cursor.execute("  SELECT IFNULL(AA.ACIOGB, ''), IFNULL(AA.IODATE, ''), IFNULL(AA.IN_ACAMTS, 0), IFNULL(AA.OUT_ACAMTS, 0)"
                                   "        , IFNULL(AA.ACCUST, ''), IFNULL(AA.CUST_NME, ''), IFNULL(AA.ACACNUMBER, ''), IFNULL(AA.ACNUM_NAME, '')"
                                   "        , IFNULL(AA.MCODE, ''), IFNULL(AA.FIN_OPT, ''), IFNULL(AA.MCODENM, ''), IFNULL(AA.ACTITLE, '')"
                                   "        , IFNULL(AA.ACSEQN, ''), IFNULL(AA.ACODE, ''), IFNULL(AA.ACODENM, ''), IFNULL(AA.GBN, '')"
                                   "        , IFNULL(AA.GBNNM, ''), IFNULL(AA.APPLYDT, ''), IFNULL(AA.ACGUBN, ''), IFNULL(AA.GBN, '')" 
                                   "        , IFNULL(AA.FIN_OPT, ''), IFNULL(AA.MID_OPT, ''), IFNULL(AA.ACUSE, ''), IFNULL(AA.ACGUBN, ''), IFNULL(AA.NME, '') FROM "
                                   " ( "
                                   "     SELECT A.ACIOGB, A.IODATE, A.ACAMTS AS IN_ACAMTS, 0 AS OUT_ACAMTS, A.ACCUST, B.CUST_NME"
                                   "            , A.ACACNUMBER, C.ACNUM_NAME, A.MCODE, A.FIN_OPT, D.MCODENM, A.ACTITLE, A.ACSEQN"
                                   "            , A.ACODE, E.RESNAM AS ACODENM, F.GBN, G.RESNAM AS GBNNM, A.APPLYDT, A.ACGUBN, A.MID_OPT, A.ACUSE "
                                   "            , IFNULL((SELECT X.EMP_NME FROM OSSIGN Y "
                                   "                LEFT OUTER JOIN PIS1TB001 X ON Y.EMP_NBR = X.EMP_NBR "
                                   "                WHERE Y.ICUST = A.ICUST AND Y.ACDATE = A.IODATE AND Y.ACSEQN = A.ACSEQN AND Y.ACIOGB = A.ACIOGB "
                                   "                AND Y.SEQ = (SELECT IFNULL(MAX(SEQ), '') FROM OSSIGN WHERE ICUST = A.ICUST AND ACDATE = A.IODATE AND ACSEQN = A.ACSEQN AND ACIOGB = A.ACIOGB AND OPT = 'Y')), '') AS NME"
                                   "     FROM SISACCTT A "
                                   "     LEFT OUTER JOIN MIS1TB003 B "
                                   "     ON A.ACCUST = B.CUST_NBR "
                                   "     LEFT OUTER JOIN ACNUMBER C "
                                   "     ON A.ACACNUMBER = C.ACNUMBER "
                                   "     LEFT OUTER JOIN OSCODEM D "
                                   "     ON A.MCODE = D.MCODE "
                                   "    LEFT OUTER JOIN OSREFCP E "
                                   "    ON A.ACODE = E.RESKEY "
                                   "    AND E.RECODE = 'ACD' "
                                   "    LEFT OUTER JOIN OSCODEM F "
                                   "    ON A.MCODE = F.MCODE "
                                   "    LEFT OUTER JOIN OSREFCP G "
                                   "    ON F.GBN = G.RESKEY "
                                   "    AND G.RECODE = 'CGB' "
                                   "     WHERE A.ACIOGB = '2' "
                                   "     AND A.ICUST = '" + str(iCust) + "'"
                                   "     UNION ALL "
                                   "     SELECT A.ACIOGB, A.IODATE, 0 AS IN_ACAMTS, A.ACAMTS AS OUT_ACAMTS, A.ACCUST, B.CUST_NME"
                                   "            , A.ACACNUMBER, C.ACNUM_NAME, A.MCODE, A.FIN_OPT, D.MCODENM, A.ACTITLE, A.ACSEQN"
                                   "            , A.ACODE, E.RESNAM AS ACODENM, F.GBN, G.RESNAM AS GBNNM, A.APPLYDT, A.ACGUBN, A.MID_OPT, A.ACUSE "
                                   "            , IFNULL((SELECT X.EMP_NME FROM OSSIGN Y "
                                   "                LEFT OUTER JOIN PIS1TB001 X ON Y.EMP_NBR = X.EMP_NBR "
                                   "                WHERE Y.ICUST = A.ICUST AND Y.ACDATE = A.IODATE AND Y.ACSEQN = A.ACSEQN AND Y.ACIOGB = A.ACIOGB "
                                   "                AND Y.SEQ = (SELECT IFNULL(MAX(SEQ), '') FROM OSSIGN WHERE ICUST = A.ICUST AND ACDATE = A.IODATE AND ACSEQN = A.ACSEQN AND ACIOGB = A.ACIOGB AND OPT = 'Y')), '') AS NME "
                                   "     FROM SISACCTT A "
                                   "     LEFT OUTER JOIN MIS1TB003 B "
                                   "     ON A.ACCUST = B.CUST_NBR "
                                   "     LEFT OUTER JOIN ACNUMBER C "
                                   "     ON A.ACACNUMBER = C.ACNUMBER "
                                   "     LEFT OUTER JOIN OSCODEM D "
                                   "     ON A.MCODE = D.MCODE "
                                   "    LEFT OUTER JOIN OSREFCP E "
                                   "    ON A.ACODE = E.RESKEY "
                                   "    AND E.RECODE = 'ACD' "
                                   "    LEFT OUTER JOIN OSCODEM F "
                                   "    ON A.MCODE = F.MCODE "
                                   "    LEFT OUTER JOIN OSREFCP G "
                                   "    ON F.GBN = G.RESKEY "
                                   "    AND G.RECODE = 'CGB' "                                   
                                   "     WHERE A.ACIOGB = '1' "
                                   "     AND A.ICUST = '" + str(iCust) + "'"
                                   " ) AA "
                                   " WHERE AA.IODATE BETWEEN '" + str(strDate) + "' AND '" + str(endDate) + "' "
                                   " ORDER BY AA.IODATE ")
                    mainresult = cursor.fetchall()

                    # 거래처
                    with connection.cursor() as cursor:
                        cursor.execute(" SELECT CUST_NBR, CUST_NME FROM MIS1TB003 WHERE ICUST = '" + str(iCust) + "' ORDER BY CUST_NBR ")
                        cboCust = cursor.fetchall()

                    with connection.cursor() as cursor:
                        cursor.execute(" SELECT ACNUMBER FROM ACNUMBER WHERE ICUST = '" + str(iCust) + "' ")
                        cboAct = cursor.fetchall()

                    with connection.cursor() as cursor:
                        cursor.execute(" SELECT A.ACBKCD, B.RESNAM FROM ACNUMBER A LEFT OUTER JOIN OSREFCP B ON A.ACBKCD = B.RESKEY AND B.RECODE = 'BNK' AND A.ICUST = '" + str(iCust) + "' "
                                       " GROUP BY A.ACBKCD, B.RESNAM ORDER BY A.ACBKCD ")
                        inputBank = cursor.fetchall()

                    return JsonResponse({'balList': balresult, 'mainList': mainresult, 'cboCust': cboCust, 'cboAct': cboAct, 'inputBank': inputBank})

            if cboCust != '' and cboAct == '':
                with connection.cursor() as cursor:
                    cursor.execute(" SELECT IFNULL(SUM(BAL), 0), IFNULL(SUM(INTOTAL), 0), IFNULL(SUM(OUTTOTAL), 0), IFNULL(SUM(BAL + INTOTAL - OUTTOTAL), 0) FROM "
                                   " ( "
                                   "    SELECT SUM(IFNULL(A.ACAMTS, 0)) AS BAL, 0 AS INTOTAL, 0 AS OUTTOTAL FROM ACBALANCE A    "
                                   "          LEFT OUTER JOIN ACNUMBER B ON A.ACNUMBER = B.ACNUMBER WHERE A.ACDATE < '" + str(strDate) + "' AND B.ACBKCD = '" + str(inputBank) + "' AND A.ICUST = '" + str(iCust) + "' "
                                   "     UNION ALL "
                                   "    SELECT 0 AS BAL, SUM(IFNULL(ACAMTS, 0)) AS INTOTAL, 0 AS OUTTOTAL FROM SISACCTT A"
                                   "           LEFT OUTER JOIN ACNUMBER B ON A.ACACNUMBER = B.ACNUMBER"
                                   "           WHERE A.ACIOGB = '2' AND A.ACDATE < '" + str(strDate) + "' AND A.ICUST = '" + str(iCust) + "' AND FIN_OPT = 'Y' "
                                   "    UNION ALL "
                                   "    SELECT 0 AS BAL, 0 AS INTOTAL, SUM(IFNULL(ACAMTS, 0)) AS OUTTOTAL FROM SISACCTT A"
                                   "           LEFT OUTER JOIN ACNUMBER B ON A.ACACNUMBER = B.ACNUMBER"
                                   "           WHERE A.ACIOGB = '1' AND A.ACDATE < '" + str(strDate) + "' AND A.ICUST = '" + str(iCust) + "' AND FIN_OPT = 'Y' "
                                   " ) AA ")
                    balresult = cursor.fetchall()

                    with connection.cursor() as cursor:
                        cursor.execute("  SELECT IFNULL(AA.ACIOGB, ''), IFNULL(AA.IODATE, ''), IFNULL(AA.IN_ACAMTS, 0), IFNULL(AA.OUT_ACAMTS, 0)"
                                       "        , IFNULL(AA.ACCUST, ''), IFNULL(AA.CUST_NME, ''), IFNULL(AA.ACACNUMBER, ''), IFNULL(AA.ACNUM_NAME, '')"
                                       "        , IFNULL(AA.MCODE, ''), IFNULL(AA.FIN_OPT, ''), IFNULL(AA.MCODENM, ''), IFNULL(AA.ACTITLE, '')"
                                       "        , IFNULL(AA.ACSEQN, ''), IFNULL(AA.ACODE, ''), IFNULL(AA.ACODENM, ''), IFNULL(AA.GBN, '')"
                                       "        , IFNULL(AA.GBNNM, ''), IFNULL(AA.APPLYDT, ''), IFNULL(AA.ACGUBN, ''), IFNULL(AA.GBN, '')"
                                       "        , IFNULL(AA.FIN_OPT, ''), IFNULL(AA.MID_OPT, ''), IFNULL(AA.ACUSE, ''), IFNULL(AA.ACGUBN, ''), IFNULL(AA.NME, '') FROM "
                                       " ( "
                                       "     SELECT A.ACIOGB, A.IODATE, A.ACAMTS AS IN_ACAMTS, 0 AS OUT_ACAMTS, A.ACCUST, B.CUST_NME"
                                       "            , A.ACACNUMBER, C.ACNUM_NAME, A.MCODE, A.FIN_OPT, D.MCODENM, A.ACTITLE, A.ACSEQN"
                                       "            , A.ACODE, E.RESNAM AS ACODENM, F.GBN, G.RESNAM AS GBNNM, C.ACBKCD, H.RESNAM AS BANKNM, A.APPLYDT, A.ACGUBN, A.MID_OPT, A.ACUSE "
                                       "            , IFNULL((SELECT X.EMP_NME FROM OSSIGN Y "
                                       "                LEFT OUTER JOIN PIS1TB001 X ON Y.EMP_NBR = X.EMP_NBR "
                                       "                WHERE Y.ICUST = A.ICUST AND Y.ACDATE = A.IODATE AND Y.ACSEQN = A.ACSEQN AND Y.ACIOGB = A.ACIOGB "
                                       "                AND Y.SEQ = (SELECT IFNULL(MAX(SEQ), '') FROM OSSIGN WHERE ICUST = A.ICUST AND ACDATE = A.IODATE AND ACSEQN = A.ACSEQN AND ACIOGB = A.ACIOGB AND OPT = 'Y')), '') AS NME "
                                       "     FROM SISACCTT A "
                                       "     LEFT OUTER JOIN MIS1TB003 B "
                                       "     ON A.ACCUST = B.CUST_NBR "
                                       "     LEFT OUTER JOIN ACNUMBER C "
                                       "     ON A.ACACNUMBER = C.ACNUMBER "
                                       "     LEFT OUTER JOIN OSCODEM D "
                                       "     ON A.MCODE = D.MCODE "
                                       "    LEFT OUTER JOIN OSREFCP E "
                                       "    ON A.ACODE = E.RESKEY "
                                       "    AND E.RECODE = 'ACD' "
                                       "    LEFT OUTER JOIN OSCODEM F "
                                       "    ON A.MCODE = F.MCODE "
                                       "    LEFT OUTER JOIN OSREFCP G "
                                       "    ON F.GBN = G.RESKEY "
                                       "    AND G.RECODE = 'CGB' "
                                       "    LEFT OUTER JOIN OSREFCP H"
                                       "    ON C.ACBKCD = H.RESKEY"
                                       "    AND H.RECODE = 'BNK'"
                                       "     WHERE A.ACIOGB = '2' "
                                       "     AND A.ICUST = '" + str(iCust) + "'"
                                       "     UNION ALL "
                                       "     SELECT A.ACIOGB, A.IODATE, 0 AS IN_ACAMTS, A.ACAMTS AS OUT_ACAMTS, A.ACCUST, B.CUST_NME"
                                       "            , A.ACACNUMBER, C.ACNUM_NAME, A.MCODE, A.FIN_OPT, D.MCODENM, A.ACTITLE, A.ACSEQN"
                                       "            , A.ACODE, E.RESNAM AS ACODENM, F.GBN, G.RESNAM AS GBNNM, C.ACBKCD, H.RESNAM AS BANKNM, A.APPLYDT, A.ACGUBN, A.MID_OPT, A.ACUSE "
                                       "            , IFNULL((SELECT X.EMP_NME FROM OSSIGN Y "
                                       "                LEFT OUTER JOIN PIS1TB001 X ON Y.EMP_NBR = X.EMP_NBR "
                                       "                WHERE Y.ICUST = A.ICUST AND Y.ACDATE = A.IODATE AND Y.ACSEQN = A.ACSEQN AND Y.ACIOGB = A.ACIOGB "
                                       "                AND Y.SEQ = (SELECT IFNULL(MAX(SEQ), '') FROM OSSIGN WHERE ICUST = A.ICUST AND ACDATE = A.IODATE AND ACSEQN = A.ACSEQN AND ACIOGB = A.ACIOGB AND OPT = 'Y')), '') AS NME "
                                       "     FROM SISACCTT A "
                                       "     LEFT OUTER JOIN MIS1TB003 B "
                                       "     ON A.ACCUST = B.CUST_NBR "
                                       "     LEFT OUTER JOIN ACNUMBER C "
                                       "     ON A.ACACNUMBER = C.ACNUMBER "
                                       "     LEFT OUTER JOIN OSCODEM D "
                                       "     ON A.MCODE = D.MCODE "
                                       "    LEFT OUTER JOIN OSREFCP E "
                                       "    ON A.ACODE = E.RESKEY "
                                       "    AND E.RECODE = 'ACD' "
                                       "    LEFT OUTER JOIN OSCODEM F "
                                       "    ON A.MCODE = F.MCODE "
                                       "    LEFT OUTER JOIN OSREFCP G "
                                       "    ON F.GBN = G.RESKEY "
                                       "    AND G.RECODE = 'CGB' "
                                       "    LEFT OUTER JOIN OSREFCP H"
                                       "    ON C.ACBKCD = H.RESKEY"
                                       "    AND H.RECODE = 'BNK'"
                                       "     WHERE A.ACIOGB = '1' "
                                       "     AND A.ICUST = '" + str(iCust) + "'"
                                       " ) AA "
                                       " WHERE AA.IODATE BETWEEN '" + str(strDate) + "' AND '" + str(endDate) + "' "
                                       " AND AA.ACCUST = '" + str(cboCust) + "' "
                                       " ORDER BY AA.IODATE ")
                        mainresult = cursor.fetchall()

                    return JsonResponse({'balList': balresult, 'mainList': mainresult})

            if cboAct != '' and cboCust == '':
                with connection.cursor() as cursor:
                    cursor.execute(" SELECT IFNULL(SUM(BAL), 0), IFNULL(SUM(INTOTAL), 0), IFNULL(SUM(OUTTOTAL), 0), IFNULL(SUM(BAL + INTOTAL - OUTTOTAL), 0) FROM "
                                   " (  "
                                   "    SELECT SUM(IFNULL(ACAMTS, 0)) AS BAL, 0 AS INTOTAL, 0 AS OUTTOTAL FROM ACBALANCE "
                                   "            WHERE ACDATE < '" + str(strDate) + "' AND ACNUMBER = '" + str(cboAct) + "' AND ICUST = '" + str(iCust) + "' "
                                   "     UNION ALL "
                                   "    SELECT 0 AS BAL, SUM(IFNULL(ACAMTS, 0)) AS INTOTAL, 0 AS OUTTOTAL FROM SISACCTT A"
                                   "           LEFT OUTER JOIN ACNUMBER B ON A.ACACNUMBER = B.ACNUMBER"
                                   "           WHERE A.ACIOGB = '2' AND A.ACACNUMBER = '" + str(cboAct) + "' "
                                   "           AND A.ACDATE < '" + str(strDate) + "' AND A.ICUST = '" + str(iCust) + "' AND FIN_OPT = 'Y' "
                                   "    UNION ALL "
                                   "    SELECT 0 AS BAL, 0 AS INTOTAL, SUM(IFNULL(ACAMTS, 0)) AS OUTTOTAL FROM SISACCTT A"
                                   "           LEFT OUTER JOIN ACNUMBER B ON A.ACACNUMBER = B.ACNUMBER"
                                   "           WHERE A.ACIOGB = '1'AND A.ACACNUMBER = '" + str(cboAct) + "' "
                                   "           AND A.ACDATE < '" + str(strDate) + "' AND A.ICUST = '" + str(iCust) + "' AND FIN_OPT = 'Y' "
                                   " ) AA ")
                    # cursor.execute(" SELECT IFNULL(SUM(ACAMTS), 0) FROM ACBALANCE WHERE ACDATE < '" + str(strDate) + "' AND ACNUMBER = '" + str(cboAct) + "' AND ICUST = '" + str(iCust) + "' ")
                    balresult = cursor.fetchall()

                with connection.cursor() as cursor:
                    cursor.execute("  SELECT IFNULL(AA.ACIOGB, ''), IFNULL(AA.IODATE, ''), IFNULL(AA.IN_ACAMTS, 0), IFNULL(AA.OUT_ACAMTS, 0)"
                                   "        , IFNULL(AA.ACCUST, ''), IFNULL(AA.CUST_NME, ''), IFNULL(AA.ACACNUMBER, ''), IFNULL(AA.ACNUM_NAME, '')"
                                   "        , IFNULL(AA.MCODE, ''), IFNULL(AA.FIN_OPT, ''), IFNULL(AA.MCODENM, ''), IFNULL(AA.ACTITLE, '')"
                                   "        , IFNULL(AA.ACSEQN, ''), IFNULL(AA.ACODE, ''), IFNULL(AA.ACODENM, ''), IFNULL(AA.GBN, '')"
                                   "        , IFNULL(AA.GBNNM, ''), IFNULL(AA.APPLYDT, ''), IFNULL(AA.ACGUBN, ''), IFNULL(AA.GBN, '')"
                                   "        , IFNULL(AA.FIN_OPT, ''), IFNULL(AA.MID_OPT, ''), IFNULL(AA.ACUSE, ''), IFNULL(AA.ACGUBN, ''), IFNULL(AA.NME, '') FROM "
                                   " ( "
                                   "     SELECT A.ACIOGB, A.IODATE, A.ACAMTS AS IN_ACAMTS, 0 AS OUT_ACAMTS, A.ACCUST, B.CUST_NME"
                                   "            , A.ACACNUMBER, C.ACNUM_NAME, A.MCODE, A.FIN_OPT, D.MCODENM, A.ACTITLE, A.ACSEQN"
                                   "            , A.ACODE, E.RESNAM AS ACODENM, F.GBN, G.RESNAM AS GBNNM, A.APPLYDT, A.ACGUBN, A.MID_OPT, A.ACUSE  "
                                   "            , IFNULL((SELECT X.EMP_NME FROM OSSIGN Y "
                                   "                LEFT OUTER JOIN PIS1TB001 X ON Y.EMP_NBR = X.EMP_NBR "
                                   "                WHERE Y.ICUST = A.ICUST AND Y.ACDATE = A.IODATE AND Y.ACSEQN = A.ACSEQN AND Y.ACIOGB = A.ACIOGB "
                                   "                AND Y.SEQ = (SELECT IFNULL(MAX(SEQ), '') FROM OSSIGN WHERE ICUST = A.ICUST AND ACDATE = A.IODATE AND ACSEQN = A.ACSEQN AND ACIOGB = A.ACIOGB AND OPT = 'Y')), '') AS NME "
                                   "     FROM SISACCTT A "
                                   "     LEFT OUTER JOIN MIS1TB003 B "
                                   "     ON A.ACCUST = B.CUST_NBR "
                                   "     LEFT OUTER JOIN ACNUMBER C "
                                   "     ON A.ACACNUMBER = C.ACNUMBER "
                                   "     LEFT OUTER JOIN OSCODEM D "
                                   "     ON A.MCODE = D.MCODE "
                                   "    LEFT OUTER JOIN OSREFCP E "
                                   "    ON A.ACODE = E.RESKEY "
                                   "    AND E.RECODE = 'ACD' "
                                   "    LEFT OUTER JOIN OSCODEM F "
                                   "    ON A.MCODE = F.MCODE "
                                   "    LEFT OUTER JOIN OSREFCP G "
                                   "    ON F.GBN = G.RESKEY "
                                   "    AND G.RECODE = 'CGB' "
                                   "     WHERE A.ACIOGB = '2' "
                                   "     AND A.ICUST = '" + str(iCust) + "'"
                                   "     UNION ALL "
                                   "     SELECT A.ACIOGB, A.IODATE, 0 AS IN_ACAMTS, A.ACAMTS AS OUT_ACAMTS, A.ACCUST, B.CUST_NME"
                                   "            , A.ACACNUMBER, C.ACNUM_NAME, A.MCODE, A.FIN_OPT, D.MCODENM, A.ACTITLE, A.ACSEQN"
                                   "            , A.ACODE, E.RESNAM AS ACODENM, F.GBN, G.RESNAM AS GBNNM, A.APPLYDT, A.ACGUBN, A.MID_OPT, A.ACUSE "
                                   "            , IFNULL((SELECT X.EMP_NME FROM OSSIGN Y "
                                   "                LEFT OUTER JOIN PIS1TB001 X ON Y.EMP_NBR = X.EMP_NBR "
                                   "                WHERE Y.ICUST = A.ICUST AND Y.ACDATE = A.IODATE AND Y.ACSEQN = A.ACSEQN AND Y.ACIOGB = A.ACIOGB "
                                   "                AND Y.SEQ = (SELECT IFNULL(MAX(SEQ), '') FROM OSSIGN WHERE ICUST = A.ICUST AND ACDATE = A.IODATE AND ACSEQN = A.ACSEQN AND ACIOGB = A.ACIOGB AND OPT = 'Y')), '') AS NME "
                                   "     FROM SISACCTT A "
                                   "     LEFT OUTER JOIN MIS1TB003 B "
                                   "     ON A.ACCUST = B.CUST_NBR "
                                   "     LEFT OUTER JOIN ACNUMBER C "
                                   "     ON A.ACACNUMBER = C.ACNUMBER "
                                   "     LEFT OUTER JOIN OSCODEM D "
                                   "     ON A.MCODE = D.MCODE "
                                   "    LEFT OUTER JOIN OSREFCP E "
                                   "    ON A.ACODE = E.RESKEY "
                                   "    AND E.RECODE = 'ACD' "
                                   "    LEFT OUTER JOIN OSCODEM F "
                                   "    ON A.MCODE = F.MCODE "
                                   "    LEFT OUTER JOIN OSREFCP G "
                                   "    ON F.GBN = G.RESKEY "
                                   "    AND G.RECODE = 'CGB' "                                 
                                   "     WHERE A.ACIOGB = '1' "
                                   "     AND A.ICUST = '" + str(iCust) + "'"
                                   " ) AA "
                                   " WHERE AA.IODATE BETWEEN '" + str(strDate) + "' AND '" + str(endDate) + "' "
                                   " AND AA.ACACNUMBER = '" + str(cboAct) + "' "
                                   " ORDER BY AA.IODATE ")
                    mainresult = cursor.fetchall()

                return JsonResponse({'balList': balresult, 'mainList': mainresult})

            if cboAct != '' and cboCust != '':
                with connection.cursor() as cursor:
                    cursor.execute(" SELECT IFNULL(SUM(BAL), 0), IFNULL(SUM(INTOTAL), 0), IFNULL(SUM(OUTTOTAL), 0), IFNULL(SUM(BAL + INTOTAL - OUTTOTAL), 0) FROM "
                                   " ("
                                   "    SELECT SUM(IFNULL(A.ACAMTS, 0)) AS BAL, 0 AS INTOTAL, 0 AS OUTTOTAL FROM ACBALANCE A "
                                   "            LEFT OUTER JOIN ACNUMBER B ON A.ACNUMBER = B.ACNUMBER "
                                   "            WHERE A.ACDATE < '" + str(strDate) + "' AND A.ACNUMBER = '" + str(cboAct) + "' AND A.ICUST = '" + str(iCust) + "' "
                                   "     UNION ALL "
                                   "    SELECT 0 AS BAL, SUM(IFNULL(ACAMTS, 0)) AS INTOTAL, 0 AS OUTTOTAL FROM SISACCTT A"
                                   "           LEFT OUTER JOIN ACNUMBER B ON A.ACACNUMBER = B.ACNUMBER"
                                   "           WHERE A.ACIOGB = '2' AND A.ACACNUMBER = '" + str(cboAct) + "' "
                                   "           AND A.ACDATE < '" + str(strDate) + "' AND A.ICUST = '" + str(iCust) + "' AND FIN_OPT = 'Y' "
                                   "    UNION ALL "
                                   "    SELECT 0 AS BAL, 0 AS INTOTAL, SUM(IFNULL(ACAMTS, 0)) AS OUTTOTAL FROM SISACCTT A"
                                   "           LEFT OUTER JOIN ACNUMBER B ON A.ACACNUMBER = B.ACNUMBER"
                                   "           WHERE A.ACIOGB = '1' AND A.ACACNUMBER = '" + str(cboAct) + "' "
                                   "           AND A.ACDATE < '" + str(strDate) + "' AND A.ICUST = '" + str(iCust) + "' AND FIN_OPT = 'Y' "
                                   " ) AA ")
                    # cursor.execute(" SELECT IFNULL(SUM(ACAMTS), 0) FROM ACBALANCE WHERE ACDATE < '" + str(strDate) + "' AND ACNUMBER = '" + str(cboAct) + "' AND ICUST = '" + str(iCust) + "' ")
                    balresult = cursor.fetchall()

                with connection.cursor() as cursor:
                    cursor.execute("  SELECT IFNULL(AA.ACIOGB, ''), IFNULL(AA.IODATE, ''), IFNULL(AA.IN_ACAMTS, 0), IFNULL(AA.OUT_ACAMTS, 0)"
                                   "            , IFNULL(AA.ACCUST, ''), IFNULL(AA.CUST_NME, ''), IFNULL(AA.ACACNUMBER, ''), IFNULL(AA.ACNUM_NAME, '')"
                                   "            , IFNULL(AA.MCODE, ''), IFNULL(AA.FIN_OPT, ''), IFNULL(AA.MCODENM, ''), IFNULL(AA.ACTITLE, '')"
                                   "            , IFNULL(AA.ACSEQN, ''), IFNULL(AA.ACODE, ''), IFNULL(AA.ACODENM, ''), IFNULL(AA.GBN, ''), IFNULL(AA.GBNNM, '')"
                                   "            , IFNULL(AA.ACBKCD, ''), IFNULL(AA.BANKNM, ''), IFNULL(AA.APPLYDT, ''), IFNULL(AA.ACGUBN, ''), IFNULL(AA.MID_OPT, '') "
                                   "            , IFNULL(AA.ACUSE, ''), IFNULL(AA.ACGUBN, ''), IFNULL(AA.NME, '') FROM "
                                   " ( "
                                   "     SELECT A.ACIOGB, A.IODATE, A.ACAMTS AS IN_ACAMTS, 0 AS OUT_ACAMTS, A.ACCUST, B.CUST_NME"
                                   "            , A.ACACNUMBER, C.ACNUM_NAME, A.MCODE, A.FIN_OPT, D.MCODENM, A.ACTITLE, A.ACSEQN"
                                   "            , A.ACODE, E.RESNAM AS ACODENM, F.GBN, G.RESNAM AS GBNNM, C.ACBKCD, H.RESNAM AS BANKNM, A.APPLYDT, A.ACGUBN, A.MID_OPT, A.ACUSE"
                                   "            , IFNULL((SELECT X.EMP_NME FROM OSSIGN Y "
                                   "                LEFT OUTER JOIN PIS1TB001 X ON Y.EMP_NBR = X.EMP_NBR "
                                   "                WHERE Y.ICUST = A.ICUST AND Y.ACDATE = A.IODATE AND Y.ACSEQN = A.ACSEQN AND Y.ACIOGB = A.ACIOGB "
                                   "                AND Y.SEQ = (SELECT IFNULL(MAX(SEQ), '') FROM OSSIGN WHERE ICUST = A.ICUST AND ACDATE = A.IODATE AND ACSEQN = A.ACSEQN AND ACIOGB = A.ACIOGB AND OPT = 'Y')), '') AS NME "
                                   "     FROM SISACCTT A "
                                   "     LEFT OUTER JOIN MIS1TB003 B "
                                   "     ON A.ACCUST = B.CUST_NBR "
                                   "     LEFT OUTER JOIN ACNUMBER C "
                                   "     ON A.ACACNUMBER = C.ACNUMBER "
                                   "     LEFT OUTER JOIN OSCODEM D "
                                   "     ON A.MCODE = D.MCODE "
                                   "    LEFT OUTER JOIN OSREFCP E "
                                   "    ON A.ACODE = E.RESKEY "
                                   "    AND E.RECODE = 'ACD' "
                                   "    LEFT OUTER JOIN OSCODEM F "
                                   "    ON A.MCODE = F.MCODE "
                                   "    LEFT OUTER JOIN OSREFCP G "
                                   "    ON F.GBN = G.RESKEY "
                                   "    AND G.RECODE = 'CGB' "
                                   "    LEFT OUTER JOIN OSREFCP H"
                                   "    ON C.ACBKCD = H.RESKEY"
                                   "    AND H.RECODE = 'BNK'"
                                   "     WHERE A.ACIOGB = '2' "
                                   "     AND A.ICUST = '" + str(iCust) + "'"
                                   "     UNION ALL "
                                   "     SELECT A.ACIOGB, A.IODATE, 0 AS IN_ACAMTS, A.ACAMTS AS OUT_ACAMTS, A.ACCUST, B.CUST_NME"
                                   "            , A.ACACNUMBER, C.ACNUM_NAME, A.MCODE, A.FIN_OPT, D.MCODENM, A.ACTITLE, A.ACSEQN"
                                   "            , A.ACODE, E.RESNAM AS ACODENM, F.GBN, G.RESNAM AS GBNNM, C.ACBKCD, H.RESNAM AS BANKNM, A.APPLYDT, A.ACGUBN, A.MID_OPT, A.ACUSE "
                                   "            , IFNULL((SELECT X.EMP_NME FROM OSSIGN Y "
                                   "                LEFT OUTER JOIN PIS1TB001 X ON Y.EMP_NBR = X.EMP_NBR "
                                   "                WHERE Y.ICUST = A.ICUST AND Y.ACDATE = A.IODATE AND Y.ACSEQN = A.ACSEQN AND Y.ACIOGB = A.ACIOGB "
                                   "                AND Y.SEQ = (SELECT IFNULL(MAX(SEQ), '') FROM OSSIGN WHERE ICUST = A.ICUST AND ACDATE = A.IODATE AND ACSEQN = A.ACSEQN AND ACIOGB = A.ACIOGB AND OPT = 'Y')), '') AS NME "
                                   "     FROM SISACCTT A "
                                   "     LEFT OUTER JOIN MIS1TB003 B "
                                   "     ON A.ACCUST = B.CUST_NBR "
                                   "     LEFT OUTER JOIN ACNUMBER C "
                                   "     ON A.ACACNUMBER = C.ACNUMBER "
                                   "     LEFT OUTER JOIN OSCODEM D "
                                   "     ON A.MCODE = D.MCODE "
                                   "    LEFT OUTER JOIN OSREFCP E "
                                   "    ON A.ACODE = E.RESKEY "
                                   "    AND E.RECODE = 'ACD' "
                                   "    LEFT OUTER JOIN OSCODEM F "
                                   "    ON A.MCODE = F.MCODE "
                                   "    LEFT OUTER JOIN OSREFCP G "
                                   "    ON F.GBN = G.RESKEY "
                                   "    AND G.RECODE = 'CGB' "
                                   "    LEFT OUTER JOIN OSREFCP H"
                                   "    ON C.ACBKCD = H.RESKEY"
                                   "    AND H.RECODE = 'BNK'"
                                   "     WHERE A.ACIOGB = '1' "
                                   "     AND A.ICUST = '" + str(iCust) + "'"
                                   " ) AA "
                                   " WHERE AA.IODATE BETWEEN '" + strDate + "' AND '" + endDate + "' "
                                   " AND AA.ACACNUMBER = '" + str(cboAct) + "' "
                                   " AND AA.ACCUST = '" + str(cboCust) + "' "
                                   " ORDER BY AA.IODATE ")
                    mainresult = cursor.fetchall()

                return JsonResponse({'balList': balresult, 'mainList': mainresult})

        # 등급이 1이거나 아니면 총금액은 조회되지 않는다.
        if int(chkEmp[0][0]) == 2:
            with connection.cursor() as cursor:
                cursor.execute(" SELECT EMP_DEPT FROM PIS1TB001 WHERE EMP_NBR = '" + str(creUser) + "' AND ICUST = '" + str(iCust) + "' ")
                emp = cursor.fetchall()

                empDept = emp[0][0]

            if Gbn != '':
                if Gbn == '1' or Gbn == '4':
                    balresult = ''
                    with connection.cursor() as cursor:
                        cursor.execute(
                            "  SELECT IFNULL(AA.ACIOGB, ''), IFNULL(AA.IODATE, ''), IFNULL(AA.IN_ACAMTS, 0), IFNULL(AA.OUT_ACAMTS, 0)"
                            "        , IFNULL(AA.ACCUST, ''), IFNULL(AA.CUST_NME, ''), IFNULL(AA.ACACNUMBER, ''), IFNULL(AA.ACNUM_NAME, '')"
                            "        , IFNULL(AA.MCODE, ''), IFNULL(AA.FIN_OPT, ''), IFNULL(AA.MCODENM, ''), IFNULL(AA.ACTITLE, '')"
                            "        , IFNULL(AA.ACSEQN, ''), IFNULL(AA.ACODE, ''), IFNULL(AA.ACODENM, ''), IFNULL(AA.GBN, '')"
                            "        , IFNULL(AA.GBNNM, ''), IFNULL(AA.APPLYDT, ''), IFNULL(AA.ACGUBN, ''), IFNULL(AA.GBN, '')"
                            "        , IFNULL(AA.FIN_OPT, ''), IFNULL(AA.MID_OPT, ''), IFNULL(AA.ACUSE, ''), IFNULL(AA.ACGUBN, ''), IFNULL(AA.NME, '') FROM "
                            " ( "
                            "     SELECT A.ACIOGB, A.IODATE, A.ACAMTS AS IN_ACAMTS, 0 AS OUT_ACAMTS, A.ACCUST, B.CUST_NME"
                            "            , A.ACACNUMBER, C.ACNUM_NAME, A.MCODE, A.FIN_OPT, D.MCODENM, A.ACTITLE, A.ACSEQN"
                            "            , A.ACODE, E.RESNAM AS ACODENM, F.GBN, G.RESNAM AS GBNNM, A.APPLYDT, A.ACGUBN, A.MID_OPT, A.ACUSE "
                            "            , IFNULL((SELECT X.EMP_NME FROM OSSIGN Y "
                            "                LEFT OUTER JOIN PIS1TB001 X ON Y.EMP_NBR = X.EMP_NBR "
                            "                WHERE Y.ICUST = A.ICUST AND Y.ACDATE = A.IODATE AND Y.ACSEQN = A.ACSEQN AND Y.ACIOGB = A.ACIOGB "
                            "                AND Y.SEQ = (SELECT IFNULL(MAX(SEQ), '') FROM OSSIGN WHERE ICUST = A.ICUST AND ACDATE = A.IODATE AND ACSEQN = A.ACSEQN AND ACIOGB = A.ACIOGB AND OPT = 'Y')), '') AS NME "
                            "     FROM SISACCTT A "
                            "     LEFT OUTER JOIN MIS1TB003 B "
                            "     ON A.ACCUST = B.CUST_NBR "
                            "     LEFT OUTER JOIN ACNUMBER C "
                            "     ON A.ACACNUMBER = C.ACNUMBER "
                            "     LEFT OUTER JOIN OSCODEM D "
                            "     ON A.MCODE = D.MCODE "
                            "    LEFT OUTER JOIN OSREFCP E "
                            "    ON A.ACODE = E.RESKEY "
                            "    AND E.RECODE = 'ACD' "
                            "    LEFT OUTER JOIN OSCODEM F "
                            "    ON A.MCODE = F.MCODE "
                            "    LEFT OUTER JOIN OSREFCP G "
                            "    ON F.GBN = G.RESKEY "
                            "    AND G.RECODE = 'CGB' "
                            "    LEFT OUTER JOIN PIS1TB001 I "
                            "    ON A.CRE_USER = I.EMP_NBR "
                            "    WHERE A.ACIOGB = '2' "
                            "    AND A.ICUST = '" + str(iCust) + "'"
                            "    AND A.MID_OPT = 'Y'"
                            "    AND A.FIN_OPT = 'N'"
                           "    UNION ALL "
                           "    SELECT A.ACIOGB, A.IODATE, 0 AS IN_ACAMTS, A.ACAMTS AS OUT_ACAMTS, A.ACCUST, B.CUST_NME"
                           "           , A.ACACNUMBER, C.ACNUM_NAME, A.MCODE, A.FIN_OPT, D.MCODENM, A.ACTITLE, A.ACSEQN"
                           "            , A.ACODE, E.RESNAM AS ACODENM, F.GBN, G.RESNAM AS GBNNM, A.APPLYDT, A.ACGUBN, A.MID_OPT, A.ACUSE "
                           "            , IFNULL((SELECT X.EMP_NME FROM OSSIGN Y "
                           "                LEFT OUTER JOIN PIS1TB001 X ON Y.EMP_NBR = X.EMP_NBR "
                           "                WHERE Y.ICUST = A.ICUST AND Y.ACDATE = A.IODATE AND Y.ACSEQN = A.ACSEQN AND Y.ACIOGB = A.ACIOGB "
                           "                AND Y.SEQ = (SELECT IFNULL(MAX(SEQ), '') FROM OSSIGN WHERE ICUST = A.ICUST AND ACDATE = A.IODATE AND ACSEQN = A.ACSEQN AND ACIOGB = A.ACIOGB AND OPT = 'Y')), '') AS NME "
                           "    FROM SISACCTT A "
                           "    LEFT OUTER JOIN MIS1TB003 B "
                           "    ON A.ACCUST = B.CUST_NBR "
                           "    LEFT OUTER JOIN ACNUMBER C "
                           "    ON A.ACACNUMBER = C.ACNUMBER "
                           "    LEFT OUTER JOIN OSCODEM D "
                           "    ON A.MCODE = D.MCODE "
                           "    LEFT OUTER JOIN OSREFCP E "
                           "    ON A.ACODE = E.RESKEY "
                           "    AND E.RECODE = 'ACD' "
                           "    LEFT OUTER JOIN OSCODEM F "
                           "    ON A.MCODE = F.MCODE "
                           "    LEFT OUTER JOIN OSREFCP G "
                           "    ON F.GBN = G.RESKEY "
                           "    AND G.RECODE = 'CGB' "
                           "    LEFT OUTER JOIN PIS1TB001 I "
                           "    ON A.CRE_USER = I.EMP_NBR "
                           "    WHERE A.ACIOGB = '1' "
                           "    AND A.ICUST = '" + str(iCust) + "'"
                            "    AND A.MID_OPT = 'Y'"
                            "    AND A.FIN_OPT = 'N'"
                           " ) AA "
                           " WHERE AA.IODATE BETWEEN '" + str(strDate) + "' AND '" + str(endDate) + "' "
                           " ORDER BY AA.IODATE ")
                        mainresult = cursor.fetchall()
                        return JsonResponse({'balList': balresult, 'mainList': mainresult})

                if Gbn == '2':
                    balresult = ''
                    with connection.cursor() as cursor:
                        cursor.execute(
                            "  SELECT IFNULL(AA.ACIOGB, ''), IFNULL(AA.IODATE, ''), IFNULL(AA.IN_ACAMTS, 0), IFNULL(AA.OUT_ACAMTS, 0)"
                            "        , IFNULL(AA.ACCUST, ''), IFNULL(AA.CUST_NME, ''), IFNULL(AA.ACACNUMBER, ''), IFNULL(AA.ACNUM_NAME, '')"
                            "        , IFNULL(AA.MCODE, ''), IFNULL(AA.FIN_OPT, ''), IFNULL(AA.MCODENM, ''), IFNULL(AA.ACTITLE, '')"
                            "        , IFNULL(AA.ACSEQN, ''), IFNULL(AA.ACODE, ''), IFNULL(AA.ACODENM, ''), IFNULL(AA.GBN, '')"
                            "        , IFNULL(AA.GBNNM, ''), IFNULL(AA.APPLYDT, ''), IFNULL(AA.ACGUBN, ''), IFNULL(AA.GBN, '')"
                            "        , IFNULL(AA.FIN_OPT, ''), IFNULL(AA.MID_OPT, ''), IFNULL(AA.ACUSE, ''), IFNULL(AA.ACGUBN, ''), IFNULL(AA.NME, '') FROM "
                            " ( "
                            "     SELECT A.ACIOGB, A.IODATE, A.ACAMTS AS IN_ACAMTS, 0 AS OUT_ACAMTS, A.ACCUST, B.CUST_NME"
                            "            , A.ACACNUMBER, C.ACNUM_NAME, A.MCODE, A.FIN_OPT, D.MCODENM, A.ACTITLE, A.ACSEQN"
                            "            , A.ACODE, E.RESNAM AS ACODENM, F.GBN, G.RESNAM AS GBNNM, A.APPLYDT, A.ACGUBN, A.MID_OPT, A.ACUSE "
                            "            , IFNULL((SELECT X.EMP_NME FROM OSSIGN Y "
                            "                LEFT OUTER JOIN PIS1TB001 X ON Y.EMP_NBR = X.EMP_NBR "
                            "                WHERE Y.ICUST = A.ICUST AND Y.ACDATE = A.IODATE AND Y.ACSEQN = A.ACSEQN AND Y.ACIOGB = A.ACIOGB "
                            "                AND Y.SEQ = (SELECT IFNULL(MAX(SEQ), '') FROM OSSIGN WHERE ICUST = A.ICUST AND ACDATE = A.IODATE AND ACSEQN = A.ACSEQN AND ACIOGB = A.ACIOGB AND OPT = 'Y')), '') AS NME "
                            "     FROM SISACCTT A "
                            "     LEFT OUTER JOIN MIS1TB003 B "
                            "     ON A.ACCUST = B.CUST_NBR "
                            "     LEFT OUTER JOIN ACNUMBER C "
                            "     ON A.ACACNUMBER = C.ACNUMBER "
                            "     LEFT OUTER JOIN OSCODEM D "
                            "     ON A.MCODE = D.MCODE "
                            "    LEFT OUTER JOIN OSREFCP E "
                            "    ON A.ACODE = E.RESKEY "
                            "    AND E.RECODE = 'ACD' "
                            "    LEFT OUTER JOIN OSCODEM F "
                            "    ON A.MCODE = F.MCODE "
                            "    LEFT OUTER JOIN OSREFCP G "
                            "    ON F.GBN = G.RESKEY "
                            "    AND G.RECODE = 'CGB' "
                            "    LEFT OUTER JOIN PIS1TB001 I "
                            "    ON A.CRE_USER = I.EMP_NBR "
                            "    WHERE A.ACIOGB = '2' "
                            "    AND A.ICUST = '" + str(iCust) + "'"
                            "    AND A.MID_OPT = 'N'"
                            "    AND A.FIN_OPT = 'N'"
                           "    UNION ALL "
                           "    SELECT A.ACIOGB, A.IODATE, 0 AS IN_ACAMTS, A.ACAMTS AS OUT_ACAMTS, A.ACCUST, B.CUST_NME"
                           "           , A.ACACNUMBER, C.ACNUM_NAME, A.MCODE, A.FIN_OPT, D.MCODENM, A.ACTITLE, A.ACSEQN"
                           "            , A.ACODE, E.RESNAM AS ACODENM, F.GBN, G.RESNAM AS GBNNM, A.APPLYDT, A.ACGUBN, A.MID_OPT, A.ACUSE "
                           "            , IFNULL((SELECT X.EMP_NME FROM OSSIGN Y "
                           "                LEFT OUTER JOIN PIS1TB001 X ON Y.EMP_NBR = X.EMP_NBR "
                           "                WHERE Y.ICUST = A.ICUST AND Y.ACDATE = A.IODATE AND Y.ACSEQN = A.ACSEQN AND Y.ACIOGB = A.ACIOGB "
                           "                AND Y.SEQ = (SELECT IFNULL(MAX(SEQ), '') FROM OSSIGN WHERE ICUST = A.ICUST AND ACDATE = A.IODATE AND ACSEQN = A.ACSEQN AND ACIOGB = A.ACIOGB AND OPT = 'Y')), '') AS NME "
                           "    FROM SISACCTT A "
                           "    LEFT OUTER JOIN MIS1TB003 B "
                           "    ON A.ACCUST = B.CUST_NBR "
                           "    LEFT OUTER JOIN ACNUMBER C "
                           "    ON A.ACACNUMBER = C.ACNUMBER "
                           "    LEFT OUTER JOIN OSCODEM D "
                           "    ON A.MCODE = D.MCODE "
                           "    LEFT OUTER JOIN OSREFCP E "
                           "    ON A.ACODE = E.RESKEY "
                           "    AND E.RECODE = 'ACD' "
                           "    LEFT OUTER JOIN OSCODEM F "
                           "    ON A.MCODE = F.MCODE "
                           "    LEFT OUTER JOIN OSREFCP G "
                           "    ON F.GBN = G.RESKEY "
                           "    AND G.RECODE = 'CGB' "
                           "    LEFT OUTER JOIN PIS1TB001 I "
                           "    ON A.CRE_USER = I.EMP_NBR "
                           "    WHERE A.ACIOGB = '1' "
                           "    AND A.ICUST = '" + str(iCust) + "'"
                            "    AND A.MID_OPT = 'N'"
                            "    AND A.FIN_OPT = 'N'"
                           " ) AA "
                           " WHERE AA.IODATE BETWEEN '" + str(strDate) + "' AND '" + str(endDate) + "' "
                           " ORDER BY AA.IODATE ")
                        mainresult = cursor.fetchall()
                        return JsonResponse({'balList': balresult, 'mainList': mainresult})

                if Gbn == '3':
                    balresult = ''
                    with connection.cursor() as cursor:
                        cursor.execute(
                            "  SELECT IFNULL(AA.ACIOGB, ''), IFNULL(AA.IODATE, ''), IFNULL(AA.IN_ACAMTS, 0), IFNULL(AA.OUT_ACAMTS, 0)"
                            "        , IFNULL(AA.ACCUST, ''), IFNULL(AA.CUST_NME, ''), IFNULL(AA.ACACNUMBER, ''), IFNULL(AA.ACNUM_NAME, '')"
                            "        , IFNULL(AA.MCODE, ''), IFNULL(AA.FIN_OPT, ''), IFNULL(AA.MCODENM, ''), IFNULL(AA.ACTITLE, '')"
                            "        , IFNULL(AA.ACSEQN, ''), IFNULL(AA.ACODE, ''), IFNULL(AA.ACODENM, ''), IFNULL(AA.GBN, '')"
                            "        , IFNULL(AA.GBNNM, ''), IFNULL(AA.APPLYDT, ''), IFNULL(AA.ACGUBN, ''), IFNULL(AA.GBN, '')"
                            "        , IFNULL(AA.FIN_OPT, ''), IFNULL(AA.MID_OPT, ''), IFNULL(AA.ACUSE, ''), IFNULL(AA.ACGUBN, ''), IFNULL(AA.NME, '') FROM "
                            " ( "
                            "     SELECT A.ACIOGB, A.IODATE, A.ACAMTS AS IN_ACAMTS, 0 AS OUT_ACAMTS, A.ACCUST, B.CUST_NME"
                            "            , A.ACACNUMBER, C.ACNUM_NAME, A.MCODE, A.FIN_OPT, D.MCODENM, A.ACTITLE, A.ACSEQN"
                            "            , A.ACODE, E.RESNAM AS ACODENM, F.GBN, G.RESNAM AS GBNNM, A.APPLYDT, A.ACGUBN, A.MID_OPT, A.ACUSE "
                            "            , IFNULL((SELECT X.EMP_NME FROM OSSIGN Y "
                            "                LEFT OUTER JOIN PIS1TB001 X ON Y.EMP_NBR = X.EMP_NBR "
                            "                WHERE Y.ICUST = A.ICUST AND Y.ACDATE = A.IODATE AND Y.ACSEQN = A.ACSEQN AND Y.ACIOGB = A.ACIOGB "
                            "                AND Y.SEQ = (SELECT IFNULL(MAX(SEQ), '') FROM OSSIGN WHERE ICUST = A.ICUST AND ACDATE = A.IODATE AND ACSEQN = A.ACSEQN AND ACIOGB = A.ACIOGB AND OPT = 'Y')), '') AS NME "
                            "     FROM SISACCTT A "
                            "     LEFT OUTER JOIN MIS1TB003 B "
                            "     ON A.ACCUST = B.CUST_NBR "
                            "     LEFT OUTER JOIN ACNUMBER C "
                            "     ON A.ACACNUMBER = C.ACNUMBER "
                            "     LEFT OUTER JOIN OSCODEM D "
                            "     ON A.MCODE = D.MCODE "
                            "    LEFT OUTER JOIN OSREFCP E "
                            "    ON A.ACODE = E.RESKEY "
                            "    AND E.RECODE = 'ACD' "
                            "    LEFT OUTER JOIN OSCODEM F "
                            "    ON A.MCODE = F.MCODE "
                            "    LEFT OUTER JOIN OSREFCP G "
                            "    ON F.GBN = G.RESKEY "
                            "    AND G.RECODE = 'CGB' "
                            "    LEFT OUTER JOIN PIS1TB001 I "
                            "    ON A.CRE_USER = I.EMP_NBR "
                            "    WHERE A.ACIOGB = '2' "
                            "    AND A.ICUST = '" + str(iCust) + "'"
                            "    AND A.MID_OPT = 'Y'"
                            "    AND A.FIN_OPT = 'Y'"
                           "    UNION ALL "
                           "    SELECT A.ACIOGB, A.IODATE, 0 AS IN_ACAMTS, A.ACAMTS AS OUT_ACAMTS, A.ACCUST, B.CUST_NME"
                           "           , A.ACACNUMBER, C.ACNUM_NAME, A.MCODE, A.FIN_OPT, D.MCODENM, A.ACTITLE, A.ACSEQN"
                           "            , A.ACODE, E.RESNAM AS ACODENM, F.GBN, G.RESNAM AS GBNNM, A.APPLYDT, A.ACGUBN, A.MID_OPT, A.ACUSE "
                           "            , IFNULL((SELECT X.EMP_NME FROM OSSIGN Y "
                           "                LEFT OUTER JOIN PIS1TB001 X ON Y.EMP_NBR = X.EMP_NBR "
                           "                WHERE Y.ICUST = A.ICUST AND Y.ACDATE = A.IODATE AND Y.ACSEQN = A.ACSEQN AND Y.ACIOGB = A.ACIOGB "
                           "                AND Y.SEQ = (SELECT IFNULL(MAX(SEQ), '') FROM OSSIGN WHERE ICUST = A.ICUST AND ACDATE = A.IODATE AND ACSEQN = A.ACSEQN AND ACIOGB = A.ACIOGB AND OPT = 'Y')), '') AS NME "
                           "    FROM SISACCTT A "
                           "    LEFT OUTER JOIN MIS1TB003 B "
                           "    ON A.ACCUST = B.CUST_NBR "
                           "    LEFT OUTER JOIN ACNUMBER C "
                           "    ON A.ACACNUMBER = C.ACNUMBER "
                           "    LEFT OUTER JOIN OSCODEM D "
                           "    ON A.MCODE = D.MCODE "
                           "    LEFT OUTER JOIN OSREFCP E "
                           "    ON A.ACODE = E.RESKEY "
                           "    AND E.RECODE = 'ACD' "
                           "    LEFT OUTER JOIN OSCODEM F "
                           "    ON A.MCODE = F.MCODE "
                           "    LEFT OUTER JOIN OSREFCP G "
                           "    ON F.GBN = G.RESKEY "
                           "    AND G.RECODE = 'CGB' "
                           "    LEFT OUTER JOIN PIS1TB001 I "
                           "    ON A.CRE_USER = I.EMP_NBR "
                           "    WHERE A.ACIOGB = '1' "
                           "    AND A.ICUST = '" + str(iCust) + "'"
                            "    AND A.MID_OPT = 'Y'"
                            "    AND A.FIN_OPT = 'Y'"
                           " ) AA "
                           " WHERE AA.IODATE BETWEEN '" + str(strDate) + "' AND '" + str(endDate) + "' "
                           " ORDER BY AA.IODATE ")
                        mainresult = cursor.fetchall()
                        return JsonResponse({'balList': balresult, 'mainList': mainresult})

            if empName != '':
                with connection.cursor() as cursor:
                    cursor.execute(" SELECT EMP_NBR FROM PIS1TB001 WHERE EMP_NME LIKE '%" + str(empName) + "%' ")
                    result = cursor.fetchall()
                    empCode = result[0][0]

                balresult = ''
                with connection.cursor() as cursor:
                    cursor.execute(
                        "  SELECT IFNULL(AA.ACIOGB, ''), IFNULL(AA.IODATE, ''), IFNULL(AA.IN_ACAMTS, 0), IFNULL(AA.OUT_ACAMTS, 0)"
                        "        , IFNULL(AA.ACCUST, ''), IFNULL(AA.CUST_NME, ''), IFNULL(AA.ACACNUMBER, ''), IFNULL(AA.ACNUM_NAME, '')"
                        "        , IFNULL(AA.MCODE, ''), IFNULL(AA.FIN_OPT, ''), IFNULL(AA.MCODENM, ''), IFNULL(AA.ACTITLE, '')"
                        "        , IFNULL(AA.ACSEQN, ''), IFNULL(AA.ACODE, ''), IFNULL(AA.ACODENM, ''), IFNULL(AA.GBN, '')"
                        "        , IFNULL(AA.GBNNM, ''), IFNULL(AA.APPLYDT, ''), IFNULL(AA.ACGUBN, ''), IFNULL(AA.GBN, '')"
                        "        , IFNULL(AA.FIN_OPT, ''), IFNULL(AA.MID_OPT, ''), IFNULL(AA.ACUSE, ''), IFNULL(AA.ACGUBN, ''), IFNULL(AA.NME, '') FROM "
                        " ( "
                        "     SELECT A.ACIOGB, A.IODATE, A.ACAMTS AS IN_ACAMTS, 0 AS OUT_ACAMTS, A.ACCUST, B.CUST_NME"
                        "            , A.ACACNUMBER, C.ACNUM_NAME, A.MCODE, A.FIN_OPT, D.MCODENM, A.ACTITLE, A.ACSEQN"
                        "            , A.ACODE, E.RESNAM AS ACODENM, F.GBN, G.RESNAM AS GBNNM, A.APPLYDT, A.ACGUBN, A.MID_OPT, A.ACUSE "
                        "            , IFNULL((SELECT X.EMP_NME FROM OSSIGN Y "
                        "                LEFT OUTER JOIN PIS1TB001 X ON Y.EMP_NBR = X.EMP_NBR "
                        "                WHERE Y.ICUST = A.ICUST AND Y.ACDATE = A.IODATE AND Y.ACSEQN = A.ACSEQN AND Y.ACIOGB = A.ACIOGB "
                        "                AND Y.SEQ = (SELECT IFNULL(MAX(SEQ), '') FROM OSSIGN WHERE ICUST = A.ICUST AND ACDATE = A.IODATE AND ACSEQN = A.ACSEQN AND ACIOGB = A.ACIOGB AND OPT = 'Y')), '') AS NME "
                        "     FROM SISACCTT A "
                        "     LEFT OUTER JOIN MIS1TB003 B "
                        "     ON A.ACCUST = B.CUST_NBR "
                        "     LEFT OUTER JOIN ACNUMBER C "
                        "     ON A.ACACNUMBER = C.ACNUMBER "
                        "     LEFT OUTER JOIN OSCODEM D "
                        "     ON A.MCODE = D.MCODE "
                        "    LEFT OUTER JOIN OSREFCP E "
                        "    ON A.ACODE = E.RESKEY "
                        "    AND E.RECODE = 'ACD' "
                        "    LEFT OUTER JOIN OSCODEM F "
                        "    ON A.MCODE = F.MCODE "
                        "    LEFT OUTER JOIN OSREFCP G "
                        "    ON F.GBN = G.RESKEY "
                        "    AND G.RECODE = 'CGB' "
                        "    LEFT OUTER JOIN PIS1TB001 I "
                        "    ON A.CRE_USER = I.EMP_NBR "
                        "    WHERE A.ACIOGB = '2' "
                        "    AND A.ICUST = '" + str(iCust) + "'"
                        "    AND A.CRE_USER = '" + str(empCode) + "'"
                       "    UNION ALL "
                       "    SELECT A.ACIOGB, A.IODATE, 0 AS IN_ACAMTS, A.ACAMTS AS OUT_ACAMTS, A.ACCUST, B.CUST_NME"
                       "           , A.ACACNUMBER, C.ACNUM_NAME, A.MCODE, A.FIN_OPT, D.MCODENM, A.ACTITLE, A.ACSEQN"
                       "            , A.ACODE, E.RESNAM AS ACODENM, F.GBN, G.RESNAM AS GBNNM, A.APPLYDT, A.ACGUBN, A.MID_OPT, A.ACUSE "
                       "            , IFNULL((SELECT X.EMP_NME FROM OSSIGN Y "
                       "                LEFT OUTER JOIN PIS1TB001 X ON Y.EMP_NBR = X.EMP_NBR "
                       "                WHERE Y.ICUST = A.ICUST AND Y.ACDATE = A.IODATE AND Y.ACSEQN = A.ACSEQN AND Y.ACIOGB = A.ACIOGB "
                       "                AND Y.SEQ = (SELECT IFNULL(MAX(SEQ), '') FROM OSSIGN WHERE ICUST = A.ICUST AND ACDATE = A.IODATE AND ACSEQN = A.ACSEQN AND ACIOGB = A.ACIOGB AND OPT = 'Y')), '') AS NME "
                       "    FROM SISACCTT A "
                       "    LEFT OUTER JOIN MIS1TB003 B "
                       "    ON A.ACCUST = B.CUST_NBR "
                       "    LEFT OUTER JOIN ACNUMBER C "
                       "    ON A.ACACNUMBER = C.ACNUMBER "
                       "    LEFT OUTER JOIN OSCODEM D "
                       "    ON A.MCODE = D.MCODE "
                       "    LEFT OUTER JOIN OSREFCP E "
                       "    ON A.ACODE = E.RESKEY "
                       "    AND E.RECODE = 'ACD' "
                       "    LEFT OUTER JOIN OSCODEM F "
                       "    ON A.MCODE = F.MCODE "
                       "    LEFT OUTER JOIN OSREFCP G "
                       "    ON F.GBN = G.RESKEY "
                       "    AND G.RECODE = 'CGB' "
                       "    LEFT OUTER JOIN PIS1TB001 I "
                       "    ON A.CRE_USER = I.EMP_NBR "
                       "    WHERE A.ACIOGB = '1' "
                       "    AND A.ICUST = '" + str(iCust) + "'"
                       "    AND A.CRE_USER = '" + str(empCode) + "' "
                       " ) AA "
                       " WHERE AA.IODATE BETWEEN '" + str(strDate) + "' AND '" + str(endDate) + "' "
                       " ORDER BY AA.IODATE ")
                    mainresult = cursor.fetchall()

                    return JsonResponse({'balList': balresult, 'mainList': mainresult})

            if payGbn != '':
                balresult = ''
                with connection.cursor() as cursor:
                    cursor.execute(
                        "  SELECT IFNULL(AA.ACIOGB, ''), IFNULL(AA.IODATE, ''), IFNULL(AA.IN_ACAMTS, 0), IFNULL(AA.OUT_ACAMTS, 0)"
                        "        , IFNULL(AA.ACCUST, ''), IFNULL(AA.CUST_NME, ''), IFNULL(AA.ACACNUMBER, ''), IFNULL(AA.ACNUM_NAME, '')"
                        "        , IFNULL(AA.MCODE, ''), IFNULL(AA.FIN_OPT, ''), IFNULL(AA.MCODENM, ''), IFNULL(AA.ACTITLE, '')"
                        "        , IFNULL(AA.ACSEQN, ''), IFNULL(AA.ACODE, ''), IFNULL(AA.ACODENM, ''), IFNULL(AA.GBN, '')"
                        "        , IFNULL(AA.GBNNM, ''), IFNULL(AA.APPLYDT, ''), IFNULL(AA.ACGUBN, ''), IFNULL(AA.GBN, '')"
                        "        , IFNULL(AA.FIN_OPT, ''), IFNULL(AA.MID_OPT, ''), IFNULL(AA.ACUSE, ''), IFNULL(AA.ACGUBN, ''), IFNULL(AA.NME, '') FROM "
                        " ( "
                        "     SELECT A.ACIOGB, A.IODATE, A.ACAMTS AS IN_ACAMTS, 0 AS OUT_ACAMTS, A.ACCUST, B.CUST_NME"
                        "            , A.ACACNUMBER, C.ACNUM_NAME, A.MCODE, A.FIN_OPT, D.MCODENM, A.ACTITLE, A.ACSEQN"
                        "            , A.ACODE, E.RESNAM AS ACODENM, F.GBN, G.RESNAM AS GBNNM, A.APPLYDT, A.ACGUBN, A.MID_OPT, A.ACUSE "
                        "            , IFNULL((SELECT X.EMP_NME FROM OSSIGN Y "
                        "                LEFT OUTER JOIN PIS1TB001 X ON Y.EMP_NBR = X.EMP_NBR "
                        "                WHERE Y.ICUST = A.ICUST AND Y.ACDATE = A.IODATE AND Y.ACSEQN = A.ACSEQN AND Y.ACIOGB = A.ACIOGB "
                        "                AND Y.SEQ = (SELECT IFNULL(MAX(SEQ), '') FROM OSSIGN WHERE ICUST = A.ICUST AND ACDATE = A.IODATE AND ACSEQN = A.ACSEQN AND ACIOGB = A.ACIOGB AND OPT = 'Y')), '') AS NME "
                        "     FROM SISACCTT A "
                        "     LEFT OUTER JOIN MIS1TB003 B "
                        "     ON A.ACCUST = B.CUST_NBR "
                        "     LEFT OUTER JOIN ACNUMBER C "
                        "     ON A.ACACNUMBER = C.ACNUMBER "
                        "     LEFT OUTER JOIN OSCODEM D "
                        "     ON A.MCODE = D.MCODE "
                        "    LEFT OUTER JOIN OSREFCP E "
                        "    ON A.ACODE = E.RESKEY "
                        "    AND E.RECODE = 'ACD' "
                        "    LEFT OUTER JOIN OSCODEM F "
                        "    ON A.MCODE = F.MCODE "
                        "    LEFT OUTER JOIN OSREFCP G "
                        "    ON F.GBN = G.RESKEY "
                        "    AND G.RECODE = 'CGB' "
                        "    LEFT OUTER JOIN PIS1TB001 I "
                        "    ON A.CRE_USER = I.EMP_NBR "
                        "    WHERE A.ACIOGB = '2' "
                        "    AND A.ICUST = '" + str(iCust) + "'"
                        "    AND A.ACGUBN = '" + str(payGbn) + "'"
                       "    UNION ALL "
                       "    SELECT A.ACIOGB, A.IODATE, 0 AS IN_ACAMTS, A.ACAMTS AS OUT_ACAMTS, A.ACCUST, B.CUST_NME"
                       "           , A.ACACNUMBER, C.ACNUM_NAME, A.MCODE, A.FIN_OPT, D.MCODENM, A.ACTITLE, A.ACSEQN"
                       "            , A.ACODE, E.RESNAM AS ACODENM, F.GBN, G.RESNAM AS GBNNM, A.APPLYDT, A.ACGUBN, A.MID_OPT, A.ACUSE "
                       "            , IFNULL((SELECT X.EMP_NME FROM OSSIGN Y "
                       "                LEFT OUTER JOIN PIS1TB001 X ON Y.EMP_NBR = X.EMP_NBR "
                       "                WHERE Y.ICUST = A.ICUST AND Y.ACDATE = A.IODATE AND Y.ACSEQN = A.ACSEQN AND Y.ACIOGB = A.ACIOGB "
                       "                AND Y.SEQ = (SELECT IFNULL(MAX(SEQ), '') FROM OSSIGN WHERE ICUST = A.ICUST AND ACDATE = A.IODATE AND ACSEQN = A.ACSEQN AND ACIOGB = A.ACIOGB AND OPT = 'Y')), '') AS NME "
                       "    FROM SISACCTT A "
                       "    LEFT OUTER JOIN MIS1TB003 B "
                       "    ON A.ACCUST = B.CUST_NBR "
                       "    LEFT OUTER JOIN ACNUMBER C "
                       "    ON A.ACACNUMBER = C.ACNUMBER "
                       "    LEFT OUTER JOIN OSCODEM D "
                       "    ON A.MCODE = D.MCODE "
                       "    LEFT OUTER JOIN OSREFCP E "
                       "    ON A.ACODE = E.RESKEY "
                       "    AND E.RECODE = 'ACD' "
                       "    LEFT OUTER JOIN OSCODEM F "
                       "    ON A.MCODE = F.MCODE "
                       "    LEFT OUTER JOIN OSREFCP G "
                       "    ON F.GBN = G.RESKEY "
                       "    AND G.RECODE = 'CGB' "
                       "    LEFT OUTER JOIN PIS1TB001 I "
                       "    ON A.CRE_USER = I.EMP_NBR "
                       "    WHERE A.ACIOGB = '1' "
                       "    AND A.ICUST = '" + str(iCust) + "'"
                       "    AND A.ACGUBN = '" + str(payGbn) + "' "
                       " ) AA "
                       " WHERE AA.IODATE BETWEEN '" + str(strDate) + "' AND '" + str(endDate) + "' "
                       " ORDER BY AA.IODATE ")
                    mainresult = cursor.fetchall()

                    return JsonResponse({'balList': balresult, 'mainList': mainresult})

            if strDate != '' and endDate != '' and cboAct == '' and cboCust == '':
                balresult = ''
                with connection.cursor() as cursor:
                    cursor.execute("  SELECT IFNULL(AA.ACIOGB, ''), IFNULL(AA.IODATE, ''), IFNULL(AA.IN_ACAMTS, 0), IFNULL(AA.OUT_ACAMTS, 0)"
                                   "        , IFNULL(AA.ACCUST, ''), IFNULL(AA.CUST_NME, ''), IFNULL(AA.ACACNUMBER, ''), IFNULL(AA.ACNUM_NAME, '')"
                                   "        , IFNULL(AA.MCODE, ''), IFNULL(AA.FIN_OPT, ''), IFNULL(AA.MCODENM, ''), IFNULL(AA.ACTITLE, '')"
                                   "        , IFNULL(AA.ACSEQN, ''), IFNULL(AA.ACODE, ''), IFNULL(AA.ACODENM, ''), IFNULL(AA.GBN, '')"
                                   "        , IFNULL(AA.GBNNM, ''), IFNULL(AA.APPLYDT, ''), IFNULL(AA.ACGUBN, ''), IFNULL(AA.GBN, '')"
                                   "        , IFNULL(AA.FIN_OPT, ''), IFNULL(AA.MID_OPT, ''), IFNULL(AA.ACUSE, ''), IFNULL(AA.ACGUBN, ''), IFNULL(AA.NME, '') FROM "
                                   " ( "
                                   "     SELECT A.ACIOGB, A.IODATE, A.ACAMTS AS IN_ACAMTS, 0 AS OUT_ACAMTS, A.ACCUST, B.CUST_NME"
                                   "            , A.ACACNUMBER, C.ACNUM_NAME, A.MCODE, A.FIN_OPT, D.MCODENM, A.ACTITLE, A.ACSEQN"
                                   "            , A.ACODE, E.RESNAM AS ACODENM, F.GBN, G.RESNAM AS GBNNM, A.APPLYDT, A.ACGUBN, A.MID_OPT, A.ACUSE "
                                   "            , IFNULL((SELECT X.EMP_NME FROM OSSIGN Y "
                                   "                LEFT OUTER JOIN PIS1TB001 X ON Y.EMP_NBR = X.EMP_NBR "
                                   "                WHERE Y.ICUST = A.ICUST AND Y.ACDATE = A.IODATE AND Y.ACSEQN = A.ACSEQN AND Y.ACIOGB = A.ACIOGB "
                                   "                AND Y.SEQ = (SELECT IFNULL(MAX(SEQ), '') FROM OSSIGN WHERE ICUST = A.ICUST AND ACDATE = A.IODATE AND ACSEQN = A.ACSEQN AND ACIOGB = A.ACIOGB AND OPT = 'Y')), '') AS NME "
                                   "     FROM SISACCTT A "
                                   "     LEFT OUTER JOIN MIS1TB003 B "
                                   "     ON A.ACCUST = B.CUST_NBR "
                                   "     LEFT OUTER JOIN ACNUMBER C "
                                   "     ON A.ACACNUMBER = C.ACNUMBER "
                                   "     LEFT OUTER JOIN OSCODEM D "
                                   "     ON A.MCODE = D.MCODE "
                                   "    LEFT OUTER JOIN OSREFCP E "
                                   "    ON A.ACODE = E.RESKEY "
                                   "    AND E.RECODE = 'ACD' "
                                   "    LEFT OUTER JOIN OSCODEM F "
                                   "    ON A.MCODE = F.MCODE "
                                   "    LEFT OUTER JOIN OSREFCP G "
                                   "    ON F.GBN = G.RESKEY "
                                   "    AND G.RECODE = 'CGB' "
                                   "    LEFT OUTER JOIN PIS1TB001 I "
                                   "    ON A.CRE_USER = I.EMP_NBR "
                                   "    WHERE A.ACIOGB = '2' "
                                   "    AND A.ICUST = '" + str(iCust) + "'"
                                   "    AND I.EMP_DEPT = '" + str(empDept) + "'"
                                   "    UNION ALL "
                                   "    SELECT A.ACIOGB, A.IODATE, 0 AS IN_ACAMTS, A.ACAMTS AS OUT_ACAMTS, A.ACCUST, B.CUST_NME"
                                   "           , A.ACACNUMBER, C.ACNUM_NAME, A.MCODE, A.FIN_OPT, D.MCODENM, A.ACTITLE, A.ACSEQN"
                                   "            , A.ACODE, E.RESNAM AS ACODENM, F.GBN, G.RESNAM AS GBNNM, A.APPLYDT, A.ACGUBN, A.MID_OPT, A.ACUSE "
                                   "            , IFNULL((SELECT X.EMP_NME FROM OSSIGN Y "
                                   "                LEFT OUTER JOIN PIS1TB001 X ON Y.EMP_NBR = X.EMP_NBR "
                                   "                WHERE Y.ICUST = A.ICUST AND Y.ACDATE = A.IODATE AND Y.ACSEQN = A.ACSEQN AND Y.ACIOGB = A.ACIOGB "
                                   "                AND Y.SEQ = (SELECT IFNULL(MAX(SEQ), '') FROM OSSIGN WHERE ICUST = A.ICUST AND ACDATE = A.IODATE AND ACSEQN = A.ACSEQN AND ACIOGB = A.ACIOGB AND OPT = 'Y')), '') AS NME "
                                   "    FROM SISACCTT A "
                                   "    LEFT OUTER JOIN MIS1TB003 B "
                                   "    ON A.ACCUST = B.CUST_NBR "
                                   "    LEFT OUTER JOIN ACNUMBER C "
                                   "    ON A.ACACNUMBER = C.ACNUMBER "
                                   "    LEFT OUTER JOIN OSCODEM D "
                                   "    ON A.MCODE = D.MCODE "
                                   "    LEFT OUTER JOIN OSREFCP E "
                                   "    ON A.ACODE = E.RESKEY "
                                   "    AND E.RECODE = 'ACD' "
                                   "    LEFT OUTER JOIN OSCODEM F "
                                   "    ON A.MCODE = F.MCODE "
                                   "    LEFT OUTER JOIN OSREFCP G "
                                   "    ON F.GBN = G.RESKEY "
                                   "    AND G.RECODE = 'CGB' "
                                   "    LEFT OUTER JOIN PIS1TB001 I "
                                   "    ON A.CRE_USER = I.EMP_NBR "                                     
                                   "    WHERE A.ACIOGB = '1' "
                                   "    AND A.ICUST = '" + str(iCust) + "'"
                                   "    AND I.EMP_DEPT = '" + str(empDept) + "' "
                                   " ) AA "
                                   " WHERE AA.IODATE BETWEEN '" + str(strDate) + "' AND '" + str(endDate) + "' "
                                   " ORDER BY AA.IODATE ")
                    mainresult = cursor.fetchall()

                    # 거래처
                    with connection.cursor() as cursor:
                        cursor.execute(" SELECT CUST_NBR, CUST_NME FROM MIS1TB003 WHERE ICUST = '" + str(iCust) + "' ORDER BY CUST_NBR ")
                        cboCust = cursor.fetchall()

                    with connection.cursor() as cursor:
                        cursor.execute(" SELECT ACNUMBER FROM ACNUMBER WHERE ICUST = '" + str(iCust) + "' ")
                        cboAct = cursor.fetchall()

                    with connection.cursor() as cursor:
                        cursor.execute(" SELECT A.ACBKCD, B.RESNAM FROM ACNUMBER A LEFT OUTER JOIN OSREFCP B ON A.ACBKCD = B.RESKEY AND B.RECODE = 'BNK' AND A.ICUST = '" + str(iCust) + "' "
                                       " GROUP BY A.ACBKCD, B.RESNAM ORDER BY A.ACBKCD ")
                        inputBank = cursor.fetchall()

                    return JsonResponse({'balList': balresult, 'mainList': mainresult, 'cboCust': cboCust, 'cboAct': cboAct, 'inputBank': inputBank})

            if cboCust != '' and cboAct == '':
                balresult = ''
                with connection.cursor() as cursor:
                    cursor.execute("  SELECT IFNULL(AA.ACIOGB, ''), IFNULL(AA.IODATE, ''), IFNULL(AA.IN_ACAMTS, 0), IFNULL(AA.OUT_ACAMTS, 0)"
                                   "        , IFNULL(AA.ACCUST, ''), IFNULL(AA.CUST_NME, ''), IFNULL(AA.ACACNUMBER, ''), IFNULL(AA.ACNUM_NAME, '')"
                                   "        , IFNULL(AA.MCODE, ''), IFNULL(AA.FIN_OPT, ''), IFNULL(AA.MCODENM, ''), IFNULL(AA.ACTITLE, '')"
                                   "        , IFNULL(AA.ACSEQN, ''), IFNULL(AA.ACODE, ''), IFNULL(AA.ACODENM, ''), IFNULL(AA.GBN, ''), IFNULL(AA.GBNNM, '')"
                                   "        , IFNULL(AA.ACBKCD, ''), IFNULL(AA.BANKNM, ''), IFNULL(AA.APPLYDT, ''), IFNULL(AA.ACGUBN, '')"
                                   "        , IFNULL(AA.MID_OPT, ''), IFNULL(AA.ACUSE, ''), IFNULL(AA.ACGUBN, ''), IFNULL(AA.NME, '')  FROM "
                                   " ( "
                                   "     SELECT A.ACIOGB, A.IODATE, A.ACAMTS AS IN_ACAMTS, 0 AS OUT_ACAMTS, A.ACCUST, B.CUST_NME"
                                   "            , A.ACACNUMBER, C.ACNUM_NAME, A.MCODE, A.FIN_OPT, D.MCODENM, A.ACTITLE, A.ACSEQN"
                                   "            , A.ACODE, E.RESNAM AS ACODENM, F.GBN, G.RESNAM AS GBNNM, C.ACBKCD, H.RESNAM AS BANKNM, A.APPLYDT, A.ACGUBN, A.MID_OPT, A.ACUSE "
                                   "            , IFNULL((SELECT X.EMP_NME FROM OSSIGN Y "
                                   "                LEFT OUTER JOIN PIS1TB001 X ON Y.EMP_NBR = X.EMP_NBR "
                                   "                WHERE Y.ICUST = A.ICUST AND Y.ACDATE = A.IODATE AND Y.ACSEQN = A.ACSEQN AND Y.ACIOGB = A.ACIOGB "
                                   "                AND Y.SEQ = (SELECT IFNULL(MAX(SEQ), '') FROM OSSIGN WHERE ICUST = A.ICUST AND ACDATE = A.IODATE AND ACSEQN = A.ACSEQN AND ACIOGB = A.ACIOGB AND OPT = 'Y')), '') AS NME "
                                   "     FROM SISACCTT A "
                                   "     LEFT OUTER JOIN MIS1TB003 B "
                                   "     ON A.ACCUST = B.CUST_NBR "
                                   "     LEFT OUTER JOIN ACNUMBER C "
                                   "     ON A.ACACNUMBER = C.ACNUMBER "
                                   "     LEFT OUTER JOIN OSCODEM D "
                                   "     ON A.MCODE = D.MCODE "
                                   "    LEFT OUTER JOIN OSREFCP E "
                                   "    ON A.ACODE = E.RESKEY "
                                   "    AND E.RECODE = 'ACD' "
                                   "    LEFT OUTER JOIN OSCODEM F "
                                   "    ON A.MCODE = F.MCODE "
                                   "    LEFT OUTER JOIN OSREFCP G "
                                   "    ON F.GBN = G.RESKEY "
                                   "    AND G.RECODE = 'CGB' "
                                   "    LEFT OUTER JOIN OSREFCP H"
                                   "    ON C.ACBKCD = H.RESKEY"
                                   "    AND H.RECODE = 'BNK'"
                                   "    LEFT OUTER JOIN PIS1TB001 I "
                                   "    ON A.CRE_USER = I.EMP_NBR "
                                   "    WHERE A.ACIOGB = '2' "
                                   "    AND A.ICUST = '" + str(iCust) + "'"
                                   "    AND I.EMP_DEPT = '" + str(empDept) + "' "
                                   "    UNION ALL "
                                   "    SELECT A.ACIOGB, A.IODATE, 0 AS IN_ACAMTS, A.ACAMTS AS OUT_ACAMTS, A.ACCUST, B.CUST_NME"
                                   "           , A.ACACNUMBER, C.ACNUM_NAME, A.MCODE, A.FIN_OPT, D.MCODENM, A.ACTITLE, A.ACSEQN"
                                   "            , A.ACODE, E.RESNAM AS ACODENM, F.GBN, G.RESNAM AS GBNNM, C.ACBKCD, H.RESNAM AS BANKNM, A.APPLYDT, A.ACGUBN, A.MID_OPT, A.ACUSE   "
                                   "            , IFNULL((SELECT X.EMP_NME FROM OSSIGN Y "
                                   "                LEFT OUTER JOIN PIS1TB001 X ON Y.EMP_NBR = X.EMP_NBR "
                                   "                WHERE Y.ICUST = A.ICUST AND Y.ACDATE = A.IODATE AND Y.ACSEQN = A.ACSEQN AND Y.ACIOGB = A.ACIOGB "
                                   "                AND Y.SEQ = (SELECT IFNULL(MAX(SEQ), '') FROM OSSIGN WHERE ICUST = A.ICUST AND ACDATE = A.IODATE AND ACSEQN = A.ACSEQN AND ACIOGB = A.ACIOGB AND OPT = 'Y')), '') AS NME "
                                   "    FROM SISACCTT A "
                                   "    LEFT OUTER JOIN MIS1TB003 B "
                                   "    ON A.ACCUST = B.CUST_NBR "
                                   "    LEFT OUTER JOIN ACNUMBER C "
                                   "    ON A.ACACNUMBER = C.ACNUMBER "
                                   "    LEFT OUTER JOIN OSCODEM D "
                                   "    ON A.MCODE = D.MCODE "
                                   "    LEFT OUTER JOIN OSREFCP E "
                                   "    ON A.ACODE = E.RESKEY "
                                   "    AND E.RECODE = 'ACD' "
                                   "    LEFT OUTER JOIN OSCODEM F "
                                   "    ON A.MCODE = F.MCODE "
                                   "    LEFT OUTER JOIN OSREFCP G "
                                   "    ON F.GBN = G.RESKEY "
                                   "    AND G.RECODE = 'CGB' "
                                   "    LEFT OUTER JOIN OSREFCP H"
                                   "    ON C.ACBKCD = H.RESKEY"
                                   "    AND H.RECODE = 'BNK'"
                                   "    LEFT OUTER JOIN PIS1TB001 I "
                                   "    ON A.CRE_USER = I.EMP_NBR "
                                   "    WHERE A.ACIOGB = '1' "
                                   "    AND A.ICUST = '" + str(iCust) + "'"
                                   "    AND I.EMP_DEPT = '" + str(empDept) + "' "
                                   " ) AA "
                                   " WHERE AA.IODATE BETWEEN '" + str(strDate) + "' AND '" + str(endDate) + "' "
                                   " AND AA.ACCUST = '" + str(cboCust) + "' "
                                   " ORDER BY AA.IODATE ")
                    mainresult = cursor.fetchall()

                return JsonResponse({'balList': balresult, 'mainList': mainresult})

            if cboAct != '' and cboCust == '':
                balresult = ''
                with connection.cursor() as cursor:
                    cursor.execute("  SELECT IFNULL(AA.ACIOGB, ''), IFNULL(AA.IODATE, ''), IFNULL(AA.IN_ACAMTS, 0), IFNULL(AA.OUT_ACAMTS, 0)"
                                   "        , IFNULL(AA.ACCUST, ''), IFNULL(AA.CUST_NME, ''), IFNULL(AA.ACACNUMBER, ''), IFNULL(AA.ACNUM_NAME, '')"
                                   "        , IFNULL(AA.MCODE, ''), IFNULL(AA.FIN_OPT, ''), IFNULL(AA.MCODENM, ''), IFNULL(AA.ACTITLE, '')"
                                   "        , IFNULL(AA.ACSEQN, ''), IFNULL(AA.ACODE, ''), IFNULL(AA.ACODENM, ''), IFNULL(AA.GBN, '')"
                                   "        , IFNULL(AA.GBNNM, ''), IFNULL(AA.APPLYDT, ''), IFNULL(AA.ACGUBN, ''), IFNULL(AA.GBN, '')"
                                   "        , IFNULL(AA.FIN_OPT, ''), IFNULL(AA.MID_OPT, ''), IFNULL(AA.ACUSE, ''), IFNULL(AA.ACGUBN, ''), IFNULL(AA.NME, '') FROM "
                                   " ( "
                                   "     SELECT A.ACIOGB, A.IODATE, A.ACAMTS AS IN_ACAMTS, 0 AS OUT_ACAMTS, A.ACCUST, B.CUST_NME"
                                   "            , A.ACACNUMBER, C.ACNUM_NAME, A.MCODE, A.FIN_OPT, D.MCODENM, A.ACTITLE, A.ACSEQN"
                                   "            , A.ACODE, E.RESNAM AS ACODENM, F.GBN, G.RESNAM AS GBNNM, A.APPLYDT, A.ACGUBN, A.MID_OPT, A.ACUSE  "
                                   "            , IFNULL((SELECT X.EMP_NME FROM OSSIGN Y "
                                   "                LEFT OUTER JOIN PIS1TB001 X ON Y.EMP_NBR = X.EMP_NBR "
                                   "                WHERE Y.ICUST = A.ICUST AND Y.ACDATE = A.IODATE AND Y.ACSEQN = A.ACSEQN AND Y.ACIOGB = A.ACIOGB "
                                   "                AND Y.SEQ = (SELECT IFNULL(MAX(SEQ), '') FROM OSSIGN WHERE ICUST = A.ICUST AND ACDATE = A.IODATE AND ACSEQN = A.ACSEQN AND ACIOGB = A.ACIOGB AND OPT = 'Y')), '') AS NME "
                                   "     FROM SISACCTT A "
                                   "     LEFT OUTER JOIN MIS1TB003 B "
                                   "     ON A.ACCUST = B.CUST_NBR "
                                   "     LEFT OUTER JOIN ACNUMBER C "
                                   "     ON A.ACACNUMBER = C.ACNUMBER "
                                   "     LEFT OUTER JOIN OSCODEM D "
                                   "     ON A.MCODE = D.MCODE "
                                   "    LEFT OUTER JOIN OSREFCP E "
                                   "    ON A.ACODE = E.RESKEY "
                                   "    AND E.RECODE = 'ACD' "
                                   "    LEFT OUTER JOIN OSCODEM F "
                                   "    ON A.MCODE = F.MCODE "
                                   "    LEFT OUTER JOIN OSREFCP G "
                                   "    ON F.GBN = G.RESKEY "
                                   "    AND G.RECODE = 'CGB' "
                                   "    LEFT OUTER JOIN PIS1TB001 I "
                                   "    ON A.CRE_USER = I.EMP_NBR "
                                   "    WHERE A.ACIOGB = '2' "
                                   "    AND A.ICUST = '" + str(iCust) + "'"
                                   "    AND I.EMP_DEPT = '" + str(empDept) + "' "
                                   "    UNION ALL "
                                   "    SELECT A.ACIOGB, A.IODATE, 0 AS IN_ACAMTS, A.ACAMTS AS OUT_ACAMTS, A.ACCUST, B.CUST_NME"
                                   "           , A.ACACNUMBER, C.ACNUM_NAME, A.MCODE, A.FIN_OPT, D.MCODENM, A.ACTITLE, A.ACSEQN"
                                   "            , A.ACODE, E.RESNAM AS ACODENM, F.GBN, G.RESNAM AS GBNNM, A.APPLYDT, A.ACGUBN, A.MID_OPT, A.ACUSE  "
                                   "            , IFNULL((SELECT X.EMP_NME FROM OSSIGN Y "
                                   "                LEFT OUTER JOIN PIS1TB001 X ON Y.EMP_NBR = X.EMP_NBR "
                                   "                WHERE Y.ICUST = A.ICUST AND Y.ACDATE = A.IODATE AND Y.ACSEQN = A.ACSEQN AND Y.ACIOGB = A.ACIOGB "
                                   "                AND Y.SEQ = (SELECT IFNULL(MAX(SEQ), '') FROM OSSIGN WHERE ICUST = A.ICUST AND ACDATE = A.IODATE AND ACSEQN = A.ACSEQN AND ACIOGB = A.ACIOGB AND OPT = 'Y')), '') AS NME "
                                   "    FROM SISACCTT A "
                                   "    LEFT OUTER JOIN MIS1TB003 B "
                                   "    ON A.ACCUST = B.CUST_NBR "
                                   "    LEFT OUTER JOIN ACNUMBER C "
                                   "    ON A.ACACNUMBER = C.ACNUMBER "
                                   "    LEFT OUTER JOIN OSCODEM D "
                                   "    ON A.MCODE = D.MCODE "
                                   "    LEFT OUTER JOIN OSREFCP E "
                                   "    ON A.ACODE = E.RESKEY "
                                   "    AND E.RECODE = 'ACD' "
                                   "    LEFT OUTER JOIN OSCODEM F "
                                   "    ON A.MCODE = F.MCODE "
                                   "    LEFT OUTER JOIN OSREFCP G "
                                   "    ON F.GBN = G.RESKEY "
                                   "    AND G.RECODE = 'CGB' "                 
                                   "    LEFT OUTER JOIN PIS1TB001 I "
                                   "    ON A.CRE_USER = I.EMP_NBR "                                      
                                   "    WHERE A.ACIOGB = '1' "
                                   "    AND A.ICUST = '" + str(iCust) + "'"
                                   "    AND I.EMP_DEPT = '" + str(empDept) + "'"
                                   " ) AA "
                                   " WHERE AA.IODATE BETWEEN '" + str(strDate) + "' AND '" + str(endDate) + "' "
                                   " AND AA.ACACNUMBER = '" + str(cboAct) + "' "
                                   " ORDER BY AA.IODATE ")
                    mainresult = cursor.fetchall()

                return JsonResponse({'balList': balresult, 'mainList': mainresult})

            if cboAct != '' and cboCust != '':
                balresult = ''
                with connection.cursor() as cursor:
                    cursor.execute("  SELECT IFNULL(AA.ACIOGB, ''), IFNULL(AA.IODATE, ''), IFNULL(AA.IN_ACAMTS, 0), IFNULL(AA.OUT_ACAMTS, 0)"
                                   "        , IFNULL(AA.ACCUST, ''), IFNULL(AA.CUST_NME, ''), IFNULL(AA.ACACNUMBER, ''), IFNULL(AA.ACNUM_NAME, '')"
                                   "        , IFNULL(AA.MCODE, ''), IFNULL(AA.FIN_OPT, ''), IFNULL(AA.MCODENM, ''), IFNULL(AA.ACTITLE, '')"
                                   "        , IFNULL(AA.ACSEQN, ''), IFNULL(AA.ACODE, ''), IFNULL(AA.ACODENM, ''), IFNULL(AA.GBN, ''), IFNULL(AA.GBNNM, '')"
                                   "        , IFNULL(AA.ACBKCD, ''), IFNULL(AA.BANKNM, ''), IFNULL(AA.APPLYDT, ''), IFNULL(AA.ACGUBN, ''), IFNULL(AA.MID_OPT, '')"
                                   "        , IFNULL(AA.ACUSE, ''), IFNULL(AA.ACGUBN, ''), IFNULL(AA.NME, '') FROM "
                                   " ( "
                                   "     SELECT A.ACIOGB, A.IODATE, A.ACAMTS AS IN_ACAMTS, 0 AS OUT_ACAMTS, A.ACCUST, B.CUST_NME"
                                   "            , A.ACACNUMBER, C.ACNUM_NAME, A.MCODE, A.FIN_OPT, D.MCODENM, A.ACTITLE, A.ACSEQN"
                                   "            , A.ACODE, E.RESNAM AS ACODENM, F.GBN, G.RESNAM AS GBNNM, C.ACBKCD, H.RESNAM AS BANKNM, A.APPLYDT, A.ACGUBN, A.MID_OPT, A.ACUSE "
                                   "            , IFNULL((SELECT X.EMP_NME FROM OSSIGN Y "
                                   "                LEFT OUTER JOIN PIS1TB001 X ON Y.EMP_NBR = X.EMP_NBR "
                                   "                WHERE Y.ICUST = A.ICUST AND Y.ACDATE = A.IODATE AND Y.ACSEQN = A.ACSEQN AND Y.ACIOGB = A.ACIOGB "
                                   "                AND Y.SEQ = (SELECT IFNULL(MAX(SEQ), '') FROM OSSIGN WHERE ICUST = A.ICUST AND ACDATE = A.IODATE AND ACSEQN = A.ACSEQN AND ACIOGB = A.ACIOGB AND OPT = 'Y')), '') AS NME "
                                   "     FROM SISACCTT A "
                                   "     LEFT OUTER JOIN MIS1TB003 B "
                                   "     ON A.ACCUST = B.CUST_NBR "
                                   "     LEFT OUTER JOIN ACNUMBER C "
                                   "     ON A.ACACNUMBER = C.ACNUMBER "
                                   "     LEFT OUTER JOIN OSCODEM D "
                                   "     ON A.MCODE = D.MCODE "
                                   "    LEFT OUTER JOIN OSREFCP E "
                                   "    ON A.ACODE = E.RESKEY "
                                   "    AND E.RECODE = 'ACD' "
                                   "    LEFT OUTER JOIN OSCODEM F "
                                   "    ON A.MCODE = F.MCODE "
                                   "    LEFT OUTER JOIN OSREFCP G "
                                   "    ON F.GBN = G.RESKEY "
                                   "    AND G.RECODE = 'CGB' "
                                   "    LEFT OUTER JOIN OSREFCP H"
                                   "    ON C.ACBKCD = H.RESKEY"
                                   "    AND H.RECODE = 'BNK'"
                                   "    LEFT OUTER JOIN PIS1TB001 I "
                                   "    ON A.CRE_USER = I.EMP_NBR "
                                   "    WHERE A.ACIOGB = '2' "
                                   "    AND A.ICUST = '" + str(iCust) + "'"
                                   "    AND I.EMP_DEPT = '" + str(empDept) + "' "
                                   "    UNION ALL "
                                   "    SELECT A.ACIOGB, A.IODATE, 0 AS IN_ACAMTS, A.ACAMTS AS OUT_ACAMTS, A.ACCUST, B.CUST_NME"
                                   "           , A.ACACNUMBER, C.ACNUM_NAME, A.MCODE, A.FIN_OPT, D.MCODENM, A.ACTITLE, A.ACSEQN"
                                   "            , A.ACODE, E.RESNAM AS ACODENM, F.GBN, G.RESNAM AS GBNNM, C.ACBKCD, H.RESNAM AS BANKNM, A.APPLYDT, A.ACGUBN, A.MID_OPT, A.ACUSE "
                                   "            , IFNULL((SELECT X.EMP_NME FROM OSSIGN Y "
                                   "                LEFT OUTER JOIN PIS1TB001 X ON Y.EMP_NBR = X.EMP_NBR "
                                   "                WHERE Y.ICUST = A.ICUST AND Y.ACDATE = A.IODATE AND Y.ACSEQN = A.ACSEQN AND Y.ACIOGB = A.ACIOGB "
                                   "                AND Y.SEQ = (SELECT IFNULL(MAX(SEQ), '') FROM OSSIGN WHERE ICUST = A.ICUST AND ACDATE = A.IODATE AND ACSEQN = A.ACSEQN AND ACIOGB = A.ACIOGB AND OPT = 'Y')), '') AS NME "
                                   "    FROM SISACCTT A "
                                   "    LEFT OUTER JOIN MIS1TB003 B "
                                   "    ON A.ACCUST = B.CUST_NBR "
                                   "    LEFT OUTER JOIN ACNUMBER C "
                                   "    ON A.ACACNUMBER = C.ACNUMBER "
                                   "    LEFT OUTER JOIN OSCODEM D "
                                   "    ON A.MCODE = D.MCODE "
                                   "    LEFT OUTER JOIN OSREFCP E "
                                   "    ON A.ACODE = E.RESKEY "
                                   "    AND E.RECODE = 'ACD' "
                                   "    LEFT OUTER JOIN OSCODEM F "
                                   "    ON A.MCODE = F.MCODE "
                                   "    LEFT OUTER JOIN OSREFCP G "
                                   "    ON F.GBN = G.RESKEY "
                                   "    AND G.RECODE = 'CGB' "
                                   "    LEFT OUTER JOIN OSREFCP H"
                                   "    ON C.ACBKCD = H.RESKEY"
                                   "    AND H.RECODE = 'BNK'"
                                   "    LEFT OUTER JOIN PIS1TB001 I "
                                   "    ON A.CRE_USER = I.EMP_NBR "
                                   "    WHERE A.ACIOGB = '1' "
                                   "    AND A.ICUST = '" + str(iCust) + "'"
                                   "    AND I.EMP_DEPT = '" + str(empDept) + "' "
                                   " ) AA "
                                   " WHERE AA.IODATE BETWEEN '" + strDate + "' AND '" + endDate + "' "
                                   " AND AA.ACACNUMBER = '" + str(cboAct) + "' "
                                   " AND AA.ACCUST = '" + str(cboCust) + "' "
                                   " ORDER BY AA.IODATE ")
                    mainresult = cursor.fetchall()

                return JsonResponse({'balList': balresult, 'mainList': mainresult})

    if chkEmp[0][0] == '' or int(chkEmp[0][0]) > 2:
        if Gbn != '':
            if Gbn == '1' or Gbn == '4':
                balresult = ''
                with connection.cursor() as cursor:
                    cursor.execute(
                        "  SELECT IFNULL(AA.ACIOGB, ''), IFNULL(AA.IODATE, ''), IFNULL(AA.IN_ACAMTS, 0), IFNULL(AA.OUT_ACAMTS, 0)"
                        "        , IFNULL(AA.ACCUST, ''), IFNULL(AA.CUST_NME, ''), IFNULL(AA.ACACNUMBER, ''), IFNULL(AA.ACNUM_NAME, '')"
                        "        , IFNULL(AA.MCODE, ''), IFNULL(AA.FIN_OPT, ''), IFNULL(AA.MCODENM, ''), IFNULL(AA.ACTITLE, '')"
                        "        , IFNULL(AA.ACSEQN, ''), IFNULL(AA.ACODE, ''), IFNULL(AA.ACODENM, ''), IFNULL(AA.GBN, '')"
                        "        , IFNULL(AA.GBNNM, ''), IFNULL(AA.APPLYDT, ''), IFNULL(AA.ACGUBN, ''), IFNULL(AA.GBN, '')"
                        "        , IFNULL(AA.FIN_OPT, ''), IFNULL(AA.MID_OPT, ''), IFNULL(AA.ACUSE, ''), IFNULL(AA.ACGUBN, ''), IFNULL(AA.NME, '') FROM "
                        " ( "
                        "     SELECT A.ACIOGB, A.IODATE, A.ACAMTS AS IN_ACAMTS, 0 AS OUT_ACAMTS, A.ACCUST, B.CUST_NME"
                        "            , A.ACACNUMBER, C.ACNUM_NAME, A.MCODE, A.FIN_OPT, D.MCODENM, A.ACTITLE, A.ACSEQN"
                        "            , A.ACODE, E.RESNAM AS ACODENM, F.GBN, G.RESNAM AS GBNNM, A.APPLYDT, A.ACGUBN, A.MID_OPT, A.ACUSE "
                        "            , IFNULL((SELECT X.EMP_NME FROM OSSIGN Y "
                        "                LEFT OUTER JOIN PIS1TB001 X ON Y.EMP_NBR = X.EMP_NBR "
                        "                WHERE Y.ICUST = A.ICUST AND Y.ACDATE = A.IODATE AND Y.ACSEQN = A.ACSEQN AND Y.ACIOGB = A.ACIOGB "
                        "                AND Y.SEQ = (SELECT IFNULL(MAX(SEQ), '') FROM OSSIGN WHERE ICUST = A.ICUST AND ACDATE = A.IODATE AND ACSEQN = A.ACSEQN AND ACIOGB = A.ACIOGB AND OPT = 'Y')), '') AS NME "
                        "     FROM SISACCTT A "
                        "     LEFT OUTER JOIN MIS1TB003 B "
                        "     ON A.ACCUST = B.CUST_NBR "
                        "     LEFT OUTER JOIN ACNUMBER C "
                        "     ON A.ACACNUMBER = C.ACNUMBER "
                        "     LEFT OUTER JOIN OSCODEM D "
                        "     ON A.MCODE = D.MCODE "
                        "    LEFT OUTER JOIN OSREFCP E "
                        "    ON A.ACODE = E.RESKEY "
                        "    AND E.RECODE = 'ACD' "
                        "    LEFT OUTER JOIN OSCODEM F "
                        "    ON A.MCODE = F.MCODE "
                        "    LEFT OUTER JOIN OSREFCP G "
                        "    ON F.GBN = G.RESKEY "
                        "    AND G.RECODE = 'CGB' "
                        "    LEFT OUTER JOIN PIS1TB001 I "
                        "    ON A.CRE_USER = I.EMP_NBR "
                        "    WHERE A.ACIOGB = '2' "
                        "    AND A.ICUST = '" + str(iCust) + "'"
                        "    AND A.MID_OPT = 'Y'"
                        "    AND A.FIN_OPT = 'N'"
                        "    UNION ALL "
                        "    SELECT A.ACIOGB, A.IODATE, 0 AS IN_ACAMTS, A.ACAMTS AS OUT_ACAMTS, A.ACCUST, B.CUST_NME"
                        "           , A.ACACNUMBER, C.ACNUM_NAME, A.MCODE, A.FIN_OPT, D.MCODENM, A.ACTITLE, A.ACSEQN"
                        "            , A.ACODE, E.RESNAM AS ACODENM, F.GBN, G.RESNAM AS GBNNM, A.APPLYDT, A.ACGUBN, A.MID_OPT, A.ACUSE "
                        "            , IFNULL((SELECT X.EMP_NME FROM OSSIGN Y "
                        "                LEFT OUTER JOIN PIS1TB001 X ON Y.EMP_NBR = X.EMP_NBR "
                        "                WHERE Y.ICUST = A.ICUST AND Y.ACDATE = A.IODATE AND Y.ACSEQN = A.ACSEQN AND Y.ACIOGB = A.ACIOGB "
                        "                AND Y.SEQ = (SELECT IFNULL(MAX(SEQ), '') FROM OSSIGN WHERE ICUST = A.ICUST AND ACDATE = A.IODATE AND ACSEQN = A.ACSEQN AND ACIOGB = A.ACIOGB AND OPT = 'Y')), '') AS NME "
                        "    FROM SISACCTT A "
                        "    LEFT OUTER JOIN MIS1TB003 B "
                        "    ON A.ACCUST = B.CUST_NBR "
                        "    LEFT OUTER JOIN ACNUMBER C "
                        "    ON A.ACACNUMBER = C.ACNUMBER "
                        "    LEFT OUTER JOIN OSCODEM D "
                        "    ON A.MCODE = D.MCODE "
                        "    LEFT OUTER JOIN OSREFCP E "
                        "    ON A.ACODE = E.RESKEY "
                        "    AND E.RECODE = 'ACD' "
                        "    LEFT OUTER JOIN OSCODEM F "
                        "    ON A.MCODE = F.MCODE "
                        "    LEFT OUTER JOIN OSREFCP G "
                        "    ON F.GBN = G.RESKEY "
                        "    AND G.RECODE = 'CGB' "
                        "    LEFT OUTER JOIN PIS1TB001 I "
                        "    ON A.CRE_USER = I.EMP_NBR "
                        "    WHERE A.ACIOGB = '1' "
                        "    AND A.ICUST = '" + str(iCust) + "'"
                        "    AND A.MID_OPT = 'Y'"
                        "    AND A.FIN_OPT = 'N'"
                        " ) AA "
                        " WHERE AA.IODATE BETWEEN '" + str(strDate) + "' AND '" + str(endDate) + "' "
                        " ORDER BY AA.IODATE ")
                    mainresult = cursor.fetchall()
                    return JsonResponse({'balList': balresult, 'mainList': mainresult})

            if Gbn == '2':
                balresult = ''
                with connection.cursor() as cursor:
                    cursor.execute(
                        "  SELECT IFNULL(AA.ACIOGB, ''), IFNULL(AA.IODATE, ''), IFNULL(AA.IN_ACAMTS, 0), IFNULL(AA.OUT_ACAMTS, 0)"
                        "        , IFNULL(AA.ACCUST, ''), IFNULL(AA.CUST_NME, ''), IFNULL(AA.ACACNUMBER, ''), IFNULL(AA.ACNUM_NAME, '')"
                        "        , IFNULL(AA.MCODE, ''), IFNULL(AA.FIN_OPT, ''), IFNULL(AA.MCODENM, ''), IFNULL(AA.ACTITLE, '')"
                        "        , IFNULL(AA.ACSEQN, ''), IFNULL(AA.ACODE, ''), IFNULL(AA.ACODENM, ''), IFNULL(AA.GBN, '')"
                        "        , IFNULL(AA.GBNNM, ''), IFNULL(AA.APPLYDT, ''), IFNULL(AA.ACGUBN, ''), IFNULL(AA.GBN, '')"
                        "        , IFNULL(AA.FIN_OPT, ''), IFNULL(AA.MID_OPT, ''), IFNULL(AA.ACUSE, ''), IFNULL(AA.ACGUBN, ''), IFNULL(AA.NME, '') FROM "
                        " ( "
                        "     SELECT A.ACIOGB, A.IODATE, A.ACAMTS AS IN_ACAMTS, 0 AS OUT_ACAMTS, A.ACCUST, B.CUST_NME"
                        "            , A.ACACNUMBER, C.ACNUM_NAME, A.MCODE, A.FIN_OPT, D.MCODENM, A.ACTITLE, A.ACSEQN"
                        "            , A.ACODE, E.RESNAM AS ACODENM, F.GBN, G.RESNAM AS GBNNM, A.APPLYDT, A.ACGUBN, A.MID_OPT, A.ACUSE "
                        "            , IFNULL((SELECT X.EMP_NME FROM OSSIGN Y "
                        "                LEFT OUTER JOIN PIS1TB001 X ON Y.EMP_NBR = X.EMP_NBR "
                        "                WHERE Y.ICUST = A.ICUST AND Y.ACDATE = A.IODATE AND Y.ACSEQN = A.ACSEQN AND Y.ACIOGB = A.ACIOGB "
                        "                AND Y.SEQ = (SELECT IFNULL(MAX(SEQ), '') FROM OSSIGN WHERE ICUST = A.ICUST AND ACDATE = A.IODATE AND ACSEQN = A.ACSEQN AND ACIOGB = A.ACIOGB AND OPT = 'Y')), '') AS NME "
                        "     FROM SISACCTT A "
                        "     LEFT OUTER JOIN MIS1TB003 B "
                        "     ON A.ACCUST = B.CUST_NBR "
                        "     LEFT OUTER JOIN ACNUMBER C "
                        "     ON A.ACACNUMBER = C.ACNUMBER "
                        "     LEFT OUTER JOIN OSCODEM D "
                        "     ON A.MCODE = D.MCODE "
                        "    LEFT OUTER JOIN OSREFCP E "
                        "    ON A.ACODE = E.RESKEY "
                        "    AND E.RECODE = 'ACD' "
                        "    LEFT OUTER JOIN OSCODEM F "
                        "    ON A.MCODE = F.MCODE "
                        "    LEFT OUTER JOIN OSREFCP G "
                        "    ON F.GBN = G.RESKEY "
                        "    AND G.RECODE = 'CGB' "
                        "    LEFT OUTER JOIN PIS1TB001 I "
                        "    ON A.CRE_USER = I.EMP_NBR "
                        "    WHERE A.ACIOGB = '2' "
                        "    AND A.ICUST = '" + str(iCust) + "'"
                        "    AND A.MID_OPT = 'N'"
                        "    AND A.FIN_OPT = 'N'"
                        "    UNION ALL "
                        "    SELECT A.ACIOGB, A.IODATE, 0 AS IN_ACAMTS, A.ACAMTS AS OUT_ACAMTS, A.ACCUST, B.CUST_NME"
                        "           , A.ACACNUMBER, C.ACNUM_NAME, A.MCODE, A.FIN_OPT, D.MCODENM, A.ACTITLE, A.ACSEQN"
                        "            , A.ACODE, E.RESNAM AS ACODENM, F.GBN, G.RESNAM AS GBNNM, A.APPLYDT, A.ACGUBN, A.MID_OPT, A.ACUSE "
                        "            , IFNULL((SELECT X.EMP_NME FROM OSSIGN Y "
                        "                LEFT OUTER JOIN PIS1TB001 X ON Y.EMP_NBR = X.EMP_NBR "
                        "                WHERE Y.ICUST = A.ICUST AND Y.ACDATE = A.IODATE AND Y.ACSEQN = A.ACSEQN AND Y.ACIOGB = A.ACIOGB "
                        "                AND Y.SEQ = (SELECT IFNULL(MAX(SEQ), '') FROM OSSIGN WHERE ICUST = A.ICUST AND ACDATE = A.IODATE AND ACSEQN = A.ACSEQN AND ACIOGB = A.ACIOGB AND OPT = 'Y')), '') AS NME "
                        "    FROM SISACCTT A "
                        "    LEFT OUTER JOIN MIS1TB003 B "
                        "    ON A.ACCUST = B.CUST_NBR "
                        "    LEFT OUTER JOIN ACNUMBER C "
                        "    ON A.ACACNUMBER = C.ACNUMBER "
                        "    LEFT OUTER JOIN OSCODEM D "
                        "    ON A.MCODE = D.MCODE "
                        "    LEFT OUTER JOIN OSREFCP E "
                        "    ON A.ACODE = E.RESKEY "
                        "    AND E.RECODE = 'ACD' "
                        "    LEFT OUTER JOIN OSCODEM F "
                        "    ON A.MCODE = F.MCODE "
                        "    LEFT OUTER JOIN OSREFCP G "
                        "    ON F.GBN = G.RESKEY "
                        "    AND G.RECODE = 'CGB' "
                        "    LEFT OUTER JOIN PIS1TB001 I "
                        "    ON A.CRE_USER = I.EMP_NBR "
                        "    WHERE A.ACIOGB = '1' "
                        "    AND A.ICUST = '" + str(iCust) + "'"
                        "    AND A.MID_OPT = 'N'"
                        "    AND A.FIN_OPT = 'N'"
                        " ) AA "
                        " WHERE AA.IODATE BETWEEN '" + str(strDate) + "' AND '" + str(endDate) + "' "
                        " ORDER BY AA.IODATE ")
                    mainresult = cursor.fetchall()
                    return JsonResponse({'balList': balresult, 'mainList': mainresult})

            if Gbn == '3':
                balresult = ''
                with connection.cursor() as cursor:
                    cursor.execute(
                        "  SELECT IFNULL(AA.ACIOGB, ''), IFNULL(AA.IODATE, ''), IFNULL(AA.IN_ACAMTS, 0), IFNULL(AA.OUT_ACAMTS, 0)"
                        "        , IFNULL(AA.ACCUST, ''), IFNULL(AA.CUST_NME, ''), IFNULL(AA.ACACNUMBER, ''), IFNULL(AA.ACNUM_NAME, '')"
                        "        , IFNULL(AA.MCODE, ''), IFNULL(AA.FIN_OPT, ''), IFNULL(AA.MCODENM, ''), IFNULL(AA.ACTITLE, '')"
                        "        , IFNULL(AA.ACSEQN, ''), IFNULL(AA.ACODE, ''), IFNULL(AA.ACODENM, ''), IFNULL(AA.GBN, '')"
                        "        , IFNULL(AA.GBNNM, ''), IFNULL(AA.APPLYDT, ''), IFNULL(AA.ACGUBN, ''), IFNULL(AA.GBN, '')"
                        "        , IFNULL(AA.FIN_OPT, ''), IFNULL(AA.MID_OPT, ''), IFNULL(AA.ACUSE, ''), IFNULL(AA.ACGUBN, ''), IFNULL(AA.NME, '') FROM "
                        " ( "
                        "     SELECT A.ACIOGB, A.IODATE, A.ACAMTS AS IN_ACAMTS, 0 AS OUT_ACAMTS, A.ACCUST, B.CUST_NME"
                        "            , A.ACACNUMBER, C.ACNUM_NAME, A.MCODE, A.FIN_OPT, D.MCODENM, A.ACTITLE, A.ACSEQN"
                        "            , A.ACODE, E.RESNAM AS ACODENM, F.GBN, G.RESNAM AS GBNNM, A.APPLYDT, A.ACGUBN, A.MID_OPT, A.ACUSE "
                        "            , IFNULL((SELECT X.EMP_NME FROM OSSIGN Y "
                        "                LEFT OUTER JOIN PIS1TB001 X ON Y.EMP_NBR = X.EMP_NBR "
                        "                WHERE Y.ICUST = A.ICUST AND Y.ACDATE = A.IODATE AND Y.ACSEQN = A.ACSEQN AND Y.ACIOGB = A.ACIOGB "
                        "                AND Y.SEQ = (SELECT IFNULL(MAX(SEQ), '') FROM OSSIGN WHERE ICUST = A.ICUST AND ACDATE = A.IODATE AND ACSEQN = A.ACSEQN AND ACIOGB = A.ACIOGB AND OPT = 'Y')), '') AS NME "
                        "     FROM SISACCTT A "
                        "     LEFT OUTER JOIN MIS1TB003 B "
                        "     ON A.ACCUST = B.CUST_NBR "
                        "     LEFT OUTER JOIN ACNUMBER C "
                        "     ON A.ACACNUMBER = C.ACNUMBER "
                        "     LEFT OUTER JOIN OSCODEM D "
                        "     ON A.MCODE = D.MCODE "
                        "    LEFT OUTER JOIN OSREFCP E "
                        "    ON A.ACODE = E.RESKEY "
                        "    AND E.RECODE = 'ACD' "
                        "    LEFT OUTER JOIN OSCODEM F "
                        "    ON A.MCODE = F.MCODE "
                        "    LEFT OUTER JOIN OSREFCP G "
                        "    ON F.GBN = G.RESKEY "
                        "    AND G.RECODE = 'CGB' "
                        "    LEFT OUTER JOIN PIS1TB001 I "
                        "    ON A.CRE_USER = I.EMP_NBR "
                        "    WHERE A.ACIOGB = '2' "
                        "    AND A.ICUST = '" + str(iCust) + "'"
                        "    AND A.MID_OPT = 'Y'"
                        "    AND A.FIN_OPT = 'Y'"
                        "    UNION ALL "
                        "    SELECT A.ACIOGB, A.IODATE, 0 AS IN_ACAMTS, A.ACAMTS AS OUT_ACAMTS, A.ACCUST, B.CUST_NME"
                        "           , A.ACACNUMBER, C.ACNUM_NAME, A.MCODE, A.FIN_OPT, D.MCODENM, A.ACTITLE, A.ACSEQN"
                        "            , A.ACODE, E.RESNAM AS ACODENM, F.GBN, G.RESNAM AS GBNNM, A.APPLYDT, A.ACGUBN, A.MID_OPT, A.ACUSE "
                        "            , IFNULL((SELECT X.EMP_NME FROM OSSIGN Y "
                        "                LEFT OUTER JOIN PIS1TB001 X ON Y.EMP_NBR = X.EMP_NBR "
                        "                WHERE Y.ICUST = A.ICUST AND Y.ACDATE = A.IODATE AND Y.ACSEQN = A.ACSEQN AND Y.ACIOGB = A.ACIOGB "
                        "                AND Y.SEQ = (SELECT IFNULL(MAX(SEQ), '') FROM OSSIGN WHERE ICUST = A.ICUST AND ACDATE = A.IODATE AND ACSEQN = A.ACSEQN AND ACIOGB = A.ACIOGB AND OPT = 'Y')), '') AS NME "
                        "    FROM SISACCTT A "
                        "    LEFT OUTER JOIN MIS1TB003 B "
                        "    ON A.ACCUST = B.CUST_NBR "
                        "    LEFT OUTER JOIN ACNUMBER C "
                        "    ON A.ACACNUMBER = C.ACNUMBER "
                        "    LEFT OUTER JOIN OSCODEM D "
                        "    ON A.MCODE = D.MCODE "
                        "    LEFT OUTER JOIN OSREFCP E "
                        "    ON A.ACODE = E.RESKEY "
                        "    AND E.RECODE = 'ACD' "
                        "    LEFT OUTER JOIN OSCODEM F "
                        "    ON A.MCODE = F.MCODE "
                        "    LEFT OUTER JOIN OSREFCP G "
                        "    ON F.GBN = G.RESKEY "
                        "    AND G.RECODE = 'CGB' "
                        "    LEFT OUTER JOIN PIS1TB001 I "
                        "    ON A.CRE_USER = I.EMP_NBR "
                        "    WHERE A.ACIOGB = '1' "
                        "    AND A.ICUST = '" + str(iCust) + "'"
                        "    AND A.MID_OPT = 'Y'"
                        "    AND A.FIN_OPT = 'Y'"
                        " ) AA "
                        " WHERE AA.IODATE BETWEEN '" + str(strDate) + "' AND '" + str(endDate) + "' "
                        " ORDER BY AA.IODATE ")
                    mainresult = cursor.fetchall()
                    return JsonResponse({'balList': balresult, 'mainList': mainresult})

        if empName != '':
            with connection.cursor() as cursor:
                cursor.execute(" SELECT EMP_NBR FROM PIS1TB001 WHERE EMP_NME LIKE '%" + str(empName) + "%' ")
                result = cursor.fetchall()
                empCode = result[0][0]

            balresult = ''
            with connection.cursor() as cursor:
                cursor.execute("  SELECT IFNULL(AA.ACIOGB, ''), IFNULL(AA.IODATE, ''), IFNULL(AA.IN_ACAMTS, 0), IFNULL(AA.OUT_ACAMTS, 0)"
                               "        , IFNULL(AA.ACCUST, ''), IFNULL(AA.CUST_NME, ''), IFNULL(AA.ACACNUMBER, ''), IFNULL(AA.ACNUM_NAME, '')"
                               "        , IFNULL(AA.MCODE, ''), IFNULL(AA.FIN_OPT, ''), IFNULL(AA.MCODENM, ''), IFNULL(AA.ACTITLE, '')"
                               "        , IFNULL(AA.ACSEQN, ''), IFNULL(AA.ACODE, ''), IFNULL(AA.ACODENM, ''), IFNULL(AA.GBN, '')"
                               "        , IFNULL(AA.GBNNM, ''), IFNULL(AA.APPLYDT, ''), IFNULL(AA.ACGUBN, ''), IFNULL(AA.GBN, '')"
                               "        , IFNULL(AA.FIN_OPT, ''), IFNULL(AA.MID_OPT, ''), IFNULL(AA.ACUSE, ''), IFNULL(AA.ACGUBN, ''), IFNULL(AA.NME, '') FROM "
                               " ( "
                               "     SELECT A.ACIOGB, A.IODATE, A.ACAMTS AS IN_ACAMTS, 0 AS OUT_ACAMTS, A.ACCUST, B.CUST_NME"
                               "            , A.ACACNUMBER, C.ACNUM_NAME, A.MCODE, A.FIN_OPT, D.MCODENM, A.ACTITLE, A.ACSEQN"
                               "            , A.ACODE, E.RESNAM AS ACODENM, F.GBN, G.RESNAM AS GBNNM, A.APPLYDT, A.ACGUBN, A.MID_OPT, A.ACUSE  "
                               "            , IFNULL((SELECT X.EMP_NME FROM OSSIGN Y "
                               "                LEFT OUTER JOIN PIS1TB001 X ON Y.EMP_NBR = X.EMP_NBR "
                               "                WHERE Y.ICUST = A.ICUST AND Y.ACDATE = A.IODATE AND Y.ACSEQN = A.ACSEQN AND Y.ACIOGB = A.ACIOGB "
                               "                AND Y.SEQ = (SELECT IFNULL(MAX(SEQ), '') FROM OSSIGN WHERE ICUST = A.ICUST AND ACDATE = A.IODATE AND ACSEQN = A.ACSEQN AND ACIOGB = A.ACIOGB AND OPT = 'Y')), '') AS NME "
                               "     FROM SISACCTT A "
                               "     LEFT OUTER JOIN MIS1TB003 B "
                               "     ON A.ACCUST = B.CUST_NBR "
                               "     LEFT OUTER JOIN ACNUMBER C "
                               "     ON A.ACACNUMBER = C.ACNUMBER "
                               "     LEFT OUTER JOIN OSCODEM D "
                               "     ON A.MCODE = D.MCODE "
                               "    LEFT OUTER JOIN OSREFCP E "
                               "    ON A.ACODE = E.RESKEY "
                               "    AND E.RECODE = 'ACD' "
                               "    LEFT OUTER JOIN OSCODEM F "
                               "    ON A.MCODE = F.MCODE "
                               "    LEFT OUTER JOIN OSREFCP G "
                               "    ON F.GBN = G.RESKEY "
                               "    AND G.RECODE = 'CGB' "
                               "     WHERE A.ACIOGB = '2' "
                               "     AND A.ICUST = '" + str(iCust) + "'"
                               "     AND A.CRE_USER = '" + str(empCode) + "'"
                               "     UNION ALL "
                               "     SELECT A.ACIOGB, A.IODATE, 0 AS IN_ACAMTS, A.ACAMTS AS OUT_ACAMTS, A.ACCUST, B.CUST_NME"
                               "            , A.ACACNUMBER, C.ACNUM_NAME, A.MCODE, A.FIN_OPT, D.MCODENM, A.ACTITLE, A.ACSEQN"
                               "            , A.ACODE, E.RESNAM AS ACODENM, F.GBN, G.RESNAM AS GBNNM, A.APPLYDT, A.ACGUBN, A.MID_OPT, A.ACUSE  "
                               "            , IFNULL((SELECT X.EMP_NME FROM OSSIGN Y "
                               "                LEFT OUTER JOIN PIS1TB001 X ON Y.EMP_NBR = X.EMP_NBR "
                               "                WHERE Y.ICUST = A.ICUST AND Y.ACDATE = A.IODATE AND Y.ACSEQN = A.ACSEQN AND Y.ACIOGB = A.ACIOGB "
                               "                AND Y.SEQ = (SELECT IFNULL(MAX(SEQ), '') FROM OSSIGN WHERE ICUST = A.ICUST AND ACDATE = A.IODATE AND ACSEQN = A.ACSEQN AND ACIOGB = A.ACIOGB AND OPT = 'Y')), '') AS NME "
                               "     FROM SISACCTT A "
                               "     LEFT OUTER JOIN MIS1TB003 B "
                               "     ON A.ACCUST = B.CUST_NBR "
                               "     LEFT OUTER JOIN ACNUMBER C "
                               "     ON A.ACACNUMBER = C.ACNUMBER "
                               "     LEFT OUTER JOIN OSCODEM D "
                               "     ON A.MCODE = D.MCODE "
                               "    LEFT OUTER JOIN OSREFCP E "
                               "    ON A.ACODE = E.RESKEY "
                               "    AND E.RECODE = 'ACD' "
                               "    LEFT OUTER JOIN OSCODEM F "
                               "    ON A.MCODE = F.MCODE "
                               "    LEFT OUTER JOIN OSREFCP G "
                               "    ON F.GBN = G.RESKEY "
                               "    AND G.RECODE = 'CGB' "                                   
                               "     WHERE A.ACIOGB = '1' "
                               "     AND A.ICUST = '" + str(iCust) + "'"
                               "     AND A.CRE_USER = '" + str(empCode) + "'"
                               " ) AA "
                               " WHERE AA.IODATE BETWEEN '" + str(strDate) + "' AND '" + str(endDate) + "' "
                               " ORDER BY AA.IODATE ")
                mainresult = cursor.fetchall()

            return JsonResponse({'balList': balresult, 'mainList': mainresult})

        if payGbn != '':
            balresult = ''
            with connection.cursor() as cursor:
                cursor.execute("  SELECT IFNULL(AA.ACIOGB, ''), IFNULL(AA.IODATE, ''), IFNULL(AA.IN_ACAMTS, 0), IFNULL(AA.OUT_ACAMTS, 0)"
                               "        , IFNULL(AA.ACCUST, ''), IFNULL(AA.CUST_NME, ''), IFNULL(AA.ACACNUMBER, ''), IFNULL(AA.ACNUM_NAME, '')"
                               "        , IFNULL(AA.MCODE, ''), IFNULL(AA.FIN_OPT, ''), IFNULL(AA.MCODENM, ''), IFNULL(AA.ACTITLE, '')"
                               "        , IFNULL(AA.ACSEQN, ''), IFNULL(AA.ACODE, ''), IFNULL(AA.ACODENM, ''), IFNULL(AA.GBN, '')"
                               "        , IFNULL(AA.GBNNM, ''), IFNULL(AA.APPLYDT, ''), IFNULL(AA.ACGUBN, ''), IFNULL(AA.GBN, '')"
                               "        , IFNULL(AA.FIN_OPT, ''), IFNULL(AA.MID_OPT, ''), IFNULL(AA.ACUSE, ''), IFNULL(AA.ACGUBN, ''), IFNULL(AA.NME, '') FROM "
                               " ( "
                               "     SELECT A.ACIOGB, A.IODATE, A.ACAMTS AS IN_ACAMTS, 0 AS OUT_ACAMTS, A.ACCUST, B.CUST_NME"
                               "            , A.ACACNUMBER, C.ACNUM_NAME, A.MCODE, A.FIN_OPT, D.MCODENM, A.ACTITLE, A.ACSEQN"
                               "            , A.ACODE, E.RESNAM AS ACODENM, F.GBN, G.RESNAM AS GBNNM, A.APPLYDT, A.ACGUBN, A.MID_OPT, A.ACUSE  "
                               "            , IFNULL((SELECT X.EMP_NME FROM OSSIGN Y "
                               "                LEFT OUTER JOIN PIS1TB001 X ON Y.EMP_NBR = X.EMP_NBR "
                               "                WHERE Y.ICUST = A.ICUST AND Y.ACDATE = A.IODATE AND Y.ACSEQN = A.ACSEQN AND Y.ACIOGB = A.ACIOGB "
                               "                AND Y.SEQ = (SELECT IFNULL(MAX(SEQ), '') FROM OSSIGN WHERE ICUST = A.ICUST AND ACDATE = A.IODATE AND ACSEQN = A.ACSEQN AND ACIOGB = A.ACIOGB AND OPT = 'Y')), '') AS NME "
                               "     FROM SISACCTT A "
                               "     LEFT OUTER JOIN MIS1TB003 B "
                               "     ON A.ACCUST = B.CUST_NBR "
                               "     LEFT OUTER JOIN ACNUMBER C "
                               "     ON A.ACACNUMBER = C.ACNUMBER "
                               "     LEFT OUTER JOIN OSCODEM D "
                               "     ON A.MCODE = D.MCODE "
                               "    LEFT OUTER JOIN OSREFCP E "
                               "    ON A.ACODE = E.RESKEY "
                               "    AND E.RECODE = 'ACD' "
                               "    LEFT OUTER JOIN OSCODEM F "
                               "    ON A.MCODE = F.MCODE "
                               "    LEFT OUTER JOIN OSREFCP G "
                               "    ON F.GBN = G.RESKEY "
                               "    AND G.RECODE = 'CGB' "
                               "     WHERE A.ACIOGB = '2' "
                               "     AND A.ICUST = '" + str(iCust) + "'"
                               "     AND A.ACGUBN = '" + str(payGbn) + "'"
                               "     UNION ALL "
                               "     SELECT A.ACIOGB, A.IODATE, 0 AS IN_ACAMTS, A.ACAMTS AS OUT_ACAMTS, A.ACCUST, B.CUST_NME"
                               "            , A.ACACNUMBER, C.ACNUM_NAME, A.MCODE, A.FIN_OPT, D.MCODENM, A.ACTITLE, A.ACSEQN"
                               "            , A.ACODE, E.RESNAM AS ACODENM, F.GBN, G.RESNAM AS GBNNM, A.APPLYDT, A.ACGUBN, A.MID_OPT, A.ACUSE  "
                               "            , IFNULL((SELECT X.EMP_NME FROM OSSIGN Y "
                               "                LEFT OUTER JOIN PIS1TB001 X ON Y.EMP_NBR = X.EMP_NBR "
                               "                WHERE Y.ICUST = A.ICUST AND Y.ACDATE = A.IODATE AND Y.ACSEQN = A.ACSEQN AND Y.ACIOGB = A.ACIOGB "
                               "                AND Y.SEQ = (SELECT IFNULL(MAX(SEQ), '') FROM OSSIGN WHERE ICUST = A.ICUST AND ACDATE = A.IODATE AND ACSEQN = A.ACSEQN AND ACIOGB = A.ACIOGB AND OPT = 'Y')), '') AS NME "
                               "     FROM SISACCTT A "
                               "     LEFT OUTER JOIN MIS1TB003 B "
                               "     ON A.ACCUST = B.CUST_NBR "
                               "     LEFT OUTER JOIN ACNUMBER C "
                               "     ON A.ACACNUMBER = C.ACNUMBER "
                               "     LEFT OUTER JOIN OSCODEM D "
                               "     ON A.MCODE = D.MCODE "
                               "    LEFT OUTER JOIN OSREFCP E "
                               "    ON A.ACODE = E.RESKEY "
                               "    AND E.RECODE = 'ACD' "
                               "    LEFT OUTER JOIN OSCODEM F "
                               "    ON A.MCODE = F.MCODE "
                               "    LEFT OUTER JOIN OSREFCP G "
                               "    ON F.GBN = G.RESKEY "
                               "    AND G.RECODE = 'CGB' "                                   
                               "     WHERE A.ACIOGB = '1' "
                               "     AND A.ICUST = '" + str(iCust) + "'"
                               "     AND A.ACGUBN = '" + str(payGbn) + "'"
                               " ) AA "
                               " WHERE AA.IODATE BETWEEN '" + str(strDate) + "' AND '" + str(endDate) + "' "
                               " ORDER BY AA.IODATE ")
                mainresult = cursor.fetchall()

            return JsonResponse({'balList': balresult, 'mainList': mainresult})

        if strDate != '' and endDate != '' and cboAct == '' and cboCust == '':
            balresult = ''
            with connection.cursor() as cursor:
                cursor.execute("  SELECT IFNULL(AA.ACIOGB, ''), IFNULL(AA.IODATE, ''), IFNULL(AA.IN_ACAMTS, 0), IFNULL(AA.OUT_ACAMTS, 0)"
                               "        , IFNULL(AA.ACCUST, ''), IFNULL(AA.CUST_NME, ''), IFNULL(AA.ACACNUMBER, ''), IFNULL(AA.ACNUM_NAME, '')"
                               "        , IFNULL(AA.MCODE, ''), IFNULL(AA.FIN_OPT, ''), IFNULL(AA.MCODENM, ''), IFNULL(AA.ACTITLE, '')"
                               "        , IFNULL(AA.ACSEQN, ''), IFNULL(AA.ACODE, ''), IFNULL(AA.ACODENM, ''), IFNULL(AA.GBN, '')"
                               "        , IFNULL(AA.GBNNM, ''), IFNULL(AA.APPLYDT, ''), IFNULL(AA.ACGUBN, ''), IFNULL(AA.GBN, '')"
                               "        , IFNULL(AA.FIN_OPT, ''), IFNULL(AA.MID_OPT, ''), IFNULL(AA.ACUSE, ''), IFNULL(AA.ACGUBN, ''), IFNULL(AA.NME, '') FROM "
                               " ( "
                               "     SELECT A.ACIOGB, A.IODATE, A.ACAMTS AS IN_ACAMTS, 0 AS OUT_ACAMTS, A.ACCUST, B.CUST_NME"
                               "            , A.ACACNUMBER, C.ACNUM_NAME, A.MCODE, A.FIN_OPT, D.MCODENM, A.ACTITLE, A.ACSEQN"
                               "            , A.ACODE, E.RESNAM AS ACODENM, F.GBN, G.RESNAM AS GBNNM, A.APPLYDT, A.ACGUBN, A.MID_OPT, A.ACUSE  "
                               "            , IFNULL((SELECT X.EMP_NME FROM OSSIGN Y "
                               "                LEFT OUTER JOIN PIS1TB001 X ON Y.EMP_NBR = X.EMP_NBR "
                               "                WHERE Y.ICUST = A.ICUST AND Y.ACDATE = A.IODATE AND Y.ACSEQN = A.ACSEQN AND Y.ACIOGB = A.ACIOGB "
                               "                AND Y.SEQ = (SELECT IFNULL(MAX(SEQ), '') FROM OSSIGN WHERE ICUST = A.ICUST AND ACDATE = A.IODATE AND ACSEQN = A.ACSEQN AND ACIOGB = A.ACIOGB AND OPT = 'Y')), '') AS NME "
                               "     FROM SISACCTT A "
                               "     LEFT OUTER JOIN MIS1TB003 B "
                               "     ON A.ACCUST = B.CUST_NBR "
                               "     LEFT OUTER JOIN ACNUMBER C "
                               "     ON A.ACACNUMBER = C.ACNUMBER "
                               "     LEFT OUTER JOIN OSCODEM D "
                               "     ON A.MCODE = D.MCODE "
                               "    LEFT OUTER JOIN OSREFCP E "
                               "    ON A.ACODE = E.RESKEY "
                               "    AND E.RECODE = 'ACD' "
                               "    LEFT OUTER JOIN OSCODEM F "
                               "    ON A.MCODE = F.MCODE "
                               "    LEFT OUTER JOIN OSREFCP G "
                               "    ON F.GBN = G.RESKEY "
                               "    AND G.RECODE = 'CGB' "
                               "     WHERE A.ACIOGB = '2' "
                               "     AND A.ICUST = '" + str(iCust) + "'"
                               "     AND A.CRE_USER = '" + str(creUser) + "'"
                               "     UNION ALL "
                               "     SELECT A.ACIOGB, A.IODATE, 0 AS IN_ACAMTS, A.ACAMTS AS OUT_ACAMTS, A.ACCUST, B.CUST_NME"
                               "            , A.ACACNUMBER, C.ACNUM_NAME, A.MCODE, A.FIN_OPT, D.MCODENM, A.ACTITLE, A.ACSEQN"
                               "            , A.ACODE, E.RESNAM AS ACODENM, F.GBN, G.RESNAM AS GBNNM, A.APPLYDT, A.ACGUBN, A.MID_OPT, A.ACUSE  "
                               "            , IFNULL((SELECT X.EMP_NME FROM OSSIGN Y "
                               "                LEFT OUTER JOIN PIS1TB001 X ON Y.EMP_NBR = X.EMP_NBR "
                               "                WHERE Y.ICUST = A.ICUST AND Y.ACDATE = A.IODATE AND Y.ACSEQN = A.ACSEQN AND Y.ACIOGB = A.ACIOGB "
                               "                AND Y.SEQ = (SELECT IFNULL(MAX(SEQ), '') FROM OSSIGN WHERE ICUST = A.ICUST AND ACDATE = A.IODATE AND ACSEQN = A.ACSEQN AND ACIOGB = A.ACIOGB AND OPT = 'Y')), '') AS NME "
                               "     FROM SISACCTT A "
                               "     LEFT OUTER JOIN MIS1TB003 B "
                               "     ON A.ACCUST = B.CUST_NBR "
                               "     LEFT OUTER JOIN ACNUMBER C "
                               "     ON A.ACACNUMBER = C.ACNUMBER "
                               "     LEFT OUTER JOIN OSCODEM D "
                               "     ON A.MCODE = D.MCODE "
                               "    LEFT OUTER JOIN OSREFCP E "
                               "    ON A.ACODE = E.RESKEY "
                               "    AND E.RECODE = 'ACD' "
                               "    LEFT OUTER JOIN OSCODEM F "
                               "    ON A.MCODE = F.MCODE "
                               "    LEFT OUTER JOIN OSREFCP G "
                               "    ON F.GBN = G.RESKEY "
                               "    AND G.RECODE = 'CGB' "                                   
                               "     WHERE A.ACIOGB = '1' "
                               "     AND A.ICUST = '" + str(iCust) + "'"
                               "     AND A.CRE_USER = '" + str(creUser) + "'"
                               " ) AA "
                               " WHERE AA.IODATE BETWEEN '" + str(strDate) + "' AND '" + str(endDate) + "' "
                               " ORDER BY AA.IODATE ")
                mainresult = cursor.fetchall()

                # 거래처
                with connection.cursor() as cursor:
                    cursor.execute(" SELECT CUST_NBR, CUST_NME FROM MIS1TB003 WHERE ICUST = '" + str(iCust) + "' ORDER BY CUST_NBR ")
                    cboCust = cursor.fetchall()

                with connection.cursor() as cursor:
                    cursor.execute(" SELECT ACNUMBER FROM ACNUMBER WHERE ICUST = '" + str(iCust) + "' ")
                    cboAct = cursor.fetchall()

                with connection.cursor() as cursor:
                    cursor.execute(" SELECT A.ACBKCD, B.RESNAM FROM ACNUMBER A LEFT OUTER JOIN OSREFCP B ON A.ACBKCD = B.RESKEY AND B.RECODE = 'BNK' AND A.ICUST = '" + str(iCust) + "' "
                                   " GROUP BY A.ACBKCD, B.RESNAM ORDER BY A.ACBKCD ")
                    inputBank = cursor.fetchall()

            return JsonResponse({'balList': balresult, 'mainList': mainresult, 'cboCust': cboCust, 'cboAct': cboAct, 'inputBank': inputBank})

        if cboCust != '' and cboAct == '':
            balresult = ''

            with connection.cursor() as cursor:
                cursor.execute("  SELECT IFNULL(AA.ACIOGB, ''), IFNULL(AA.IODATE, ''), IFNULL(AA.IN_ACAMTS, 0), IFNULL(AA.OUT_ACAMTS, 0)"
                               "        , IFNULL(AA.ACCUST, ''), IFNULL(AA.CUST_NME, ''), IFNULL(AA.ACACNUMBER, ''), IFNULL(AA.ACNUM_NAME, '')"
                               "        , IFNULL(AA.MCODE, ''), IFNULL(AA.FIN_OPT, ''), IFNULL(AA.MCODENM, ''), IFNULL(AA.ACTITLE, '')"
                               "        , IFNULL(AA.ACSEQN, ''), IFNULL(AA.ACODE, ''), IFNULL(AA.ACODENM, ''), IFNULL(AA.GBN, ''), IFNULL(AA.GBNNM, '')"
                               "        , IFNULL(AA.ACBKCD, ''), IFNULL(AA.BANKNM, ''), IFNULL(AA.APPLYDT, ''), IFNULL(AA.ACGUBN, ''), IFNULL(AA.MID_OPT, '')"
                               "        , IFNULL(AA.ACUSE, ''), IFNULL(AA.ACGUBN, ''), IFNULL(AA.NME, '')  FROM "
                               " ( "
                               "     SELECT A.ACIOGB, A.IODATE, A.ACAMTS AS IN_ACAMTS, 0 AS OUT_ACAMTS, A.ACCUST, B.CUST_NME"
                               "            , A.ACACNUMBER, C.ACNUM_NAME, A.MCODE, A.FIN_OPT, D.MCODENM, A.ACTITLE, A.ACSEQN"
                               "            , A.ACODE, E.RESNAM AS ACODENM, F.GBN, G.RESNAM AS GBNNM, C.ACBKCD, H.RESNAM AS BANKNM, A.APPLYDT, A.ACGUBN, A.MID_OPT, A.ACUSE "
                               "            , IFNULL((SELECT X.EMP_NME FROM OSSIGN Y "
                               "                LEFT OUTER JOIN PIS1TB001 X ON Y.EMP_NBR = X.EMP_NBR "
                               "                WHERE Y.ICUST = A.ICUST AND Y.ACDATE = A.IODATE AND Y.ACSEQN = A.ACSEQN AND Y.ACIOGB = A.ACIOGB "
                               "                AND Y.SEQ = (SELECT IFNULL(MAX(SEQ), '') FROM OSSIGN WHERE ICUST = A.ICUST AND ACDATE = A.IODATE AND ACSEQN = A.ACSEQN AND ACIOGB = A.ACIOGB AND OPT = 'Y')), '') AS NME "
                               "     FROM SISACCTT A "
                               "     LEFT OUTER JOIN MIS1TB003 B "
                               "     ON A.ACCUST = B.CUST_NBR "
                               "     LEFT OUTER JOIN ACNUMBER C "
                               "     ON A.ACACNUMBER = C.ACNUMBER "
                               "     LEFT OUTER JOIN OSCODEM D "
                               "     ON A.MCODE = D.MCODE "
                               "    LEFT OUTER JOIN OSREFCP E "
                               "    ON A.ACODE = E.RESKEY "
                               "    AND E.RECODE = 'ACD' "
                               "    LEFT OUTER JOIN OSCODEM F "
                               "    ON A.MCODE = F.MCODE "
                               "    LEFT OUTER JOIN OSREFCP G "
                               "    ON F.GBN = G.RESKEY "
                               "    AND G.RECODE = 'CGB' "
                               "    LEFT OUTER JOIN OSREFCP H"
                               "    ON C.ACBKCD = H.RESKEY"
                               "    AND H.RECODE = 'BNK'"
                               "     WHERE A.ACIOGB = '2' "
                               "     AND A.ICUST = '" + str(iCust) + "'"
                               "     AND A.CRE_USER = '" + str(creUser) + "'"
                               "     UNION ALL "
                               "     SELECT A.ACIOGB, A.IODATE, 0 AS IN_ACAMTS, A.ACAMTS AS OUT_ACAMTS, A.ACCUST, B.CUST_NME"
                               "            , A.ACACNUMBER, C.ACNUM_NAME, A.MCODE, A.FIN_OPT, D.MCODENM, A.ACTITLE, A.ACSEQN"
                               "            , A.ACODE, E.RESNAM AS ACODENM, F.GBN, G.RESNAM AS GBNNM, C.ACBKCD, H.RESNAM AS BANKNM, A.APPLYDT, A.ACGUBN, A.MID_OPT, A.ACUSE "
                               "            , IFNULL((SELECT X.EMP_NME FROM OSSIGN Y "
                               "                LEFT OUTER JOIN PIS1TB001 X ON Y.EMP_NBR = X.EMP_NBR "
                               "                WHERE Y.ICUST = A.ICUST AND Y.ACDATE = A.IODATE AND Y.ACSEQN = A.ACSEQN AND Y.ACIOGB = A.ACIOGB "
                               "                AND Y.SEQ = (SELECT IFNULL(MAX(SEQ), '') FROM OSSIGN WHERE ICUST = A.ICUST AND ACDATE = A.IODATE AND ACSEQN = A.ACSEQN AND ACIOGB = A.ACIOGB AND OPT = 'Y')), '') AS NME "
                               "     FROM SISACCTT A "
                               "     LEFT OUTER JOIN MIS1TB003 B "
                               "     ON A.ACCUST = B.CUST_NBR "
                               "     LEFT OUTER JOIN ACNUMBER C "
                               "     ON A.ACACNUMBER = C.ACNUMBER "
                               "     LEFT OUTER JOIN OSCODEM D "
                               "     ON A.MCODE = D.MCODE "
                               "    LEFT OUTER JOIN OSREFCP E "
                               "    ON A.ACODE = E.RESKEY "
                               "    AND E.RECODE = 'ACD' "
                               "    LEFT OUTER JOIN OSCODEM F "
                               "    ON A.MCODE = F.MCODE "
                               "    LEFT OUTER JOIN OSREFCP G "
                               "    ON F.GBN = G.RESKEY "
                               "    AND G.RECODE = 'CGB' "
                               "    LEFT OUTER JOIN OSREFCP H"
                               "    ON C.ACBKCD = H.RESKEY"
                               "    AND H.RECODE = 'BNK'"
                               "     WHERE A.ACIOGB = '1' "
                               "     AND A.ICUST = '" + str(iCust) + "'"
                               "     AND A.CRE_USER = '" + str(creUser) + "'"
                               " ) AA "
                               " WHERE AA.IODATE BETWEEN '" + str(strDate) + "' AND '" + str(endDate) + "' "
                               " AND AA.ACCUST = '" + str(cboCust) + "' "
                               " ORDER BY AA.IODATE ")
                mainresult = cursor.fetchall()

            return JsonResponse({'balList': balresult, 'mainList': mainresult})

        if cboAct != '' and cboCust == '':
            balresult = ''
            with connection.cursor() as cursor:
                cursor.execute("  SELECT IFNULL(AA.ACIOGB, ''), IFNULL(AA.IODATE, ''), IFNULL(AA.IN_ACAMTS, 0), IFNULL(AA.OUT_ACAMTS, 0)"
                               "        , IFNULL(AA.ACCUST, ''), IFNULL(AA.CUST_NME, ''), IFNULL(AA.ACACNUMBER, ''), IFNULL(AA.ACNUM_NAME, '')"
                               "        , IFNULL(AA.MCODE, ''), IFNULL(AA.FIN_OPT, ''), IFNULL(AA.MCODENM, ''), IFNULL(AA.ACTITLE, '')"
                               "        , IFNULL(AA.ACSEQN, ''), IFNULL(AA.ACODE, ''), IFNULL(AA.ACODENM, ''), IFNULL(AA.GBN, '')"
                               "        , IFNULL(AA.GBNNM, ''), IFNULL(AA.APPLYDT, ''), IFNULL(AA.ACGUBN, ''), IFNULL(AA.GBN, '')"
                               "        , IFNULL(AA.FIN_OPT, ''), IFNULL(AA.MID_OPT, ''), IFNULL(AA.ACUSE, ''), IFNULL(AA.ACGUBN, ''), IFNULL(AA.NME, '') FROM "
                               " ( "
                               "     SELECT A.ACIOGB, A.IODATE, A.ACAMTS AS IN_ACAMTS, 0 AS OUT_ACAMTS, A.ACCUST, B.CUST_NME"
                               "            , A.ACACNUMBER, C.ACNUM_NAME, A.MCODE, A.FIN_OPT, D.MCODENM, A.ACTITLE, A.ACSEQN"
                               "            , A.ACODE, E.RESNAM AS ACODENM, F.GBN, G.RESNAM AS GBNNM, A.APPLYDT, A.ACGUBN, A.MID_OPT, A.ACUSE "
                               "            , IFNULL((SELECT X.EMP_NME FROM OSSIGN Y "
                               "                LEFT OUTER JOIN PIS1TB001 X ON Y.EMP_NBR = X.EMP_NBR "
                               "                WHERE Y.ICUST = A.ICUST AND Y.ACDATE = A.IODATE AND Y.ACSEQN = A.ACSEQN AND Y.ACIOGB = A.ACIOGB "
                               "                AND Y.SEQ = (SELECT IFNULL(MAX(SEQ), '') FROM OSSIGN WHERE ICUST = A.ICUST AND ACDATE = A.IODATE AND ACSEQN = A.ACSEQN AND ACIOGB = A.ACIOGB AND OPT = 'Y')), '') AS NME "
                               "     FROM SISACCTT A "
                               "     LEFT OUTER JOIN MIS1TB003 B "
                               "     ON A.ACCUST = B.CUST_NBR "
                               "     LEFT OUTER JOIN ACNUMBER C "
                               "     ON A.ACACNUMBER = C.ACNUMBER "
                               "     LEFT OUTER JOIN OSCODEM D "
                               "     ON A.MCODE = D.MCODE "
                               "    LEFT OUTER JOIN OSREFCP E "
                               "    ON A.ACODE = E.RESKEY "
                               "    AND E.RECODE = 'ACD' "
                               "    LEFT OUTER JOIN OSCODEM F "
                               "    ON A.MCODE = F.MCODE "
                               "    LEFT OUTER JOIN OSREFCP G "
                               "    ON F.GBN = G.RESKEY "
                               "    AND G.RECODE = 'CGB' "
                               "     WHERE A.ACIOGB = '2' "
                               "     AND A.ICUST = '" + str(iCust) + "'"
                               "     AND A.CRE_USER = '" + str(creUser) + "'"
                               "     UNION ALL "
                               "     SELECT A.ACIOGB, A.IODATE, 0 AS IN_ACAMTS, A.ACAMTS AS OUT_ACAMTS, A.ACCUST, B.CUST_NME"
                               "            , A.ACACNUMBER, C.ACNUM_NAME, A.MCODE, A.FIN_OPT, D.MCODENM, A.ACTITLE, A.ACSEQN"
                               "            , A.ACODE, E.RESNAM AS ACODENM, F.GBN, G.RESNAM AS GBNNM, A.APPLYDT, A.ACGUBN, A.MID_OPT, A.ACUSE "
                               "            , IFNULL((SELECT X.EMP_NME FROM OSSIGN Y "
                               "                LEFT OUTER JOIN PIS1TB001 X ON Y.EMP_NBR = X.EMP_NBR "
                               "                WHERE Y.ICUST = A.ICUST AND Y.ACDATE = A.IODATE AND Y.ACSEQN = A.ACSEQN AND Y.ACIOGB = A.ACIOGB "
                               "                AND Y.SEQ = (SELECT IFNULL(MAX(SEQ), '') FROM OSSIGN WHERE ICUST = A.ICUST AND ACDATE = A.IODATE AND ACSEQN = A.ACSEQN AND ACIOGB = A.ACIOGB AND OPT = 'Y')), '') AS NME "
                               "     FROM SISACCTT A "
                               "     LEFT OUTER JOIN MIS1TB003 B "
                               "     ON A.ACCUST = B.CUST_NBR "
                               "     LEFT OUTER JOIN ACNUMBER C "
                               "     ON A.ACACNUMBER = C.ACNUMBER "
                               "     LEFT OUTER JOIN OSCODEM D "
                               "     ON A.MCODE = D.MCODE "
                               "    LEFT OUTER JOIN OSREFCP E "
                               "    ON A.ACODE = E.RESKEY "
                               "    AND E.RECODE = 'ACD' "
                               "    LEFT OUTER JOIN OSCODEM F "
                               "    ON A.MCODE = F.MCODE "
                               "    LEFT OUTER JOIN OSREFCP G "
                               "    ON F.GBN = G.RESKEY "
                               "    AND G.RECODE = 'CGB' "                                 
                               "     WHERE A.ACIOGB = '1' "
                               "     AND A.ICUST = '" + str(iCust) + "'"
                               "     AND A.CRE_USER = '" + str(creUser) + "'"
                               " ) AA "
                               " WHERE AA.IODATE BETWEEN '" + str(strDate) + "' AND '" + str(endDate) + "' "
                               " AND AA.ACACNUMBER = '" + str(cboAct) + "' "
                               " ORDER BY AA.IODATE ")
                mainresult = cursor.fetchall()

            return JsonResponse({'balList': balresult, 'mainList': mainresult})

        if cboAct != '' and cboCust != '':
            balresult = ''

            with connection.cursor() as cursor:
                cursor.execute("  SELECT IFNULL(AA.ACIOGB, ''), IFNULL(AA.IODATE, ''), IFNULL(AA.IN_ACAMTS, 0), IFNULL(AA.OUT_ACAMTS, 0)"
                               "        , IFNULL(AA.ACCUST, ''), IFNULL(AA.CUST_NME, ''), IFNULL(AA.ACACNUMBER, ''), IFNULL(AA.ACNUM_NAME, '')"
                               "        , IFNULL(AA.MCODE, ''), IFNULL(AA.FIN_OPT, ''), IFNULL(AA.MCODENM, ''), IFNULL(AA.ACTITLE, '')"
                               "        , IFNULL(AA.ACSEQN, ''), IFNULL(AA.ACODE, ''), IFNULL(AA.ACODENM, ''), IFNULL(AA.GBN, ''), IFNULL(AA.GBNNM, '')"
                               "        , IFNULL(AA.ACBKCD, ''), IFNULL(AA.BANKNM, ''), IFNULL(AA.APPLYDT, ''), IFNULL(AA.ACGUBN, ''), IFNULL(AA.MID_OPT, '')"
                               "        , IFNULL(AA.ACUSE, ''), IFNULL(AA.ACGUBN, ''), IFNULL(AA.NME, '')FROM "
                               " ( "
                               "     SELECT A.ACIOGB, A.IODATE, A.ACAMTS AS IN_ACAMTS, 0 AS OUT_ACAMTS, A.ACCUST, B.CUST_NME"
                               "            , A.ACACNUMBER, C.ACNUM_NAME, A.MCODE, A.FIN_OPT, D.MCODENM, A.ACTITLE, A.ACSEQN"
                               "            , A.ACODE, E.RESNAM AS ACODENM, F.GBN, G.RESNAM AS GBNNM, C.ACBKCD, H.RESNAM AS BANKNM, A.APPLYDT, A.ACGUBN, A.MID_OPT, A.ACUSE  "
                               "            , IFNULL((SELECT X.EMP_NME FROM OSSIGN Y "
                               "                LEFT OUTER JOIN PIS1TB001 X ON Y.EMP_NBR = X.EMP_NBR "
                               "                WHERE Y.ICUST = A.ICUST AND Y.ACDATE = A.IODATE AND Y.ACSEQN = A.ACSEQN AND Y.ACIOGB = A.ACIOGB "
                               "                AND Y.SEQ = (SELECT IFNULL(MAX(SEQ), '') FROM OSSIGN WHERE ICUST = A.ICUST AND ACDATE = A.IODATE AND ACSEQN = A.ACSEQN AND ACIOGB = A.ACIOGB AND OPT = 'Y')), '') AS NME "
                               "     FROM SISACCTT A "
                               "     LEFT OUTER JOIN MIS1TB003 B "
                               "     ON A.ACCUST = B.CUST_NBR "
                               "     LEFT OUTER JOIN ACNUMBER C "
                               "     ON A.ACACNUMBER = C.ACNUMBER "
                               "     LEFT OUTER JOIN OSCODEM D "
                               "     ON A.MCODE = D.MCODE "
                               "    LEFT OUTER JOIN OSREFCP E "
                               "    ON A.ACODE = E.RESKEY "
                               "    AND E.RECODE = 'ACD' "
                               "    LEFT OUTER JOIN OSCODEM F "
                               "    ON A.MCODE = F.MCODE "
                               "    LEFT OUTER JOIN OSREFCP G "
                               "    ON F.GBN = G.RESKEY "
                               "    AND G.RECODE = 'CGB' "
                               "    LEFT OUTER JOIN OSREFCP H"
                               "    ON C.ACBKCD = H.RESKEY"
                               "    AND H.RECODE = 'BNK'"
                               "     WHERE A.ACIOGB = '2' "
                               "     AND A.ICUST = '" + str(iCust) + "'"
                               "     AND A.CRE_USER = '" + str(creUser) + "'"
                               "     UNION ALL "
                               "     SELECT A.ACIOGB, A.IODATE, 0 AS IN_ACAMTS, A.ACAMTS AS OUT_ACAMTS, A.ACCUST, B.CUST_NME"
                               "            , A.ACACNUMBER, C.ACNUM_NAME, A.MCODE, A.FIN_OPT, D.MCODENM, A.ACTITLE, A.ACSEQN"
                               "            , A.ACODE, E.RESNAM AS ACODENM, F.GBN, G.RESNAM AS GBNNM, C.ACBKCD, H.RESNAM AS BANKNM, A.APPLYDT, A.ACGUBN, A.MID_OPT, A.ACUSE "
                               "            , IFNULL((SELECT X.EMP_NME FROM OSSIGN Y "
                               "                LEFT OUTER JOIN PIS1TB001 X ON Y.EMP_NBR = X.EMP_NBR "
                               "                WHERE Y.ICUST = A.ICUST AND Y.ACDATE = A.IODATE AND Y.ACSEQN = A.ACSEQN AND Y.ACIOGB = A.ACIOGB "
                               "                AND Y.SEQ = (SELECT IFNULL(MAX(SEQ), '') FROM OSSIGN WHERE ICUST = A.ICUST AND ACDATE = A.IODATE AND ACSEQN = A.ACSEQN AND ACIOGB = A.ACIOGB AND OPT = 'Y')), '') AS NME "
                               "     FROM SISACCTT A "
                               "     LEFT OUTER JOIN MIS1TB003 B "
                               "     ON A.ACCUST = B.CUST_NBR "
                               "     LEFT OUTER JOIN ACNUMBER C "
                               "     ON A.ACACNUMBER = C.ACNUMBER "
                               "     LEFT OUTER JOIN OSCODEM D "
                               "     ON A.MCODE = D.MCODE "
                               "    LEFT OUTER JOIN OSREFCP E "
                               "    ON A.ACODE = E.RESKEY "
                               "    AND E.RECODE = 'ACD' "
                               "    LEFT OUTER JOIN OSCODEM F "
                               "    ON A.MCODE = F.MCODE "
                               "    LEFT OUTER JOIN OSREFCP G "
                               "    ON F.GBN = G.RESKEY "
                               "    AND G.RECODE = 'CGB' "
                               "    LEFT OUTER JOIN OSREFCP H"
                               "    ON C.ACBKCD = H.RESKEY"
                               "    AND H.RECODE = 'BNK'"
                               "     WHERE A.ACIOGB = '1' "
                               "     AND A.ICUST = '" + str(iCust) + "'"
                               "     AND A.CRE_USER = '" + str(creUser) + "'"
                               " ) AA "
                               " WHERE AA.IODATE BETWEEN '" + strDate + "' AND '" + endDate + "' "
                               " AND AA.ACACNUMBER = '" + str(cboAct) + "' "
                               " AND AA.ACCUST = '" + str(cboCust) + "' "
                               " ORDER BY AA.IODATE ")
                mainresult = cursor.fetchall()

            return JsonResponse({'balList': balresult, 'mainList': mainresult})

    else:
        balresult = ''
        with connection.cursor() as cursor:
            cursor.execute("  SELECT IFNULL(AA.ACIOGB, ''), IFNULL(AA.IODATE, ''), IFNULL(AA.IN_ACAMTS, 0), IFNULL(AA.OUT_ACAMTS, 0)"
                           "        , IFNULL(AA.ACCUST, ''), IFNULL(AA.CUST_NME, ''), IFNULL(AA.ACACNUMBER, ''), IFNULL(AA.ACNUM_NAME, '')"
                           "        , IFNULL(AA.MCODE, ''), IFNULL(AA.FIN_OPT, ''), IFNULL(AA.MCODENM, ''), IFNULL(AA.ACTITLE, '')"
                           "        , IFNULL(AA.ACSEQN, ''), IFNULL(AA.ACODE, ''), IFNULL(AA.ACODENM, ''), IFNULL(AA.GBN, '')"
                           "        , IFNULL(AA.GBNNM, '') , IFNULL(AA.APPLYDT, ''), IFNULL(AA.ACGUBN, ''), IFNULL(AA.GBN, '')"
                           "        , IFNULL(AA.FIN_OPT, ''), IFNULL(AA.MID_OPT, ''), IFNULL(AA.ACUSE, ''), IFNULL(AA.ACGUBN, ''), IFNULL(AA.NME, '') FROM "
                           " ( "
                           "     SELECT A.ACIOGB, A.IODATE, A.ACAMTS AS IN_ACAMTS, 0 AS OUT_ACAMTS, A.ACCUST, B.CUST_NME"
                           "            , A.ACACNUMBER, C.ACNUM_NAME, A.MCODE, A.FIN_OPT, D.MCODENM, A.ACTITLE, A.ACSEQN"
                           "            , A.ACODE, E.RESNAM AS ACODENM, F.GBN, G.RESNAM AS GBNNM, A.APPLYDT, A.ACGUBN, A.MID_OPT, A.ACUSE "
                           "            , IFNULL((SELECT X.EMP_NME FROM OSSIGN Y "
                           "                LEFT OUTER JOIN PIS1TB001 X ON Y.EMP_NBR = X.EMP_NBR "
                           "                WHERE Y.ICUST = A.ICUST AND Y.ACDATE = A.IODATE AND Y.ACSEQN = A.ACSEQN AND Y.ACIOGB = A.ACIOGB "
                           "                AND Y.SEQ = (SELECT IFNULL(MAX(SEQ), '') FROM OSSIGN WHERE ICUST = A.ICUST AND ACDATE = A.IODATE AND ACSEQN = A.ACSEQN AND ACIOGB = A.ACIOGB AND OPT = 'Y')), '') AS NME "
                           "     FROM SISACCTT A "
                           "     LEFT OUTER JOIN MIS1TB003 B "
                           "     ON A.ACCUST = B.CUST_NBR "
                           "     LEFT OUTER JOIN ACNUMBER C "
                           "     ON A.ACACNUMBER = C.ACNUMBER "
                           "     LEFT OUTER JOIN OSCODEM D "
                           "     ON A.MCODE = D.MCODE "
                           "    LEFT OUTER JOIN OSREFCP E "
                           "    ON A.ACODE = E.RESKEY "
                           "    AND E.RECODE = 'ACD' "
                           "    LEFT OUTER JOIN OSCODEM F "
                           "    ON A.MCODE = F.MCODE "
                           "    LEFT OUTER JOIN OSREFCP G "
                           "    ON F.GBN = G.RESKEY "
                           "    AND G.RECODE = 'CGB' "
                           "     WHERE A.ACIOGB = '2' "
                           "     AND A.ICUST = '" + str(iCust) + "'"
                           "     AND A.CRE_USER = '" + str(creUser) + "'"
                           "     UNION ALL "
                           "     SELECT A.ACIOGB, A.IODATE, 0 AS IN_ACAMTS, A.ACAMTS AS OUT_ACAMTS, A.ACCUST, B.CUST_NME"
                           "            , A.ACACNUMBER, C.ACNUM_NAME, A.MCODE, A.FIN_OPT, D.MCODENM, A.ACTITLE, A.ACSEQN"
                           "            , A.ACODE, E.RESNAM AS ACODENM, F.GBN, G.RESNAM AS GBNNM, A.APPLYDT, A.ACGUBN, A.MID_OPT, A.ACUSE "
                           "            , IFNULL((SELECT X.EMP_NME FROM OSSIGN Y "
                           "                LEFT OUTER JOIN PIS1TB001 X ON Y.EMP_NBR = X.EMP_NBR "
                           "                WHERE Y.ICUST = A.ICUST AND Y.ACDATE = A.IODATE AND Y.ACSEQN = A.ACSEQN AND Y.ACIOGB = A.ACIOGB "
                           "                AND Y.SEQ = (SELECT IFNULL(MAX(SEQ), '') FROM OSSIGN WHERE ICUST = A.ICUST AND ACDATE = A.IODATE AND ACSEQN = A.ACSEQN AND ACIOGB = A.ACIOGB AND OPT = 'Y')), '') AS NME "
                           "     FROM SISACCTT A "
                           "     LEFT OUTER JOIN MIS1TB003 B "
                           "     ON A.ACCUST = B.CUST_NBR "
                           "     LEFT OUTER JOIN ACNUMBER C "
                           "     ON A.ACACNUMBER = C.ACNUMBER "
                           "     LEFT OUTER JOIN OSCODEM D "
                           "     ON A.MCODE = D.MCODE "
                           "    LEFT OUTER JOIN OSREFCP E "
                           "    ON A.ACODE = E.RESKEY "
                           "    AND E.RECODE = 'ACD' "
                           "    LEFT OUTER JOIN OSCODEM F "
                           "    ON A.MCODE = F.MCODE "
                           "    LEFT OUTER JOIN OSREFCP G "
                           "    ON F.GBN = G.RESKEY "
                           "    AND G.RECODE = 'CGB' "
                           "     WHERE A.ACIOGB = '1' "
                           "     AND A.ICUST = '" + str(iCust) + "'"
                           "     AND A.CRE_USER = '" + str(creUser) + "'"
                           " ) AA "
                           " WHERE AA.IODATE BETWEEN '" + str(strDate ) + "' AND '" + str(endDate) + "' "
                           " ORDER BY AA.IODATE ")
            mainresult = cursor.fetchall()

        return JsonResponse({'balList': balresult, 'mainList': mainresult})


def apvLine_modal_search(request):
    empList = json.loads(request.POST.get('empList'))
    cboDpt = request.POST.get('cboDpt')
    # ioDate = request.POST.get('ioDate').replace("-", "")
    # acIogb = request.POST.get('acIogb')
    # acSeq = request.POST.get('acSeq')
    # mCode = request.POST.get('mCode')
    creUser = request.session.get("userId")
    iCust = request.session.get("USER_ICUST")

    if empList:
        for emp in empList:
            acc_split_list = emp.split(',')
            with connection.cursor() as cursor:
                cursor.execute(" SELECT IFNULL(EMP_DEPT, ''), IFNULL(EMP_GBN, ''), IFNULL(EMP_NBR, ''), IFNULL(EMP_NME, '') "
                               " FROM PIS1TB001 "
                               " WHERE EMP_DEPT = '" + acc_split_list[0] + "' AND EMP_GBN = '" + acc_split_list[1] + "' "
                               " AND EMP_NBR = '" + acc_split_list[2] + "' AND ICUST = '" + iCust + "' ")
                subresult = cursor.fetchall()

                return JsonResponse({'subList': subresult})

    if cboDpt:
        with connection.cursor() as cursor:
            cursor.execute(" SELECT IFNULL(A.EMP_DEPT, ''), IFNULL(B.RESNAM, ''), IFNULL(A.EMP_GBN, '')"
                           "        , IFNULL(C.RESNAM, ''), IFNULL(A.EMP_NBR, ''), IFNULL(A.EMP_NME, '') "
                           " FROM PIS1TB001 A "
                           " LEFT OUTER JOIN OSREFCP B "
                           " ON A.EMP_DEPT = B.RESKEY "
                           " AND B.RECODE = 'DPT' "
                           " LEFT OUTER JOIN OSREFCP C "
                           " ON A.EMP_GBN = C.RESKEY "
                           " AND C.RECODE = 'JJO' "
                           " WHERE A.ICUST = '" + str(iCust) + "'"
                           " AND A.EMP_DEPT = '" + str(cboDpt) + "' "
                           " AND A.EMP_NBR != '" + str(creUser) + "' ")
            mainresult = cursor.fetchall()

            return JsonResponse({'mainList': mainresult})

    else:
        with connection.cursor() as cursor:
            cursor.execute(" SELECT IFNULL(A.EMP_DEPT, ''), IFNULL(B.RESNAM, ''), IFNULL(A.EMP_GBN, '')"
                           "        , IFNULL(C.RESNAM, ''), IFNULL(A.EMP_NBR, ''), IFNULL(A.EMP_NME, '') "
                           " FROM PIS1TB001 A "
                           " LEFT OUTER JOIN OSREFCP B "
                           " ON A.EMP_DEPT = B.RESKEY "
                           " AND B.RECODE = 'DPT' "
                           " LEFT OUTER JOIN OSREFCP C "
                           " ON A.EMP_GBN = C.RESKEY "
                           " AND C.RECODE = 'JJO' "
                           " WHERE A.EMP_NBR != '" + str(creUser) + "' "
                           "   AND A.ICUST = '" + str(iCust) + "' ")
            mainresult = cursor.fetchall()
            print(mainresult)

            with connection.cursor() as cursor:
                cursor.execute(" SELECT RESKEY, RESNAM FROM OSREFCP WHERE RECODE = 'DPT' AND ICUST = '" + iCust + "' ORDER BY RESKEY ")
                cboDpt = cursor.fetchall()

            return JsonResponse({'mainList': mainresult, "cboDpt": cboDpt})

# def apvLine_modal_save(request):
#     empArray = json.loads(request.POST.get('empArrList'))
#
#     empArrayLists = list(filter(len, empArray))
#     for data in range(len(empArrayLists)):
#         with connection.cursor() as cursor:
#             cursor.execute("SELECT SEQ FROM tmpsign WHERE EMP_GBN = '" + empArrayLists[data]["fixCode"] + "' AND EMP_NBR = '" + empArrayLists[data]["empNbr"] + "' ")
#             empresult = cursor.fetchall()
#
#             if empresult:
#                 seq = empresult[0][0]
#
#                 with connection.cursor() as cursor:
#                     cursor.execute(" UPDATE tmpsign SET "
#                                     "   EMP_DPT = '" + empArrayLists[data]["empDpt"] + "' "
#                                     " , EMP_GBN = '" + empArrayLists[data]["empGbn"] + "' "
#                                     " , EMP_NBR = '" + empArrayLists[data]["empNbr"] + "' "
#                                     " , EMP_NME = '" + empArrayLists[data]["empNme"] + "' "
#                                     " WHERE SEQ = '" + seq + "' ")
#                     connection.commit()
#
#             else:
#                 with connection.cursor() as cursor:
#                     cursor.execute(" INSERT INTO tmpsign "
#                                   " ( "
#                                   "   SEQ "
#                                   " , EMP_DPT "
#                                   " , EMP_GBN "
#                                   " , EMP_NBR "
#                                   " , EMP_NME "
#                                   " ) "
#                                   "  VALUES "
#                                   " ( "
#                                   "  (SELECT IFNULL (LPAD(MAX(A.SEQ + 1), '4', '0'), 0001) AS COUNTED FROM tmpsign A) "
#                                   " ,'" + empArrayLists[data]["empDpt"] + "' "
#                                   " ,'" + empArrayLists[data]["empGbn"] + "' "
#                                   " ,'" + empArrayLists[data]["empNbr"] + "' "
#                                   " ,'" + empArrayLists[data]["empNme"] + "' "
#                                   " ) "
#                                   )
#                     connection.commit()
#
#     with connection.cursor() as cursor:
#         cursor.execute("SELECT SEQ, EMP_DPT, EMP_GBN, EMP_NBR, EMP_NME FROM tmpsign ORDER BY SEQ ASC ")
#         empresult = cursor.fetchall()
#
#     return JsonResponse({'arrList': "Y", 'empList': empresult})

def chkWriter(request):
    acIogb = request.POST.get('acIogb')
    ioDate = request.POST.get('ioDate')
    acMcode = request.POST.get('acMcode')
    cboGbn = request.POST.get('cboGbn')
    acSeqn = request.POST.get("acSeqn")
    creUser = request.session.get("userId")
    iCust = request.session.get("USER_ICUST")

    # 은행명
    with connection.cursor() as cursor:
        cursor.execute(" SELECT * FROM SISACCTT WHERE IODATE = '" + str(ioDate) + "' AND ACIOGB = '" + str(acIogb) + "' AND ACSEQN = '" + str(acSeqn) + "' "
                       "                        AND MCODE = '" + str(acMcode) + "' AND CRE_USER = '" + str(creUser) + "' AND ICUST = '" + str(iCust) + "' ")
        chkEmp = cursor.fetchall()

    with connection.cursor() as cursor:
        cursor.execute(" SELECT ACGUBN FROM SISACCTT WHERE IODATE = '" + str(ioDate) + "' AND ACIOGB = '" + str(acIogb) + "' AND ACSEQN = '" + str(acSeqn) + "' "
                       "                        AND MCODE = '" + str(acMcode) + "' AND ICUST = '" + str(iCust) + "' ")
        chkAcGbn = cursor.fetchall()

    return JsonResponse({'chkEmp': chkEmp, "chkAcGbn": chkAcGbn})



def cboList(request):
    gbn = request.POST.get("gbn")
    creUser = request.session.get("userId")
    iCust = request.session.get("USER_ICUST")

    # 거래처
    if gbn != '':
        if gbn == '1':
            with connection.cursor() as cursor:
                cursor.execute(
                    " SELECT CUST_NBR, CUST_NME FROM MIS1TB003 WHERE ICUST = '" + str(iCust) + "' AND CUST_GBN = '1' OR CUST_GBN = '3' ")
                cboCust = cursor.fetchall()

            with connection.cursor() as cursor:
                cursor.execute(
                    " SELECT MCODE, MCODENM FROM OSCODEM WHERE ICUST = '" + str(iCust) + "' AND MCODE LIKE '5%' ORDER BY MCODE ASC ")
                cboMCode = cursor.fetchall()

        if gbn == '2':
            with connection.cursor() as cursor:
                cursor.execute(
                    " SELECT CUST_NBR, CUST_NME FROM MIS1TB003 WHERE ICUST = '" + str(iCust) + "' AND CUST_GBN = '1' OR CUST_GBN = '3' ")
                cboCust = cursor.fetchall()

            with connection.cursor() as cursor:
                cursor.execute(
                    " SELECT MCODE, MCODENM FROM OSCODEM WHERE ICUST = '" + str(iCust) + "' AND MCODE LIKE '4%' ORDER BY MCODE ASC ")
                cboMCode = cursor.fetchall()

        # 결제방법
        with connection.cursor() as cursor:
            cursor.execute(" SELECT RESKEY, RESNAM FROM OSREFCP WHERE RECODE = 'PGB' AND ICUST = '" + str(
                iCust) + "' ORDER BY RESKEY ")
            cboPay = cursor.fetchall()

        # 계좌번호
        with connection.cursor() as cursor:
            cursor.execute(" SELECT ACNUMBER FROM ACNUMBER WHERE ICUST = '" + str(iCust) + "' ")
            cboAcnumber = cursor.fetchall()

        # 카드번호
        with connection.cursor() as cursor:
            cursor.execute(" SELECT CARDNUM FROM ACCARD WHERE ICUST = '" + str(iCust) + "' ")
            cboCard = cursor.fetchall()

        # 은행명
        with connection.cursor() as cursor:
            cursor.execute(
                " SELECT A.ACBKCD, B.RESNAM FROM ACNUMBER A LEFT OUTER JOIN OSREFCP B ON A.ACBKCD = B.RESKEY AND B.RECODE = 'BNK' AND A.ICUST = '" + str(
                    iCust) + "' GROUP BY A.ACBKCD, B.RESNAM ORDER BY A.ACBKCD ")
            cboBank = cursor.fetchall()

        # 입출금구분
        with connection.cursor() as cursor:
            cursor.execute(" SELECT RESKEY, RESNAM FROM OSREFCP WHERE RECODE = 'OUA' AND ICUST = '" + str(
                iCust) + "' ORDER BY RESKEY ")
            cboGgn = cursor.fetchall()

        # 카드명
        with connection.cursor() as cursor:
            cursor.execute(" SELECT RESKEY, RESNAM FROM OSREFCP WHERE RECODE = 'COC' AND ICUST = '" + str(iCust) + "' ")
            cardName = cursor.fetchall()

            return JsonResponse({'cboCust': cboCust, 'cboGgn': cboGgn, 'cboMCode': cboMCode, 'cboPay': cboPay,
                                 'cboAcnumber': cboAcnumber, 'cboCard': cboCard,
                                 "cboBank": cboBank, "cardName": cardName})
    # 회계게정
    # with connection.cursor() as cursor:
    #     cursor.execute(" SELECT ACODE, ACODENM FROM OSCODEA WHERE ICUST = '" + iCust + "' ORDER BY ACODE ASC ")
    #     cboACode = cursor.fetchall()

    if gbn == '':
        # 결제방법
        with connection.cursor() as cursor:
            cursor.execute(" SELECT RESKEY, RESNAM FROM OSREFCP WHERE RECODE = 'PGB' AND ICUST = '" + str(iCust) + "' ORDER BY RESKEY ")
            cboPay = cursor.fetchall()

        # 계좌번호
        with connection.cursor() as cursor:
            cursor.execute(" SELECT ACNUMBER FROM ACNUMBER WHERE ICUST = '" + str(iCust) + "' ")
            cboAcnumber = cursor.fetchall()

        # 카드번호
        with connection.cursor() as cursor:
            cursor.execute(" SELECT CARDNUM FROM ACCARD WHERE ICUST = '" + str(iCust) + "' ")
            cboCard = cursor.fetchall()

        # 은행명
        with connection.cursor() as cursor:
            cursor.execute(
                " SELECT A.ACBKCD, B.RESNAM FROM ACNUMBER A LEFT OUTER JOIN OSREFCP B ON A.ACBKCD = B.RESKEY AND B.RECODE = 'BNK' AND A.ICUST = '" + str(iCust) + "' GROUP BY A.ACBKCD, B.RESNAM ORDER BY A.ACBKCD ")
            cboBank = cursor.fetchall()

        # 카드명
        with connection.cursor() as cursor:
            cursor.execute(" SELECT RESKEY, RESNAM FROM OSREFCP WHERE RECODE = 'COC' AND ICUST = '" + str(iCust) + "' ")
            cardName = cursor.fetchall()

            return JsonResponse({'cboPay': cboPay, 'cboAcnumber': cboAcnumber, 'cboCard': cboCard,
                                 "cboBank": cboBank, "cardName": cardName})




def paymentViews_search(request):
    acIogb = request.POST.get('acIogb')
    ioDate = request.POST.get('ioDate')
    acNum = request.POST.get('acNum')
    acCust = request.POST.get('acCust')
    acMcode = request.POST.get('acMcode')
    cboGbn = request.POST.get('cboGbn')
    cboCard = request.POST.get('cboCard')
    acSeqn = request.POST.get("acSeqn")
    creUser = request.session.get("userId")
    iCust = request.session.get("USER_ICUST")

    if cboCard:
        # 거래처
        with connection.cursor() as cursor:
            cursor.execute(" SELECT ACNUMBER, CARDNUM FROM ACCARD WHERE CARDNUM = '" + str(cboCard) + "' AND ICUST = '" + str(iCust) + "' ")
            cboActNum = cursor.fetchall()

        # 카드
        with connection.cursor() as cursor:
            cursor.execute(" SELECT ACPAYDTE FROM ACCARD WHERE CARDNUM = '" + str(cboCard) + "' AND ICUST = '" + str(iCust) + "' ")
            cboCard = cursor.fetchall()

        # 은행명
        with connection.cursor() as cursor:
            cursor.execute(" SELECT A.ACBKCD, B.RESNAM FROM ACNUMBER A LEFT OUTER JOIN OSREFCP B ON A.ACBKCD = B.RESKEY AND B.RECODE = 'BNK' AND A.ICUST = '" + str(iCust) + "' GROUP BY A.ACBKCD, B.RESNAM ORDER BY A.ACBKCD ")
            cboBank = cursor.fetchall()

        return JsonResponse({'cboActNum': cboActNum, "cboCard": cboCard, "cboBank": cboBank})

    if acIogb != '' and acCust == '':
        with connection.cursor() as cursor:
            # 거래처구분/명/행/결제방법명/결제방법코드/입출금구분/계정/금액/순번/날짜/계좌번호
            cursor.execute(" SELECT IFNULL(A.ACSEQN,''), IFNULL(A.ACCUST, ''), IFNULL(B.CUST_NME, '') "
                           "    , IFNULL(A.ACRECN,''), IFNULL(A.ACGUBN,''), IFNULL(C.RESNAM,'') "
                           "    , IFNULL(A.ACIOGB,''), IFNULL(E.RESNAM, ''), IFNULL(A.MCODE,''), IFNULL(D.MCODENM, '') "
                           "    , IFNULL(A.ACAMTS, 0), IFNULL(A.IODATE,''), IFNULL(A.ACACNUMBER,'') "
                           "    , IFNULL(A.ACGUNO_BK,''), IFNULL(F.RESNAM, '') , IFNULL(A.ACBUNHO,''), IFNULL(A.ACGUNO_DT,'')"
                           "    , IFNULL(A.ACODE,''), IFNULL(G.RESNAM, ''), IFNULL(A.ACDESC, ''), IFNULL(A.EXDATE,''), IFNULL(A.ACTITLE,'')"
                           "    , IFNULL(A.ACCARD, ''), IFNULL(A.FIN_OPT, ''), IFNULL(A.ACUSE, ''), IFNULL(A.ACINFO, ''), IFNULL(H.ACBKCD, '')"
                           "    , IFNULL(A.APPLYDT, ''), IFNULL(A.CRE_USER, ''), IFNULL(I.EMP_CLS, ''), IFNULL(A.ACINFO, ''), IFNULL(J.CARDTYPE, '')"
                           "    , IFNULL(J.GBN, ''), IFNULL(I.EMP_NME,''), IFNULL(A.ACDATE, ''), IFNULL(A.MID_OPT, ''), IFNULL(A.PRE_PAY, ''), IFNULL(A.MID_OPT_GBN, '')   "
                           "    , IFNULL(A.ACFOLDER, ''), IFNULL(A.ACFOLDER2,''), IFNULL(A.ACFOLDER3, ''), IFNULL(A.ACFOLDER4, ''), IFNULL(A.ACFOLDER5, '')   "
                           "    FROM SISACCTT A "
                           "    LEFT OUTER JOIN MIS1TB003 B "
                           "    ON A.ACCUST = B.CUST_NBR "
                           "    LEFT OUTER JOIN OSREFCP C "
                           "    ON A.ACGUBN = C.RESKEY "
                           "    AND C.RECODE = 'OUB' "
                           "    LEFT OUTER JOIN OSCODEM D "
                           "    ON A.MCODE = D.MCODE "
                           "    LEFT OUTER JOIN OSREFCP G "
                           "    ON A.ACODE = G.RESKEY "
                           "    AND G.RECODE = 'ACD' "
                           "    LEFT OUTER JOIN OSREFCP E "
                           "    ON A.ACIOGB = E.RESKEY "
                           "    AND E.RECODE = 'OUA' "
                           "    LEFT OUTER JOIN OSREFCP F "
                           "    ON A.ACGUNO_BK = F.RESKEY "
                           "    AND F.RECODE = 'BNK' "
                           "    LEFT OUTER JOIN ACNUMBER H "
                           "    ON A.ACACNUMBER = H.ACNUMBER "
                           "    LEFT OUTER JOIN PIS1TB001 I "
                           "    ON A.CRE_USER = I.EMP_NBR "
                           "    LEFT OUTER JOIN ACCARD J "
                           "    ON A.ACCARD = J.CARDNUM "
                           "    WHERE A.IODATE = '" + str(ioDate) + "' "
                           "    AND A.ACIOGB = '" + str(acIogb) + "' "
                           "    AND A.ACSEQN = '" + str(acSeqn) + "'"
                           "    AND A.ICUST = '" + str(iCust) + "'")
            subresult = cursor.fetchall()

        with connection.cursor() as cursor:
            cursor.execute(" SELECT A.SEQ, A.EMP_NBR, B.EMP_NME, B.EMP_FOLDER, A.ACDATE, A.ACSEQN, A.ACIOGB, A.OPT "
                           " FROM OSSIGN A "
                           " LEFT OUTER JOIN PIS1TB001 B "
                           " ON A.EMP_NBR = B.EMP_NBR "
                           " WHERE A.ACDATE = '" + str(ioDate) + "' "
                           " AND A.ACSEQN = '" + str(acSeqn) + "' "
                           " AND A.ACIOGB = '" + str(acIogb) + "' "
                           " AND A.ICUST = '" + str(iCust) + "' "
                           " ORDER BY SEQ ASC ")
            empresult = cursor.fetchall()
        # 결재할사람
        with connection.cursor() as cursor:
            cursor.execute(" SELECT A.SEQ, A.EMP_NBR, B.EMP_NME FROM OSSIGN A "
                           " LEFT OUTER JOIN PIS1TB001 B ON A.EMP_NBR = B.EMP_NBR"
                           " WHERE A.ACDATE = '" + str(ioDate) + "' AND A.ACIOGB = '" + str(acIogb) + "' "
                           "   AND A.ACSEQN = '" + str(acSeqn) + "' AND A.ICUST = '" + str(iCust) + "'  ")
            permit = cursor.fetchall()

        # 결재한건
        with connection.cursor() as cursor:
            cursor.execute(" SELECT COUNT(*) FROM OSSIGN "
                           " WHERE ACDATE = '" + str(ioDate) + "' AND ACIOGB = '" + str(acIogb) + "' "
                           " AND ACSEQN = '" + str(acSeqn) + "' AND ICUST = '" + str(iCust) + "' AND OPT = 'Y' ")
            chkApv = cursor.fetchall()

        # 거래처
        if acCust == '':
            custGbn = subresult[0][6]
            # 매입처
            if custGbn == '1':
                with connection.cursor() as cursor:
                    cursor.execute(" SELECT CUST_NBR, CUST_NME FROM MIS1TB003 WHERE ICUST = '" + str(iCust) + "' AND CUST_GBN = '1' OR CUST_GBN = '3' ")
                    cboCust = cursor.fetchall()
            # 매출처
            if custGbn == '2':
                with connection.cursor() as cursor:
                    cursor.execute(" SELECT CUST_NBR, CUST_NME FROM MIS1TB003 WHERE ICUST = '" + str(iCust) + "' AND CUST_GBN = '2' OR CUST_GBN = '3' ")
                    cboCust = cursor.fetchall()
            else:
                with connection.cursor() as cursor:
                    cursor.execute(" SELECT CUST_NBR, CUST_NME FROM MIS1TB003 WHERE ICUST = '" + str(iCust) + "' ")
                    cboCust = cursor.fetchall()

        # 입출금구분
        with connection.cursor() as cursor:
            cursor.execute(" SELECT RESKEY, RESNAM FROM OSREFCP WHERE RECODE = 'OUA' AND ICUST = '" + str(iCust) + "' ORDER BY RESKEY ")
            cboGgn = cursor.fetchall()

        # 관리계정
        with connection.cursor() as cursor:
            cursor.execute(" SELECT MCODE, MCODENM FROM OSCODEM WHERE ICUST = '" + str(iCust) + "' ORDER BY MCODE ASC ")
            cboMCode = cursor.fetchall()

        # 회계게정
        # with connection.cursor() as cursor:
        #     cursor.execute(" SELECT ACODE, ACODENM FROM OSCODEA WHERE ICUST = '" + iCust + "' ORDER BY ACODE ASC ")
        #     cboACode = cursor.fetchall()

        # 결제방법
        with connection.cursor() as cursor:
            cursor.execute(" SELECT RESKEY, RESNAM FROM OSREFCP WHERE RECODE = 'PGB' AND ICUST = '" + str(iCust) + "' ORDER BY RESKEY ")
            cboPay = cursor.fetchall()

        # 계좌번호
        if subresult[0][32] != '':
            gbn = subresult[0][32]
            with connection.cursor() as cursor:
                cursor.execute(" SELECT ACNUMBER FROM ACCARD WHERE ICUST = '" + str(iCust) + "' AND GBN = '" + str(gbn) + "' ")
                cboAcnumber = cursor.fetchall()
        else:
            with connection.cursor() as cursor:
                cursor.execute(" SELECT ACNUMBER FROM ACNUMBER WHERE ICUST = '" + str(iCust) + "' ")
                cboAcnumber = cursor.fetchall()

        # 카드번호
        if subresult[0][32] != '':
            gbn = subresult[0][32]
            with connection.cursor() as cursor:
                cursor.execute(" SELECT CARDNUM FROM ACCARD WHERE ICUST = '" + str(iCust) + "' AND GBN = '" + str(gbn) + "' ")
                cboCard = cursor.fetchall()
        else:
            with connection.cursor() as cursor:
                cursor.execute(" SELECT CARDNUM FROM ACCARD WHERE ICUST = '" + str(iCust) + "' ")
                cboCard = cursor.fetchall()

        # 은행명
        with connection.cursor() as cursor:
            cursor.execute(" SELECT A.ACBKCD, B.RESNAM FROM ACNUMBER A LEFT OUTER JOIN OSREFCP B ON A.ACBKCD = B.RESKEY AND B.RECODE = 'BNK' AND A.ICUST = '" + str(iCust) + "' GROUP BY A.ACBKCD, B.RESNAM ORDER BY A.ACBKCD ")
            cboBank = cursor.fetchall()

        # 카드명
        if subresult[0][32] != '':
            gbn = subresult[0][32]
            with connection.cursor() as cursor:
                cursor.execute("  SELECT A.CARDTYPE, B.RESNAM FROM ACCARD A LEFT OUTER JOIN OSREFCP B "
                                " ON A.CARDTYPE = B.RESKEY "
                                " AND B.RECODE = 'COC' "
                                " WHERE A.ICUST = '" + str(iCust) + "' AND A.GBN = '" + str(gbn) + "' ")
            cardName = cursor.fetchall()
        else:
            with connection.cursor() as cursor:
                cursor.execute(
                    " SELECT RESKEY, RESNAM FROM OSREFCP WHERE RECODE = 'COC' AND ICUST = '" + str(iCust) + "' ")
            cardName = cursor.fetchall()

        return JsonResponse({'subList': subresult, 'permit': permit, 'cboCust': cboCust, 'cboGgn': cboGgn
                                , 'cboMCode': cboMCode, 'cboPay': cboPay, 'cboAcnumber': cboAcnumber
                                , 'cboCard': cboCard, "cboBank": cboBank, "cardName": cardName, "chkApv": chkApv, 'empResult': empresult})

    if acIogb != '' and acCust != '':
        with connection.cursor() as cursor:
            # 거래처구분/명/행/결제방법명/결제방법코드/입출금구분/계정/금액/순번/날짜/계좌번호
            cursor.execute(" SELECT IFNULL(A.ACSEQN,''), IFNULL(A.ACCUST, ''), IFNULL(B.CUST_NME, '') "
                           "    , IFNULL(A.ACRECN,''), IFNULL(A.ACGUBN,''), IFNULL(C.RESNAM,'') "
                           "    , IFNULL(A.ACIOGB,''), IFNULL(E.RESNAM, ''), IFNULL(A.MCODE,''), IFNULL(D.MCODENM, '') "
                           "    , IFNULL(A.ACAMTS, 0), IFNULL(A.IODATE,''), IFNULL(A.ACACNUMBER,'') "
                           "    , IFNULL(A.ACGUNO_BK,''), IFNULL(F.RESNAM, '') , IFNULL(A.ACBUNHO,''), IFNULL(A.ACGUNO_DT,'')"
                           "    , IFNULL(A.ACODE,''), IFNULL(G.RESNAM, ''), IFNULL(A.ACDESC, ''), IFNULL(A.EXDATE,''), IFNULL(A.ACTITLE,'')"
                           "    , IFNULL(A.ACCARD, ''), IFNULL(A.FIN_OPT, ''), IFNULL(A.ACUSE, ''), IFNULL(A.ACINFO, ''), IFNULL(H.ACBKCD, '')"
                           "    , IFNULL(A.APPLYDT, ''), IFNULL(A.CRE_USER, ''), IFNULL(I.EMP_CLS, ''), IFNULL(A.ACINFO, ''), IFNULL(J.CARDTYPE, '')"
                           "    , IFNULL(A.CRE_USER,''), IFNULL(I.EMP_NME,''), IFNULL(A.ACDATE, ''), IFNULL(A.MID_OPT, ''), IFNULL(A.PRE_PAY, ''), IFNULL(A.MID_OPT_GBN, '')  "
                           "    , IFNULL(A.ACFOLDER, ''), IFNULL(A.ACFOLDER2,''), IFNULL(A.ACFOLDER3, ''), IFNULL(A.ACFOLDER4, ''), IFNULL(A.ACFOLDER5, '')   "
                           "    FROM SISACCTT A "
                           "    LEFT OUTER JOIN MIS1TB003 B "
                           "    ON A.ACCUST = B.CUST_NBR "
                           "    LEFT OUTER JOIN OSREFCP C "
                           "    ON A.ACGUBN = C.RESKEY "
                           "    AND C.RECODE = 'OUB' "
                           "    LEFT OUTER JOIN OSCODEM D "
                           "    ON A.MCODE = D.MCODE "
                           "    LEFT OUTER JOIN OSREFCP G "
                           "    ON A.ACODE = G.RESKEY "
                           "    AND G.RECODE = 'ACD' "
                           "    LEFT OUTER JOIN OSREFCP E "
                           "    ON A.ACIOGB = E.RESKEY "
                           "    AND E.RECODE = 'OUA' "
                           "    LEFT OUTER JOIN OSREFCP F "
                           "    ON A.ACGUNO_BK = F.RESKEY "
                           "    AND F.RECODE = 'BNK' "
                           "    LEFT OUTER JOIN ACNUMBER H "
                           "    ON A.ACACNUMBER = H.ACNUMBER "
                           "    LEFT OUTER JOIN PIS1TB001 I "
                           "    ON A.CRE_USER = I.EMP_NBR "
                           "    LEFT OUTER JOIN ACCARD J "
                           "    ON A.ACCARD = J.CARDNUM "
                           "    WHERE A.IODATE = '" + str(ioDate) + "' "
                           "    AND A.ACIOGB = '" + str(acIogb) + "' "
                           "    AND A.ACCUST = '" + str(acCust) + "'"
                           "    AND A.MCODE = '" + str(acMcode) + "' "
                           "    AND A.ACSEQN = '" + str(acSeqn) + "'"
                           "    AND A.ICUST = '" + str(iCust) + "'")
            subresult = cursor.fetchall()

        with connection.cursor() as cursor:
            cursor.execute(" SELECT A.SEQ, A.EMP_NBR, B.EMP_NME, B.EMP_FOLDER, A.ACDATE, A.ACSEQN, A.ACIOGB, A.OPT "
                           " FROM OSSIGN A "
                           " LEFT OUTER JOIN PIS1TB001 B "
                           " ON A.EMP_NBR = B.EMP_NBR "
                           " WHERE A.ACDATE = '" + str(ioDate) + "' "
                           " AND A.ACSEQN = '" + str(acSeqn) + "' "
                           " AND A.ACIOGB = '" + str(acIogb) + "' "
                           " AND A.ICUST = '" + str(iCust) + "' "
                           " ORDER BY SEQ ASC ")
            empresult = cursor.fetchall()

        # 결재할사람
        with connection.cursor() as cursor:
            cursor.execute(" SELECT A.SEQ, A.EMP_NBR, B.EMP_NME FROM OSSIGN A "
                           " LEFT OUTER JOIN PIS1TB001 B ON A.EMP_NBR = B.EMP_NBR"
                           " WHERE A.ACDATE = '" + str(ioDate) + "' AND A.ACIOGB = '" + str(acIogb) + "' "
                           "   AND A.ACSEQN = '" + str(acSeqn) + "' AND A.ICUST = '" + str(iCust) + "' ")
            permit = cursor.fetchall()

        # 결재한건
        with connection.cursor() as cursor:
            cursor.execute(" SELECT COUNT(*) FROM OSSIGN "
                           " WHERE ACDATE = '" + str(ioDate) + "' AND ACIOGB = '" + str(acIogb) + "' "
                           " AND ACSEQN = '" + str(acSeqn) + "' AND ICUST = '" + str(iCust) + "' AND OPT = 'N' ")
            chkApv = cursor.fetchall()

        # 거래처
        with connection.cursor() as cursor:
            cursor.execute(" SELECT CUST_NBR, CUST_NME FROM MIS1TB003 WHERE ICUST = '" + str(iCust) + "' ")
            cboCust = cursor.fetchall()

        # 입출금구분
        with connection.cursor() as cursor:
            cursor.execute(" SELECT RESKEY, RESNAM FROM OSREFCP WHERE RECODE = 'OUA' AND ICUST = '" + str(iCust) + "' ORDER BY RESKEY ")
            cboGgn = cursor.fetchall()

        # 관리계정
        with connection.cursor() as cursor:
            cursor.execute(" SELECT MCODE, MCODENM FROM OSCODEM WHERE ICUST = '" + str(iCust) + "' ORDER BY MCODE ASC ")
            cboMCode = cursor.fetchall()

            # 회계게정
            # with connection.cursor() as cursor:
            #     cursor.execute(" SELECT ACODE, ACODENM FROM OSCODEA WHERE ICUST = '" + iCust + "' ORDER BY ACODE ASC ")
            #     cboACode = cursor.fetchall()

        # 결제방법
        with connection.cursor() as cursor:
            cursor.execute(" SELECT RESKEY, RESNAM FROM OSREFCP WHERE RECODE = 'PGB' AND ICUST = '" + str(iCust) + "' ORDER BY RESKEY ")
            cboPay = cursor.fetchall()

        # 계좌번호
        with connection.cursor() as cursor:
            cursor.execute(" SELECT ACNUMBER FROM ACNUMBER WHERE ICUST = '" + str(iCust) + "' ")
            cboAcnumber = cursor.fetchall()

        # 카드번호
        with connection.cursor() as cursor:
            cursor.execute(" SELECT CARDNUM FROM ACCARD WHERE ICUST = '" + str(iCust) + "' ")
            cboCard = cursor.fetchall()

        # 은행명
        with connection.cursor() as cursor:
            cursor.execute(" SELECT A.ACBKCD, B.RESNAM FROM ACNUMBER A LEFT OUTER JOIN OSREFCP B ON A.ACBKCD = B.RESKEY AND B.RECODE = 'BNK' AND A.ICUST = '" + str(iCust) + "' GROUP BY A.ACBKCD, B.RESNAM ORDER BY A.ACBKCD ")
            cboBank = cursor.fetchall()

        # 카드명
        with connection.cursor() as cursor:
            cursor.execute(
                " SELECT RESKEY, RESNAM FROM OSREFCP WHERE RECODE = 'COC' AND ICUST = '" + str(iCust) + "' ")
            cardName = cursor.fetchall()


        return JsonResponse({'subList': subresult, 'permit': permit, 'cboCust': cboCust, 'cboGgn': cboGgn
                                , 'cboMCode': cboMCode, 'cboPay': cboPay, 'cboAcnumber': cboAcnumber
                                , 'cboCard': cboCard, "cboBank": cboBank, "cardName": cardName, "chkApv": chkApv, 'empResult': empresult})

    # 출금
    if cboGbn == '1':
        # 거래처
        with connection.cursor() as cursor:
            cursor.execute(" SELECT CUST_NBR, CUST_NME FROM MIS1TB003 WHERE ICUST = '" + str(iCust) + "' AND CUST_GBN = '1' OR CUST_GBN = '3'")
            cboCust = cursor.fetchall()

        # 입출금구분
        with connection.cursor() as cursor:
            cursor.execute(" SELECT RESKEY, RESNAM FROM OSREFCP WHERE RECODE = 'OUA' AND ICUST = '" + str(iCust) + "' ORDER BY RESKEY ")
            cboGgn = cursor.fetchall()

        # 관리계정
        with connection.cursor() as cursor:
            cursor.execute(" SELECT MCODE, MCODENM FROM OSCODEM WHERE MCODE LIKE '5%' AND ICUST = '" + str(iCust) + "' ORDER BY MCODE ASC ")
            cboMCode = cursor.fetchall()

        # 결제방법
        with connection.cursor() as cursor:
            cursor.execute(" SELECT RESKEY, RESNAM FROM OSREFCP WHERE RECODE = 'PGB' AND ICUST = '" + str(iCust) + "' ORDER BY RESKEY ")
            cboPay = cursor.fetchall()

        # 계좌번호
        with connection.cursor() as cursor:
            cursor.execute(" SELECT ACNUMBER FROM ACNUMBER WHERE ICUST = '" + str(iCust) + "' ")
            cboAcnumber = cursor.fetchall()

        # 카드번호
        with connection.cursor() as cursor:
            cursor.execute(" SELECT CARDNUM FROM ACCARD WHERE ICUST = '" + str(iCust) + "' ")
            cboCard = cursor.fetchall()

        # 은행명
        with connection.cursor() as cursor:
            cursor.execute(" SELECT A.ACBKCD, B.RESNAM FROM ACNUMBER A LEFT OUTER JOIN OSREFCP B ON A.ACBKCD = B.RESKEY AND B.RECODE = 'BNK' AND A.ICUST = '" + str(iCust) + "' "
                           "    GROUP BY A.ACBKCD, B.RESNAM ORDER BY A.ACBKCD ")
            cboBank = cursor.fetchall()

        # 카드명
        with connection.cursor() as cursor:
            cursor.execute(" SELECT RESKEY, RESNAM FROM OSREFCP WHERE RECODE = 'COC' AND ICUST = '" + str(iCust) + "' ")
            cardName = cursor.fetchall()

        return JsonResponse({'cboCust': cboCust, 'cboGgn': cboGgn, 'cboMCode': cboMCode, 'cboPay': cboPay, 'cboAcnumber': cboAcnumber, 'cboCard': cboCard, "cboBank": cboBank, "cardName": cardName})

    # 입금
    else:
        # 거래처
        with connection.cursor() as cursor:
            cursor.execute(" SELECT CUST_NBR, CUST_NME FROM MIS1TB003 WHERE ICUST = '" + str(iCust) + "' AND CUST_GBN = '2' OR CUST_GBN = '3' ")
            cboCust = cursor.fetchall()

        # 입출금구분
        with connection.cursor() as cursor:
            cursor.execute(" SELECT RESKEY, RESNAM FROM OSREFCP WHERE RECODE = 'OUA' AND ICUST = '" + str(iCust) + "' ORDER BY RESKEY ")
            cboGgn = cursor.fetchall()

        # 관리계정
        with connection.cursor() as cursor:
            cursor.execute(" SELECT MCODE, MCODENM FROM OSCODEM WHERE MCODE LIKE '4%' AND ICUST = '" + str(iCust) + "' ORDER BY MCODE ASC ")
            cboMCode = cursor.fetchall()

        # 결제방법
        with connection.cursor() as cursor:
            cursor.execute(" SELECT RESKEY, RESNAM FROM OSREFCP WHERE RECODE = 'PGB' AND ICUST = '" + str(iCust) + "' ORDER BY RESKEY ")
            cboPay = cursor.fetchall()

        # 계좌번호
        with connection.cursor() as cursor:
            cursor.execute(" SELECT ACNUMBER FROM ACNUMBER WHERE ICUST = '" + str(iCust) + "' ")
            cboAcnumber = cursor.fetchall()

        # 카드번호
        with connection.cursor() as cursor:
            cursor.execute(" SELECT CARDNUM FROM ACCARD WHERE ICUST = '" + str(iCust) + "' ")
            cboCard = cursor.fetchall()

        # 은행명
        with connection.cursor() as cursor:
            cursor.execute(" SELECT A.ACBKCD, B.RESNAM FROM ACNUMBER A LEFT OUTER JOIN OSREFCP B ON A.ACBKCD = B.RESKEY AND B.RECODE = 'BNK' AND A.ICUST = '" + str(iCust) + "' "
                           "    GROUP BY A.ACBKCD, B.RESNAM ORDER BY A.ACBKCD ")
            cboBank = cursor.fetchall()

        # 카드명
        with connection.cursor() as cursor:
            cursor.execute(" SELECT RESKEY, RESNAM FROM OSREFCP WHERE RECODE = 'COC' AND ICUST = '" + str(iCust) + "' ")
            cardName = cursor.fetchall()

        return JsonResponse({'cboCust': cboCust, 'cboGgn': cboGgn, 'cboMCode': cboMCode, 'cboPay': cboPay, 'cboAcnumber': cboAcnumber, 'cboCard': cboCard, "cboBank": cboBank, "cardName": cardName})


def cboCardType_search(request):
    cardType = request.POST.get("cardType")
    cardName = request.POST.get("cardName")
    creUser = request.session.get("userId")
    iCust = request.session.get("USER_ICUST")

    if cardType != '':
        with connection.cursor() as cursor:
            cursor.execute("  SELECT A.CARDTYPE, B.RESNAM FROM ACCARD A LEFT OUTER JOIN OSREFCP B "
                            " ON A.CARDTYPE = B.RESKEY "
                            " AND B.RECODE = 'COC' "
                            " WHERE A.ICUST = '" + str(iCust) + "' AND A.GBN = '" + str(cardType) + "' "
                            " GROUP BY A.CARDTYPE, B.RESNAM ")
            cboCardName = cursor.fetchall()

        with connection.cursor() as cursor:
            cursor.execute(" SELECT CARDNUM FROM ACCARD WHERE GBN = '" + str(cardType) + "' AND ICUST = '" + str(iCust) + "' ")
            cboCardGbn = cursor.fetchall()

        return JsonResponse({"cboCardName": cboCardName, "cboCardGbn": cboCardGbn})

    if cardName != '':
        with connection.cursor() as cursor:
            cursor.execute(" SELECT CARDNUM FROM ACCARD WHERE CARDTYPE = '" + str(cardName) + "' GBN = '" + str(cardType) + "' AND ICUST = '" + str(iCust) + "' ")
            cboCardGbn = cursor.fetchall()

        return JsonResponse({"cboCardGbn": cboCardGbn})


def cboActNum_search(request):
    cboCardName = request.POST.get("cboCardName")
    cboCardType = request.POST.get("cboCardType")
    cboBank = request.POST.get("cboBank")
    card = request.POST.get("card")
    creUser = request.session.get("userId")
    iCust = request.session.get("USER_ICUST")

    if cboCardName:
        with connection.cursor() as cursor:
            cursor.execute(" SELECT CARDNUM FROM ACCARD WHERE GBN = '" + str(cboCardType) + "' AND CARDTYPE = '" + str(cboCardName) + "' AND ICUST = '" + str(iCust) + "' ")
            cboCard = cursor.fetchall()

        return JsonResponse({"cboCard": cboCard})

    if cboBank:
        with connection.cursor() as cursor:
            cursor.execute(" SELECT ACNUMBER FROM ACNUMBER WHERE ACBKCD = '" + str(cboBank) + "' AND ICUST = '" + str(iCust) + "'")
            cboAct = cursor.fetchall()

        return JsonResponse({'cboAct': cboAct})

    if card:
        with connection.cursor() as cursor:
            cursor.execute(" SELECT ACNUMBER FROM ACCARD WHERE CARDNUM = '" + str(card) + "' AND ICUST = '" + str(iCust) + "'")
            cboAct = cursor.fetchall()

        return JsonResponse({'cboAct': cboAct})

    else:
        with connection.cursor() as cursor:
            cursor.execute(" SELECT ACNUMBER FROM ACNUMBER WHERE ICUST = '" + str(iCust) + "'")
            cboAct = cursor.fetchall()

        with connection.cursor() as cursor:
            cursor.execute(" SELECT A.ACBKCD, B.RESNAM FROM ACNUMBER A "
                            " LEFT OUTER JOIN OSREFCP B "
                            " ON A.ACBKCD = B.RESKEY "
                            " AND B.RECODE = 'BNK' "
                            " WHERE A.ICUST = '" + str(iCust) + "' "
                            " GROUP BY A.ACBKCD, B.RESNAM")
            cboBank = cursor.fetchall()

        return JsonResponse({'cboAct': cboAct, 'cboBank': cboBank})

def paymentViews_save(request):
    empArray = json.loads(request.POST.get('empArrList'))
    ioDate = request.POST.get("txtWitRegDate").replace('-', '')
    exDate = request.POST.get("txtExDate").replace('-', '')
    acSeqn = request.POST.get("txtWitSeq")
    acTitle = request.POST.get("txtTitle")
    acRecn = request.POST.get("txtWitRecn")
    acCust = request.POST.get("cboWitCust")     # 거래처
    acIogb = request.POST.get("cboWitGbn")  # 구분(입금2/출금1)
    mCode = request.POST.get("cboAdminCode")  # 관리계정
    # acCode = request.POST.get("cboActCode")  # 회계계정
    acAmts = request.POST.get("txtWitPrice").replace(',', '')      # 금액
    acBank = request.POST.get("cboBank")  # 은행
    acAcnumber = request.POST.get("cboWitActNum")     # 계좌번호
    acGubn = request.POST.get("cboWitMethod")     # 결제방법
    acCard = request.POST.get("cboWitCard")
    acDesc = request.POST.get("txtWitRemark")     # 비고
    acUse = request.POST.get("txtWhere")  # 사용처
    acApply = request.POST.get("txtApplyDate")  # 적용년월
    # prePay = request.POST.get("chkPre")  # 선지급
    creUser = request.session.get("userId")
    iCust = request.session.get("USER_ICUST")
    acDate = request.POST.get("txtExDate").replace('-', '')
    cashDate = request.POST.get("txtCashDate")
    acInfo = request.POST.get("txtInfo")
    # txtCustAct = request.POST.get("txtCustAct")  # 거래처계좌번호
    # 전결처리
    txtApvAll = request.POST.get("txtApvAll")
    midOptGbn = ''
    midOpt = 'N'
    finOpt = 'N'
    # file = request.FILES.get('file')

    # if (file is None):
    #     file = ''
    # url = '/Users/thenaeunsys/Documents/ImportFile/'
    #
    # if file is None or not None:
    #     if len(request.FILES) != 0:
    #         myfile = request.FILES['file']
    #         fs = FileSystemStorage()
    #         filename = fs.save(myfile.name, myfile)
    #         Rfilenameloc = url + filename
    #
    #     else:
    #         Rfilenameloc = file

    # fileOverwriteYn = request.POST.get("fileOverwriteYn")
    #
    # uploaded_file_list = request.FILES.getlist('file')
    # # if uploaded_file is None:
    # #     uploaded_file = ''
    # uploaded_file_full_path = ['', '', '', '', '']
    # if uploaded_file_list:
    #     for i in range(len(uploaded_file_list)):
    #         if i > 4:
    #             break;
    #
    #         uploaded_file = uploaded_file_list[i]
    #         # 원하는 경로 설정, FileResponse
    #         # desired_path = "D:/NE_FTP/MAS_FILES/중요문건"
    #         # desired_path = "D:\\NE_FTP\\MAS_FILES\\"
    #         # desired_path = "D:\\NE_FTP\\MAS_FILES\\UploadFiles\\"
    #         # desired_path = "D:/NE_FTP/MAS_FILES/UploadFiles/"
    #         # desired_path = "/Users/thenaeunsys/Documents/ImportFile/"
    #         # desired_path = "/D:/NE_FTP/사업장/산양화학/Dodument/"
    #
    #
    #         desired_path = "D:/COMPANY/SANYANG/DOCUMENTS/"
    #         # 해당 디렉토리가 없으면 생성
    #         if not os.path.exists(desired_path):
    #             os.makedirs(desired_path)
    #
    #         destination = os.path.join(desired_path, uploaded_file.name)
    #
    #         # 해당 경로에 동일한 이름의 파일이 있다면
    #         if os.path.exists(destination):
    #             if fileOverwriteYn == 'Y':
    #                 os.remove(destination)
    #             else:
    #                 return JsonResponse({'sucYn': 'N', 'message': "same file name exists"})
    #
    #         with open(destination, 'wb+') as destination_file:
    #             for chunk in uploaded_file.chunks():
    #                 destination_file.write(chunk)
    #
    #         uploaded_file_full_path[i] = destination

    fileOverwriteYn = request.POST.get("fileOverwriteYn")

    uploaded_file_1 = request.FILES.get('file1')
    uploaded_file_2 = request.FILES.get('file2')
    uploaded_file_3 = request.FILES.get('file3')
    uploaded_file_4 = request.FILES.get('file4')
    uploaded_file_5 = request.FILES.get('file5')

    file_delete_yn_1 = request.POST.get('file_del_yn1')
    file_delete_yn_2 = request.POST.get('file_del_yn2')
    file_delete_yn_3 = request.POST.get('file_del_yn3')
    file_delete_yn_4 = request.POST.get('file_del_yn4')
    file_delete_yn_5 = request.POST.get('file_del_yn5')

    uploaded_file_list = [uploaded_file_1, uploaded_file_2, uploaded_file_3, uploaded_file_4, uploaded_file_5]
    file_delete_yn_list = [file_delete_yn_1, file_delete_yn_2, file_delete_yn_3, file_delete_yn_4, file_delete_yn_5]

    uploaded_file_path = ['', '', '', '', '']

    for i in range(len(uploaded_file_list)):

        uploaded_file = uploaded_file_list[i]

        # 파일 삭제 여부가 Y인 경우
        if file_delete_yn_list[i] == 'Y':
            # 새로 업로드된 파일이 없는 경우
            if not uploaded_file:
                uploaded_file_path[i] = ''

                # 다음 파일로 넘어감
                continue

            # 새로 업로드된 파일이 있는 경우(새 파일로 덮어쓰기)
            else:
                pass

        elif file_delete_yn_list[i] == 'N':
            # 새로 업로드된 파일이 없는 경우
            if not uploaded_file:
                # 기존 파일을 유지
                uploaded_file_path[i] = 'KEEP FILE'

                # 다음 파일로 넘어감
                continue

            # 새로 업로드된 파일이 있는 경우(새 파일로 덮어쓰기)
            else:
                pass

        # 파일이 없는 경우
        if uploaded_file is None:
            # 다음 파일로 넘어감
            continue

        # 디렉토리가 없으면 생성
        if not os.path.exists(settings.MEDIA_ROOT):
            os.makedirs(settings.MEDIA_ROOT)

        # static/media 하위에 파일 저장을 위한 상대 경로 생성
        relative_path = os.path.join('/static/media/', uploaded_file.name)

        # 실제 파일 시스템에 저장될 전체 경로 생성
        destination = os.path.join(settings.MEDIA_ROOT, uploaded_file.name)

        # 해당 경로에 동일한 이름의 파일이 있다면
        if os.path.exists(destination):
            if fileOverwriteYn == 'Y':
                os.remove(destination)
            else:
                return JsonResponse({'sucYn': 'N', 'message': "same file name exists"})

        with open(destination, 'wb+') as destination_file:
            for chunk in uploaded_file.chunks():
                destination_file.write(chunk)

        uploaded_file_path[i] = relative_path




    if acSeqn:
        # 예정일이 없는경우
        if acDate == '' or acDate is None:
            if exDate != '' or exDate is not None:
                acDate = exDate
            if exDate == '' or exDate is None:
                exDate = ''
                acDate = ioDate
        # 현금결재시 예정일 지정
        if acGubn == '1':
            exDate = cashDate.replace('-', '')
            acDate = cashDate.replace('-', '')
        # 계산서시 거래처 계호
        # if acGubn == '2':
        #     acAcnumber = txtCustAct
        # 전결시(전결구분)
        if txtApvAll == '100':
            midOpt = 'Y'
            midOptGbn = 'Y'
        # 선지급
        # if prePay != 'Y':
        #     prePay = 'N'

        with connection.cursor() as cursor:
            cursor.execute(" SELECT ACODE FROM OSCODEM WHERE MCODE = '" + str(mCode) + "' AND ICUST = '" + str(iCust) + "' ")
            result = cursor.fetchall()
            aCode = result[0][0]

        # with connection.cursor() as cursor:
        #     cursor.execute("    UPDATE  SISACCTT SET"
        #                    "     ACGUBN = '" + str(acGubn) + "' "
        #                    ",    MCODE = '" + str(mCode) + "' "
        #                    ",    ACODE = '" + str(aCode) + "' "
        #                    ",    GBN = (SELECT GBN FROM OSCODEM A WHERE MCODE = '" + str(mCode) + "' AND ICUST = '" + str(iCust) + "') "
        #                    ",    ACTITLE = '" + str(acTitle) + "' "
        #                    ",    ACAMTS = '" + str(acAmts) + "' "
        #                    ",    ACACNUMBER = '" + str(acAcnumber) + "' "
        #                    ",    ACDESC = '" + str(acDesc) + "' "
        #                    ",    ACGUNO_BK = '" + str(acBank) + "' "
        #                    ",    ACFOLDER = '" + str(uploaded_file_full_path[0]) + "' "
        #                    ",    ACFOLDER2 = '" + str(uploaded_file_full_path[1]) + "' "
        #                    ",    ACFOLDER3 = '" + str(uploaded_file_full_path[2]) + "' "
        #                    ",    ACFOLDER4 = '" + str(uploaded_file_full_path[3]) + "' "
        #                    ",    ACFOLDER5 = '" + str(uploaded_file_full_path[4]) + "' "
        #                    ",    EXDATE = '" + str(exDate) + "' "
        #                    ",    ACDATE = '" + str(acDate) + "' "
        #                    ",    ACCARD = '" + str(acCard) + "' "
        #                    ",    ACUSE = '" + str(acUse) + "' "
        #                    ",    ACINFO = '" + str(acInfo) + "' "
        #                    ",    ACCUST = '" + str(acCust) + "' "
        #                    ",    MID_OPT = '" + str(midOpt) + "' "
        #                    ",    MID_OPT_GBN = '" + str(midOptGbn) + "' "
        #                    ",    FIN_OPT = '" + str(finOpt) + "' "
        #                    ",    APPLYDT = '" + str(acApply).replace('-', '') + "' "
        #                    ",    PRE_PAY = '" + str(prePay) + "' "
        #                    ",    UPD_USER = '" + str(creUser) + "' "
        #                    ",    UPD_DT = date_format(now(), '%Y%m%d') "
        #                    "     WHERE IODATE = '" + str(ioDate) + "' "
        #                    "     AND ACIOGB = '" + str(acIogb) + "' "
        #                    "     AND ACSEQN = '" + str(acSeqn) + "' "
        #                    "     AND ICUST = '" + str(iCust) + "' "
        #                    )
        #     connection.commit()

        with connection.cursor() as cursor:
            query = "UPDATE SISACCTT SET " \
                    "ACGUBN = %s, " \
                    "MCODE = %s, " \
                    "ACODE = %s, " \
                    "GBN = (SELECT GBN FROM OSCODEM A WHERE MCODE = %s AND ICUST = %s), " \
                    "ACTITLE = %s, " \
                    "ACAMTS = %s, " \
                    "ACACNUMBER = %s, " \
                    "ACDESC = %s, " \
                    "ACGUNO_BK = %s, " \
                    "EXDATE = %s, " \
                    "ACDATE = %s, " \
                    "ACCARD = %s, " \
                    "ACUSE = %s, " \
                    "ACINFO = %s, " \
                    "ACCUST = %s, " \
                    "MID_OPT = %s, " \
                    "FIN_OPT = %s, " \
                    "APPLYDT = %s, " \
                    "UPD_USER = %s, " \
                    "UPD_DT = date_format(now(), '%%Y%%m%%d') " \

            params = [str(acGubn), str(mCode), str(aCode), str(mCode), str(iCust), str(acTitle), str(acAmts), str(acAcnumber), str(acDesc), str(acBank), str(exDate), str(acDate), str(acCard), str(acUse), str(acInfo), str(acCust), str(midOpt), str(finOpt), str(acApply).replace('-', ''), str(creUser)]

            # 기존 파일은 유지하고 새로운 파일만 업데이트함.
            for i in range(len(uploaded_file_path)):
                if uploaded_file_path[i] != 'KEEP FILE':
                    if i == 0:
                        query += ", ACFOLDER = %s "
                    else:
                        query += f", ACFOLDER{i + 1} = %s "
                    params.append(uploaded_file_path[i])

            query += "WHERE IODATE = %s AND ACIOGB = %s AND ACSEQN = %s AND ICUST = %s"
            params.extend([ioDate, acIogb, acSeqn, iCust])

            cursor.execute(query, params)

        connection.commit()



        with connection.cursor() as cursor:
            cursor.execute(" SELECT COUNT(SEQ) FROM OSSIGN WHERE ACDATE = '" + str(ioDate) + "' AND ACSEQN = '" + str(acSeqn) + "' AND ACIOGB = '" +  str(acIogb) + "' "
                           "        AND ICUST = '" + str(iCust) + "'  ")
            result = cursor.fetchall()
            count = int(result[0][0])
        #
        if count > 0:
            with connection.cursor() as cursor:
                cursor.execute(" DELETE FROM OSSIGN "
                               "   WHERE ACDATE = '" + str(ioDate) + "'  "
                               "   AND ACSEQN = '" + str(acSeqn) + "' "
                               "   AND ACIOGB = '" + str(acIogb) + "' "
                               "   AND ICUST = '" + str(iCust) + "' "
                )
                connection.commit()
        # 들어오는 순서대로 emp_nbr(순번)으로 데이터 넣어주기
        opt = 'N'
        empArrayLists = list(filter(len, empArray))
        for data in range(len(empArrayLists)):

            with connection.cursor() as cursor:
                cursor.execute(" INSERT INTO OSSIGN "
                               "    ( "
                               "     ACDATE "
                               "   , ACSEQN "
                               "   , SEQ "
                               "   , EMP_NBR "
                               "   , OPT "
                               "   , ACIOGB "
                               "   , ICUST "
                               "   , CRE_USER "
                               "   , CRE_DT "   
                               "    ) "
                               "    VALUES "
                               "    ( "
                               "     '" + str(ioDate) + "' "
                               "     , '" + str(acSeqn) + "' "
                               "     , ( SELECT IFNULL (MAX(SEQ) + 1,1) AS COUNTED FROM OSSIGN A WHERE ACDATE = '" + str(ioDate) + "' AND ACSEQN = '" + str(acSeqn) + "' AND ACIOGB = '" + str(acIogb) + "' AND ICUST = '" + str(iCust) + "' ) "
                               "     , '" + empArrayLists[data]["empNbr"] + "' "
                               "     , '" + str(opt) + "' "
                               "     , '" + str(acIogb) + "' "
                               "     , '" + str(iCust) + "' "
                               "     , '" + str(creUser) + "' "
                               "     , date_format(now(), '%Y%m%d') "
                               "     ) "
                )
                connection.commit()

        return JsonResponse({'sucYn': "Y"})

    else:
        # 예정일이 없을시
        if acDate == '' or acDate is None:
            if exDate != '' or exDate is not None:
                acDate = exDate
            if exDate == '' or exDate is None:
                exDate = ''
                acDate = ioDate
        # 체크카드시 없을시
        # if acGubn == '4':
        #     midOpt = 'Y'
        #     finOpt = 'Y'
        # 현금선택시 예정일지정
        if acGubn == '1':
            exDate = cashDate.replace('-', '')
            acDate = cashDate.replace('-', '')
        # 계산서선택시 계좌번호 가져오기
        # if acGubn == '2':
        #     acAcnumber = txtCustAct
        # 전결시
        if txtApvAll == '100':
            midOpt = 'Y'
            midOptGbn = 'Y'
        # 선지급
        # if prePay != 'Y':
        #     prePay = 'N'

        with connection.cursor() as cursor:
            cursor.execute(" SELECT ACODE FROM OSCODEM WHERE MCODE = '" + str(mCode) + "' AND ICUST = '" + str(iCust) + "' ")
            result = cursor.fetchall()
            aCode = result[0][0]

        if acSeqn == '' or acSeqn is None:
            with connection.cursor() as cursor:
                cursor.execute("INSERT INTO SISACCTT "
                               "   (    "
                               "     IODATE "
                               ",    ACSEQN "
                               ",    ACIOGB "
                               ",    ACTITLE "
                               ",    ACCUST "
                               ",    ACGUBN "
                               ",    MCODE "
                               ",    ACODE "
                               ",    GBN "
                               ",    ACAMTS "
                               ",    ACACNUMBER "
                               ",    ACRECN "
                               ",    ACDESC "
                               ",    CRE_USER "
                               ",    CRE_DT "
                               ",    ICUST "
                               ",    ACGUNO_BK "
                               ",    ACFOLDER "
                               ",    ACFOLDER2 "
                               ",    ACFOLDER3 "
                               ",    ACFOLDER4 "
                               ",    ACFOLDER5 "
                               ",    EXDATE "
                               ",    ACDATE "
                               ",    ACCARD "
                               ",    ACUSE "
                               ",    APPLYDT "
                               ",    ACINFO "
                               # ",    PRE_PAY "
                               ",    MID_OPT "
                               ",    MID_OPT_GBN "
                               ",    FIN_OPT "
                               "    ) "
                               "    VALUES "
                               "    (   "
                               "    '" + str(ioDate) + "'"
                               ",   (SELECT IFNULL (MAX(ACSEQN) + 1,1) AS COUNTED FROM SISACCTT A WHERE IODATE = '" + str(ioDate) + "' AND ACIOGB = '" + str(acIogb) + "' AND ICUST = '" + str(iCust) + "') "
                               ",   '" + str(acIogb) + "'"
                               ",   '" + str(acTitle) + "'"
                               ",   '" + str(acCust) + "'"
                               ",   '" + str(acGubn) + "'"
                               ",   '" + str(mCode) + "'"
                               ",   '" + str(aCode) + "'"
                               ",   (SELECT GBN FROM OSCODEM A WHERE MCODE = '" + str(mCode) + "' AND ICUST = '" + str(iCust) + "')"
                               ",   '" + str(acAmts) + "'"
                               ",   '" + str(acAcnumber) + "'"
                               ",   (SELECT IFNULL (MAX(ACRECN) + 1,1) AS COUNTED FROM SISACCTT A WHERE ACDATE = '" + str(ioDate) + "' AND ACIOGB = '" + str(acIogb) + "'AND ICUST = '" + str(iCust) + "' ) "
                               ",   '" + str(acDesc) + "'"
                               ",   '" + str(creUser) + "'"
                               ",   date_format(now(), '%Y%m%d') "
                               ",   '" + str(iCust) + "'"
                               ",   '" + str(acBank) + "'"
                               ",   '" + str(uploaded_file_path[0]) + "'"
                               ",   '" + str(uploaded_file_path[1]) + "'"
                               ",   '" + str(uploaded_file_path[2]) + "'"
                               ",   '" + str(uploaded_file_path[3]) + "'"
                               ",   '" + str(uploaded_file_path[4]) + "'"                                            
                               ",    '" + str(exDate) + "'"
                               ",    '" + str(acDate) + "'"
                               ",    '" + str(acCard) + "'"
                               ",    '" + str(acUse) + "'"
                               ",    '" + str(acApply).replace('-', '') + "'"
                               ",    '" + str(acInfo) + "'"
                               # ",    '" + str(prePay) + "' "
                               ",    '" + str(midOpt) + "' "
                               ",    '" + str(midOptGbn) + "' "
                               ",    '" + str(finOpt) + "' "
                               "    )   "
                               )
                connection.commit()

                with connection.cursor() as cursor:
                    cursor.execute(" SELECT MAX(ACSEQN) FROM SISACCTT WHERE IODATE = '" + str(ioDate) + "' AND ACIOGB = '" + str(acIogb) + "' AND ICUST = '" + str(iCust) + "' ")
                    result2 = cursor.fetchall()

                    seq = result2[0][0]

                # 들어오는 순서대로 emp_nbr(순번)으로 데이터 넣어주기
                opt = 'N'
                empArrayLists = list(filter(len, empArray))
                for data in range(len(empArrayLists)):
                    with connection.cursor() as cursor:
                        cursor.execute(" INSERT INTO OSSIGN "
                                       "    ( "
                                       "     ACDATE "
                                       "   , ACSEQN "
                                       "   , SEQ "
                                       "   , EMP_NBR "
                                       "   , OPT "
                                       "   , ACIOGB "
                                       "   , ICUST "
                                       "   , CRE_USER "
                                       "   , CRE_DT "   
                                       "    ) "
                                       "    VALUES "
                                       "    ( "
                                       "     '" + str(ioDate) + "' "
                                       "     , '" + str(seq) + "' "
                                       "     , ( SELECT IFNULL (MAX(SEQ) + 1,1) AS COUNTED FROM OSSIGN A WHERE ACDATE = '" + str(ioDate) + "'  AND ACSEQN = '" + str(seq) + "' AND ACIOGB = '" + str(acIogb) + "' AND ICUST = '" + str(iCust) + "' ) "
                                       "     , '" + empArrayLists[data]["empNbr"] + "' "
                                       "     , '" + str(opt) + "' "
                                       "     , '" + str(acIogb) + "' "
                                       "     , '" + str(iCust) + "' "
                                       "     , '" + str(creUser) + "' "
                                       "     , date_format(now(), '%Y%m%d') "
                                       "     ) "
                        )
                        connection.commit()

            return JsonResponse({'sucYn': "Y"})


def offSetViews_save(request):
    ioDate = request.POST.get("regDate").replace('-', '') # 등록일자
    acSeqn = request.POST.get("acSeqn")               # 순번
    acIogb = request.POST.get("acIogb")  # 구분(입금2/출금1)
    acAmts = request.POST.get("acAmts").replace(',', '')      # 금액
    acDesc = request.POST.get("acDesc")     # 비고
    outAct = request.POST.get("outAct")     # 출금계좌
    inAct = request.POST.get("inAct")  # 입금계좌
    creUser = request.session.get("userId")
    iCust = request.session.get("USER_ICUST")

    if acIogb == '3':
        # with connection.cursor() as cursor:
        #     cursor.execute(" SELECT COUNT(ACSEQN) AS COUNTED FROM SISACCTT A "
        #                    "    WHERE ACDATE = '" + str(ioDate) + "' "
        #                    "    AND ACIOGB = '" + str(acIogb) + "' "
        #                    "    AND ACSEQN = '" + str(acIogb) + "' "                               ""
        #                    "    AND ICUST = '" + str(iCust) + "' ")
        #     result = cursor.fetchall()
        #     count = int(result[0][0])

    # if count > 0:
    #     # 출금정보
    #     with connection.cursor() as cursor:
    #         cursor.execute( " UPDATE SISACCTT SET "
    #                         "       ACAMTS = '" + str(acAmts) + "' "
    #                         "     , ACACNUMBER = '" + str(outAct) + "' "
    #                         "     , ACDESC = '" + str(acDesc) + "' "
    #                         "     , UPD_USER = '" + str(creUser) + "' "
    #                         "     , UPD_DT = date_format(now(), '%Y%m%d') "
    #                         "     , EXDATE = '" + str(ioDate) + "' "
    #                         "     , ACDATE = '" + str(ioDate) + "' "
    #                         " WHERE ACSEQN = '" + str(acSeqn) + "' "
    #                         " AND ACIOGB = '1' "
    #                         " AND IODATE = '" + str(ioDate) + "' "
    #                         " AND ICUST = '" + str(iCust) + "' "
    #                         )
    #         connection.commit()
    #     # 입금정보
    #     with connection.cursor() as cursor:
    #         cursor.execute( " UPDATE SISACCTT SET "
    #                         "       ACAMTS = '" + str(acAmts) + "' "
    #                         "     , ACACNUMBER = '" + str(inAct) + "' "
    #                         "     , ACDESC = '" + str(acDesc) + "' "
    #                         "     , UPD_USER = '" + str(creUser) + "' "
    #                         "     , UPD_DT = date_format(now(), '%Y%m%d') "
    #                         "     , EXDATE = '" + str(ioDate) + "' "
    #                         "     , ACDATE = '" + str(ioDate) + "' "
    #                         " WHERE ACSEQN = '" + str(acSeqn) + "' "
    #                         " AND ACIOGB = '2' "
    #                         " AND IODATE = '" + str(ioDate) + "' "
    #                         " AND ICUST = '" + str(iCust) + "' "
    #                         )
    #         connection.commit()
    #
    #     # 대체정보
    #     with connection.cursor() as cursor:
    #         cursor.execute( " UPDATE SISACCTT SET "
    #                         "       ACAMTS = '" + str(acAmts) + "' "
    #                         "     , ACDESC = '" + str(acDesc) + "' "
    #                         "     , UPD_USER = '" + str(creUser) + "' "
    #                         "     , UPD_DT = date_format(now(), '%Y%m%d') "
    #                         "     , EXDATE = '" + str(ioDate) + "' "
    #                         "     , ACDATE = '" + str(ioDate) + "' "
    #                         "     , OFF_DATE = '" + str(ioDate) + "' "
    #                         "     , OFF_AMTS = '" + str(acAmts) + "' "
    #                         " WHERE ACSEQN = '" + str(acSeqn) + "' "
    #                         " AND ACIOGB = '3' "
    #                         " AND IODATE = '" + str(ioDate) + "' "
    #                         " AND ICUST = '" + str(iCust) + "' "
    #                         " AND OFF_GBN = 'off' "
    #                         " AND FIN_OPT = 'Y' "
    #                         )
    #         connection.commit()
    #
    #     return JsonResponse({'sucYn': "Y"})
    #
    # else:
        # 출금정보
        with connection.cursor() as cursor:
            cursor.execute( "INSERT INTO SISACCTT "
                            "   (    "
                            "     IODATE "
                            ",    ACSEQN "
                            ",    ACIOGB "
                            ",    ACAMTS "
                            ",    ACACNUMBER "
                            ",    ACDESC "
                            ",    CRE_USER "
                            ",    CRE_DT "
                            ",    ICUST "
                            ",    EXDATE "
                            ",    ACDATE "
                            ",    MID_OPT "
                            ",    FIN_OPT "
                            ",    OFF_GBN "
                            "    ) "
                            "    VALUES "
                            "    (   "
                            "    '" + str(ioDate) + "'"
                            ",   (SELECT IFNULL (MAX(ACSEQN) + 1,1) AS COUNTED FROM SISACCTT A WHERE IODATE = '" + str(ioDate) + "' AND ACIOGB = '1' )  "
                            ",   '1'"
                            ",   '" + str(acAmts) + "'"
                            ",   '" + str(outAct) + "'"
                            ",   '" + str(acDesc) + "'"
                            ",   '" + str(creUser) + "'"
                            ",   date_format(now(), '%Y%m%d') "
                            ",   '" + str(iCust) + "'"
                            ",   '" + str(ioDate) + "'"
                            ",   '" + str(ioDate) + "'"
                            ",   'Y' "
                            ",   'Y' "
                            ",   'off' "
                            "    )   "
                            )
            connection.commit()

        # 입금정보
        with connection.cursor() as cursor:
            cursor.execute("INSERT INTO SISACCTT "
                            "   (    "
                            "     IODATE "
                            ",    ACSEQN "
                            ",    ACIOGB "
                            ",    ACAMTS "
                            ",    ACACNUMBER "
                            ",    ACDESC "
                            ",    CRE_USER "
                            ",    CRE_DT "
                            ",    ICUST "
                            ",    EXDATE "
                            ",    ACDATE "
                            ",    MID_OPT "
                            ",    FIN_OPT "
                            ",    OFF_GBN "
                            "    ) "
                            "    VALUES "
                            "    (   "
                            "    '" + str(ioDate) + "'"
                            ",   (SELECT IFNULL (MAX(ACSEQN) + 1,1) AS COUNTED FROM SISACCTT A WHERE IODATE = '" + str(ioDate) + "' AND ACIOGB = '2' )  "
                            ",   '2'"
                            ",   '" + str(acAmts) + "'"
                            ",   '" + str(inAct) + "'"
                            ",   '" + str(acDesc) + "'"
                            ",   '" + str(creUser) + "'"
                            ",   date_format(now(), '%Y%m%d') "
                            ",   '" + str(iCust) + "'"
                            ",   '" + str(ioDate) + "'"
                            ",   '" + str(ioDate) + "'"
                            ",   'Y' "
                            ",   'Y' "
                            ",   'off' "
                            "    )   "
                               )
            connection.commit()

        # 대체정보
        with connection.cursor() as cursor:
            cursor.execute("INSERT INTO SISACCTT "
                            "   (    "
                            "     IODATE "
                            ",    ACSEQN "
                            ",    ACIOGB "
                            ",    ACAMTS "
                            ",    ACDESC "
                            ",    CRE_USER "
                            ",    CRE_DT "
                            ",    ICUST "
                            ",    EXDATE "
                            ",    ACDATE "
                            ",    MID_OPT "
                            ",    FIN_OPT "
                            ",    OFF_GBN "
                            "    ) "
                            "    VALUES "
                            "    (   "
                            "    '" + str(ioDate) + "'"
                            ",   (SELECT IFNULL (MAX(ACSEQN) + 1,1) AS COUNTED FROM SISACCTT A WHERE IODATE = '" + str(ioDate) + "' AND ACIOGB = '3' )  "
                            ",   '3'"
                            ",   '" + str(acAmts) + "'"
                            ",   '" + str(acDesc) + "'"
                            ",   '" + str(creUser) + "'"
                            ",   date_format(now(), '%Y%m%d') "
                            ",   '" + str(iCust) + "'"
                            ",   '" + str(ioDate) + "'"
                            ",   '" + str(ioDate) + "'"
                            ",   'Y' "
                            ",   'Y' "
                            ",   'off' "
                            "    )   "
                           )
            connection.commit()

        # 출금정보
        with connection.cursor() as cursor:
            cursor.execute("INSERT INTO ACTSTMENT "
                           "   (    "
                           "     ACDATE "
                           ",    PMSEQN "
                           ",    ACSEQN "
                           ",    SEQ "
                           ",    ACIOGB "
                           ",    ACAMTS "
                           ",    ACACNUMBER "
                           ",    ACDESC "
                           ",    CRE_USER "
                           ",    CRE_DT "
                           ",    ICUST "
                           ",    MID_OPT "
                           ",    FIN_OPT "
                           ",    OFF_GBN "
                           "    ) "
                           "    VALUES "
                           "    (   "
                           "    '" + str(ioDate) + "' "
                           ",   '0' " 
                           ",   (SELECT IFNULL (MAX(ACSEQN) + 1,1) AS COUNTED FROM ACTSTMENT A WHERE ACDATE = '" + str(ioDate).replace("-", "") + "' AND ACIOGB = '1' ) "                                        
                           ",   '1' "
                           ",   '1'"
                           ",   '" + str(acAmts) + "'"                                                                                                                     
                           ",   '" + str(outAct) + "'"
                           ",   '" + str(acDesc) + "'"
                           ",   '" + str(creUser) + "'"
                           ",   date_format(now(), '%Y%m%d') "
                           ",   '" + str(iCust) + "'"
                           ",   'Y' "
                           ",   'Y' "
                           ",   'off' "
                           "    )   "
                           )
            connection.commit()

        # # 입금정보
        with connection.cursor() as cursor:
            cursor.execute("INSERT INTO ACTSTMENT "
                           "   (    "
                           "     ACDATE "
                           ",    PMSEQN "
                           ",    ACSEQN "
                           ",    SEQ "
                           ",    ACIOGB "
                           ",    ACAMTS "
                           ",    ACACNUMBER "
                           ",    ACDESC "
                           ",    CRE_USER "
                           ",    CRE_DT "
                           ",    ICUST "
                           ",    MID_OPT "
                           ",    FIN_OPT "
                           ",    OFF_GBN "
                           "    ) "
                           "    VALUES "
                           "    (   "
                           "    '" + str(ioDate) + "' "
                           ",   '0' " 
                           ",   (SELECT IFNULL (MAX(ACSEQN) + 1,1) AS COUNTED FROM ACTSTMENT A WHERE ACDATE = '" + str(ioDate).replace("-", "") + "' AND ACIOGB = '2' ) "                                        
                           ",   '2' "
                           ",   '2'"
                           ",   '" + str(acAmts) + "'"                                                                                                
                           ",   '" + str(inAct) + "'"
                           ",   '" + str(acDesc) + "'"
                           ",   '" + str(creUser) + "'"
                           ",   date_format(now(), '%Y%m%d') "
                           ",   '" + str(iCust) + "'"
                           ",   'Y' "
                           ",   'Y' "
                           ",   'off' "
                           "    )   "
                           )
            connection.commit()

        # # 대체정보
        with connection.cursor() as cursor:
            cursor.execute("INSERT INTO ACTSTMENT "
                           "   (    "
                           "     ACDATE "
                           ",    PMSEQN "
                           ",    ACSEQN "
                           ",    SEQ "
                           ",    ACIOGB "
                           ",    ACAMTS "
                           ",    ACACNUMBER "
                           ",    ACDESC "
                           ",    CRE_USER "
                           ",    CRE_DT "
                           ",    ICUST "
                           ",    MID_OPT "
                           ",    FIN_OPT "
                           ",    OFF_GBN "
                           "    ) "
                           "    VALUES "
                           "    (   "
                           "    '" + str(ioDate) + "' "
                           ",   '0' " 
                           ",   (SELECT IFNULL (MAX(ACSEQN) + 1,1) AS COUNTED FROM ACTSTMENT A WHERE ACDATE = '" + str(ioDate).replace("-", "") + "' AND ACIOGB = '3' ) "                                        
                           ",   '3' "
                           ",   '3'"
                           ",   '" + str(acAmts) + "'"                                                                                                
                           ",   ''"
                           ",   '" + str(acDesc) + "'"
                           ",   '" + str(creUser) + "'"
                           ",   date_format(now(), '%Y%m%d') "
                           ",   '" + str(iCust) + "'"
                           ",   'Y' "
                           ",   'Y' "
                           ",   'off' "
                           "    )   "
                           )
            connection.commit()

        return JsonResponse({'sucYn': "Y"})



def payment_dlt_check(request):
    iCust = request.session.get("USER_ICUST")
    dataList = json.loads(request.POST.get('arrList'))

    for cust in dataList:
        acc_split_list = cust.split(',')
        with connection.cursor() as cursor:
            cursor.execute(" SELECT MID_OPT, FIN_OPT FROM SISACCTT WHERE ACSEQN = '" + acc_split_list[5] + "'"
                               "                      AND ACIOGB = '" + acc_split_list[0] + "' "
                               "                      AND IODATE = '" + acc_split_list[1] + "'"
                               "                      AND ACACNUMBER = '" + acc_split_list[2] + "' "
                               "                      AND ACCUST = '" + acc_split_list[3] + "' "
                               "                      AND MCODE = '" + acc_split_list[4] + "' "
                               "                      AND ICUST = '" + str(iCust) + "' ")
            result = cursor.fetchall()

        # 결재 진행중
        if result[0][0] == 'Y' or result[0][0] == 'R' or result[0][1] == 'Y':
            YN = 'Y'

        # 결재 미진행
        if result[0][0] == 'N' and result[0][1] == 'N':
            YN = 'N'

        return JsonResponse({'YN': YN})


def paymentViews_dlt(request):
    creUser = request.session.get("userId")
    iCust = request.session.get("USER_ICUST")
    if request.method == "POST":
        dataList = json.loads(request.POST.get('arrList'))
        print(dataList)
        for cust in dataList:
            acc_split_list = cust.split(',')
            with connection.cursor() as cursor:
                cursor.execute(" DELETE FROM SISACCTT WHERE ACSEQN = '" + acc_split_list[5] + "'"
                               "                      AND ACIOGB = '" + acc_split_list[0] + "' "
                               "                      AND IODATE = '" + acc_split_list[1] + "'"
                               "                      AND ACACNUMBER = '" + acc_split_list[2] + "' "
                               "                      AND ACCUST = '" + acc_split_list[3] + "' "
                               "                      AND MCODE = '" + acc_split_list[4] + "' "
                               "                      AND ICUST = '" + str(iCust) + "'")
                connection.commit()

            with connection.cursor() as cursor:
                cursor.execute(" SELECT COUNT(SEQ) FROM OSSIGN WHERE ACSEQN = '" + acc_split_list[5] + "' AND ACIOGB = '" + acc_split_list[0] + "' "
                               "                                AND ACDATE = '" + acc_split_list[1] + "'  AND ICUST = '" + str(iCust) + "' ")
                result = cursor.fetchall()
                count = int(result[0][0])

            if count > 0:
                with connection.cursor() as cursor:
                    cursor.execute(" DELETE FROM OSSIGN WHERE ACSEQN = '" + acc_split_list[5] + "'"
                                   "                      AND ACIOGB = '" + acc_split_list[0] + "' "
                                   "                      AND ACDATE = '" + acc_split_list[1] + "'"
                                   "                      AND ICUST = '" + str(iCust) + "'")
                    connection.commit()

        return JsonResponse({'sucYn': "Y"})

    else:
        return render(request, 'finance/withdraw-reg-sheet.html')


def checkLimit_search(request):
    price = request.POST.get('price')
    date = request.POST.get('date')
    userId = request.session.get('userId')
    iCust = request.session.get('USER_ICUST')

    with connection.cursor() as cursor:
        cursor.execute(" SELECT EMP_LIMIT FROM PIS1TB001 WHERE EMP_NBR = '" + userId + "' AND ICUST = '" + iCust + "' ")
        result = cursor.fetchall()

        limit = result[0][0]

    with connection.cursor() as cursor:
        cursor.execute(" SELECT IFNULL(SUM(ACAMTS), 0) FROM SISACCTT WHERE CRE_USER = '" + userId + "' AND SUBSTRING(IODATE, 0, 6) = '" + date + "' AND ACIOGB = '1' AND ICUST = '" + iCust + "' ")
        result2 = cursor.fetchall()

        spent = result2[0][0]

        if int(limit) >= int(price) + int(spent):
            YN = 'Y'

        elif int(limit) < int(price) + int(spent):
            YN = 'N'

        return JsonResponse({'YN': YN})



def open_file(request):
    # file_path = "/Users/thenaeunsys/Documents/OutputFile/"

    file_path = "\\Users\\thenaeunsys\\Desktop\\Time.txt\\"

    # 한글 파일명 처리를 위한 인코딩
    filename = quote(os.path.basename(file_path).encode('utf-8'))

    response = FileResponse(open(file_path, 'rb'))
    response['Content-Disposition'] = 'attachment; filename*=UTF-8\'\'%s' % filename

    # response = HttpResponse(FileWrapper(open(zip_filename, 'rb')), content_type='application/zip')
    # response['Content-Disposition'] = 'attachment; filename="downloaded_files.zip"'
    return response



# 파일 불러오기
def download_file(request):
    ioDate = request.GET.get('ioDate').replace('-', '')
    acSeqn = request.GET.get('acSeqn').replace('null', '')
    acIogb = request.GET.get('acIogb').replace('null', '')
    acCust = request.GET.get('acCust').replace('null', '')
    iCust = request.session.get("USER_ICUST")

    with connection.cursor() as cursor:
        cursor.execute(
                    "    SELECT  ACFOLDER, ACFOLDER2, ACFOLDER3, ACFOLDER4, ACFOLDER5"
                    "     FROM SISACCTT "
                    "     WHERE IODATE = '" + str(ioDate) + "' "
                    "     AND ACIOGB = '" + str(acIogb) + "' "
                    "     AND ACCUST = '" + str(acCust) + "' "
                    "     AND ACSEQN = '" + str(acSeqn) + "' "
                    "     AND ICUST = '" + str(iCust) + "' "
                       )
        result = cursor.fetchall()
    file_path_list = []
    #     file_path = result[0][0]
    #
    # if file_path:
    if result:
        # desired_path = "/Users/thenaeunsys/Documents/OutputFile/"

        desired_path = "D:/COMPANY/SANYANG/OutputFile/"

        zip_filename = desired_path + 'zipfile.zip'

        with zipfile.ZipFile(zip_filename, 'w') as zip_file:
            file_path_list = result[0]

            for file_path in file_path_list:
                if file_path and os.path.exists(file_path):
                    zip_file.write(file_path, os.path.basename(file_path))

        # 한글 파일명 처리를 위한 인코딩
        # filename = quote(os.path.basename(file_path).encode('utf-8'))

        # response = FileResponse(open(file_path, 'rb'))
        # response['Content-Disposition'] = 'attachment; filename*=UTF-8\'\'%s' % filename

        response = HttpResponse(FileWrapper(open(zip_filename, 'rb')), content_type='application/zip')
        response['Content-Disposition'] = 'attachment; filename="downloaded_files.zip"'
        return response
    else:
        return render(request, "finance/back.html")




def file_viewer(request):

    # 파일 경로 가져오기
    file_uri = request.GET.get('file_uri')

    # 도메인 가져오기
    base_url = f"{request.scheme}://{request.get_host()}"

    # 파일 URL
    file_url = f"{base_url}{file_uri}"

    # 파일 뷰어 URL
    file_viewer_url = f'https://view.officeapps.live.com/op/embed.aspx?src={file_url}'

    return render(request, 'file/file-viewer.html', {'file_viewer_url': file_viewer_url})






# with connection.cursor() as cursor:
#     cursor.execute(" SELECT SEQ FROM OSSIGN WHERE ACDATE = '" + str(acDate) + "' AND ACSEQN = '" + str(acSeqn) + "' AND ACIOGB = '" +  str(acIogb) + "' "
#                    "        AND EMP_NBR = '" + empArrayLists[data]["empNbr"] + "' AND ICUST = '" + str(iCust) + "'  ")
#     result3 = cursor.fetchall()

# if (len(result3) == 0):
#     with connection.cursor() as cursor:
#         cursor.execute("    UPDATE  OSSIGN SET"
#                        "     OPT = '" + str(opt) + "' "
#                        ",    ACIOGB = (SELECT GBN FROM OSCODEM A WHERE MCODE = '" + str(mCode) + "' AND ICUST = '" + str(iCust) + "') "
#                        "     WHERE ACDATE = '" + str(acDate) + "' "
#                        "     AND ACSEQN = '" + str(acSeqn) + "' "
#                        "     AND SEQ = '" + str(acSeqn) + "' "
#                        "     AND ICUST = '" + str(iCust) + "' "
#                        "     AND EMP_NBR = '" + empArrayLists[data]["empNbr"] + "' "
#                        )
#
#         connection.commit()

    # fileOverwriteYn = request.POST.get("fileOverwriteYn")
    #
    # uploaded_file = request.FILES.get('file')
    # if uploaded_file is None:
    #     uploaded_file = ''
    #
    # if uploaded_file:
    #     # 원하는 경로 설정, FileResponse
    #     # desired_path = "D:/NE_FTP/MAS_FILES/중요문건"
    #     # desired_path = "D:\\NE_FTP\\MAS_FILES\\"
    #     # desired_path = "D:\\NE_FTP\\MAS_FILES\\UploadFiles\\"
    #     # desired_path = "D:/NE_FTP/MAS_FILES/UploadFiles/"
    #     # desired_path = "/Users/thenaeunsys/Documents/ImportFile/"
    #     # desired_path = "/D:/NE_FTP/사업장/산양화학/Dodument/"
    #     desired_path = "D:/COMPANY/SANYANG/DOCUMENTS/"
    #     # 해당 디렉토리가 없으면 생성
    #     if not os.path.exists(desired_path):
    #         os.makedirs(desired_path)
    #
    #     destination = os.path.join(desired_path, uploaded_file.name)
    #
    #     # 해당 경로에 동일한 이름의 파일이 있다면
    #     if os.path.exists(destination):
    #         if fileOverwriteYn == 'Y':
    #             os.remove(destination)
    #         else:
    #             return JsonResponse({'sucYn': 'N', 'message': "same file name exists"})
    #
    #     with open(destination, 'wb+') as destination_file:
    #         for chunk in uploaded_file.chunks():
    #             destination_file.write(chunk)
    #
    #     uploaded_file = destination
