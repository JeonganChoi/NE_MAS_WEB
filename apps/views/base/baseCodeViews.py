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


def baseCodeViews(request):

    return render(request, "base/base-code.html")

def baseCodeViews_search(request):
    mainCode = request.POST.get('mainCode')
    iCust = request.session.get('USER_ICUST')

    if mainCode is not None and mainCode != '':
        with connection.cursor() as cursor:
            cursor.execute(" SELECT RECODE, RECNAM, RESKEY, RESNAM FROM OSREFCP "
                           "        WHERE RECODE LIKE '%" + mainCode + "%' AND ICUST = '" + str(iCust) + "' ")
            subresult = cursor.fetchall()

        return JsonResponse({"subList": subresult})

    else:
        with connection.cursor() as cursor:
            cursor.execute(" SELECT RECODE, RECNAM FROM OSREFCP WHERE ICUST = '" + str(iCust) + "' "
                           "        AND RECODE != 'UST' AND RECODE != 'MOP' AND RECODE != 'EOC' "
                           "        GROUP BY RECODE, RECNAM "
                           "        ORDER BY RECODE ")
            mainresult = cursor.fetchall()

        return JsonResponse({"mainList": mainresult})

# 저장 및 업데이트
def baseCodeViews_save(request):
    iCust = request.session.get('USER_ICUST')

    print(request.POST.getlist('subCode'))
    reskey_list = request.POST.getlist('subCode')
    recode_list = request.POST.getlist('mainCode')
    recnam_list = request.POST.getlist('mainName')
    resnam_list = request.POST.getlist('subName')

    for r in range(len(reskey_list)):
        RESKEY = reskey_list[r]
        RESNAM = resnam_list[r]
        RECODE = recode_list[r]
        RECNAM = recnam_list[r]

        with connection.cursor() as cursor:
            cursor.execute(" SELECT RESKEY FROM OSREFCP WHERE RECODE = '" + str(RECODE) + "' AND RESKEY = '" + str(RESKEY) + "' ")
            result = cursor.fetchall()

        if result:
            with connection.cursor() as cursor:
                cursor.execute(" UPDATE OSREFCP SET "
                               "      RECNAM = '" + str(RECNAM) + "' "
                               "    , RESNAM = '" + str(RESNAM) + "' "
                               " WHERE RECODE = '" + str(RECODE) + "' "
                               " AND RESKEY = '" + str(RESKEY) + "' "
                               " AND ICUST = '" + str(iCust) + "'"
                               )
                connection.commit()
        else:
            with connection.cursor() as cursor:
                cursor.execute("INSERT INTO OSREFCP "
                               "("
                               "    RESKEY"
                               "    , RECODE"
                               "    , RECNAM"
                               "    , RESNAM"
                               "    , ICUST"
                               ") "
                               "VALUES"
                               "("
                               "    '" + str(RESKEY) + "'"
                               "    , '" + str(RECODE) + "'"
                               "    , '" + str(RECNAM) + "'"
                               "    , '" + str(RESNAM) + "'"
                               "    , '" + str(iCust) + "'"
                               ")"
                               )
                connection.commit()

    return render(request, 'base/base-code.html')


def baseCodeViews_dlt(request):
    iCust = request.session.get('USER_ICUST')

    if request.method == "POST":
        dataList = json.loads(request.POST.get('arrList'))
        print(dataList)
        for code in dataList:
            acc_split_list = code.split(',')
            with connection.cursor() as cursor:
                cursor.execute(" DELETE FROM OSREFCP WHERE RECODE = '" + acc_split_list[0] + "' "
                               "                         AND RESKEY = '" + acc_split_list[1] + "' "
                               "                         AND ICUST = '" + str(iCust) + "'")
                connection.commit()

        return JsonResponse({'sucYn': "Y"})

    else:
        return render(request, 'base/base-code.html')