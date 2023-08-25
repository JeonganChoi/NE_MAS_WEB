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

# 내역별
def breakdownBalanceViews(request):

    return render(request, "currentstate/breakdown-sheet.html")

def breakdownBalanceViews_search(request):
    date = request.POST.get('date')

    with connection.cursor() as cursor:
        cursor.execute(" SELECT RESKEY, RESNAM FROM OSREFCP WHERE RECODE = 'BNK' ")
        headresult = cursor.fetchall()
        mainList = []

    with connection.cursor() as cursor:
        cursor.execute(" SELECT B.ACBKCD, IFNULL(SUM(A.ACAMTS), 0) "
                       " FROM SISACCTT A "
                       " LEFT OUTER JOIN ACNUMBER B "
                       " ON A.ACACNUMBER = B.ACNUMBER "
                       " WHERE A.ACDATE > '" + date + "' "
                       " GROUP BY B.ACBKCD "
                       " ORDER BY B.ACBKCD ASC ")
        mainresult = cursor.fetchall()

        # for i in range(len(headresult)):
        #     bnkCode = headresult[i][0]
        #     with connection.cursor() as cursor:
        #         cursor.execute(" SELECT B.ACBKCD, IFNULL(SUM(A.ACAMTS), 0) "
        #                        " FROM SISACCTT A "
        #                        " LEFT OUTER JOIN ACNUMBER B "
        #                        " ON A.ACACNUMBER = B.ACNUMBER "
        #                        " WHERE B.ACBKCD = '" + bnkCode + "' "
        #                        " AND A.ACDATE > '" + date + "' "
        #                        " GROUP BY B.ACBKCD ")
        #         mainresult = cursor.fetchall()
        #         mainList += [mainresult]
        #         print(mainList)

        return JsonResponse({"headList": headresult, 'mainList': mainresult})