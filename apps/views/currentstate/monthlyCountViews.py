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

    with connection.cursor() as cursor:
        cursor.execute(" SELECT RESKEY, RESNAM FROM OSREFCP WHERE RECODE = 'AGB' ")
        headerresult = cursor.fetchall()
        print(headerresult)

    # 매입/매출
    with connection.cursor() as cursor:
        cursor.execute(" SELECT A.OPT, B.MCODENM, B.GBN2 FROM OSBILL A LEFT OUTER JOIN OSCODEM B ON A.OPT = B.MCODE "
                       "    WHERE YEAR(BAL_DD) = '" + year + "' "
                       "    GROUP BY A.OPT, B.MCODENM, B.GBN2 ")
        headresult = cursor.fetchall()
        print(headresult)

    # 입금/출금
    with connection.cursor() as cursor:
        cursor.execute(" SELECT A.MCODE, B.MCODENM, B.GBN2 FROM SISACCTT A LEFT OUTER JOIN OSCODEM B ON A.MCODE = B.MCODE"
                       "    WHERE YEAR(ACDATE) = '" + year + "' "
                       "    GROUP BY A.MCODE, B.MCODENM, B.GBN2 ")
        headresult2 = cursor.fetchall()
        print(headresult2)

    # 매입/매출
    with connection.cursor() as cursor:
        cursor.execute("SELECT    IFNULL(SUM(AA.MONTH01), 0) AS MONTH01, IFNULL(SUM(AA.MONTH02), 0) AS MONTH02, IFNULL(SUM(AA.MONTH03), 0) AS MONTH03 "
                       "        , IFNULL(SUM(AA.MONTH04), 0) AS MONTH04, IFNULL(SUM(AA.MONTH05), 0) AS MONTH05, IFNULL(SUM(AA.MONTH06), 0) AS MONTH06 "
                       "        , IFNULL(SUM(AA.MONTH07), 0) AS MONTH07, IFNULL(SUM(AA.MONTH08), 0) AS MONTH08, IFNULL(SUM(AA.MONTH09), 0) AS MONTH09 "
                       "        , IFNULL(SUM(AA.MONTH10), 0) AS MONTH10, IFNULL(SUM(AA.MONTH11), 0) AS MONTH11, IFNULL(SUM(AA.MONTH12), 0) AS MONTH12"
                       "        , AA.OPT, AA.MCODENM, AA.GBN2, AA.YEAR "
                       " FROM "
                       "     ( SELECT        A.OPT, B.MCODENM, B.GBN2, YEAR(BAL_DD) AS YEAR "
                       "                   , (CASE WHEN MONTH(BAL_DD) = '01' THEN SUM(AMTS) END) AS MONTH01 "
                       "                   , (CASE WHEN MONTH(BAL_DD) = '02' THEN SUM(AMTS) END) AS MONTH02 "
                       "                   , (CASE WHEN MONTH(BAL_DD) = '03' THEN SUM(AMTS) END) AS MONTH03 "
                       "                   , (CASE WHEN MONTH(BAL_DD) = '04' THEN SUM(AMTS) END) AS MONTH04 "
                       "                   , (CASE WHEN MONTH(BAL_DD) = '05' THEN SUM(AMTS) END) AS MONTH05 "
                       "                   , (CASE WHEN MONTH(BAL_DD) = '06' THEN SUM(AMTS) END) AS MONTH06 "
                       "                   , (CASE WHEN MONTH(BAL_DD) = '07' THEN SUM(AMTS) END) AS MONTH07 "
                       "                   , (CASE WHEN MONTH(BAL_DD) = '08' THEN SUM(AMTS) END) AS MONTH08 "
                       "                   , (CASE WHEN MONTH(BAL_DD) = '09' THEN SUM(AMTS) END) AS MONTH09 "
                       "                   , (CASE WHEN MONTH(BAL_DD) = '10' THEN SUM(AMTS) END) AS MONTH10 "
                       "                   , (CASE WHEN MONTH(BAL_DD) = '11' THEN SUM(AMTS) END) AS MONTH11 "
                       "                   , (CASE WHEN MONTH(BAL_DD) = '12' THEN SUM(AMTS) END) AS MONTH12 "
                       "              FROM OSBILL A "
                       "              LEFT OUTER JOIN OSCODEM B "
                       "              ON A.OPT = B.MCODE "
                       "              WHERE YEAR(BAL_DD) = '" + year + "' "
                       "              GROUP BY A.OPT, B.MCODENM, B.GBN2, MONTH(A.BAL_DD), BAL_DD "
                       "              ORDER BY MONTH(A.BAL_DD)) AA WHERE AA.YEAR IS NOT NULL AND AA.YEAR = '" + year + "' GROUP BY AA.OPT, AA.MCODENM, AA.GBN2, AA.YEAR ");
        mainresult = cursor.fetchall()
        print(mainresult)

    # 입금/출금
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
                       "              WHERE YEAR(ACDATE) = '" + year + "' "
                       "              GROUP BY A.MCODE, B.MCODENM, B.GBN2, MONTH(A.ACDATE), ACDATE "
                       "              ORDER BY MONTH(A.ACDATE)) AA WHERE AA.YEAR IS NOT NULL AND AA.YEAR = '" + year + "' GROUP BY AA.MCODE, AA.MCODENM, AA.GBN2, AA.YEAR ");

        mainresult2 = cursor.fetchall()
        print(mainresult2)

    return JsonResponse({"headerList": headerresult, "headList": headresult, 'headList2': headresult2, 'mainList': mainresult, 'mainList2': mainresult2})