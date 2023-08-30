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
def montlyProfitLossViews(request):

    return render(request, "currentstate/profit-loss-sheet.html")


def montlyProfitLossViews_search(request):
    ym = request.POST.get('ym')
    yyyy = request.POST.get('yyyy')
    mm = request.POST.get('mm')

    with connection.cursor() as cursor:
        cursor.execute(" SELECT RESKEY, RESNAM FROM OSREFCP WHERE RECODE = 'MCD' ")
        mheadresult = cursor.fetchall()

    with connection.cursor() as cursor:
        cursor.execute("  SELECT A.MCODE_M, B.RESNAM, A.MCODE, A.MCODENM FROM OSCODEM A "
                       " LEFT OUTER JOIN OSREFCP B "
                       " ON A.MCODE_M = B.RESKEY "
                       " AND B.RECODE = 'MCD' ")
        headresult = cursor.fetchall()

    with connection.cursor() as cursor:
        cursor.execute(" SELECT IFNULL(AA.MCODE_M, ''), IFNULL(AA.RESNAM, '')"
                       "        , IFNULL(AA.OPT, ''), IFNULL(AA.MCODENM, '')"
                       "        , IFNULL(SUM(AA.TOTAL), 0), IFNULL(AVG(AA.AVG), 0)  "
                       " FROM ( "
                       "     SELECT B.MCODE_M, C.RESNAM, A.OPT, B.MCODENM, SUM(A.AMTS) AS TOTAL, AVG(A.AMTS) AS AVG "
                       "     FROM OSBILL A "
                       "     LEFT OUTER JOIN OSCODEM B "
                       "     ON A.OPT = B.MCODE "
                       "     LEFT OUTER JOIN OSREFCP C "
                       "     ON B.MCODE_M = C.RESKEY "
                       "     AND C.RECODE = 'MCD' "
                       "     WHERE A.OPT LIKE '5%' "
                       "     AND YEAR(A.BAL_DD) = '" + yyyy + "' AND MONTH(A.BAL_DD) = '" + mm + "' "
                       "     GROUP BY A.OPT, B.MCODE_M, C.RESNAM, B.MCODENM "
                       "     UNION ALL "
                       "     SELECT B.MCODE_M, C.RESNAM, A.OPT, B.MCODENM, SUM(A.AMTS) AS TOTAL, AVG(A.AMTS) AS AVG "
                       "     FROM OSBILL A "
                       "     LEFT OUTER JOIN OSCODEM B "
                       "     ON A.OPT = B.MCODE "
                       "     LEFT OUTER JOIN OSREFCP C "
                       "     ON B.MCODE_M = C.RESKEY "
                       "     AND C.RECODE = 'MCD' "
                       "     WHERE A.OPT LIKE '4%' "
                       "     AND YEAR(A.BAL_DD) = '" + yyyy + "' AND MONTH(A.BAL_DD) = '" + mm + "' "
                       "     GROUP BY A.OPT, B.MCODE_M, C.RESNAM, B.MCODENM "
                       "     UNION ALL "
                       "     SELECT B.MCODE_M, C.RESNAM, A.MCODE, B.MCODENM, SUM(A.ACAMTS) AS TOTAL, AVG(A.ACAMTS) AS AVG "
                       "     FROM SISACCTT A "
                       "     LEFT OUTER JOIN OSCODEM B "
                       "     ON A.MCODE = B.MCODE "
                       "     LEFT OUTER JOIN OSREFCP C "
                       "     ON B.MCODE_M = C.RESKEY "
                       "     AND C.RECODE = 'MCD' "
                       "     WHERE A.MCODE LIKE '5%' "
                       "     AND YEAR(A.ACDATE) = '" + yyyy + "' AND MONTH(A.ACDATE) = '" + mm + "' "
                       "     GROUP BY A.MCODE, B.MCODE_M, C.RESNAM, B.MCODENM "
                       "     UNION ALL "
                       "     SELECT B.MCODE_M, C.RESNAM, A.MCODE, B.MCODENM, SUM(A.ACAMTS) AS TOTAL, AVG(A.ACAMTS) AS AVG "
                       "     FROM SISACCTT A "
                       "     LEFT OUTER JOIN OSCODEM B "
                       "     ON A.MCODE = B.MCODE "
                       "     LEFT OUTER JOIN OSREFCP C "
                       "     ON B.MCODE_M = C.RESKEY "
                       "     AND C.RECODE = 'MCD' "
                       "     WHERE A.MCODE LIKE '4%' "
                       "     AND YEAR(A.ACDATE) = '" + yyyy + "' AND MONTH(A.ACDATE) = '" + mm + "' "
                       "     GROUP BY A.MCODE, B.MCODE_M, C.RESNAM, B.MCODENM "
                       "    ) AA  "
                       " GROUP BY AA.MCODE_M, AA.RESNAM, AA.OPT, AA.MCODENM ")
        mainresult = cursor.fetchall()
        print(mainresult)

    return JsonResponse({'mheadList': mheadresult, 'headList': headresult, 'mainList': mainresult})