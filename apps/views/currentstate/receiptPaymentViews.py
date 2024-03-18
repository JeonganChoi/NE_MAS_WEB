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

# 월별 자금 유동 현황
def receiptPaymentViews(request):
    userId = request.session.get('userId')
    if userId == '' or userId is None:
        return redirect("/page-404/")
    else:
        return render(request, "currentstate/receipts-payments-sheet.html")

def receiptPaymentViews_search(request):
    strDate = request.POST.get('strDate').replace("-", "")
    endDate = request.POST.get('endDate').replace("-", "")
    act = request.POST.get('act')
    cust = request.POST.get('cust')
    creUser = request.session.get("userId")
    iCust = request.session.get("USER_ICUST")

    temp = [act, cust]
    if all(temp):
        with connection.cursor() as cursor:
            cursor.execute(" SELECT IFNULL(SUM(BAL), 0), IFNULL(SUM(INTOTAL), 0), IFNULL(SUM(OUTTOTAL), 0), IFNULL(SUM(BAL + INTOTAL - OUTTOTAL), 0) FROM "
                           " (SELECT SUM(IFNULL(ACAMTS, 0)) AS BAL, 0 AS INTOTAL, 0 AS OUTTOTAL FROM ACBALANCE WHERE ACDATE < '" + str(strDate) + "' AND ICUST = '" + str(iCust) + "' "
                           " UNION ALL "
                           " SELECT 0 AS BAL, SUM(IFNULL(ACAMTS, 0)) AS INTOTAL, 0 AS OUTTOTAL FROM ACTSTMENT "
                           "        WHERE ACIOGB = '2' AND ACCUST = '" + str(cust) + "' AND ACACNUMBER = '" + str(act) + "' "
                           "        AND ACDATE BETWEEN '" + str(strDate) + "' AND '" + str(endDate) + "' AND ICUST = '" + str(iCust) + "' "
                           " UNION ALL "
                           " SELECT 0 AS BAL, 0 AS INTOTAL, SUM(IFNULL(ACAMTS, 0)) AS OUTTOTAL FROM ACTSTMENT "
                           "        WHERE ACIOGB = '1' AND ACCUST = '" + str(cust) + "' AND ACACNUMBER = '" + str(act) + "' "
                           "        AND ACDATE BETWEEN '" + str(strDate) + "' AND '" + str(endDate) + "' AND ICUST = '" + str(iCust) + "' "
                           " ) AA ")
            balresult = cursor.fetchall()

            # cursor.execute(" SELECT IFNULL(SUM(ACAMTS), 0) FROM SISACCTT "
            #                "    WHERE ACDATE > '" + strDate + "' AND ACCUST = '" + cust + "' AND ACACNUMBER = '" + act + "' ")

        with connection.cursor() as cursor:
            cursor.execute("  SELECT IFNULL(ACIOGB, ''), IFNULL(ACDATE, ''), IFNULL(IN_ACAMTS, 0), IFNULL(OUT_ACAMTS, 0), IFNULL(ACCUST, ''), IFNULL(CUST_NME, ''), IFNULL(ACACNUMBER, ''), IFNULL(ACNUM_NAME, '') FROM "
                           " ( "
                           "     SELECT A.ACIOGB, A.ACDATE, A.ACAMTS AS IN_ACAMTS, 0 AS OUT_ACAMTS, A.ACCUST, B.CUST_NME, A.ACACNUMBER, C.ACNUM_NAME "
                           "     FROM ACTSTMENT A "
                           "     LEFT OUTER JOIN MIS1TB003 B "
                           "     ON A.ACCUST = B.CUST_NBR "
                           "     LEFT OUTER JOIN ACNUMBER C "
                           "     ON A.ACACNUMBER = C.ACNUMBER "
                           "     WHERE A.ACIOGB = '2' "
                           "     AND A.ICUST = '" + str(iCust) + "' "
                           "     UNION ALL "
                           "     SELECT A.ACIOGB, A.ACDATE, 0 AS IN_ACAMTS, A.ACAMTS AS OUT_ACAMTS, A.ACCUST, B.CUST_NME, A.ACACNUMBER, C.ACNUM_NAME "
                           "     FROM ACTSTMENT A "
                           "     LEFT OUTER JOIN MIS1TB003 B "
                           "     ON A.ACCUST = B.CUST_NBR "
                           "     LEFT OUTER JOIN ACNUMBER C "
                           "     ON A.ACACNUMBER = C.ACNUMBER "
                           "     WHERE A.ACIOGB = '1' "
                           "     AND A.ICUST = '" + str(iCust) + "' "
                           " ) AA "
                           " WHERE AA.ACDATE BETWEEN '" + str(strDate) + "' AND '" + str(endDate) + "' "
                           " AND AA.ACCUST = '" + str(cust) + "' "
                           " AND AA.ACACNUMBER = '" + str(act) + "' "
                           " ORDER BY AA.ACDATE ")
            mainresult = cursor.fetchall()

        return JsonResponse({'balList': balresult, 'mainList': mainresult})

    if any(temp):
        with connection.cursor() as cursor:
            cursor.execute(" SELECT IFNULL(SUM(BAL), 0), IFNULL(SUM(INTOTAL), 0), IFNULL(SUM(OUTTOTAL), 0), IFNULL(SUM(BAL + INTOTAL - OUTTOTAL), 0) FROM "
                           " (SELECT SUM(IFNULL(ACAMTS, 0)) AS BAL, 0 AS INTOTAL, 0 AS OUTTOTAL FROM ACBALANCE WHERE ACDATE < '" + str(strDate) + "' AND ICUST = '" + str(iCust) + "' "
                           " UNION ALL "
                           " SELECT 0 AS BAL, SUM(IFNULL(ACAMTS, 0)) AS INTOTAL, 0 AS OUTTOTAL FROM ACTSTMENT "
                           "        WHERE ACIOGB = '2' AND ACDATE BETWEEN '" + str(strDate) + "' AND '" + str(endDate) + "' AND ICUST = '" + str(iCust) + "' "
                           "        AND ACCUST = '" + str(cust) + "' OR ACACNUMBER = '" + str(act) + "'  "
                           " UNION ALL "
                           " SELECT 0 AS BAL, 0 AS INTOTAL, SUM(IFNULL(ACAMTS, 0)) AS OUTTOTAL FROM ACTSTMENT "
                           "        WHERE ACIOGB = '1' AND ACDATE BETWEEN '" + str(strDate) + "' AND '" + str(endDate) + "' AND ICUST = '" + str(iCust) + "' "
                           "        AND ACCUST = '" + str(cust) + "' OR ACACNUMBER = '" + str(act) + "' "
                           " ) AA ")
            balresult = cursor.fetchall()

        # with connection.cursor() as cursor:
        #     cursor.execute(" SELECT IFNULL(SUM(ACAMTS), 0) FROM SISACCTT "
        #                    "    WHERE ACDATE > '" + strDate + "' AND ACACNUMBER = '" + act + "' ")
        #     balresult = cursor.fetchall()

        with connection.cursor() as cursor:
            cursor.execute(
                "  SELECT IFNULL(ACIOGB, ''), IFNULL(ACDATE, ''), IFNULL(IN_ACAMTS, 0), IFNULL(OUT_ACAMTS, 0), IFNULL(ACCUST, ''), IFNULL(CUST_NME, ''), IFNULL(ACACNUMBER, ''), IFNULL(ACNUM_NAME, '') FROM "
                " ( "
                "     SELECT A.ACIOGB, A.ACDATE, A.ACAMTS AS IN_ACAMTS, 0 AS OUT_ACAMTS, A.ACCUST, B.CUST_NME, A.ACACNUMBER, C.ACNUM_NAME "
                "     FROM ACTSTMENT A "
                "     LEFT OUTER JOIN MIS1TB003 B "
                "     ON A.ACCUST = B.CUST_NBR "
                "     LEFT OUTER JOIN ACNUMBER C "
                "     ON A.ACACNUMBER = C.ACNUMBER "
                "     WHERE A.ACIOGB = '2' "
                "     AND A.ICUST = '" + str(iCust) + "' "
                "     UNION ALL "
                "     SELECT A.ACIOGB, A.ACDATE, 0 AS IN_ACAMTS, A.ACAMTS AS OUT_ACAMTS, A.ACCUST, B.CUST_NME, A.ACACNUMBER, C.ACNUM_NAME "
                "     FROM ACTSTMENT A "
                "     LEFT OUTER JOIN MIS1TB003 B "
                "     ON A.ACCUST = B.CUST_NBR "
                "     LEFT OUTER JOIN ACNUMBER C "
                "     ON A.ACACNUMBER = C.ACNUMBER "
                "     WHERE A.ACIOGB = '1' "
                "     AND A.ICUST = '" + str(iCust) + "' "
                " ) AA "
                " WHERE AA.ACDATE BETWEEN '" + str(strDate) + "' AND '" + str(endDate) + "' "
                " AND AA.ACACNUMBER = '" + str(act) + "' "
                "  OR AA.ACCUST = '" + str(cust) + "'"
                " ORDER BY AA.ACDATE ")
            mainresult = cursor.fetchall()

        return JsonResponse({'balList': balresult, 'mainList': mainresult})

    else:
        with connection.cursor() as cursor:
            cursor.execute(" SELECT IFNULL(SUM(BAL), 0), IFNULL(SUM(INTOTAL), 0), IFNULL(SUM(OUTTOTAL), 0), IFNULL(SUM(BAL + INTOTAL - OUTTOTAL), 0) FROM "
                           " (SELECT SUM(IFNULL(ACAMTS, 0)) AS BAL, 0 AS INTOTAL, 0 AS OUTTOTAL FROM ACBALANCE WHERE ACDATE < '" + str(strDate) + "' AND ICUST = '" + str(iCust) + "' "
                           " UNION ALL "
                           " SELECT 0 AS BAL, SUM(IFNULL(ACAMTS, 0)) AS INTOTAL, 0 AS OUTTOTAL FROM ACTSTMENT WHERE ACIOGB = '2' AND ACDATE < '" + str(strDate) + "' AND ICUST = '" + str(iCust) + "' "
                           " UNION ALL "
                           " SELECT 0 AS BAL, 0 AS INTOTAL, SUM(IFNULL(ACAMTS, 0)) AS OUTTOTAL FROM ACTSTMENT WHERE ACIOGB = '1' AND ACDATE < '" + str(strDate) + "' AND ICUST = '" + str(iCust) + "' "
                           " ) AA ")
            balresult = cursor.fetchall()

        with connection.cursor() as cursor:
            cursor.execute("  SELECT IFNULL(ACIOGB, ''), IFNULL(ACDATE, ''), IFNULL(IN_ACAMTS, 0), IFNULL(OUT_ACAMTS, 0), IFNULL(ACCUST, ''), IFNULL(CUST_NME, ''), IFNULL(ACACNUMBER, ''), IFNULL(ACNUM_NAME, '') FROM "
                            " ( "
                            "     SELECT A.ACIOGB, A.ACDATE, A.ACAMTS AS IN_ACAMTS, 0 AS OUT_ACAMTS, A.ACCUST, B.CUST_NME, A.ACACNUMBER, C.ACNUM_NAME "
                            "     FROM ACTSTMENT A "
                            "     LEFT OUTER JOIN MIS1TB003 B "
                            "     ON A.ACCUST = B.CUST_NBR "
                            "     LEFT OUTER JOIN ACNUMBER C "
                            "     ON A.ACACNUMBER = C.ACNUMBER "
                            "     WHERE A.ACIOGB = '2' "
                            "       AND A.ICUST = '" + str(iCust) + "'"
                            "     UNION ALL "
                            "     SELECT A.ACIOGB, A.ACDATE, 0 AS IN_ACAMTS, A.ACAMTS AS OUT_ACAMTS, A.ACCUST, B.CUST_NME, A.ACACNUMBER, C.ACNUM_NAME "
                            "     FROM ACTSTMENT A "
                            "     LEFT OUTER JOIN MIS1TB003 B "
                            "     ON A.ACCUST = B.CUST_NBR "
                            "     LEFT OUTER JOIN ACNUMBER C "
                            "     ON A.ACACNUMBER = C.ACNUMBER "
                            "     WHERE A.ACIOGB = '1' "
                            "       AND A.ICUST = '" + str(iCust) + "'"
                            " ) AA "
                            " WHERE AA.ACDATE BETWEEN '" + str(strDate) + "' AND '" + str(endDate) + "' "
                            " ORDER BY AA.ACDATE ")
            mainresult = cursor.fetchall()
            print(mainresult)

        with connection.cursor() as cursor:
            cursor.execute(" SELECT CUST_NBR, CUST_NME FROM MIS1TB003 WHERE ICUST = '" + str(iCust) + "' ORDER BY CUST_NBR ")
            cboCust = cursor.fetchall()

        with connection.cursor() as cursor:
            cursor.execute(" SELECT ACNUMBER FROM ACNUMBER WHERE ICUST = '" + str(iCust) + "' ORDER BY ACNUMBER ")
            cboAct = cursor.fetchall()

        return JsonResponse({'balList': balresult, 'mainList': mainresult, 'cboCust': cboCust, 'cboAct': cboAct})