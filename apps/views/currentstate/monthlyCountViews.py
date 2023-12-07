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

# 월별집계
def montlyCountViews(request):

    return render(request, "currentstate/monthly-countReport.html")

def montlyCountViews_search(request):
    year = request.POST.get('Year')
    user = request.session.get('userId')
    iCust = request.session.get('USER_ICUST')

    with connection.cursor() as cursor:
        cursor.execute(" SELECT RESKEY, RESNAM FROM OSREFCP WHERE RECODE = 'MCD' AND ICUST = '" + str(iCust) + "' ")
        headerresult = cursor.fetchall()

    with connection.cursor() as cursor:
        cursor.execute(" SELECT MCODE_M, MCODE, MCODENM FROM OSCODEM WHERE ICUST = '" + str(iCust) + "' ORDER BY MCODE ")
        mCoderesult = cursor.fetchall()

    # 매입
    with connection.cursor() as cursor:
        cursor.execute(" SELECT IFNULL(MCODE, ''), IFNULL(MCODENM, ''), IFNULL(MCODE_M, '') FROM OSCODEM  "
                       " WHERE ICUST = '" + str(iCust) + "' AND MCODE LIKE '51%' "
                       " GROUP BY MCODE, MCODENM, MCODE_M ")
        inheadresult = cursor.fetchall()

    # 매출
    with connection.cursor() as cursor:
        cursor.execute(" SELECT IFNULL(MCODE, ''), IFNULL(MCODENM, ''), IFNULL(MCODE_M, '') FROM OSCODEM  "
                       " WHERE ICUST = '" + str(iCust) + "' AND MCODE LIKE '41%' "
                       " GROUP BY MCODE, MCODENM, MCODE_M ")
        outheadresult = cursor.fetchall()

    # 입금
    with connection.cursor() as cursor:
        cursor.execute(" SELECT IFNULL(MCODE, ''), IFNULL(MCODENM, ''), IFNULL(MCODE_M, '') FROM OSCODEM  "
                       " WHERE ICUST = '" + str(iCust) + "' AND MCODE LIKE '43%' "
                       " GROUP BY MCODE, MCODENM, MCODE_M ")
        deheadresult = cursor.fetchall()

    # 출금
    with connection.cursor() as cursor:
        cursor.execute(" SELECT IFNULL(MCODE, ''), IFNULL(MCODENM, ''), IFNULL(MCODE_M, '') FROM OSCODEM  "
                       " WHERE ICUST = '" + str(iCust) + "' AND MCODE LIKE '53%' OR MCODE LIKE '55%' "
                       " GROUP BY MCODE, MCODENM, MCODE_M ")
        wiheadresult = cursor.fetchall()

    # 매입
    with connection.cursor() as cursor:
        cursor.execute("  SELECT     IFNULL(SUM(AA.MONTH01), 0) AS MONTH01, IFNULL(SUM(AA.MONTH02), 0) AS MONTH02, IFNULL(SUM(AA.MONTH03), 0) AS MONTH03 "
                       "           , IFNULL(SUM(AA.MONTH04), 0) AS MONTH04, IFNULL(SUM(AA.MONTH05), 0) AS MONTH05, IFNULL(SUM(AA.MONTH06), 0) AS MONTH06 "
                       "           , IFNULL(SUM(AA.MONTH07), 0) AS MONTH07, IFNULL(SUM(AA.MONTH08), 0) AS MONTH08, IFNULL(SUM(AA.MONTH09), 0) AS MONTH09 "
                       "           , IFNULL(SUM(AA.MONTH10), 0) AS MONTH10, IFNULL(SUM(AA.MONTH11), 0) AS MONTH11, IFNULL(SUM(AA.MONTH12), 0) AS MONTH12"
                       "           , AA.MCODE, AA.MCODENM, AA.GBN2, AA.YEAR "
                       " FROM "
                       "     ( SELECT        A.MCODE, B.MCODENM, B.GBN2, YEAR(ACDATE) AS YEAR "
                       "                   , (CASE WHEN MONTH(ACDATE) = '01' THEN SUM(ACAMTS) END) AS MONTH01 "
                       "                   , (CASE WHEN MONTH(ACDATE) = '02' THEN SUM(ACAMTS) END) AS MONTH02 "
                       "                   , (CASE WHEN MONTH(ACDATE) = '03' THEN SUM(ACAMTS) END) AS MONTH03 "
                       "                   , (CASE WHEN MONTH(ACDATE) = '04' THEN SUM(ACAMTS) END) AS MONTH04 "
                       "                   , (CASE WHEN MONTH(ACDATE) = '05' THEN SUM(ACAMTS) END) AS MONTH05 "
                       "                   , (CASE WHEN MONTH(ACDATE) = '06' THEN SUM(ACAMTS) END) AS MONTH06 "
                       "                   , (CASE WHEN MONTH(ACDATE) = '07' THEN SUM(ACAMTS) END) AS MONTH07 "
                       "                   , (CASE WHEN MONTH(ACDATE) = '08' THEN SUM(ACAMTS) END) AS MONTH08 "
                       "                   , (CASE WHEN MONTH(ACDATE) = '09' THEN SUM(ACAMTS) END) AS MONTH09 "
                       "                   , (CASE WHEN MONTH(ACDATE) = '10' THEN SUM(ACAMTS) END) AS MONTH10 "
                       "                   , (CASE WHEN MONTH(ACDATE) = '11' THEN SUM(ACAMTS) END) AS MONTH11 "
                       "                   , (CASE WHEN MONTH(ACDATE) = '12' THEN SUM(ACAMTS) END) AS MONTH12 "
                       "              FROM SISACCTT A "
                       "              LEFT OUTER JOIN OSCODEM B "
                       "              ON A.MCODE = B.MCODE "
                       "              WHERE YEAR(ACDATE) = '" + year + "' AND B.MCODE LIKE '51%' "
                       "              GROUP BY A.MCODE, B.MCODENM, B.GBN2, MONTH(A.ACDATE), ACDATE "
                       "              ORDER BY MONTH(A.ACDATE)) AA WHERE AA.YEAR IS NOT NULL AND AA.YEAR = '" + year + "' GROUP BY AA.MCODE, AA.MCODENM, AA.GBN2, AA.YEAR ");

        mainresult = cursor.fetchall()

    # 매출
    with connection.cursor() as cursor:
        cursor.execute("  SELECT     IFNULL(SUM(AA.MONTH01), 0) AS MONTH01, IFNULL(SUM(AA.MONTH02), 0) AS MONTH02, IFNULL(SUM(AA.MONTH03), 0) AS MONTH03 "
                       "           , IFNULL(SUM(AA.MONTH04), 0) AS MONTH04, IFNULL(SUM(AA.MONTH05), 0) AS MONTH05, IFNULL(SUM(AA.MONTH06), 0) AS MONTH06 "
                       "           , IFNULL(SUM(AA.MONTH07), 0) AS MONTH07, IFNULL(SUM(AA.MONTH08), 0) AS MONTH08, IFNULL(SUM(AA.MONTH09), 0) AS MONTH09 "
                       "           , IFNULL(SUM(AA.MONTH10), 0) AS MONTH10, IFNULL(SUM(AA.MONTH11), 0) AS MONTH11, IFNULL(SUM(AA.MONTH12), 0) AS MONTH12"
                       "           , AA.MCODE, AA.MCODENM, AA.GBN2, AA.YEAR "
                       " FROM "
                       "     ( SELECT        A.MCODE, B.MCODENM, B.GBN2, YEAR(ACDATE) AS YEAR "
                       "                   , (CASE WHEN MONTH(ACDATE) = '01' THEN SUM(ACAMTS) END) AS MONTH01 "
                       "                   , (CASE WHEN MONTH(ACDATE) = '02' THEN SUM(ACAMTS) END) AS MONTH02 "
                       "                   , (CASE WHEN MONTH(ACDATE) = '03' THEN SUM(ACAMTS) END) AS MONTH03 "
                       "                   , (CASE WHEN MONTH(ACDATE) = '04' THEN SUM(ACAMTS) END) AS MONTH04 "
                       "                   , (CASE WHEN MONTH(ACDATE) = '05' THEN SUM(ACAMTS) END) AS MONTH05 "
                       "                   , (CASE WHEN MONTH(ACDATE) = '06' THEN SUM(ACAMTS) END) AS MONTH06 "
                       "                   , (CASE WHEN MONTH(ACDATE) = '07' THEN SUM(ACAMTS) END) AS MONTH07 "
                       "                   , (CASE WHEN MONTH(ACDATE) = '08' THEN SUM(ACAMTS) END) AS MONTH08 "
                       "                   , (CASE WHEN MONTH(ACDATE) = '09' THEN SUM(ACAMTS) END) AS MONTH09 "
                       "                   , (CASE WHEN MONTH(ACDATE) = '10' THEN SUM(ACAMTS) END) AS MONTH10 "
                       "                   , (CASE WHEN MONTH(ACDATE) = '11' THEN SUM(ACAMTS) END) AS MONTH11 "
                       "                   , (CASE WHEN MONTH(ACDATE) = '12' THEN SUM(ACAMTS) END) AS MONTH12 "
                       "              FROM SISACCTT A "
                       "              LEFT OUTER JOIN OSCODEM B "
                       "              ON A.MCODE = B.MCODE "
                       "              WHERE YEAR(ACDATE) = '" + year + "' AND B.MCODE LIKE '41%' "
                       "              GROUP BY A.MCODE, B.MCODENM, B.GBN2, MONTH(A.ACDATE), ACDATE "
                       "              ORDER BY MONTH(A.ACDATE)) AA WHERE AA.YEAR IS NOT NULL AND AA.YEAR = '" + year + "' GROUP BY AA.MCODE, AA.MCODENM, AA.GBN2, AA.YEAR ");

        mainresult3 = cursor.fetchall()

    # 입금
    with connection.cursor() as cursor:
        cursor.execute("  SELECT     IFNULL(SUM(AA.MONTH01), 0) AS MONTH01, IFNULL(SUM(AA.MONTH02), 0) AS MONTH02, IFNULL(SUM(AA.MONTH03), 0) AS MONTH03 "
                       "           , IFNULL(SUM(AA.MONTH04), 0) AS MONTH04, IFNULL(SUM(AA.MONTH05), 0) AS MONTH05, IFNULL(SUM(AA.MONTH06), 0) AS MONTH06 "
                       "           , IFNULL(SUM(AA.MONTH07), 0) AS MONTH07, IFNULL(SUM(AA.MONTH08), 0) AS MONTH08, IFNULL(SUM(AA.MONTH09), 0) AS MONTH09 "
                       "           , IFNULL(SUM(AA.MONTH10), 0) AS MONTH10, IFNULL(SUM(AA.MONTH11), 0) AS MONTH11, IFNULL(SUM(AA.MONTH12), 0) AS MONTH12"
                       "           , AA.MCODE, AA.MCODENM, AA.GBN2, AA.YEAR "
                       " FROM "
                       "     ( SELECT        A.MCODE, B.MCODENM, B.GBN2, YEAR(ACDATE) AS YEAR "
                       "                   , (CASE WHEN MONTH(ACDATE) = '01' THEN SUM(ACAMTS) END) AS MONTH01 "
                       "                   , (CASE WHEN MONTH(ACDATE) = '02' THEN SUM(ACAMTS) END) AS MONTH02 "
                       "                   , (CASE WHEN MONTH(ACDATE) = '03' THEN SUM(ACAMTS) END) AS MONTH03 "
                       "                   , (CASE WHEN MONTH(ACDATE) = '04' THEN SUM(ACAMTS) END) AS MONTH04 "
                       "                   , (CASE WHEN MONTH(ACDATE) = '05' THEN SUM(ACAMTS) END) AS MONTH05 "
                       "                   , (CASE WHEN MONTH(ACDATE) = '06' THEN SUM(ACAMTS) END) AS MONTH06 "
                       "                   , (CASE WHEN MONTH(ACDATE) = '07' THEN SUM(ACAMTS) END) AS MONTH07 "
                       "                   , (CASE WHEN MONTH(ACDATE) = '08' THEN SUM(ACAMTS) END) AS MONTH08 "
                       "                   , (CASE WHEN MONTH(ACDATE) = '09' THEN SUM(ACAMTS) END) AS MONTH09 "
                       "                   , (CASE WHEN MONTH(ACDATE) = '10' THEN SUM(ACAMTS) END) AS MONTH10 "
                       "                   , (CASE WHEN MONTH(ACDATE) = '11' THEN SUM(ACAMTS) END) AS MONTH11 "
                       "                   , (CASE WHEN MONTH(ACDATE) = '12' THEN SUM(ACAMTS) END) AS MONTH12 "
                       "              FROM SISACCTT A "
                       "              LEFT OUTER JOIN OSCODEM B "
                       "              ON A.MCODE = B.MCODE "
                       "              WHERE YEAR(ACDATE) = '" + year + "' AND B.MCODE LIKE '43%' "
                       "              GROUP BY A.MCODE, B.MCODENM, B.GBN2, MONTH(A.ACDATE), ACDATE "
                       "              ORDER BY MONTH(A.ACDATE)) AA WHERE AA.YEAR IS NOT NULL AND AA.YEAR = '" + year + "' GROUP BY AA.MCODE, AA.MCODENM, AA.GBN2, AA.YEAR ");

        mainresult2 = cursor.fetchall()

    # 출금
    with connection.cursor() as cursor:
        cursor.execute("  SELECT     IFNULL(SUM(AA.MONTH01), 0) AS MONTH01, IFNULL(SUM(AA.MONTH02), 0) AS MONTH02, IFNULL(SUM(AA.MONTH03), 0) AS MONTH03 "
                       "           , IFNULL(SUM(AA.MONTH04), 0) AS MONTH04, IFNULL(SUM(AA.MONTH05), 0) AS MONTH05, IFNULL(SUM(AA.MONTH06), 0) AS MONTH06 "
                       "           , IFNULL(SUM(AA.MONTH07), 0) AS MONTH07, IFNULL(SUM(AA.MONTH08), 0) AS MONTH08, IFNULL(SUM(AA.MONTH09), 0) AS MONTH09 "
                       "           , IFNULL(SUM(AA.MONTH10), 0) AS MONTH10, IFNULL(SUM(AA.MONTH11), 0) AS MONTH11, IFNULL(SUM(AA.MONTH12), 0) AS MONTH12"
                       "           , AA.MCODE, AA.MCODENM, AA.GBN2, AA.YEAR "
                       " FROM "
                       "     ( SELECT        A.MCODE, B.MCODENM, B.GBN2, YEAR(ACDATE) AS YEAR "
                       "                   , (CASE WHEN MONTH(ACDATE) = '01' THEN SUM(ACAMTS) END) AS MONTH01 "
                       "                   , (CASE WHEN MONTH(ACDATE) = '02' THEN SUM(ACAMTS) END) AS MONTH02 "
                       "                   , (CASE WHEN MONTH(ACDATE) = '03' THEN SUM(ACAMTS) END) AS MONTH03 "
                       "                   , (CASE WHEN MONTH(ACDATE) = '04' THEN SUM(ACAMTS) END) AS MONTH04 "
                       "                   , (CASE WHEN MONTH(ACDATE) = '05' THEN SUM(ACAMTS) END) AS MONTH05 "
                       "                   , (CASE WHEN MONTH(ACDATE) = '06' THEN SUM(ACAMTS) END) AS MONTH06 "
                       "                   , (CASE WHEN MONTH(ACDATE) = '07' THEN SUM(ACAMTS) END) AS MONTH07 "
                       "                   , (CASE WHEN MONTH(ACDATE) = '08' THEN SUM(ACAMTS) END) AS MONTH08 "
                       "                   , (CASE WHEN MONTH(ACDATE) = '09' THEN SUM(ACAMTS) END) AS MONTH09 "
                       "                   , (CASE WHEN MONTH(ACDATE) = '10' THEN SUM(ACAMTS) END) AS MONTH10 "
                       "                   , (CASE WHEN MONTH(ACDATE) = '11' THEN SUM(ACAMTS) END) AS MONTH11 "
                       "                   , (CASE WHEN MONTH(ACDATE) = '12' THEN SUM(ACAMTS) END) AS MONTH12 "
                       "              FROM SISACCTT A "
                       "              LEFT OUTER JOIN OSCODEM B "
                       "              ON A.MCODE = B.MCODE "
                       "              WHERE YEAR(ACDATE) = '" + year + "' AND B.MCODE LIKE '53%' OR B.MCODE LIKE '55%' "
                       "              GROUP BY A.MCODE, B.MCODENM, B.GBN2, MONTH(A.ACDATE), ACDATE "
                       "              ORDER BY MONTH(A.ACDATE)) AA WHERE AA.YEAR IS NOT NULL AND AA.YEAR = '" + year + "' GROUP BY AA.MCODE, AA.MCODENM, AA.GBN2, AA.YEAR ");

        mainresult4 = cursor.fetchall()

    return JsonResponse({"headerList": headerresult, "mCodeList": mCoderesult, "inheadList": inheadresult, "outheadList": outheadresult
                            , 'deheadList': deheadresult, 'wiheadList': wiheadresult
                            , 'mainList': mainresult, 'mainList2': mainresult2, "mainList3": mainresult3, "mainList4": mainresult4})