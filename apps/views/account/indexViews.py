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
    nowDate = now.date()
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
                           "    WHERE SUBSTRING(ACDATE, 1, 6) = '" + str(sum) + "' "
                           "    AND MCODE LIKE '51%' "
                           "    GROUP BY MONTH(ACDATE), YEAR(ACDATE) ")
            buyresult = cursor.fetchall()


    with connection.cursor() as cursor:
        cursor.execute(" SELECT SUM(ACAMTS), YEAR(ACDATE), MONTH(ACDATE) FROM SISACCTT "
                       "    WHERE ACDATE BETWEEN '20230101' AND '" + str(nowDate).replace("-", "") + "' "
                       "    AND MCODE LIKE '41%' "
                       "    GROUP BY MONTH(ACDATE), YEAR(ACDATE) ")
        saleresult = cursor.fetchall()

    with connection.cursor() as cursor:
        cursor.execute(" SELECT SUM(B.ACAMTS), A.MCODE_M FROM OSCODEM A "
                        " LEFT OUTER JOIN SISACCTT B "
                        " ON A.MCODE AND B.MCODE "
                        " WHERE B.ACDATE BETWEEN '20230101' AND '" + str(nowDate).replace("-", "") + "' "
                        " AND A.MCODE_M LIKE '4%' OR A.MCODE_M LIKE '5%' "
                        " GROUP BY A.MCODE_M ")
        pieresult = cursor.fetchall()

    return JsonResponse({"buyList": buyresult, "saleList": saleresult, "pieList": pieresult})