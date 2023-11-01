import json
import os
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



# 출금-수불장
def withRegNewViews(request):

    return render(request, "finance/withdraw-reg-sheet.html")



def receivePay_search(request):
    strDate = request.POST.get('strDate')
    endDate = request.POST.get('endDate')
    cboCust = request.POST.get('cboCust')
    cboAct = request.POST.get('cboAct')
    creUser = request.session.get("userId")
    iCust = request.session.get("USER_ICUST")

    if strDate and endDate and cboCust == '' and cboAct == '':
        with connection.cursor() as cursor:
            cursor.execute(" SELECT IFNULL(SUM(ACAMTS), 0) FROM SISACCTT WHERE IODATE > '" + str(strDate) + "' AND ICUST = '" + str(iCust) + "' ")
            balresult = cursor.fetchall()

        with connection.cursor() as cursor:
            cursor.execute("  SELECT IFNULL(AA.ACIOGB, ''), IFNULL(AA.IODATE, ''), IFNULL(AA.IN_ACAMTS, 0), IFNULL(AA.OUT_ACAMTS, 0)"
                           ", IFNULL(AA.ACCUST, ''), IFNULL(AA.CUST_NME, ''), IFNULL(AA.ACACNUMBER, ''), IFNULL(AA.ACNUM_NAME, '')"
                           ", IFNULL(AA.MCODE, ''), IFNULL(AA.FIN_OPT, ''), IFNULL(AA.MCODENM, ''), IFNULL(AA.ACTITLE, '')"
                           ", IFNULL(AA.ACSEQN, ''), IFNULL(AA.ACODE, ''), IFNULL(AA.ACODENM, ''), IFNULL(AA.GBN, ''), IFNULL(AA.GBNNM, '') FROM "
                           " ( "
                           "     SELECT A.ACIOGB, A.IODATE, A.ACAMTS AS IN_ACAMTS, 0 AS OUT_ACAMTS, A.ACCUST, B.CUST_NME"
                           "            , A.ACACNUMBER, C.ACNUM_NAME, A.MCODE, A.FIN_OPT, D.MCODENM, A.ACTITLE, A.ACSEQN, A.ACODE, E.RESNAM AS ACODENM, F.GBN, G.RESNAM AS GBNNM "
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
                           "     AND A.ICUST = '" + iCust + "'"
                           "     UNION ALL "
                           "     SELECT A.ACIOGB, A.IODATE, 0 AS IN_ACAMTS, A.ACAMTS AS OUT_ACAMTS, A.ACCUST, B.CUST_NME"
                           "            , A.ACACNUMBER, C.ACNUM_NAME, A.MCODE, A.FIN_OPT, D.MCODENM, A.ACTITLE, A.ACSEQN, A.ACODE, E.RESNAM AS ACODENM, F.GBN, G.RESNAM AS GBNNM "
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
                           "     AND A.ICUST = '" + iCust + "'"
                           " ) AA "
                           " WHERE AA.IODATE BETWEEN '" + strDate + "' AND '" + endDate + "' "
                           " ORDER BY AA.IODATE ")
            mainresult = cursor.fetchall()

            # 거래처
            with connection.cursor() as cursor:
                cursor.execute(" SELECT CUST_NBR, CUST_NME FROM MIS1TB003 WHERE ICUST = '" + iCust + "' ORDER BY CUST_NBR ")
                cboCust = cursor.fetchall()

            with connection.cursor() as cursor:
                cursor.execute(" SELECT ACNUMBER FROM ACNUMBER WHERE ICUST = '" + iCust + "' ")
                cboAct = cursor.fetchall()

            return JsonResponse({'balList': balresult, 'mainList': mainresult, 'cboCust': cboCust, 'cboAct': cboAct})

    elif cboCust and cboAct == '':
        with connection.cursor() as cursor:
            cursor.execute(" SELECT IFNULL(SUM(ACAMTS), 0) FROM SISACCTT WHERE IODATE > '" + str(strDate) + "' AND ACCUST = '" + str(cboCust) + "' AND ICUST = '" + str(iCust) + "' ")
            balresult = cursor.fetchall()

        with connection.cursor() as cursor:
            cursor.execute("  SELECT IFNULL(AA.ACIOGB, ''), IFNULL(AA.IODATE, ''), IFNULL(AA.IN_ACAMTS, 0), IFNULL(AA.OUT_ACAMTS, 0)"
                           ", IFNULL(AA.ACCUST, ''), IFNULL(AA.CUST_NME, ''), IFNULL(AA.ACACNUMBER, ''), IFNULL(AA.ACNUM_NAME, '')"
                           ", IFNULL(AA.MCODE, ''), IFNULL(AA.FIN_OPT, ''), IFNULL(AA.MCODENM, ''), IFNULL(AA.ACTITLE, '')"
                           ", IFNULL(AA.ACSEQN, ''), IFNULL(AA.ACODE, ''), IFNULL(AA.ACODENM, ''), IFNULL(AA.GBN, ''), IFNULL(AA.GBNNM, '') FROM "
                           " ( "
                           "     SELECT A.ACIOGB, A.IODATE, A.ACAMTS AS IN_ACAMTS, 0 AS OUT_ACAMTS, A.ACCUST, B.CUST_NME"
                           "            , A.ACACNUMBER, C.ACNUM_NAME, A.MCODE, A.FIN_OPT, D.MCODENM, A.ACTITLE, A.ACSEQN, A.ACODE, E.RESNAM AS ACODENM, F.GBN, G.RESNAM AS GBNNM "
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
                           "     AND A.ICUST = '" + iCust + "'"
                           "     UNION ALL "
                           "     SELECT A.ACIOGB, A.IODATE, 0 AS IN_ACAMTS, A.ACAMTS AS OUT_ACAMTS, A.ACCUST, B.CUST_NME"
                           "            , A.ACACNUMBER, C.ACNUM_NAME, A.MCODE, A.FIN_OPT, D.MCODENM, A.ACTITLE, A.ACSEQN, A.ACODE, E.RESNAM AS ACODENM, F.GBN, G.RESNAM AS GBNNM  "
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
                           "     AND A.ICUST = '" + iCust + "'"
                           " ) AA "
                           " WHERE AA.IODATE BETWEEN '" + strDate + "' AND '" + endDate + "' "
                           " AND AA.ACCUST = '" + cboCust + "' "
                           " ORDER BY AA.IODATE ")
            mainresult = cursor.fetchall()

        return JsonResponse({'balList': balresult, 'mainList': mainresult})

    elif cboAct and cboCust == '':
        with connection.cursor() as cursor:
            cursor.execute(" SELECT IFNULL(SUM(ACAMTS), 0) FROM SISACCTT WHERE IODATE > '" + str(strDate) + "' AND ACACNUMBER = '" + str(cboAct) + "' AND ICUST = '" + str(iCust) + "' ")
            balresult = cursor.fetchall()

        with connection.cursor() as cursor:
            cursor.execute("  SELECT IFNULL(AA.ACIOGB, ''), IFNULL(AA.IODATE, ''), IFNULL(AA.IN_ACAMTS, 0), IFNULL(AA.OUT_ACAMTS, 0)"
                           ", IFNULL(AA.ACCUST, ''), IFNULL(AA.CUST_NME, ''), IFNULL(AA.ACACNUMBER, ''), IFNULL(AA.ACNUM_NAME, '')"
                           ", IFNULL(AA.MCODE, ''), IFNULL(AA.FIN_OPT, ''), IFNULL(AA.MCODENM, ''), IFNULL(AA.ACTITLE, '')"
                           ", IFNULL(AA.ACSEQN, ''), IFNULL(AA.ACODE, ''), IFNULL(AA.ACODENM, ''), IFNULL(AA.GBN, ''), IFNULL(AA.GBNNM, '') FROM "
                           " ( "
                           "     SELECT A.ACIOGB, A.IODATE, A.ACAMTS AS IN_ACAMTS, 0 AS OUT_ACAMTS, A.ACCUST, B.CUST_NME"
                           "            , A.ACACNUMBER, C.ACNUM_NAME, A.MCODE, A.FIN_OPT, D.MCODENM, A.ACTITLE, A.ACSEQN, A.ACODE, E.RESNAM AS ACODENM, F.GBN, G.RESNAM AS GBNNM "
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
                           "     AND A.ICUST = '" + iCust + "'"
                           "     UNION ALL "
                           "     SELECT A.ACIOGB, A.IODATE, 0 AS IN_ACAMTS, A.ACAMTS AS OUT_ACAMTS, A.ACCUST, B.CUST_NME"
                           "            , A.ACACNUMBER, C.ACNUM_NAME, A.MCODE, A.FIN_OPT, D.MCODENM, A.ACTITLE, A.ACSEQN, A.ACODE, E.RESNAM AS ACODENM, F.GBN, G.RESNAM AS GBNNM  "
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
                           "     AND A.ICUST = '" + iCust + "'"
                           " ) AA "
                           " WHERE AA.IODATE BETWEEN '" + strDate + "' AND '" + endDate + "' "
                           " AND AA.ACACNUMBER = '" + cboAct + "' "
                           " ORDER BY AA.IODATE ")
            mainresult = cursor.fetchall()

        return JsonResponse({'balList': balresult, 'mainList': mainresult})

    else:
        with connection.cursor() as cursor:
            cursor.execute(" SELECT IFNULL(SUM(ACAMTS), 0) FROM SISACCTT WHERE IODATE > '" + str(strDate) + "' AND ACCUST = '" + str(cboCust) + "' "
                           " AND ACACNUMBER = '" + str(cboAct) + "' AND ICUST = '" + str(iCust) + "' ")
            balresult = cursor.fetchall()

        with connection.cursor() as cursor:
            cursor.execute("  SELECT IFNULL(AA.ACIOGB, ''), IFNULL(AA.IODATE, ''), IFNULL(AA.IN_ACAMTS, 0), IFNULL(AA.OUT_ACAMTS, 0)"
                           ", IFNULL(AA.ACCUST, ''), IFNULL(AA.CUST_NME, ''), IFNULL(AA.ACACNUMBER, ''), IFNULL(AA.ACNUM_NAME, '')"
                           ", IFNULL(AA.MCODE, ''), IFNULL(AA.FIN_OPT, ''), IFNULL(AA.MCODENM, ''), IFNULL(AA.ACTITLE, '')"
                           ", IFNULL(AA.ACSEQN, ''), IFNULL(AA.ACODE, ''), IFNULL(AA.ACODENM, ''), IFNULL(AA.GBN, ''), IFNULL(AA.GBNNM, '') FROM "
                           " ( "
                           "     SELECT A.ACIOGB, A.IODATE, A.ACAMTS AS IN_ACAMTS, 0 AS OUT_ACAMTS, A.ACCUST, B.CUST_NME"
                           "            , A.ACACNUMBER, C.ACNUM_NAME, A.MCODE, A.FIN_OPT, D.MCODENM, A.ACTITLE, A.ACSEQN, A.ACODE, E.RESNAM AS ACODENM, F.GBN, G.RESNAM AS GBNNM  "
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
                           "     AND A.ICUST = '" + iCust + "'"
                           "     UNION ALL "
                           "     SELECT A.ACIOGB, A.IODATE, 0 AS IN_ACAMTS, A.ACAMTS AS OUT_ACAMTS, A.ACCUST, B.CUST_NME"
                           "            , A.ACACNUMBER, C.ACNUM_NAME, A.MCODE, A.FIN_OPT, D.MCODENM, A.ACTITLE, A.ACSEQN, A.ACODE, E.RESNAM AS ACODENM, F.GBN, G.RESNAM AS GBNNM "
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
                           "     AND A.ICUST = '" + iCust + "'"
                           " ) AA "
                           " WHERE AA.IODATE BETWEEN '" + strDate + "' AND '" + endDate + "' "
                           " AND AA.ACACNUMBER = '" + cboAct + "' "
                           " AND AA.ACCUST = '" + cboCust + "' "
                           " ORDER BY AA.IODATE ")
            mainresult = cursor.fetchall()

        return JsonResponse({'balList': balresult, 'mainList': mainresult})


