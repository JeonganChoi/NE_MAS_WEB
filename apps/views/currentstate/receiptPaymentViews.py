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

    return render(request, "currentstate/receipts-payments-sheet.html")

def receiptPaymentViews_search(request):
    strDate = request.POST.get('strDate')
    endDate = request.POST.get('endDate')
    act = request.POST.get('act')
    cust = request.POST.get('cust')

    if act and cust:
        with connection.cursor() as cursor:
            cursor.execute(" SELECT IFNULL(SUM(ACAMTS), 0) FROM SISACCTT "
                           "    WHERE ACDATE > '" + strDate + "' AND ACCUST = '" + cust + "' AND ACACNUMBER = '" + act + "' ")
            balresult = cursor.fetchall()

        with connection.cursor() as cursor:
            cursor.execute(
                "  SELECT ACIOGB, ACDATE, IN_ACAMTS, OUT_ACAMTS, ACCUST, CUST_NME, ACACNUMBER, ACNUM_NAME FROM "
                " ( "
                "     SELECT A.ACIOGB, A.ACDATE, A.ACAMTS AS IN_ACAMTS, 0 AS OUT_ACAMTS, A.ACCUST, B.CUST_NME, A.ACACNUMBER, C.ACNUM_NAME "
                "     FROM SISACCTT A "
                "     LEFT OUTER JOIN MIS1TB003 B "
                "     ON A.ACCUST = B.CUST_NBR "
                "     LEFT OUTER JOIN ACNUMBER C "
                "     ON A.ACACNUMBER = C.ACNUMBER "
                "     WHERE A.ACIOGB = '2' "
                "     UNION ALL "
                "     SELECT A.ACIOGB, A.ACDATE, 0 AS IN_ACAMTS, A.ACAMTS AS OUT_ACAMTS, A.ACCUST, B.CUST_NME, A.ACACNUMBER, C.ACNUM_NAME "
                "     FROM SISACCTT A "
                "     LEFT OUTER JOIN MIS1TB003 B "
                "     ON A.ACCUST = B.CUST_NBR "
                "     LEFT OUTER JOIN ACNUMBER C "
                "     ON A.ACACNUMBER = C.ACNUMBER "
                "     WHERE A.ACIOGB = '1' "
                " ) AA "
                " WHERE AA.ACDATE BETWEEN '" + strDate + "' AND '" + endDate + "' "
                " AND AA.ACCUST = '" + cust + "' "
                " AND AA.ACACNUMBER = '" + act + "' "
                " ORDER BY AA.ACDATE ")
            mainresult = cursor.fetchall()

        return JsonResponse({'balList': balresult, 'mainList': mainresult})

    elif act:
        with connection.cursor() as cursor:
            cursor.execute(" SELECT IFNULL(SUM(ACAMTS), 0) FROM SISACCTT "
                           "    WHERE ACDATE > '" + strDate + "' AND ACACNUMBER = '" + act + "' ")
            balresult = cursor.fetchall()

        with connection.cursor() as cursor:
            cursor.execute(
                "  SELECT ACIOGB, ACDATE, IN_ACAMTS, OUT_ACAMTS, ACCUST, CUST_NME, ACACNUMBER, ACNUM_NAME FROM "
                " ( "
                "     SELECT A.ACIOGB, A.ACDATE, A.ACAMTS AS IN_ACAMTS, 0 AS OUT_ACAMTS, A.ACCUST, B.CUST_NME, A.ACACNUMBER, C.ACNUM_NAME "
                "     FROM SISACCTT A "
                "     LEFT OUTER JOIN MIS1TB003 B "
                "     ON A.ACCUST = B.CUST_NBR "
                "     LEFT OUTER JOIN ACNUMBER C "
                "     ON A.ACACNUMBER = C.ACNUMBER "
                "     WHERE A.ACIOGB = '2' "
                "     UNION ALL "
                "     SELECT A.ACIOGB, A.ACDATE, 0 AS IN_ACAMTS, A.ACAMTS AS OUT_ACAMTS, A.ACCUST, B.CUST_NME, A.ACACNUMBER, C.ACNUM_NAME "
                "     FROM SISACCTT A "
                "     LEFT OUTER JOIN MIS1TB003 B "
                "     ON A.ACCUST = B.CUST_NBR "
                "     LEFT OUTER JOIN ACNUMBER C "
                "     ON A.ACACNUMBER = C.ACNUMBER "
                "     WHERE A.ACIOGB = '1' "
                " ) AA "
                " WHERE AA.ACDATE BETWEEN '" + strDate + "' AND '" + endDate + "' "
                " AND AA.ACACNUMBER = '" + act + "' "
                " ORDER BY AA.ACDATE ")
            mainresult = cursor.fetchall()

        return JsonResponse({'balList': balresult, 'mainList': mainresult})

    elif cust:
        with connection.cursor() as cursor:
            cursor.execute(" SELECT IFNULL(SUM(ACAMTS), 0) FROM SISACCTT "
                           "    WHERE ACDATE > '" + strDate + "' AND ACCUST = '" + cust + "' ")
            balresult = cursor.fetchall()

        with connection.cursor() as cursor:
            cursor.execute(
                "  SELECT ACIOGB, ACDATE, IN_ACAMTS, OUT_ACAMTS, ACCUST, CUST_NME, ACACNUMBER, ACNUM_NAME FROM "
                " ( "
                "     SELECT A.ACIOGB, A.ACDATE, A.ACAMTS AS IN_ACAMTS, 0 AS OUT_ACAMTS, A.ACCUST, B.CUST_NME, A.ACACNUMBER, C.ACNUM_NAME "
                "     FROM SISACCTT A "
                "     LEFT OUTER JOIN MIS1TB003 B "
                "     ON A.ACCUST = B.CUST_NBR "
                "     LEFT OUTER JOIN ACNUMBER C "
                "     ON A.ACACNUMBER = C.ACNUMBER "
                "     WHERE A.ACIOGB = '2' "
                "     UNION ALL "
                "     SELECT A.ACIOGB, A.ACDATE, 0 AS IN_ACAMTS, A.ACAMTS AS OUT_ACAMTS, A.ACCUST, B.CUST_NME, A.ACACNUMBER, C.ACNUM_NAME "
                "     FROM SISACCTT A "
                "     LEFT OUTER JOIN MIS1TB003 B "
                "     ON A.ACCUST = B.CUST_NBR "
                "     LEFT OUTER JOIN ACNUMBER C "
                "     ON A.ACACNUMBER = C.ACNUMBER "
                "     WHERE A.ACIOGB = '1' "
                " ) AA "
                " WHERE AA.ACDATE BETWEEN '" + strDate + "' AND '" + endDate + "' "
                " AND AA.ACCUST = '" + cust + "' "
                " ORDER BY AA.ACDATE ")
            mainresult = cursor.fetchall()

        return JsonResponse({'balList': balresult, 'mainList': mainresult})

    else:
        with connection.cursor() as cursor:
            cursor.execute(" SELECT IFNULL(SUM(ACAMTS), 0) FROM SISACCTT WHERE ACDATE > '" + strDate + "' ")
            balresult = cursor.fetchall()


        with connection.cursor() as cursor:
            cursor.execute("  SELECT ACIOGB, ACDATE, IN_ACAMTS, OUT_ACAMTS, ACCUST, CUST_NME, ACACNUMBER, ACNUM_NAME FROM "
                            " ( "
                            "     SELECT A.ACIOGB, A.ACDATE, A.ACAMTS AS IN_ACAMTS, 0 AS OUT_ACAMTS, A.ACCUST, B.CUST_NME, A.ACACNUMBER, C.ACNUM_NAME "
                            "     FROM SISACCTT A "
                            "     LEFT OUTER JOIN MIS1TB003 B "
                            "     ON A.ACCUST = B.CUST_NBR "
                            "     LEFT OUTER JOIN ACNUMBER C "
                            "     ON A.ACACNUMBER = C.ACNUMBER "
                            "     WHERE A.ACIOGB = '2' "
                            "     UNION ALL "
                            "     SELECT A.ACIOGB, A.ACDATE, 0 AS IN_ACAMTS, A.ACAMTS AS OUT_ACAMTS, A.ACCUST, B.CUST_NME, A.ACACNUMBER, C.ACNUM_NAME "
                            "     FROM SISACCTT A "
                            "     LEFT OUTER JOIN MIS1TB003 B "
                            "     ON A.ACCUST = B.CUST_NBR "
                            "     LEFT OUTER JOIN ACNUMBER C "
                            "     ON A.ACACNUMBER = C.ACNUMBER "
                            "     WHERE A.ACIOGB = '1' "
                            " ) AA "
                            " WHERE AA.ACDATE BETWEEN '" + strDate + "' AND '" + endDate + "' "
                            " ORDER BY AA.ACDATE ")
            mainresult = cursor.fetchall()
            print(mainresult)

        with connection.cursor() as cursor:
            cursor.execute(" SELECT CUST_NBR, CUST_NME FROM MIS1TB003 ORDER BY CUST_NBR ")
            cboCust = cursor.fetchall()

        with connection.cursor() as cursor:
            cursor.execute(" SELECT ACNUMBER FROM ACNUMBER ORDER BY ACNUMBER ")
            cboAct = cursor.fetchall()

        return JsonResponse({'balList': balresult, 'mainList': mainresult, 'cboCust': cboCust, 'cboAct': cboAct})