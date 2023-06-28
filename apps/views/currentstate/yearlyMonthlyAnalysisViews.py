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

    return render(request, "currentstate/yearlyMonthly-salesReport.html")

def yearlyMontlySales_search(request):
    with connection.cursor() as cursor:
        cursor.execute(" SELECT SUM(AMTS), MONTH(BAL_DD) FROM OSBILL WHERE YEAR(BAL_DD) = '2023' GROUP BY MONTH(BAL_DD) ")

        mainresult = cursor.fetchall()

    return JsonResponse({"saleLineList": mainresult})