def apvLine_modal_search(request):
    empList = json.loads(request.POST.get('empList'))
    cboDpt = request.POST.get('cboDpt')
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
                           " WHERE A.EMP_LIMIT != '' "
                           " AND A.ICUST = '" + iCust + "'"
                           " AND A.EMP_DEPT = '" + cboDpt + "' ")
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
                           " WHERE A.EMP_LIMIT != '' "
                           " AND A.ICUST = '" + iCust + "'")
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
            cursor.execute(" SELECT ACNUMBER, CARDNUM FROM ACCARD WHERE CARDNUM = '" + cboCard + "' AND ICUST = '" + iCust + "' ")
            cboActNum = cursor.fetchall()

            return JsonResponse({'cboActNum': cboActNum})

    if acIogb and acCust == '':
        with connection.cursor() as cursor:
            # 거래처구분/명/행/결제방법명/결제방법코드/입출금구분/계정/금액/순번/날짜/계좌번호
            cursor.execute(" SELECT IFNULL(A.ACSEQN,''), IFNULL(A.ACCUST, ''), IFNULL(B.CUST_NME, '') "
                           "    , IFNULL(A.ACRECN,''), IFNULL(A.ACGUBN,''), IFNULL(C.RESNAM,'') "
                           "    , IFNULL(A.ACIOGB,''), IFNULL(E.RESNAM, ''), IFNULL(A.MCODE,''), IFNULL(D.MCODENM, '') "
                           "    , IFNULL(A.ACAMTS, 0), IFNULL(A.IODATE,''), IFNULL(A.ACACNUMBER,'') "
                           "    , IFNULL(A.ACGUNO_BK,''), IFNULL(F.RESNAM, '') , IFNULL(A.ACBUNHO,''), IFNULL(A.ACGUNO_DT,'')"
                           "    , IFNULL(A.ACODE,''), IFNULL(G.ACODENM, ''), IFNULL(A.ACDESC, ''), IFNULL(A.EXDATE,''), IFNULL(A.ACTITLE,'')"
                           "    , IFNULL(A.ACFOLDER,''), IFNULL(A.ACCARD, '') "
                           "    FROM SISACCTT A "
                           "    LEFT OUTER JOIN MIS1TB003 B "
                           "    ON A.ACCUST = B.CUST_NBR "
                           "    LEFT OUTER JOIN OSREFCP C "
                           "    ON A.ACGUBN = C.RESKEY "
                           "    AND C.RECODE = 'OUB' "
                           "    LEFT OUTER JOIN OSCODEM D "
                           "    ON A.MCODE = D.MCODE "
                           "    LEFT OUTER JOIN OSCODEA G "
                           "    ON A.ACODE = G.ACODE "
                           "    LEFT OUTER JOIN OSREFCP E "
                           "    ON A.ACIOGB = E.RESKEY "
                           "    AND E.RECODE = 'OUA' "
                           "    LEFT OUTER JOIN OSREFCP F "
                           "    ON A.ACGUNO_BK = F.RESKEY "
                           "    AND F.RECODE = 'BNK' "
                           "    WHERE A.IODATE = '" + str(ioDate) + "' "
                           "    AND A.ACIOGB = '" + str(acIogb) + "' "
                           "    AND A.ACACNUMBER = '" + str(acNum) + "' "
                           "    AND A.ACSEQN = '" + str(acSeqn) + "'"
                           "    AND A.ICUST = '" + str(iCust) + "'")
            subresult = cursor.fetchall()
            print(subresult)

            # 결재할사람
            with connection.cursor() as cursor:
                cursor.execute(" SELECT A.SEQ, A.EMP_NBR, B.EMP_NME FROM OSSIGN A "
                               " LEFT OUTER JOIN PIS1TB001 B ON A.EMP_NBR = B.EMP_NBR"
                               " WHERE A.ACDATE = '" + str(ioDate) + "' AND A.ACIOGB = '" + str(acIogb) + "' "
                               "   AND A.ACSEQN = '" + str(acSeqn) + "' AND A.ICUST = '" + iCust + "'  ")
                permit = cursor.fetchall()

            # 거래처
            with connection.cursor() as cursor:
                cursor.execute(" SELECT CUST_NBR, CUST_NME FROM MIS1TB003 WHERE ICUST = '" + iCust + "' ")
                cboCust = cursor.fetchall()

            # 입출금구분
            with connection.cursor() as cursor:
                cursor.execute(" SELECT RESKEY, RESNAM FROM OSREFCP WHERE RECODE = 'OUA' AND ICUST = '" + iCust + "' ORDER BY RESKEY ")
                cboGgn = cursor.fetchall()

            # 관리계정
            with connection.cursor() as cursor:
                cursor.execute(" SELECT MCODE, MCODENM FROM OSCODEM WHERE ICUST = '" + iCust + "' ORDER BY MCODE ASC ")
                cboMCode = cursor.fetchall()

            # 회계게정
            # with connection.cursor() as cursor:
            #     cursor.execute(" SELECT ACODE, ACODENM FROM OSCODEA WHERE ICUST = '" + iCust + "' ORDER BY ACODE ASC ")
            #     cboACode = cursor.fetchall()

            # 결제방법
            with connection.cursor() as cursor:
                cursor.execute(" SELECT RESKEY, RESNAM FROM OSREFCP WHERE RECODE = 'PGB' AND ICUST = '" + iCust + "' ORDER BY RESNAM ")
                cboPay = cursor.fetchall()

            # 계좌번호
            with connection.cursor() as cursor:
                cursor.execute(" SELECT ACNUMBER FROM ACNUMBER WHERE ICUST = '" + iCust + "' ")
                cboAcnumber = cursor.fetchall()

            # 카드번호
            with connection.cursor() as cursor:
                cursor.execute(" SELECT CARDNUM FROM ACCARD WHERE ICUST = '" + iCust + "' ")
                cboCard = cursor.fetchall()

        return JsonResponse({'subList': subresult, 'permit': permit, 'cboCust': cboCust, 'cboGgn': cboGgn
                                , 'cboMCode': cboMCode, 'cboPay': cboPay, 'cboAcnumber': cboAcnumber, 'cboCard': cboCard})

    if acIogb:
        with connection.cursor() as cursor:
            # 거래처구분/명/행/결제방법명/결제방법코드/입출금구분/계정/금액/순번/날짜/계좌번호
            cursor.execute(" SELECT IFNULL(A.ACSEQN,''), IFNULL(A.ACCUST, ''), IFNULL(B.CUST_NME, '') "
                           "    , IFNULL(A.ACRECN,''), IFNULL(A.ACGUBN,''), IFNULL(C.RESNAM,'') "
                           "    , IFNULL(A.ACIOGB,''), IFNULL(E.RESNAM, ''), IFNULL(A.MCODE,''), IFNULL(D.MCODENM, '') "
                           "    , IFNULL(A.ACAMTS, 0), IFNULL(A.IODATE,''), IFNULL(A.ACACNUMBER,'') "
                           "    , IFNULL(A.ACGUNO_BK,''), IFNULL(F.RESNAM, '') , IFNULL(A.ACBUNHO,''), IFNULL(A.ACGUNO_DT,'')"
                           "    , IFNULL(A.ACODE,''), IFNULL(G.ACODENM, ''), IFNULL(A.ACDESC, ''), IFNULL(A.EXDATE,''), IFNULL(A.ACTITLE,'')"
                           "    , IFNULL(A.ACFOLDER,''), IFNULL(A.ACCARD, '') "
                           "    FROM SISACCTT A "
                           "    LEFT OUTER JOIN MIS1TB003 B "
                           "    ON A.ACCUST = B.CUST_NBR "
                           "    LEFT OUTER JOIN OSREFCP C "
                           "    ON A.ACGUBN = C.RESKEY "
                           "    AND C.RECODE = 'OUB' "
                           "    LEFT OUTER JOIN OSCODEM D "
                           "    ON A.MCODE = D.MCODE "
                           "    LEFT OUTER JOIN OSCODEA G "
                           "    ON A.ACODE = G.ACODE "
                           "    LEFT OUTER JOIN OSREFCP E "
                           "    ON A.ACIOGB = E.RESKEY "
                           "    AND E.RECODE = 'OUA' "
                           "    LEFT OUTER JOIN OSREFCP F "
                           "    ON A.ACGUNO_BK = F.RESKEY "
                           "    AND F.RECODE = 'BNK' "
                           "    WHERE A.IODATE = '" + str(ioDate) + "' "
                           "    AND A.ACIOGB = '" + str(acIogb) + "' "
                           "    AND A.ACACNUMBER = '" + str(acNum) + "' "
                           "    AND A.ACCUST = '" + str(acCust) + "'"
                           "    AND A.MCODE = '" + str(acMcode) + "' "
                           "    AND A.ACSEQN = '" + str(acSeqn) + "'"
                           "    AND A.ICUST = '" + str(iCust) + "'")
            subresult = cursor.fetchall()
            print(subresult)

            # 결재할사람
            with connection.cursor() as cursor:
                cursor.execute(" SELECT A.SEQ, A.EMP_NBR, B.EMP_NME FROM OSSIGN A "
                               " LEFT OUTER JOIN PIS1TB001 B ON A.EMP_NBR = B.EMP_NBR"
                               " WHERE A.ACDATE = '" + str(ioDate) + "' AND A.ACIOGB = '" + str(acIogb) + "' "
                               "   AND A.ACSEQN = '" + str(acSeqn) + "' AND A.ICUST = '" + iCust + "' ")
                permit = cursor.fetchall()

            # 거래처
            with connection.cursor() as cursor:
                cursor.execute(" SELECT CUST_NBR, CUST_NME FROM MIS1TB003 WHERE ICUST = '" + iCust + "' ")
                cboCust = cursor.fetchall()

            # 입출금구분
            with connection.cursor() as cursor:
                cursor.execute(" SELECT RESKEY, RESNAM FROM OSREFCP WHERE RECODE = 'OUA' AND ICUST = '" + iCust + "' ORDER BY RESKEY ")
                cboGgn = cursor.fetchall()

            # 관리계정
            with connection.cursor() as cursor:
                cursor.execute(" SELECT MCODE, MCODENM FROM OSCODEM WHERE ICUST = '" + iCust + "' ORDER BY MCODE ASC ")
                cboMCode = cursor.fetchall()

            # 회계게정
            # with connection.cursor() as cursor:
            #     cursor.execute(" SELECT ACODE, ACODENM FROM OSCODEA WHERE ICUST = '" + iCust + "' ORDER BY ACODE ASC ")
            #     cboACode = cursor.fetchall()

            # 결제방법
            with connection.cursor() as cursor:
                cursor.execute(" SELECT RESKEY, RESNAM FROM OSREFCP WHERE RECODE = 'PGB' AND ICUST = '" + iCust + "' ORDER BY RESNAM ")
                cboPay = cursor.fetchall()

            # 계좌번호
            with connection.cursor() as cursor:
                cursor.execute(" SELECT ACNUMBER FROM ACNUMBER WHERE ICUST = '" + iCust + "' ")
                cboAcnumber = cursor.fetchall()

            # 카드번호
            with connection.cursor() as cursor:
                cursor.execute(" SELECT CARDNUM FROM ACCARD WHERE ICUST = '" + iCust + "' ")
                cboCard = cursor.fetchall()

        return JsonResponse({'subList': subresult, 'permit': permit, 'cboCust': cboCust, 'cboGgn': cboGgn
                                , 'cboMCode': cboMCode, 'cboPay': cboPay, 'cboAcnumber': cboAcnumber, 'cboCard': cboCard})

    # 출금
    if cboGbn == '1':
        # 거래처
        with connection.cursor() as cursor:
            cursor.execute(" SELECT CUST_NBR, CUST_NME FROM MIS1TB003 WHERE CUST_GBN LIKE '1' AND '3' AND ICUST = '" + iCust + "'")
            cboCust = cursor.fetchall()

        # 입출금구분
        with connection.cursor() as cursor:
            cursor.execute(" SELECT RESKEY, RESNAM FROM OSREFCP WHERE RECODE = 'OUA' AND ICUST = '" + iCust + "' ORDER BY RESKEY ")
            cboGgn = cursor.fetchall()

        # 관리계정
        with connection.cursor() as cursor:
            cursor.execute(" SELECT MCODE, MCODENM FROM OSCODEM WHERE MCODE LIKE '5%' AND ICUST = '" + iCust + "' ORDER BY MCODE ASC ")
            cboMCode = cursor.fetchall()

        # 결제방법
        with connection.cursor() as cursor:
            cursor.execute(" SELECT RESKEY, RESNAM FROM OSREFCP WHERE RECODE = 'PGB' AND ICUST = '" + iCust + "' ORDER BY RESNAM ")
            cboPay = cursor.fetchall()

        # 계좌번호
        with connection.cursor() as cursor:
            cursor.execute(" SELECT ACNUMBER FROM ACNUMBER WHERE ICUST = '" + iCust + "' ")
            cboAcnumber = cursor.fetchall()

        # 카드번호
        with connection.cursor() as cursor:
            cursor.execute(" SELECT CARDNUM FROM ACCARD WHERE ICUST = '" + iCust + "' ")
            cboCard = cursor.fetchall()

        return JsonResponse(
            {'cboCust': cboCust, 'cboGgn': cboGgn, 'cboMCode': cboMCode, 'cboPay': cboPay, 'cboAcnumber': cboAcnumber, 'cboCard': cboCard})

    # 입금
    else:
        # 거래처
        with connection.cursor() as cursor:
            cursor.execute(" SELECT CUST_NBR, CUST_NME FROM MIS1TB003 WHERE CUST_GBN LIKE '2' AND '3' AND ICUST = '" + iCust + "' ")
            cboCust = cursor.fetchall()

        # 입출금구분
        with connection.cursor() as cursor:
            cursor.execute(" SELECT RESKEY, RESNAM FROM OSREFCP WHERE RECODE = 'OUA' AND ICUST = '" + iCust + "' ORDER BY RESKEY ")
            cboGgn = cursor.fetchall()

        # 관리계정
        with connection.cursor() as cursor:
            cursor.execute(" SELECT MCODE, MCODENM FROM OSCODEM WHERE MCODE LIKE '4%' AND ICUST = '" + iCust + "' ORDER BY MCODE ASC ")
            cboMCode = cursor.fetchall()

        # 결제방법
        with connection.cursor() as cursor:
            cursor.execute(" SELECT RESKEY, RESNAM FROM OSREFCP WHERE RECODE = 'PGB' AND ICUST = '" + iCust + "' ORDER BY RESNAM ")
            cboPay = cursor.fetchall()

        # 계좌번호
        with connection.cursor() as cursor:
            cursor.execute(" SELECT ACNUMBER FROM ACNUMBER WHERE ICUST = '" + iCust + "' ")
            cboAcnumber = cursor.fetchall()

        # 카드번호
        with connection.cursor() as cursor:
            cursor.execute(" SELECT CARDNUM FROM ACCARD WHERE ICUST = '" + iCust + "' ")
            cboCard = cursor.fetchall()

        return JsonResponse({'cboCust': cboCust, 'cboGgn': cboGgn, 'cboMCode': cboMCode, 'cboPay': cboPay, 'cboAcnumber': cboAcnumber, 'cboCard': cboCard})


