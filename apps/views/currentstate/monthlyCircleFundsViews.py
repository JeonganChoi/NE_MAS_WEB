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
def montlyCircleFundsViews(request):
    userId = request.session.get('userId')
    if userId == '' or userId is None:
        return redirect("/page-404/")
    else:
        return render(request, "currentstate/monthly-circulate-fundsReport.html")

def montlyCircleFundsViews_search(request):
    year = request.POST.get('Year')
    iCust = request.session.get("USER_ICUST")

    # 매출/ 입금
    with connection.cursor() as cursor:
        cursor.execute(" SELECT IFNULL(ACCUST, ''), IFNULL(CUST_NME, '') "
                       "        , IFNULL(SUM(MONTH01), 0), IFNULL(SUM(MONTH01_IN), 0), IFNULL(SUM(MONTH02), 0), IFNULL(SUM(MONTH02_IN), 0) "
                       "        , IFNULL(SUM(MONTH03), 0), IFNULL(SUM(MONTH03_IN), 0), IFNULL(SUM(MONTH04), 0), IFNULL(SUM(MONTH04_IN), 0) "
                       "        , IFNULL(SUM(MONTH05), 0), IFNULL(SUM(MONTH05_IN), 0), IFNULL(SUM(MONTH06), 0), IFNULL(SUM(MONTH06_IN), 0) "
                       "        , IFNULL(SUM(MONTH07), 0), IFNULL(SUM(MONTH07_IN), 0), IFNULL(SUM(MONTH08), 0), IFNULL(SUM(MONTH08_IN), 0) "
                       "        , IFNULL(SUM(MONTH09), 0), IFNULL(SUM(MONTH09_IN), 0), IFNULL(SUM(MONTH10), 0), IFNULL(SUM(MONTH10_IN), 0) "
                       "        , IFNULL(SUM(MONTH11), 0), IFNULL(SUM(MONTH11_IN), 0), IFNULL(SUM(MONTH12), 0), IFNULL(SUM(MONTH12_IN), 0) "
                       "    FROM( "
                       "    SELECT A.ACCUST AS ACCUST, B.CUST_NME AS CUST_NME"
                       "          , (CASE WHEN MONTH(A.ACDATE) = '01' THEN SUM(A.ACAMTS) END) AS MONTH01 "
                       "          , 0 AS MONTH01_IN "
                       "          , (CASE WHEN MONTH(A.ACDATE) = '02' THEN SUM(A.ACAMTS) END) AS MONTH02 "
                       "          , 0 AS MONTH02_IN "
                       "          , (CASE WHEN MONTH(A.ACDATE) = '03' THEN SUM(A.ACAMTS) END) AS MONTH03 "
                       "          , 0 AS MONTH03_IN "
                       "          , (CASE WHEN MONTH(A.ACDATE) = '04' THEN SUM(A.ACAMTS) END) AS MONTH04 "
                       "          , 0 AS MONTH04_IN "
                       "          , (CASE WHEN MONTH(A.ACDATE) = '05' THEN SUM(A.ACAMTS) END) AS MONTH05 "
                       "          , 0 AS MONTH05_IN "
                       "          , (CASE WHEN MONTH(A.ACDATE) = '06' THEN SUM(A.ACAMTS) END) AS MONTH06 "
                       "          , 0 AS MONTH06_IN "
                       "          , (CASE WHEN MONTH(A.ACDATE) = '07' THEN SUM(A.ACAMTS) END) AS MONTH07 "
                       "          , 0 AS MONTH07_IN "
                       "          , (CASE WHEN MONTH(A.ACDATE) = '08' THEN SUM(A.ACAMTS) END) AS MONTH08 "
                       "          , 0 AS MONTH08_IN "
                       "          , (CASE WHEN MONTH(A.ACDATE) = '09' THEN SUM(A.ACAMTS) END) AS MONTH09 "
                       "          , 0 AS MONTH09_IN "
                       "          , (CASE WHEN MONTH(A.ACDATE) = '10' THEN SUM(A.ACAMTS) END) AS MONTH10 "
                       "          , 0 AS MONTH10_IN "
                       "          , (CASE WHEN MONTH(A.ACDATE) = '11' THEN SUM(A.ACAMTS) END) AS MONTH11 "
                       "          , 0 AS MONTH11_IN "
                       "          , (CASE WHEN MONTH(A.ACDATE) = '12' THEN SUM(A.ACAMTS) END) AS MONTH12 "
                       "          , 0 AS MONTH12_IN "
                       "    FROM SISACCTT A "
                       "    LEFT OUTER JOIN MIS1TB003 B "
                       "    ON A.ACCUST = B.CUST_NBR "
                       "    WHERE YEAR(A.ACDATE) = '" + str(year) + "' AND A.ICUST = '" + str(iCust) + "' AND A.ACGUBN = '2'  AND A.FIN_OPT = 'Y' "
                       "    AND A.MCODE LIKE '41%' "
                       "    GROUP BY A.ACCUST, B.CUST_NME, A.ACDATE, A.FIN_OPT "
                       " UNION ALL "
                       "   SELECT A.ACCUST, B.CUST_NME "
                       "          , 0 AS MONTH01 "
                       "          , (CASE WHEN MONTH(A.ACDATE) = '01' THEN SUM(A.ACAMTS) END) AS MONTH01_IN "
                       "          , 0 AS MONTH02 "
                       "          , (CASE WHEN MONTH(A.ACDATE) = '02' THEN SUM(A.ACAMTS) END) AS MONTH02_IN "
                       "          , 0 AS MONTH03 "
                       "          , (CASE WHEN MONTH(A.ACDATE) = '03' THEN SUM(A.ACAMTS) END) AS MONTH03_IN "
                       "          , 0 AS MONTH04 "
                       "          , (CASE WHEN MONTH(A.ACDATE) = '04' THEN SUM(A.ACAMTS) END) AS MONTH04_IN "
                       "          , 0 AS MONTH05 "
                       "          , (CASE WHEN MONTH(A.ACDATE) = '05' THEN SUM(A.ACAMTS) END) AS MONTH05_IN "
                       "          , 0 AS MONTH06 "
                       "          , (CASE WHEN MONTH(A.ACDATE) = '06' THEN SUM(A.ACAMTS) END) AS MONTH06_IN "
                       "          , 0 AS MONTH07 "
                       "          , (CASE WHEN MONTH(A.ACDATE) = '07' THEN SUM(A.ACAMTS) END) AS MONTH07_IN "
                       "          , 0 AS MONTH08 "
                       "          , (CASE WHEN MONTH(A.ACDATE) = '08' THEN SUM(A.ACAMTS) END) AS MONTH08_IN "
                       "          , 0 AS MONTH09 "
                       "          , (CASE WHEN MONTH(A.ACDATE) = '09' THEN SUM(A.ACAMTS) END) AS MONTH09_IN "
                       "          , 0 AS MONTH10 "
                       "          , (CASE WHEN MONTH(A.ACDATE) = '10' THEN SUM(A.ACAMTS) END) AS MONTH10_IN "
                       "          , 0 AS MONTH11 "
                       "          , (CASE WHEN MONTH(A.ACDATE) = '11' THEN SUM(A.ACAMTS) END) AS MONTH11_IN "
                       "          , 0 AS MONTH12 "
                       "          , (CASE WHEN MONTH(A.ACDATE) = '12' THEN SUM(A.ACAMTS) END) AS MONTH12_IN "
                       "    FROM SISACCTT A "
                       "    LEFT OUTER JOIN MIS1TB003 B "
                       "    ON A.ACCUST = B.CUST_NBR "
                       "    WHERE YEAR(A.ACDATE) = '" + str(year) + "' AND A.ICUST = '" + str(iCust) + "' AND A.ACIOGB = '2' AND A.FIN_OPT = 'Y' "
                       "    AND A.MCODE LIKE '43%' "
                       "    GROUP BY A.ACCUST, B.CUST_NME, A.ACDATE, A.FIN_OPT ) AA GROUP BY AA.ACCUST, AA.CUST_NME ")
        mainresult = cursor.fetchall()

    # 매입/출금
    with connection.cursor() as cursor:
        cursor.execute(" SELECT IFNULL(ACCUST, ''), IFNULL(CUST_NME, '') "
                       "       , IFNULL(SUM(MONTH01), 0), IFNULL(SUM(MONTH01_IN), 0), IFNULL(SUM(MONTH02), 0), IFNULL(SUM(MONTH02_IN), 0) "
                       "       , IFNULL(SUM(MONTH03), 0), IFNULL(SUM(MONTH03_IN), 0), IFNULL(SUM(MONTH04), 0), IFNULL(SUM(MONTH04_IN), 0) "
                       "       , IFNULL(SUM(MONTH05), 0), IFNULL(SUM(MONTH05_IN), 0), IFNULL(SUM(MONTH06), 0), IFNULL(SUM(MONTH06_IN), 0) "
                       "       , IFNULL(SUM(MONTH07), 0), IFNULL(SUM(MONTH07_IN), 0), IFNULL(SUM(MONTH08), 0), IFNULL(SUM(MONTH08_IN), 0) "
                       "       , IFNULL(SUM(MONTH09), 0), IFNULL(SUM(MONTH09_IN), 0), IFNULL(SUM(MONTH10), 0), IFNULL(SUM(MONTH10_IN), 0) "
                       "       , IFNULL(SUM(MONTH11), 0), IFNULL(SUM(MONTH11_IN), 0), IFNULL(SUM(MONTH12), 0), IFNULL(SUM(MONTH12_IN), 0) "
                       "   FROM( "
                       "   SELECT A.ACCUST AS ACCUST, B.CUST_NME AS CUST_NME "
                       "         , (CASE WHEN MONTH(A.ACDATE) = '01' THEN SUM(A.ACAMTS) END) AS MONTH01 "
                       "         , 0 AS MONTH01_IN "
                       "         , (CASE WHEN MONTH(A.ACDATE) = '02' THEN SUM(A.ACAMTS) END) AS MONTH02 "
                       "         , 0 AS MONTH02_IN "
                       "         , (CASE WHEN MONTH(A.ACDATE) = '03' THEN SUM(A.ACAMTS) END) AS MONTH03 "
                       "         , 0 AS MONTH03_IN "
                       "         , (CASE WHEN MONTH(A.ACDATE) = '04' THEN SUM(A.ACAMTS) END) AS MONTH04 "
                       "         , 0 AS MONTH04_IN "
                       "         , (CASE WHEN MONTH(A.ACDATE) = '05' THEN SUM(A.ACAMTS) END) AS MONTH05 "
                       "         , 0 AS MONTH05_IN "
                       "         , (CASE WHEN MONTH(A.ACDATE) = '06' THEN SUM(A.ACAMTS) END) AS MONTH06 "
                       "         , 0 AS MONTH06_IN "
                       "         , (CASE WHEN MONTH(A.ACDATE) = '07' THEN SUM(A.ACAMTS) END) AS MONTH07 "
                       "         , 0 AS MONTH07_IN "
                       "         , (CASE WHEN MONTH(A.ACDATE) = '08' THEN SUM(A.ACAMTS) END) AS MONTH08 "
                       "         , 0 AS MONTH08_IN "
                       "         , (CASE WHEN MONTH(A.ACDATE) = '09' THEN SUM(A.ACAMTS) END) AS MONTH09 "
                       "         , 0 AS MONTH09_IN "
                       "         , (CASE WHEN MONTH(A.ACDATE) = '10' THEN SUM(A.ACAMTS) END) AS MONTH10 "
                       "         , 0 AS MONTH10_IN "
                       "         , (CASE WHEN MONTH(A.ACDATE) = '11' THEN SUM(A.ACAMTS) END) AS MONTH11 "
                       "         , 0 AS MONTH11_IN "
                       "         , (CASE WHEN MONTH(A.ACDATE) = '12' THEN SUM(A.ACAMTS) END) AS MONTH12 "
                       "         , 0 AS MONTH12_IN "
                       "   FROM SISACCTT A "
                       "   LEFT OUTER JOIN MIS1TB003 B "
                       "   ON A.ACCUST = B.CUST_NBR "
                       "   WHERE YEAR(A.ACDATE) = '" + str(year) + "' AND A.ICUST = '" + str(iCust) + "' AND A.ACGUBN = '2' AND A.FIN_OPT = 'Y' "
                       "   AND A.MCODE LIKE '51%' "
                       "   GROUP BY A.ACCUST, B.CUST_NME, A.ACDATE, A.FIN_OPT "
                       " UNION ALL "
                       "  SELECT A.ACCUST, B.CUST_NME "
                       "         , 0 AS MONTH01 "
                       "         , (CASE WHEN MONTH(A.ACDATE) = '01' THEN SUM(A.ACAMTS) END) AS MONTH01_IN "
                       "         , 0 AS MONTH02 "
                       "         , (CASE WHEN MONTH(A.ACDATE) = '02' THEN SUM(A.ACAMTS) END) AS MONTH02_IN "
                       "         , 0 AS MONTH03 "
                       "         , (CASE WHEN MONTH(A.ACDATE) = '03' THEN SUM(A.ACAMTS) END) AS MONTH03_IN "
                       "         , 0 AS MONTH04 "
                       "         , (CASE WHEN MONTH(A.ACDATE) = '04' THEN SUM(A.ACAMTS) END) AS MONTH04_IN "
                       "         , 0 AS MONTH05 "
                       "         , (CASE WHEN MONTH(A.ACDATE) = '05' THEN SUM(A.ACAMTS) END) AS MONTH05_IN "
                       "         , 0 AS MONTH06 "
                       "         , (CASE WHEN MONTH(A.ACDATE) = '06' THEN SUM(A.ACAMTS) END) AS MONTH06_IN "
                       "         , 0 AS MONTH07 "
                       "         , (CASE WHEN MONTH(A.ACDATE) = '07' THEN SUM(A.ACAMTS) END) AS MONTH07_IN "
                       "         , 0 AS MONTH08 "
                       "         , (CASE WHEN MONTH(A.ACDATE) = '08' THEN SUM(A.ACAMTS) END) AS MONTH08_IN "
                       "         , 0 AS MONTH09 "
                       "         , (CASE WHEN MONTH(A.ACDATE) = '09' THEN SUM(A.ACAMTS) END) AS MONTH09_IN "
                       "         , 0 AS MONTH10 "
                       "         , (CASE WHEN MONTH(A.ACDATE) = '10' THEN SUM(A.ACAMTS) END) AS MONTH10_IN "
                       "         , 0 AS MONTH11 "
                       "         , (CASE WHEN MONTH(A.ACDATE) = '11' THEN SUM(A.ACAMTS) END) AS MONTH11_IN "
                       "         , 0 AS MONTH12 "
                       "         , (CASE WHEN MONTH(A.ACDATE) = '12' THEN SUM(A.ACAMTS) END) AS MONTH12_IN "
                       "   FROM SISACCTT A "
                       "   LEFT OUTER JOIN MIS1TB003 B "
                       "   ON A.ACCUST = B.CUST_NBR "
                       "   WHERE YEAR(A.ACDATE) = '" + str(year) + "' AND A.ICUST = '" + str(iCust) + "' AND A.ACIOGB = '1' AND A.FIN_OPT = 'Y' "
                       "   AND A.MCODE LIKE '53%' OR A.MCODE LIKE '55%' "
                       "   GROUP BY A.ACCUST, B.CUST_NME, A.ACDATE, A.FIN_OPT ) AA GROUP BY AA.ACCUST, AA.CUST_NME ")
        mainresult2 = cursor.fetchall()

    # with connection.cursor() as cursor:
    #     cursor.execute(" SELECT  IFNULL(MCODE, ''), IFNULL(MCODENM, ''), IFNULL(ACGUBN, ''), IFNULL(GBN_NAME, '') "
    #                    "        , IFNULL(SUM(AA.MONTH01), 0) AS MONTH01, IFNULL(SUM(AA.MONTH02), 0) AS MONTH02, IFNULL(SUM(AA.MONTH03), 0) AS MONTH03 "
    #                    "        , IFNULL(SUM(AA.MONTH04), 0) AS MONTH04, IFNULL(SUM(AA.MONTH05), 0) AS MONTH05, IFNULL(SUM(AA.MONTH06), 0) AS MONTH06 "
    #                    "        , IFNULL(SUM(AA.MONTH07), 0) AS MONTH07, IFNULL(SUM(AA.MONTH08), 0) AS MONTH08, IFNULL(SUM(AA.MONTH09), 0) AS MONTH09 "
    #                    "        , IFNULL(SUM(AA.MONTH10), 0) AS MONTH10, IFNULL(SUM(AA.MONTH11), 0) AS MONTH11, IFNULL(SUM(AA.MONTH12), 0) AS MONTH12 "
    #                    " FROM ( "
    #                    "       SELECT A.MCODE AS MCODE, B.MCODENM AS MCODENM, A.ACGUBN AS ACGUBN, D.RESNAM AS GBN_NAME "
    #                    "           , (CASE WHEN MONTH(A.ACDATE) = '01' THEN SUM(A.ACAMTS) END) AS MONTH01 "
    #                    "           , (CASE WHEN MONTH(A.ACDATE) = '02' THEN SUM(A.ACAMTS) END) AS MONTH02 "
    #                    "           , (CASE WHEN MONTH(A.ACDATE) = '03' THEN SUM(A.ACAMTS) END) AS MONTH03 "
    #                    "           , (CASE WHEN MONTH(A.ACDATE) = '04' THEN SUM(A.ACAMTS) END) AS MONTH04 "
    #                    "           , (CASE WHEN MONTH(A.ACDATE) = '05' THEN SUM(A.ACAMTS) END) AS MONTH05 "
    #                    "           , (CASE WHEN MONTH(A.ACDATE) = '06' THEN SUM(A.ACAMTS) END) AS MONTH06 "
    #                    "           , (CASE WHEN MONTH(A.ACDATE) = '07' THEN SUM(A.ACAMTS) END) AS MONTH07 "
    #                    "           , (CASE WHEN MONTH(A.ACDATE) = '08' THEN SUM(A.ACAMTS) END) AS MONTH08 "
    #                    "           , (CASE WHEN MONTH(A.ACDATE) = '09' THEN SUM(A.ACAMTS) END) AS MONTH09 "
    #                    "           , (CASE WHEN MONTH(A.ACDATE) = '10' THEN SUM(A.ACAMTS) END) AS MONTH10 "
    #                    "           , (CASE WHEN MONTH(A.ACDATE) = '11' THEN SUM(A.ACAMTS) END) AS MONTH11 "
    #                    "           , (CASE WHEN MONTH(A.ACDATE) = '12' THEN SUM(A.ACAMTS) END) AS MONTH12 "
    #                    "        FROM SISACCTT A "
    #                    "        LEFT OUTER JOIN OSCODEM B "
    #                    "        ON A.MCODE = B.MCODE "
    #                    "        LEFT OUTER JOIN OSREFCP D "
    #                    "        ON A.ACGUBN = D.RESKEY "
    #                    "        AND D.RECODE = 'AGB' "
    #                    "        WHERE YEAR(A.ACDATE) = '" + str(year) + "' "
    #                    "    GROUP BY A.MCODE, B.MCODENM, A.ACGUBN, ACDATE, ACAMTS) AA GROUP BY MCODE, MCODENM, ACGUBN, GBN_NAME ")
    #     totalresult = cursor.fetchall()

        with connection.cursor() as cursor:
            cursor.execute(" SELECT (TOTAL + INTOTAL - OUTTOTAL) AS FINAL FROM ( "
                           " SELECT IFNULL(SUM(ACAMTS), 0) AS TOTAL, 0 AS INTOTAL, 0 AS OUTTOTAL FROM ACBALANCE WHERE YEAR(ACDATE) = '" + str(year) + "' AND ICUST = '" + str(iCust) + "' "
                           " UNION ALL "
                           " SELECT 0 AS TOTAL, IFNULL(SUM(ACAMTS), 0) AS INTOTAL, 0 AS OUTTOTAL FROM SISACCTT WHERE ICUST ='" + str(iCust) + "' AND YEAR(ACDATE) = '" + str(year) + "' AND FIN_OPT = 'Y' AND MCODE LIKE '43%'  "
                           " UNION ALL "
                           " SELECT 0 AS TOTAL, 0 AS INTOTAL, IFNULL(SUM(ACAMTS), 0) AS OUTTOTAL FROM SISACCTT WHERE ICUST ='" + str(iCust) + "' AND YEAR(ACDATE) = '" + str(year) + "' AND FIN_OPT = 'Y' AND MCODE LIKE '53%' OR MCODE LIKE '55%' "
                           " ) AA ")
            lastresult = cursor.fetchall()

        with connection.cursor() as cursor:
            cursor.execute(" SELECT IFNULL(YUD, ''), IFNULL(RESNAM, '') "
                           "      , IFNULL(SUM(MONTH01), 0), IFNULL(SUM(MONTH02), 0), IFNULL(SUM(MONTH03), 0), IFNULL(SUM(MONTH04), 0) "
                           "      , IFNULL(SUM(MONTH05), 0), IFNULL(SUM(MONTH06), 0), IFNULL(SUM(MONTH07), 0), IFNULL(SUM(MONTH08), 0) "
                           "      , IFNULL(SUM(MONTH09), 0), IFNULL(SUM(MONTH10), 0), IFNULL(SUM(MONTH11), 0), IFNULL(SUM(MONTH12), 0) "
                           " FROM "
                           "     ( "
                           " SELECT IFNULL(B.YUD, '') AS YUD, IFNULL(A.RESNAM, '') AS RESNAM "
                           "            , (CASE WHEN MONTH(C.ACDATE) = '01' AND C.FIN_OPT = 'Y' THEN SUM(C.ACAMTS) END) AS MONTH01 "
                           "            , (CASE WHEN MONTH(C.ACDATE) = '02' AND C.FIN_OPT = 'Y' THEN SUM(C.ACAMTS) END) AS MONTH02 "
                           "            , (CASE WHEN MONTH(C.ACDATE) = '03' AND C.FIN_OPT = 'Y' THEN SUM(C.ACAMTS) END) AS MONTH03 "
                           "            , (CASE WHEN MONTH(C.ACDATE) = '04' AND C.FIN_OPT = 'Y' THEN SUM(C.ACAMTS) END) AS MONTH04 "
                           "            , (CASE WHEN MONTH(C.ACDATE) = '05' AND C.FIN_OPT = 'Y' THEN SUM(C.ACAMTS) END) AS MONTH05 "
                           "            , (CASE WHEN MONTH(C.ACDATE) = '06' AND C.FIN_OPT = 'Y' THEN SUM(C.ACAMTS) END) AS MONTH06 "
                           "            , (CASE WHEN MONTH(C.ACDATE) = '07' AND C.FIN_OPT = 'Y' THEN SUM(C.ACAMTS) END) AS MONTH07 "
                           "            , (CASE WHEN MONTH(C.ACDATE) = '08' AND C.FIN_OPT = 'Y' THEN SUM(C.ACAMTS) END) AS MONTH08 "
                           "            , (CASE WHEN MONTH(C.ACDATE) = '09' AND C.FIN_OPT = 'Y' THEN SUM(C.ACAMTS) END) AS MONTH09 "
                           "            , (CASE WHEN MONTH(C.ACDATE) = '10' AND C.FIN_OPT = 'Y' THEN SUM(C.ACAMTS) END) AS MONTH10 "
                           "            , (CASE WHEN MONTH(C.ACDATE) = '11' AND C.FIN_OPT = 'Y' THEN SUM(C.ACAMTS) END) AS MONTH11 "
                           "            , (CASE WHEN MONTH(C.ACDATE) = '12' AND C.FIN_OPT = 'Y' THEN SUM(C.ACAMTS) END) AS MONTH12 "
                           " FROM OSREFCP A "
                           " LEFT OUTER JOIN OSCODEM B "
                           " ON A.RESKEY = B.YUD "
                           " AND A.RECODE = 'YUD' "
                           " LEFT OUTER JOIN SISACCTT C "
                           " ON B.MCODE = C.MCODE "
                           " AND YEAR(C.ACDATE) = '" + str(year) + "'"
                           " WHERE B.ICUST = '111' AND B.YUD != NULL OR B.YUD != '' "
                           " GROUP BY B.YUD, A.RESNAM, C.ACDATE, C.FIN_OPT "
                           " ) AA GROUP BY YUD, RESNAM ")
            totalresult = cursor.fetchall()

    return JsonResponse({"mainList": mainresult, 'mainList2': mainresult2, 'totalList': totalresult, "lastList": lastresult})





# def dailyCircleFunds_search(request):
#     month = request.POST.get('month')
#     iCust = request.session.get("USER_ICUST")
#
#     with connection.cursor() as cursor:
#         cursor.execute(" SELECT * FROM OSREFCP WHERE ICUST = '" + str(iCust) + "' ")
#         totalresult = cursor.fetchall()
#
#         return JsonResponse({"totalList": totalresult})