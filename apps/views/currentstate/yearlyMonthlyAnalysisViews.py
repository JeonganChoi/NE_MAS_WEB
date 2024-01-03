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


def yearlyMontlySales(request):
    userId = request.session.get('userId')
    if userId == '' or userId is None:
        return redirect("/page-404/")
    else:
        return render(request, "currentstate/yearlyMonthly-salesReport.html")

def yearlyMontlyPurs(request):
    userId = request.session.get('userId')
    if userId == '' or userId is None:
        return redirect("/page-404/")
    else:
        return render(request, "currentstate/yearlyMonthly-pursReport.html")

def yearlyMontlySales_search(request):
    year = request.POST.get('year')
    lastyear = request.POST.get('lastyear')

    with connection.cursor() as cursor:
        cursor.execute("    SELECT  YEAR, IFNULL(SUM(MONTH01), 0) AS MONTH01, IFNULL(SUM(MONTH02), 0) AS MONTH02, IFNULL(SUM(MONTH03), 0) AS MONTH03"
                       "                , IFNULL(SUM(MONTH04), 0) AS MONTH04, IFNULL(SUM(MONTH05), 0) AS MONTH05, IFNULL(SUM(MONTH06), 0) AS MONTH06 "
                       "                , IFNULL(SUM(MONTH07), 0) AS MONTH07, IFNULL(SUM(MONTH08), 0) AS MONTH08, IFNULL(SUM(MONTH09), 0) AS MONTH09 "
                       "                , IFNULL(SUM(MONTH10), 0) AS MONTH10, IFNULL(SUM(MONTH11), 0) AS MONTH11, IFNULL(SUM(MONTH12), 0) AS MONTH12 "
                       "   FROM "
                       "       ( SELECT        YEAR(BAL_DD) AS YEAR"
                       "                     , (CASE WHEN MONTH(BAL_DD) = '01' THEN SUM(AMTS) END) AS MONTH01 "
                       "                     , (CASE WHEN MONTH(BAL_DD) = '02' THEN SUM(AMTS) END) AS MONTH02 "
                       "                     , (CASE WHEN MONTH(BAL_DD) = '03' THEN SUM(AMTS) END) AS MONTH03 "
                       "                     , (CASE WHEN MONTH(BAL_DD) = '04' THEN SUM(AMTS) END) AS MONTH04 "
                       "                     , (CASE WHEN MONTH(BAL_DD) = '05' THEN SUM(AMTS) END) AS MONTH05 "
                       "                     , (CASE WHEN MONTH(BAL_DD) = '06' THEN SUM(AMTS) END) AS MONTH06 "
                       "                     , (CASE WHEN MONTH(BAL_DD) = '07' THEN SUM(AMTS) END) AS MONTH07 "
                       "                     , (CASE WHEN MONTH(BAL_DD) = '08' THEN SUM(AMTS) END) AS MONTH08 "
                       "                     , (CASE WHEN MONTH(BAL_DD) = '09' THEN SUM(AMTS) END) AS MONTH09 "
                       "                     , (CASE WHEN MONTH(BAL_DD) = '10' THEN SUM(AMTS) END) AS MONTH10 "
                       "                     , (CASE WHEN MONTH(BAL_DD) = '11' THEN SUM(AMTS) END) AS MONTH11 "
                       "                     , (CASE WHEN MONTH(BAL_DD) = '12' THEN SUM(AMTS) END) AS MONTH12 "
                       "                FROM OSBILL "
                       "                WHERE YEAR(BAL_DD) = '" + str(year) + "' "
                       "                AND GUBUN = '2' "
                       "               GROUP BY BAL_DD, MONTH(BAL_DD) ORDER BY MONTH(BAL_DD)) A GROUP BY YEAR ")

        mainresult = cursor.fetchall()

    with connection.cursor() as cursor:
        cursor.execute(
            "    SELECT  YEAR, IFNULL(SUM(MONTH01), 0) AS MONTH01, IFNULL(SUM(MONTH02), 0) AS MONTH02, IFNULL(SUM(MONTH03), 0) AS MONTH03"
            "                , IFNULL(SUM(MONTH04), 0) AS MONTH04, IFNULL(SUM(MONTH05), 0) AS MONTH05, IFNULL(SUM(MONTH06), 0) AS MONTH06 "
            "                , IFNULL(SUM(MONTH07), 0) AS MONTH07, IFNULL(SUM(MONTH08), 0) AS MONTH08, IFNULL(SUM(MONTH09), 0) AS MONTH09 "
            "                , IFNULL(SUM(MONTH10), 0) AS MONTH10, IFNULL(SUM(MONTH11), 0) AS MONTH11, IFNULL(SUM(MONTH12), 0) AS MONTH12 "
            "   FROM "
            "       ( SELECT        YEAR(BAL_DD) AS YEAR"
            "                     , (CASE WHEN MONTH(BAL_DD) = '01' THEN SUM(AMTS) END) AS MONTH01 "
            "                     , (CASE WHEN MONTH(BAL_DD) = '02' THEN SUM(AMTS) END) AS MONTH02 "
            "                     , (CASE WHEN MONTH(BAL_DD) = '03' THEN SUM(AMTS) END) AS MONTH03 "
            "                     , (CASE WHEN MONTH(BAL_DD) = '04' THEN SUM(AMTS) END) AS MONTH04 "
            "                     , (CASE WHEN MONTH(BAL_DD) = '05' THEN SUM(AMTS) END) AS MONTH05 "
            "                     , (CASE WHEN MONTH(BAL_DD) = '06' THEN SUM(AMTS) END) AS MONTH06 "
            "                     , (CASE WHEN MONTH(BAL_DD) = '07' THEN SUM(AMTS) END) AS MONTH07 "
            "                     , (CASE WHEN MONTH(BAL_DD) = '08' THEN SUM(AMTS) END) AS MONTH08 "
            "                     , (CASE WHEN MONTH(BAL_DD) = '09' THEN SUM(AMTS) END) AS MONTH09 "
            "                     , (CASE WHEN MONTH(BAL_DD) = '10' THEN SUM(AMTS) END) AS MONTH10 "
            "                     , (CASE WHEN MONTH(BAL_DD) = '11' THEN SUM(AMTS) END) AS MONTH11 "
            "                     , (CASE WHEN MONTH(BAL_DD) = '12' THEN SUM(AMTS) END) AS MONTH12 "
            "                FROM OSBILL "
            "                WHERE YEAR(BAL_DD) = '" + str(lastyear) + "' "
            "                AND GUBUN = '2' "
            "               GROUP BY BAL_DD, MONTH(BAL_DD) ORDER BY MONTH(BAL_DD)) A GROUP BY YEAR ")

        lastresult = cursor.fetchall()

    return JsonResponse({"saleLineList": mainresult, 'lastList': lastresult, 'tbSaleList': mainresult})