def cboActNum_search(request):
    cboBank = request.POST.get("cboBank")
    creUser = request.session.get("userId")
    iCust = request.session.get("USER_ICUST")

    if cboBank:
        with connection.cursor() as cursor:
            cursor.execute(" SELECT ACNUMBER FROM ACNUMBER WHERE ACBKCD = '" + cboBank + "' AND ICUST = '" + iCust + "'")
            cboAct = cursor.fetchall()

        return JsonResponse({'cboAct': cboAct})

    else:
        with connection.cursor() as cursor:
            cursor.execute(" SELECT ACNUMBER FROM ACNUMBER WHERE ICUST = '" + iCust + "'")
            cboAct = cursor.fetchall()

        with connection.cursor() as cursor:
            cursor.execute(" SELECT A.ACBKCD, B.RESNAM FROM ACNUMBER A "
                            " LEFT OUTER JOIN OSREFCP B "
                            " ON A.ACBKCD = B.RESKEY "
                            " AND B.RECODE = 'BNK' "
                            " WHERE A.ICUST = '" + iCust + "' "
                            " GROUP BY A.ACBKCD")
            cboBank = cursor.fetchall()

        return JsonResponse({'cboAct': cboAct, 'cboBank': cboBank})

def paymentViews_save(request):
    empArray = json.loads(request.POST.get('empArrList'))
    ioDate = request.POST.get("txtWitRegDate").replace('-', '') # 등록일자
    exDate = request.POST.get("txtExDate").replace('-', '')
    acSeqn = request.POST.get("txtWitSeq")               # 순번
    acTitle = request.POST.get("txtTitle")
    acRecn = request.POST.get("txtWitRecn")
    acCust = request.POST.get("cboWitCust")     # 거래처
    acIogb = request.POST.get("cboWitGbn")  # 구분(입금2/출금1)
    mCode = request.POST.get("cboAdminCode")  # 관리계정
    # acCode = request.POST.get("cboActCode")  # 회계계정
    acAmts = request.POST.get("txtWitPrice")      # 금액
    acAcnumber = request.POST.get("cboWitActNum")     # 계좌번호
    acGubn = request.POST.get("cboWitMethod")     # 결제방법
    acCard = request.POST.get("cboWitCard")
    acDesc = request.POST.get("txtWitRemark")     # 비고
    acUse = request.POST.get("txtWhere")  # 사용처
    creUser = request.session.get("userId")
    iCust = request.session.get("USER_ICUST")
    acDate = request.POST.get("txtExDate").replace('-', '')

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

    fileOverwriteYn = request.POST.get("fileOverwriteYn")

    uploaded_file = request.FILES.get('file')

    if uploaded_file:
        # 원하는 경로 설정, FileResponse
        # desired_path = "D:/NE_FTP/MAS_FILES/중요문건"
        # desired_path = "D:\\NE_FTP\\MAS_FILES\\"
        # desired_path = "D:\\NE_FTP\\MAS_FILES\\UploadFiles\\"
        # desired_path = "D:/NE_FTP/MAS_FILES/UploadFiles/"
        desired_path = "/Users/thenaeunsys/Documents/ImportFile/"

        # 해당 디렉토리가 없으면 생성
        if not os.path.exists(desired_path):
            os.makedirs(desired_path)

        destination = os.path.join(desired_path, uploaded_file.name)

        # 해당 경로에 동일한 이름의 파일이 있다면
        if os.path.exists(destination):
            if fileOverwriteYn == 'Y':
                os.remove(destination)
            else:
                return JsonResponse({'sucYn': 'N', 'message': "same file name exists"})

        with open(destination, 'wb+') as destination_file:
            for chunk in uploaded_file.chunks():
                destination_file.write(chunk)

        Rfilenameloc = destination

    if acSeqn:
        with connection.cursor() as cursor:
            cursor.execute(" SELECT ACBKCD FROM ACNUMBER WHERE ACNUMBER = '" + acAcnumber + "' AND ICUST = '" + iCust + "' ")
            result = cursor.fetchall()  # 계좌 은행

            bnk = result[0][0]

        if exDate == '' or exDate is None:
            exDate = ioDate
            acDate = ioDate

        with connection.cursor() as cursor:
            cursor.execute("    UPDATE  SISACCTT SET"
                           "     ACGUBN = '" + str(acGubn) + "' "
                           ",    MCODE = '" + str(mCode) + "' "
                           ",    MCODE = (SELECT GBN FROM OSCODEM A WHERE MCODE = '" + str(mCode) + "' AND ICUST = '" + iCust + "') "
                           ",    ACTITLE = '" + str(acTitle) + "' "
                           ",    ACAMTS = '" + str(acAmts) + "' "
                           ",    ACACNUMBER = '" + str(acAcnumber) + "' "
                           ",    ACDESC = '" + str(acDesc) + "' "
                           ",    ACGUNO_BK = '" + str(bnk) + "' "
                           ",    ACFOLDER = '" + str(Rfilenameloc) + "' "
                           ",    EXDATE = '" + str(exDate) + "' "
                           ",    ACDATE = '" + str(acDate) + "' "
                           ",    ACCARD = '" + str(acCard) + "' "
                           ",    ACUSE = '" + str(acUse) + "' "
                           ",    UPD_USER = '" + str(creUser) + "' "
                           ",    UPD_DT = date_format(now(), '%Y%m%d') "
                           "     WHERE IODATE = '" + str(ioDate) + "' "
                           "     AND ACIOGB = '" + str(acIogb) + "' "
                           "     AND ACCUST = '" + str(acCust) + "' "
                           "     AND ACSEQN = '" + str(acSeqn) + "' "
                           "     AND ICUST = '" + str(iCust) + "' "
                           )
            connection.commit()

        # with connection.cursor() as cursor:
        #     cursor.execute(" SELECT MAX(ACSEQN) FROM SISACCTT WHERE IODATE = '" + str(ioDate) + "' AND ACIOGB = '" + str(acIogb) + "' ")
        #     result2 = cursor.fetchall()  # 계좌 은행
        #
        #     seq = result2[0][0]

        # 들어오는 순서대로 emp_nbr(순번)으로 데이터 넣어주기
        opt = 'N'
        empArrayLists = list(filter(len, empArray))
        for data in range(len(empArrayLists)):
            with connection.cursor() as cursor:
                cursor.execute(" SELECT SEQ FROM OSSIGN WHERE ACDATE = '" + str(acDate) + "' AND ACSEQN = '" + str(acSeqn) + "' AND ACIOGB = '" +  str(acIogb) + "' "
                               "        AND EMP_NBR = '" + empArrayLists[data]["empNbr"] + "' AND ICUST = '" + iCust + "'  ")
                result3 = cursor.fetchall()

                if(len(result3) != 0):
                    seq2 = result3[0][0]

                    with connection.cursor() as cursor:
                        cursor.execute(" UPDATE OSSIGN SET "
                                       "        EMP_NBR = '" + empArrayLists[data]["empNbr"] + "' "
                                       "      , OPT = '" + opt + "' "
                                       "      , ACIOGB = '" + str(acIogb) + "' "
                                       " WHERE ACDATE = '" + str(acDate) + "'  "
                                       "   AND ACSEQN = '" + str(acSeqn) + "' "
                                       "   AND SEQ = '" + str(seq2) + "' "
                                       "   AND ICUST = '" + iCust + "' "
                        )
                        connection.commit()

                else:
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
                                       "    ) "
                                       "    VALUES "
                                       "    ( "
                                       "     '" + str(acDate) + "' "
                                       "     , '" + str(acSeqn) + "' "
                                       "     , ( SELECT IFNULL (MAX(SEQ) + 1,1) AS COUNTED FROM OSSIGN A WHERE ACDATE = '" + str(ioDate) + "' AND ACSEQN = '" + str(acSeqn) + "' AND ACIOGB = '" +  str(acIogb) + "' AND ICUST = '" + iCust + "' ) "
                                       "     , '" + empArrayLists[data]["empNbr"] + "' "
                                       "     , '" + opt + "' "
                                       "     , '" + str(acIogb) + "' "
                                       "     , '" + str(iCust) + "' "
                                       "     ) "
                        )
                        connection.commit()

        return JsonResponse({'sucYn': "Y"})

    else:
        with connection.cursor() as cursor:
            cursor.execute(" SELECT ACBKCD FROM ACNUMBER WHERE ACNUMBER = '" + acAcnumber + "' AND ICUST = '" + iCust + "' ")
            result = cursor.fetchall()  # 계좌 은행

            bnk = result[0][0]

        if exDate == '' or exDate is None:
            exDate = ioDate
            acDate = ioDate

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
                               ",    EXDATE "
                               ",    ACDATE "
                               ",    ACCARD "
                               ",    ACUSE "
                               ",    FIN_OPT "
                               "    ) "
                               "    VALUES "
                               "    (   "
                               "    '" + str(ioDate) + "'"
                               ",   (SELECT IFNULL (MAX(ACSEQN) + 1,1) AS COUNTED FROM SISACCTT A WHERE ACDATE = '" + str(ioDate) + "' AND ACIOGB = '" + str(acIogb) + "' AND ICUST = '" + iCust + "') "
                               ",   '" + str(acIogb) + "'"
                               ",   '" + str(acTitle) + "'"
                               ",   '" + str(acCust) + "'"
                               ",   '" + str(acGubn) + "'"
                               ",   '" + str(mCode) + "'"
                               ",   (SELECT GBN FROM OSCODEM A WHERE MCODE = '" + str(mCode) + "' AND ICUST = '" + iCust + "')"
                               ",   '" + str(acAmts) + "'"
                               ",   '" + str(acAcnumber) + "'"
                               ",   (SELECT IFNULL (MAX(ACRECN) + 1,1) AS COUNTED FROM SISACCTT A WHERE ACDATE = '" + str(ioDate) + "' AND ACIOGB = '" + str(acIogb) + "' AND ACSEQN = '" + str(acSeqn) + "' AND ICUST = '" + iCust + "' ) "
                               ",   '" + str(acDesc) + "'"
                               ",   '" + str(creUser) + "'"
                               ",   date_format(now(), '%Y%m%d') "
                               ",   '" + str(iCust) + "'"
                               ",   '" + str(bnk) + "'"
                               ",   '" + str(Rfilenameloc) + "'"
                               ",    '" + str(exDate) + "'"
                               ",    '" + str(acDate) + "'"
                               ",    '" + str(acCard) + "'"
                               ",    '" + str(acUse) + "'"
                               ",    'N' "
                               "    )   "
                               )
                connection.commit()

                with connection.cursor() as cursor:
                    cursor.execute(" SELECT MAX(ACSEQN) FROM SISACCTT WHERE IODATE = '" + str(ioDate) + "' AND ACIOGB = '" + str(acIogb) + "' AND ICUST = '" + iCust + "' ")
                    result2 = cursor.fetchall()  # 계좌 은행

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
                                       "    ) "
                                       "    VALUES "
                                       "    ( "
                                       "     '" + str(acDate) + "' "
                                       "     , '" + str(seq) + "' "
                                       "     , ( SELECT IFNULL (MAX(SEQ) + 1,1) AS COUNTED FROM OSSIGN A WHERE ACDATE = '" + str(ioDate) + "' AND ACSEQN = '" + str(seq) + "' AND ICUST = '" + iCust + "' ) "
                                       "     , '" + empArrayLists[data]["empNbr"] + "' "
                                       "     , '" + opt + "' "
                                       "     , '" + str(acIogb) + "' "
                                       "     , '" + str(iCust) + "' "
                                       "     ) "
                        )
                        connection.commit()

            return JsonResponse({'sucYn': "Y"})


