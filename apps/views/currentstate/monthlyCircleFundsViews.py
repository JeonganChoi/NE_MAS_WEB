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

    return render(request, "currentstate/monthly-circulate-fundsReport.html")

def montlyCircleFundsViews_search(request):
    year = request.POST.get('Year')
    gbn = request.POST.get('gbn')

    if gbn == '1':
        with connection.cursor() as cursor:
            cursor.execute(" SELECT UP_CODE, CUST_NME "
                            "        , IFNULL(SUM(MONTH01), 0), IFNULL(SUM(MONTH01_IN), 0), IFNULL(SUM(MONTH02), 0), IFNULL(SUM(MONTH02_IN), 0) "
                            "        , IFNULL(SUM(MONTH03), 0), IFNULL(SUM(MONTH03_IN), 0), IFNULL(SUM(MONTH04), 0), IFNULL(SUM(MONTH04_IN), 0) "
                            "        , IFNULL(SUM(MONTH05), 0), IFNULL(SUM(MONTH05_IN), 0), IFNULL(SUM(MONTH06), 0), IFNULL(SUM(MONTH06_IN), 0) "
                            "        , IFNULL(SUM(MONTH07), 0), IFNULL(SUM(MONTH07_IN), 0), IFNULL(SUM(MONTH08), 0), IFNULL(SUM(MONTH08_IN), 0) "
                            "        , IFNULL(SUM(MONTH09), 0), IFNULL(SUM(MONTH09_IN), 0), IFNULL(SUM(MONTH10), 0), IFNULL(SUM(MONTH10_IN), 0) "
                            "        , IFNULL(SUM(MONTH11), 0), IFNULL(SUM(MONTH11_IN), 0), IFNULL(SUM(MONTH12), 0), IFNULL(SUM(MONTH12_IN), 0) "
                            "    FROM( "
                            "    SELECT A.UP_CODE AS UP_CODE, B.CUST_NME AS CUST_NME "
                            "          , (CASE WHEN MONTH(A.BAL_DD) = '01' THEN SUM(A.AMTS) END) AS MONTH01 "
                            "          , 0 AS MONTH01_IN "
                            "          , (CASE WHEN MONTH(A.BAL_DD) = '02' THEN SUM(A.AMTS) END) AS MONTH02 "
                            "          , 0 AS MONTH02_IN "
                            "          , (CASE WHEN MONTH(A.BAL_DD) = '03' THEN SUM(A.AMTS) END) AS MONTH03 "
                            "          , 0 AS MONTH03_IN "
                            "          , (CASE WHEN MONTH(A.BAL_DD) = '04' THEN SUM(A.AMTS) END) AS MONTH04 "
                            "          , 0 AS MONTH04_IN "
                            "          , (CASE WHEN MONTH(A.BAL_DD) = '05' THEN SUM(A.AMTS) END) AS MONTH05 "
                            "          , 0 AS MONTH05_IN "
                            "          , (CASE WHEN MONTH(A.BAL_DD) = '06' THEN SUM(A.AMTS) END) AS MONTH06 "
                            "          , 0 AS MONTH06_IN "
                            "          , (CASE WHEN MONTH(A.BAL_DD) = '07' THEN SUM(A.AMTS) END) AS MONTH07 "
                            "          , 0 AS MONTH07_IN "
                            "          , (CASE WHEN MONTH(A.BAL_DD) = '08' THEN SUM(A.AMTS) END) AS MONTH08 "
                            "          , 0 AS MONTH08_IN "
                            "          , (CASE WHEN MONTH(A.BAL_DD) = '09' THEN SUM(A.AMTS) END) AS MONTH09 "
                            "          , 0 AS MONTH09_IN "
                            "          , (CASE WHEN MONTH(A.BAL_DD) = '10' THEN SUM(A.AMTS) END) AS MONTH10 "
                            "          , 0 AS MONTH10_IN "
                            "          , (CASE WHEN MONTH(A.BAL_DD) = '11' THEN SUM(A.AMTS) END) AS MONTH11 "
                            "          , 0 AS MONTH11_IN "
                            "          , (CASE WHEN MONTH(A.BAL_DD) = '12' THEN SUM(A.AMTS) END) AS MONTH12 "
                            "          , 0 AS MONTH12_IN "
                            "    FROM OSBILL A "
                            "    LEFT OUTER JOIN MIS1TB003 B "
                            "    ON A.UP_CODE = B.CUST_NBR "
                            "    WHERE YEAR(A.BAL_DD) = '" + year + "' "
                            "    AND A.GUBUN = '2' "
                            "    AND A.PAY_OPT = '2' "
                            "    GROUP BY A.UP_CODE, B.CUST_NME, A.BAL_DD "
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
                            "    WHERE YEAR(A.ACDATE) = '" + year + "' "
                            "    AND ACIOGB = '1' "
                            "    AND ACGUBN = '2' "
                            "    GROUP BY A.ACCUST, B.CUST_NME, A.ACDATE ) AA GROUP BY AA.UP_CODE, AA.CUST_NME ")
            mainresult = cursor.fetchall()
            print(mainresult)

            return JsonResponse({"mainList": mainresult})

    elif gbn == '2':
        with connection.cursor() as cursor:
            cursor.execute(" SELECT UP_CODE, CUST_NME "
                           "        , IFNULL(SUM(MONTH01), 0), IFNULL(SUM(MONTH01_IN), 0), IFNULL(SUM(MONTH02), 0), IFNULL(SUM(MONTH02_IN), 0) "
                           "        , IFNULL(SUM(MONTH03), 0), IFNULL(SUM(MONTH03_IN), 0), IFNULL(SUM(MONTH04), 0), IFNULL(SUM(MONTH04_IN), 0) "
                           "        , IFNULL(SUM(MONTH05), 0), IFNULL(SUM(MONTH05_IN), 0), IFNULL(SUM(MONTH06), 0), IFNULL(SUM(MONTH06_IN), 0) "
                           "        , IFNULL(SUM(MONTH07), 0), IFNULL(SUM(MONTH07_IN), 0), IFNULL(SUM(MONTH08), 0), IFNULL(SUM(MONTH08_IN), 0) "
                           "        , IFNULL(SUM(MONTH09), 0), IFNULL(SUM(MONTH09_IN), 0), IFNULL(SUM(MONTH10), 0), IFNULL(SUM(MONTH10_IN), 0) "
                           "        , IFNULL(SUM(MONTH11), 0), IFNULL(SUM(MONTH11_IN), 0), IFNULL(SUM(MONTH12), 0), IFNULL(SUM(MONTH12_IN), 0) "
                           "    FROM( "
                           "    SELECT A.UP_CODE AS UP_CODE, B.CUST_NME AS CUST_NME "
                           "          , (CASE WHEN MONTH(A.BAL_DD) = '01' THEN SUM(A.AMTS) END) AS MONTH01 "
                           "          , 0 AS MONTH01_IN "
                           "          , (CASE WHEN MONTH(A.BAL_DD) = '02' THEN SUM(A.AMTS) END) AS MONTH02 "
                           "          , 0 AS MONTH02_IN "
                           "          , (CASE WHEN MONTH(A.BAL_DD) = '03' THEN SUM(A.AMTS) END) AS MONTH03 "
                           "          , 0 AS MONTH03_IN "
                           "          , (CASE WHEN MONTH(A.BAL_DD) = '04' THEN SUM(A.AMTS) END) AS MONTH04 "
                           "          , 0 AS MONTH04_IN "
                           "          , (CASE WHEN MONTH(A.BAL_DD) = '05' THEN SUM(A.AMTS) END) AS MONTH05 "
                           "          , 0 AS MONTH05_IN "
                           "          , (CASE WHEN MONTH(A.BAL_DD) = '06' THEN SUM(A.AMTS) END) AS MONTH06 "
                           "          , 0 AS MONTH06_IN "
                           "          , (CASE WHEN MONTH(A.BAL_DD) = '07' THEN SUM(A.AMTS) END) AS MONTH07 "
                           "          , 0 AS MONTH07_IN "
                           "          , (CASE WHEN MONTH(A.BAL_DD) = '08' THEN SUM(A.AMTS) END) AS MONTH08 "
                           "          , 0 AS MONTH08_IN "
                           "          , (CASE WHEN MONTH(A.BAL_DD) = '09' THEN SUM(A.AMTS) END) AS MONTH09 "
                           "          , 0 AS MONTH09_IN "
                           "          , (CASE WHEN MONTH(A.BAL_DD) = '10' THEN SUM(A.AMTS) END) AS MONTH10 "
                           "          , 0 AS MONTH10_IN "
                           "          , (CASE WHEN MONTH(A.BAL_DD) = '11' THEN SUM(A.AMTS) END) AS MONTH11 "
                           "          , 0 AS MONTH11_IN "
                           "          , (CASE WHEN MONTH(A.BAL_DD) = '12' THEN SUM(A.AMTS) END) AS MONTH12 "
                           "          , 0 AS MONTH12_IN "
                           "    FROM OSBILL A "
                           "    LEFT OUTER JOIN MIS1TB003 B "
                           "    ON A.UP_CODE = B.CUST_NBR "
                           "    WHERE YEAR(A.BAL_DD) = '" + year + "' "
                           "    AND A.GUBUN = '1' "
                           "    AND A.PAY_OPT = '2' "
                           "    GROUP BY A.UP_CODE, B.CUST_NME, A.BAL_DD "
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
                           "    WHERE YEAR(A.ACDATE) = '" + year + "' "
                           "    AND ACIOGB = '2' "
                           "    AND ACGUBN = '2' "
                           "    GROUP BY A.ACCUST, B.CUST_NME, A.ACDATE ) AA GROUP BY AA.UP_CODE, AA.CUST_NME ")
            mainresult = cursor.fetchall()
            print(mainresult)

            return JsonResponse({"mainList": mainresult})