def yearlyMontlyPurs_search(request):
    year = request.POST.get('year')
    lastyear = request.POST.get('lastyear')

    with connection.cursor() as cursor:
        cursor.execute("    SELECT  YEAR, IFNULL(SUM(MONTH01), 0) AS MONTH01, IFNULL(SUM(MONTH02), 0) AS MONTH02, IFNULL(SUM(MONTH03), 0) AS MONTH03"
                       "                , IFNULL(SUM(MONTH04), 0) AS MONTH04, IFNULL(SUM(MONTH05), 0) AS MONTH05, IFNULL(SUM(MONTH06), 0) AS MONTH06 "
                       "                , IFNULL(SUM(MONTH07), 0) AS MONTH07, IFNULL(SUM(MONTH08), 0) AS MONTH08, IFNULL(SUM(MONTH09), 0) AS MONTH09 "
                       "                , IFNULL(SUM(MONTH10), 0) AS MONTH10, IFNULL(SUM(MONTH11), 0) AS MONTH11, IFNULL(SUM(MONTH12), 0) AS MONTH12 "
                       "   FROM "
                       "       ( SELECT        YEAR(BAL_DD) AS YEAR"
                       "                     , (CASE WHEN MONTH(BAL_DD) = '01' THEN SUM(AMTS) END) AS MONTH01 "
                       "                     , (CASE WHEN MONTH(BAL_DD) = '02' THEN SUM(AMTS) END) AS MONTH02 "
                       "                     , (CASE WHEN MONTH(BAL_DD) = '03' THEN SUM(AMTS) END) AS MONTH03 "
                       "                     , (CASE WHEN MONTH(BAL_DD) = '04' THEN SUM(AMTS) END) AS MONTH04 "
                       "                     , (CASE WHEN MONTH(BAL_DD) = '05' THEN SUM(AMTS) END) AS MONTH05 "
                       "                     , (CASE WHEN MONTH(BAL_DD) = '06' THEN SUM(AMTS) END) AS MONTH06 "
                       "                     , (CASE WHEN MONTH(BAL_DD) = '07' THEN SUM(AMTS) END) AS MONTH07 "
                       "                     , (CASE WHEN MONTH(BAL_DD) = '08' THEN SUM(AMTS) END) AS MONTH08 "
                       "                     , (CASE WHEN MONTH(BAL_DD) = '09' THEN SUM(AMTS) END) AS MONTH09 "
                       "                     , (CASE WHEN MONTH(BAL_DD) = '10' THEN SUM(AMTS) END) AS MONTH10 "
                       "                     , (CASE WHEN MONTH(BAL_DD) = '11' THEN SUM(AMTS) END) AS MONTH11 "
                       "                     , (CASE WHEN MONTH(BAL_DD) = '12' THEN SUM(AMTS) END) AS MONTH12 "
                       "                FROM OSBILL "
                       "                WHERE YEAR(BAL_DD) = '" + str(year) + "' "
                       "                AND GUBUN = '1' "
                       "               GROUP BY BAL_DD, MONTH(BAL_DD) ORDER BY MONTH(BAL_DD)) A GROUP BY YEAR ")

        mainresult = cursor.fetchall()
        print(mainresult)

    with connection.cursor() as cursor:
        cursor.execute(
            "    SELECT  YEAR, IFNULL(SUM(MONTH01), 0) AS MONTH01, IFNULL(SUM(MONTH02), 0) AS MONTH02, IFNULL(SUM(MONTH03), 0) AS MONTH03"
            "                , IFNULL(SUM(MONTH04), 0) AS MONTH04, IFNULL(SUM(MONTH05), 0) AS MONTH05, IFNULL(SUM(MONTH06), 0) AS MONTH06 "
            "                , IFNULL(SUM(MONTH07), 0) AS MONTH07, IFNULL(SUM(MONTH08), 0) AS MONTH08, IFNULL(SUM(MONTH09), 0) AS MONTH09 "
            "                , IFNULL(SUM(MONTH10), 0) AS MONTH10, IFNULL(SUM(MONTH11), 0) AS MONTH11, IFNULL(SUM(MONTH12), 0) AS MONTH12 "
            "   FROM "
            "       ( SELECT        YEAR(BAL_DD) AS YEAR"
            "                     , (CASE WHEN MONTH(BAL_DD) = '01' THEN SUM(AMTS) END) AS MONTH01 "
            "                     , (CASE WHEN MONTH(BAL_DD) = '02' THEN SUM(AMTS) END) AS MONTH02 "
            "                     , (CASE WHEN MONTH(BAL_DD) = '03' THEN SUM(AMTS) END) AS MONTH03 "
            "                     , (CASE WHEN MONTH(BAL_DD) = '04' THEN SUM(AMTS) END) AS MONTH04 "
            "                     , (CASE WHEN MONTH(BAL_DD) = '05' THEN SUM(AMTS) END) AS MONTH05 "
            "                     , (CASE WHEN MONTH(BAL_DD) = '06' THEN SUM(AMTS) END) AS MONTH06 "
            "                     , (CASE WHEN MONTH(BAL_DD) = '07' THEN SUM(AMTS) END) AS MONTH07 "
            "                     , (CASE WHEN MONTH(BAL_DD) = '08' THEN SUM(AMTS) END) AS MONTH08 "
            "                     , (CASE WHEN MONTH(BAL_DD) = '09' THEN SUM(AMTS) END) AS MONTH09 "
            "                     , (CASE WHEN MONTH(BAL_DD) = '10' THEN SUM(AMTS) END) AS MONTH10 "
            "                     , (CASE WHEN MONTH(BAL_DD) = '11' THEN SUM(AMTS) END) AS MONTH11 "
            "                     , (CASE WHEN MONTH(BAL_DD) = '12' THEN SUM(AMTS) END) AS MONTH12 "
            "                FROM OSBILL "
            "                WHERE YEAR(BAL_DD) = '" + str(lastyear) + "' "
            "                AND GUBUN = '1' "
            "               GROUP BY BAL_DD, MONTH(BAL_DD) ORDER BY MONTH(BAL_DD)) A GROUP BY YEAR ")

        lastresult = cursor.fetchall()

    return JsonResponse({"saleLineList": mainresult, 'lastList': lastresult, 'tbSaleList': mainresult})