def offSetViews_save(request):
    empArray = json.loads(request.POST.get('empArrList'))
    ioDate = request.POST.get("txtWitRegDate2").replace('-', '') # 등록일자
    acSeqn = request.POST.get("txtWitSeq2")               # 순번
    acTitle = request.POST.get("txtTitle")
    acIogb = request.POST.get("cboWitGbn")  # 구분(입금2/출금1)
    acAmts = request.POST.get("txtWitPrice2")      # 금액
    acAcnumber = request.POST.get("cboWitActNum2")  # 계좌번호
    acDesc = request.POST.get("txtWitRemark2")     # 비고
    # 대체
    outAct = request.POST.get("cboOutAct")     # 출금계좌
    inAct = request.POST.get("cboInAct")  # 입금계좌
    offDate = request.POST.get("txtOffDate").replace('-', '')  # 대체일자

    creUser = request.session.get("userId")
    iCust = request.session.get("USER_ICUST")

    file = request.FILES.get('file')

    if (file is None):
        file = ''
    url = '/media/'

    if file is None or not None:
        if len(request.FILES) != 0:
            myfile = request.FILES['file']
            fs = FileSystemStorage()
            filename = fs.save(myfile.name, myfile)
            Rfilenameloc = url + filename

        else:
            Rfilenameloc = file

    with connection.cursor() as cursor:
        cursor.execute(" SELECT IFNULL (MAX(ACSEQN) + 1,1) AS COUNTED FROM SISACCTT A WHERE ACDATE = '" + str(ioDate) + "' AND ACIOGB = '" + str(acIogb) + "' ")
        result = cursor.fetchall()  # 계좌 은행

        acSeqn = result[0][0]

    # 출금정보
    if outAct:
        with connection.cursor() as cursor:
            cursor.execute(" SELECT ACBKCD FROM ACNUMBER WHERE ACNUMBER = '" + outAct + "' ")
            result = cursor.fetchall()  # 계좌 은행

            outBnk = result[0][0]

        if offDate == '' or offDate is None:
            offDate = ioDate

        with connection.cursor() as cursor:
            cursor.execute(
                               "INSERT INTO SISACCTT "
                               "   (    "
                               "     IODATE "
                               ",    ACSEQN "
                               ",    ACIOGB "
                               ",    ACTITLE "
                               ",    ACAMTS "
                               ",    ACACNUMBER "
                               ",    ACRECN "
                               ",    ACDESC "
                               ",    CRE_USER "
                               ",    CRE_DT "
                               ",    ICUST "
                               ",    ACGUNO_BK "
                               ",    ACFOLDER "
                               ",    EXDATE "
                               ",    ACDATE "
                               ",    FIN_OPT "
                               ",    OFF_GBN "
                               "    ) "
                               "    VALUES "
                               "    (   "
                               "    '" + str(ioDate) + "'"
                               ",   '" + str(acSeqn) + "' "
                               ",   '1'"
                               ",   '" + str(acTitle) + "'"
                               ",   '" + str(acAmts) + "'"
                               ",   '" + str(outAct) + "'"
                               ",   (SELECT IFNULL (MAX(ACRECN) + 1,1) AS COUNTED FROM SISACCTT A WHERE ACDATE = '" + str(ioDate) + "' AND ACIOGB = '" + str(acIogb) + "' AND ACSEQN = '" + str(acSeqn) + "' ) "
                               ",   '" + str(acDesc) + "'"
                               ",   '" + str(creUser) + "'"
                               ",   date_format(now(), '%Y%m%d') "
                               ",   '" + str(iCust) + "'"
                               ",   '" + str(outBnk) + "'"
                               ",   '" + str(Rfilenameloc) + "'"
                               ",   '" + str(ioDate) + "'"
                               ",   '" + str(ioDate) + "'"
                               ",   'Y' "
                               ",   'off' "
                               "    )   "
                               )
            connection.commit()

    # 입금정보
    if inAct:
        with connection.cursor() as cursor:
            cursor.execute(" SELECT ACBKCD FROM ACNUMBER WHERE ACNUMBER = '" + inAct + "' ")
            result = cursor.fetchall()  # 계좌 은행

            inBnk = result[0][0]

        if offDate == '' or offDate is None:
            offDate = ioDate

        with connection.cursor() as cursor:
            cursor.execute("INSERT INTO SISACCTT "
                               "   (    "
                               "     IODATE "
                               ",    ACSEQN "
                               ",    ACIOGB "
                               ",    ACTITLE "
                               ",    ACAMTS "
                               ",    ACACNUMBER "
                               ",    ACRECN "
                               ",    ACDESC "
                               ",    CRE_USER "
                               ",    CRE_DT "
                               ",    ICUST "
                               ",    ACGUNO_BK "
                               ",    ACFOLDER "
                               ",    EXDATE "
                               ",    ACDATE "
                               ",    FIN_OPT "
                               ",    OFF_GBN"
                               "    ) "
                               "    VALUES "
                               "    (   "
                               "    '" + str(ioDate) + "'"
                               ",   '" + str(acSeqn) + "' "
                               ",   '2'"
                               ",   '" + str(acTitle) + "'"
                               ",   '" + str(acAmts) + "'"
                               ",   '" + str(inAct) + "'"
                               ",   (SELECT IFNULL (MAX(ACRECN) + 1,1) AS COUNTED FROM SISACCTT A WHERE ACDATE = '" + str(ioDate) + "' AND ACIOGB = '" + str(acIogb) + "' AND ACSEQN = '" + str(acSeqn) + "' ) "
                               ",   '" + str(acDesc) + "'"
                               ",   '" + str(creUser) + "'"
                               ",   date_format(now(), '%Y%m%d') "
                               ",   '" + str(iCust) + "'"
                               ",   '" + str(inBnk) + "'"
                               ",   '" + str(Rfilenameloc) + "'"
                               ",   '" + str(ioDate) + "'"
                               ",   '" + str(ioDate) + "'"
                               ",   'Y'"
                               ",   'off'"
                               "    )   "
                               )
            connection.commit()

    # 대체젇보
    with connection.cursor() as cursor:
        cursor.execute("INSERT INTO SISACCTT "
                       "   (    "
                       "     IODATE "
                       ",    ACSEQN "
                       ",    ACIOGB "
                       ",    ACTITLE "
                       ",    ACAMTS "
                       ",    ACACNUMBER "
                       ",    ACRECN "
                       ",    ACDESC "
                       ",    CRE_USER "
                       ",    CRE_DT "
                       ",    ICUST "
                       ",    ACFOLDER "
                       ",    EXDATE "
                       ",    ACDATE "
                       ",    OFF_DATE "
                       ",    OFF_AMTS "
                       ",    OFF_GBN"
                       ",    FIN_OPT "
                       "    ) "
                       "    VALUES "
                       "    (   "
                       "    '" + str(ioDate) + "' "
                       ",   '" + str(acSeqn) + "' "
                       ",   '" + str(acIogb) + "' "
                       ",   '" + str(acTitle) + "' "
                       ",   '" + str(acAmts) + "' "
                       ",   '" + str(acAcnumber) + "' "
                       ",   (SELECT IFNULL (MAX(ACRECN) + 1,1) AS COUNTED FROM SISACCTT A WHERE ACDATE = '" + str(ioDate) + "' AND ACIOGB = '" + str(acIogb) + "' AND ACSEQN = '" + str(acSeqn) + "' ) "
                       ",   '" + str(acDesc) + "' "
                       ",   '" + str(creUser) + "' "
                       ",   date_format(now(), '%Y%m%d') "
                       ",   '" + str(iCust) + "' "
                       ",   '" + str(Rfilenameloc) + "' "
                       ",   '" + str(ioDate) + "' "
                       ",   '" + str(ioDate) + "' "
                       ",   '" + str(offDate) + "' "
                       ",   '" + str(acAmts) + "' "
                       ",   'off' "
                       ",   'Y' "
                       "    )   "
                       )
        connection.commit()

    # with connection.cursor() as cursor:
    #     cursor.execute(" SELECT MAX(ACSEQN) FROM SISACCTT WHERE IODATE = '" + str(ioDate).replace('-', '') + "' AND ACIOGB = '" + str(acIogb) + "' ")
    #     result2 = cursor.fetchall()  # 계좌 은행
    #
    #     seq = result2[0][0]

    # 들어오는 순서대로 emp_nbr(순번)으로 데이터 넣어주기
    # opt = 'N'
    # empArrayLists = list(filter(len, empArray))
    # for data in range(len(empArrayLists)):
    #     with connection.cursor() as cursor:
    #         cursor.execute(" INSERT INTO OSSIGN "
    #                        "    ( "
    #                        "     ACDATE "
    #                        "   , ACSEQN "
    #                        "   , SEQ "
    #                        "   , EMP_NBR "
    #                        "   , OPT "
    #                        "   , ACIOGB "
    #                        "   , ICUST "
    #                        "    ) "
    #                        "    VALUES "
    #                        "    ( "
    #                        "     '" + str(ioDate) + "' "
    #                        "     , '" + str(seq) + "' "
    #                        "     , ( SELECT IFNULL (MAX(SEQ) + 1,1) AS COUNTED FROM OSSIGN A WHERE ACDATE = '" + str(ioDate) + "' AND ACSEQN = '" + str(seq) + "' ) "
    #                        "     , '" + empArrayLists[data]["empNbr"] + "' "
    #                        "     , '" + opt + "' "
    #                        "     , '" + str(acIogb) + "' "
    #                        "     , '" + str(iCust) + "' "
    #                        "     ) "
    #         )
    #         connection.commit()

    return JsonResponse({'sucYn': "Y"})

