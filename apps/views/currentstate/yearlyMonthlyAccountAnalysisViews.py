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


def yearlyMontlyAccount(request):

    return render(request, "currentstate/yearlyMonthly-accountReport.html")

def yearlyMontlyAccount_cbo(request):
    with connection.cursor() as cursor:
        cursor.execute(" SELECT MCODE, MCODENM FROM OSCODEM ")
        cboMresult = cursor.fetchall()

        cursor.execute(" SELECT ACODE, ACODENM FROM OSCODEA ")

        cboAresult = cursor.fetchall()

    return JsonResponse({"cboMList": cboMresult, 'cboAList': cboAresult})
def yearlyMontlyAccount_search(request):
    year = request.POST.get('year')
    lastYear = int(year) - 1
    actCode = request.POST.get('actCode')

    if year != '' and year is not None and actCode != '' and actCode is not None:
        with connection.cursor() as cursor:
            cursor.execute(" SELECT  A.YEAR, IFNULL(SUM(A.MONTH01), 0) AS MONTH01, IFNULL(SUM(A.MONTH02), 0) AS MONTH02, IFNULL(SUM(A.MONTH03), 0) AS MONTH03 "
                           "               , IFNULL(SUM(A.MONTH04), 0) AS MONTH04, IFNULL(SUM(A.MONTH05), 0) AS MONTH05, IFNULL(SUM(A.MONTH06), 0) AS MONTH06 "
                           "               , IFNULL(SUM(A.MONTH07), 0) AS MONTH07, IFNULL(SUM(A.MONTH08), 0) AS MONTH08, IFNULL(SUM(MONTH09), 0) AS MONTH09 "
                           "               , IFNULL(SUM(A.MONTH10), 0) AS MONTH10, IFNULL(SUM(A.MONTH11), 0) AS MONTH11, IFNULL(SUM(MONTH12), 0) AS MONTH12 "
                           " FROM "
                           "     ( SELECT        YEAR(ACDATE) AS YEAR "
                           "                   , (CASE WHEN YEAR(ACDATE) = '" + str(year) + "' AND MONTH(ACDATE) = '01' AND ACIOGB = '1' THEN SUM(ACAMTS) END) AS MONTH01 "
                           "                   , (CASE WHEN YEAR(ACDATE) = '" + str(year) + "' AND MONTH(ACDATE) = '02' AND ACIOGB = '1' THEN SUM(ACAMTS) END) AS MONTH02 "
                           "                   , (CASE WHEN YEAR(ACDATE) = '" + str(year) + "' AND MONTH(ACDATE) = '03' AND ACIOGB = '1' THEN SUM(ACAMTS) END) AS MONTH03 "
                           "                   , (CASE WHEN YEAR(ACDATE) = '" + str(year) + "' AND MONTH(ACDATE) = '04' AND ACIOGB = '1' THEN SUM(ACAMTS) END) AS MONTH04 "
                           "                   , (CASE WHEN YEAR(ACDATE) = '" + str(year) + "' AND MONTH(ACDATE) = '05' AND ACIOGB = '1' THEN SUM(ACAMTS) END) AS MONTH05 "
                           "                   , (CASE WHEN YEAR(ACDATE) = '" + str(year) + "' AND MONTH(ACDATE) = '06' AND ACIOGB = '1' THEN SUM(ACAMTS) END) AS MONTH06 "
                           "                   , (CASE WHEN YEAR(ACDATE) = '" + str(year) + "' AND MONTH(ACDATE) = '07' AND ACIOGB = '1' THEN SUM(ACAMTS) END) AS MONTH07 "
                           "                   , (CASE WHEN YEAR(ACDATE) = '" + str(year) + "' AND MONTH(ACDATE) = '08' AND ACIOGB = '1' THEN SUM(ACAMTS) END) AS MONTH08 "
                           "                   , (CASE WHEN YEAR(ACDATE) = '" + str(year) + "' AND MONTH(ACDATE) = '09' AND ACIOGB = '1' THEN SUM(ACAMTS) END) AS MONTH09 "
                           "                   , (CASE WHEN YEAR(ACDATE) = '" + str(year) + "' AND MONTH(ACDATE) = '10' AND ACIOGB = '1' THEN SUM(ACAMTS) END) AS MONTH10 "
                           "                   , (CASE WHEN YEAR(ACDATE) = '" + str(year) + "' AND MONTH(ACDATE) = '11' AND ACIOGB = '1' THEN SUM(ACAMTS) END) AS MONTH11 "
                           "                   , (CASE WHEN YEAR(ACDATE) = '" + str(year) + "' AND MONTH(ACDATE) = '12' AND ACIOGB = '1' THEN SUM(ACAMTS) END) AS MONTH12 "
                           "              FROM SISACCTT "
                           "              WHERE YEAR(ACDATE) = '" + str(year) + "' "
                           "              AND ACCODE = '" + str(actCode) + "' "
                           "              OR MCODE = '" + str(actCode) + "' "
                           "              GROUP BY ACDATE, MONTH(ACDATE) "
                           "              ORDER BY MONTH(ACDATE)) A WHERE A.YEAR IS NOT NULL AND A.YEAR = '" + str(year) + "' GROUP BY A.YEAR ")
            mainresult = cursor.fetchall()
            print(mainresult)

        with connection.cursor() as cursor:
            cursor.execute(" SELECT  A.YEAR, IFNULL(SUM(A.MONTH01), 0) AS MONTH01, IFNULL(SUM(A.MONTH02), 0) AS MONTH02, IFNULL(SUM(A.MONTH03), 0) AS MONTH03 "
                           "               , IFNULL(SUM(A.MONTH04), 0) AS MONTH04, IFNULL(SUM(A.MONTH05), 0) AS MONTH05, IFNULL(SUM(A.MONTH06), 0) AS MONTH06 "
                           "               , IFNULL(SUM(A.MONTH07), 0) AS MONTH07, IFNULL(SUM(A.MONTH08), 0) AS MONTH08, IFNULL(SUM(A.MONTH09), 0) AS MONTH09 "
                           "               , IFNULL(SUM(A.MONTH10), 0) AS MONTH10, IFNULL(SUM(A.MONTH11), 0) AS MONTH11, IFNULL(SUM(A.MONTH12), 0) AS MONTH12 "
                           " FROM "
                           "     ( SELECT        YEAR(ACDATE) AS YEAR "
                           "                   , (CASE WHEN YEAR(ACDATE) = '" + str(lastYear) + "' AND MONTH(ACDATE) = '01' AND ACIOGB = '1' THEN SUM(ACAMTS) END) AS MONTH01 "
                           "                   , (CASE WHEN YEAR(ACDATE) = '" + str(lastYear) + "' AND MONTH(ACDATE) = '02' AND ACIOGB = '1' THEN SUM(ACAMTS) END) AS MONTH02 "
                           "                   , (CASE WHEN YEAR(ACDATE) = '" + str(lastYear) + "' AND MONTH(ACDATE) = '03' AND ACIOGB = '1' THEN SUM(ACAMTS) END) AS MONTH03 "
                           "                   , (CASE WHEN YEAR(ACDATE) = '" + str(lastYear) + "' AND MONTH(ACDATE) = '04' AND ACIOGB = '1' THEN SUM(ACAMTS) END) AS MONTH04 "
                           "                   , (CASE WHEN YEAR(ACDATE) = '" + str(lastYear) + "' AND MONTH(ACDATE) = '05' AND ACIOGB = '1' THEN SUM(ACAMTS) END) AS MONTH05 "
                           "                   , (CASE WHEN YEAR(ACDATE) = '" + str(lastYear) + "' AND MONTH(ACDATE) = '06' AND ACIOGB = '1' THEN SUM(ACAMTS) END) AS MONTH06 "
                           "                   , (CASE WHEN YEAR(ACDATE) = '" + str(lastYear) + "' AND MONTH(ACDATE) = '07' AND ACIOGB = '1' THEN SUM(ACAMTS) END) AS MONTH07 "
                           "                   , (CASE WHEN YEAR(ACDATE) = '" + str(lastYear) + "' AND MONTH(ACDATE) = '08' AND ACIOGB = '1' THEN SUM(ACAMTS) END) AS MONTH08 "
                           "                   , (CASE WHEN YEAR(ACDATE) = '" + str(lastYear) + "' AND MONTH(ACDATE) = '09' AND ACIOGB = '1' THEN SUM(ACAMTS) END) AS MONTH09 "
                           "                   , (CASE WHEN YEAR(ACDATE) = '" + str(lastYear) + "' AND MONTH(ACDATE) = '10' AND ACIOGB = '1' THEN SUM(ACAMTS) END) AS MONTH10 "
                           "                   , (CASE WHEN YEAR(ACDATE) = '" + str(lastYear) + "' AND MONTH(ACDATE) = '11' AND ACIOGB = '1' THEN SUM(ACAMTS) END) AS MONTH11 "
                           "                   , (CASE WHEN YEAR(ACDATE) = '" + str(lastYear) + "' AND MONTH(ACDATE) = '12' AND ACIOGB = '1' THEN SUM(ACAMTS) END) AS MONTH12 "
                           "              FROM SISACCTT "
                           "              WHERE YEAR(ACDATE) = '" + str(lastYear) + "' "
                           "              AND ACCODE = '" + str(actCode) + "' "
                           "              OR MCODE = '" + str(actCode) + "' "
                           "              GROUP BY ACDATE, MONTH(ACDATE) "
                           "              ORDER BY MONTH(ACDATE)) A WHERE A.YEAR IS NOT NULL AND A.YEAR = '" + str(lastYear) + "' GROUP BY A.YEAR ")
            lastresult = cursor.fetchall()

        return JsonResponse({"saleLineList": mainresult, 'lastList': lastresult})


