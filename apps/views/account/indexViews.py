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
from datetime import datetime

def buySale_index(request):
    now = datetime.now()
    year = now.year
    nowDate = now.date()
    newYear = request.POST.get('newYear')
    user = request.session.get('userId')
    iCust = request.session.get('USER_ICUST')

    sum = str(nowDate).replace("-", "")
    sum = sum[:6]
    sum = int(sum) + 1
    for i in range(12):
        sum = int(sum) - 1
        print(sum)
        with connection.cursor() as cursor:
            cursor.execute(" SELECT SUM(ACAMTS), YEAR(ACDATE), MONTH(ACDATE) FROM SISACCTT "
                           "    WHERE SUBSTRING(ACDATE, 0, 6) BETWEEN '" + str(sum) + "'  "
                           "    AND MCODE LIKE '41%' AND ICUST = '" + str(iCust) + "' "
                           "    GROUP BY MONTH(ACDATE), YEAR(ACDATE) ")
            buyresult = cursor.fetchall()
            itembomlist2 = []

            for i in range(len(buyresult)):
                itembomlist = [buyresult[i][0], buyresult[i][1], buyresult[i][2]]
                itembomlist2 += [itembomlist]
    print(itembomlist2)

    with connection.cursor() as cursor:
        cursor.execute(" SELECT IFNULL(SUM(MONTH01), 0), IFNULL(SUM(MONTH02), 0), IFNULL(SUM(MONTH03), 0), IFNULL(SUM(MONTH04), 0) "
                       "        , IFNULL(SUM(MONTH05), 0), IFNULL(SUM(MONTH06), 0), IFNULL(SUM(MONTH07), 0), IFNULL(SUM(MONTH08), 0) "
                       "        , IFNULL(SUM(MONTH09), 0), IFNULL(SUM(MONTH10), 0), IFNULL(SUM(MONTH11), 0), IFNULL(SUM(MONTH12), 0) "
                       " FROM ( "
                       " SELECT (CASE WHEN MONTH(ACDATE) = '01' THEN SUM(ACAMTS) END) AS MONTH01 "
                       "       , (CASE WHEN MONTH(ACDATE) = '02' THEN SUM(ACAMTS) END) AS MONTH02 "
                       "       , (CASE WHEN MONTH(ACDATE) = '03' THEN SUM(ACAMTS) END) AS MONTH03 "
                       "       , (CASE WHEN MONTH(ACDATE) = '04' THEN SUM(ACAMTS) END) AS MONTH04 "
                       "       , (CASE WHEN MONTH(ACDATE) = '05' THEN SUM(ACAMTS) END) AS MONTH05 "
                       "       , (CASE WHEN MONTH(ACDATE) = '06' THEN SUM(ACAMTS) END) AS MONTH06 "
                       "       , (CASE WHEN MONTH(ACDATE) = '07' THEN SUM(ACAMTS) END) AS MONTH07 "
                       "       , (CASE WHEN MONTH(ACDATE) = '08' THEN SUM(ACAMTS) END) AS MONTH08 "
                       "       , (CASE WHEN MONTH(ACDATE) = '09' THEN SUM(ACAMTS) END) AS MONTH09 "
                       "       , (CASE WHEN MONTH(ACDATE) = '10' THEN SUM(ACAMTS) END) AS MONTH10 "
                       "       , (CASE WHEN MONTH(ACDATE) = '11' THEN SUM(ACAMTS) END) AS MONTH11 "
                       "       , (CASE WHEN MONTH(ACDATE) = '12' THEN SUM(ACAMTS) END) AS MONTH12 "
                       " FROM SISACCTT "
                       " WHERE YEAR(ACDATE) = '" + str(year) + "' "
                       " AND MCODE LIKE '51%' "
                       " GROUP BY ACDATE) AA ")
        buyresult = cursor.fetchall()

    with connection.cursor() as cursor:
        cursor.execute(" SELECT IFNULL(SUM(MONTH01), 0), IFNULL(SUM(MONTH02), 0), IFNULL(SUM(MONTH03), 0), IFNULL(SUM(MONTH04), 0) "
                       "        , IFNULL(SUM(MONTH05), 0), IFNULL(SUM(MONTH06), 0), IFNULL(SUM(MONTH07), 0), IFNULL(SUM(MONTH08), 0) "
                       "        , IFNULL(SUM(MONTH09), 0), IFNULL(SUM(MONTH10), 0), IFNULL(SUM(MONTH11), 0), IFNULL(SUM(MONTH12), 0) "
                       " FROM ( "
                       " SELECT (CASE WHEN MONTH(ACDATE) = '01' THEN SUM(ACAMTS) END) AS MONTH01 "
                       "       , (CASE WHEN MONTH(ACDATE) = '02' THEN SUM(ACAMTS) END) AS MONTH02 "
                       "       , (CASE WHEN MONTH(ACDATE) = '03' THEN SUM(ACAMTS) END) AS MONTH03 "
                       "       , (CASE WHEN MONTH(ACDATE) = '04' THEN SUM(ACAMTS) END) AS MONTH04 "
                       "       , (CASE WHEN MONTH(ACDATE) = '05' THEN SUM(ACAMTS) END) AS MONTH05 "
                       "       , (CASE WHEN MONTH(ACDATE) = '06' THEN SUM(ACAMTS) END) AS MONTH06 "
                       "       , (CASE WHEN MONTH(ACDATE) = '07' THEN SUM(ACAMTS) END) AS MONTH07 "
                       "       , (CASE WHEN MONTH(ACDATE) = '08' THEN SUM(ACAMTS) END) AS MONTH08 "
                       "       , (CASE WHEN MONTH(ACDATE) = '09' THEN SUM(ACAMTS) END) AS MONTH09 "
                       "       , (CASE WHEN MONTH(ACDATE) = '10' THEN SUM(ACAMTS) END) AS MONTH10 "
                       "       , (CASE WHEN MONTH(ACDATE) = '11' THEN SUM(ACAMTS) END) AS MONTH11 "
                       "       , (CASE WHEN MONTH(ACDATE) = '12' THEN SUM(ACAMTS) END) AS MONTH12 "
                       " FROM SISACCTT "
                       " WHERE YEAR(ACDATE) = '" + str(year) + "' "
                       " AND MCODE LIKE '41%' "
                       " GROUP BY ACDATE) AA ")
        saleresult = cursor.fetchall()

    with connection.cursor() as cursor:
        cursor.execute(" SELECT SUM(B.ACAMTS), A.MCODE_M FROM OSCODEM A "
                        " LEFT OUTER JOIN SISACCTT B "
                        " ON A.MCODE AND B.MCODE "
                        " WHERE YEAR(B.ACDATE) = '" + str(year) + "' "
                        " AND A.MCODE_M LIKE '4%' OR A.MCODE_M LIKE '5%' "
                        " GROUP BY A.MCODE_M ")
        pieresult = cursor.fetchall()

    return JsonResponse({"buyList": buyresult, "saleList": saleresult, "pieList": pieresult, "itembomlist2": itembomlist2})

# cursor.execute(" SELECT SUM(ACAMTS), YEAR(ACDATE), MONTH(ACDATE) FROM SISACCTT "
#                "    WHERE ACDATE BETWEEN '" + str(newYear).replace("-", "") + "' AND '" + str(nowDate).replace("-", "") + "' "
#                "    AND MCODE LIKE '41%' "
#                "    GROUP BY MONTH(ACDATE), YEAR(ACDATE) ")


# cursor.execute(" SELECT SUM(ACAMTS), YEAR(ACDATE), MONTH(ACDATE) FROM SISACCTT "
#                "    WHERE ACDATE BETWEEN '" + str(newYear).replace("-", "") + "' AND '" + str(nowDate).replace("-", "") + "' "
#                "    AND MCODE LIKE '51%' "
#                "    GROUP BY MONTH(ACDATE), YEAR(ACDATE) ")