def paymentViews_dlt(request):
    if request.method == "POST":
        dataList = json.loads(request.POST.get('arrList'))
        print(dataList)
        for cust in dataList:
            acc_split_list = cust.split(',')
            with connection.cursor() as cursor:
                cursor.execute(" DELETE FROM SISACCTT WHERE ACSEQN = '" + acc_split_list[0] + "'"
                               "                      AND ACIOGB = '" + acc_split_list[1] + "' "
                               "                      AND IODATE = '" + acc_split_list[2] + "'"
                               "                      AND ACACNUMBER = '" + acc_split_list[3] + "' "
                               "                      AND ACCUST = '" + acc_split_list[4] + "' "
                               "                      AND MCODE = '" + acc_split_list[5] + "' ")
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



# 파일 불러오기
def download_file(request):
    ioDate = request.GET.get('ioDate').replace('-', '')
    acSeqn = request.GET.get('acSeqn')
    acIogb = request.GET.get('acIogb')
    acCust = request.GET.get('acCust')
    iCust = request.session.get("USER_ICUST")

    with connection.cursor() as cursor:
        cursor.execute(
                    "    SELECT  ACFOLDER"
                    "     FROM SISACCTT "
                    "     WHERE IODATE = '" + str(ioDate) + "' "
                    "     AND ACIOGB = '" + str(acIogb) + "' "
                    "     AND ACCUST = '" + str(acCust) + "' "
                    "     AND ACSEQN = '" + str(acSeqn) + "' "
                    "     AND ICUST = '" + str(iCust) + "' "
                       )
        result = cursor.fetchall()

    #     file_path = result[0][0]
    #
    # if file_path:
    if result:
        file_path = result[0][0]
        # 한글 파일명 처리를 위한 인코딩
        filename = quote(os.path.basename(file_path).encode('utf-8'))

        response = FileResponse(open(file_path, 'rb'))
        response['Content-Disposition'] = 'attachment; filename*=UTF-8\'\'%s' % filename
        return response
    else:
        return render(request, "finance/back.html")