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


def purSaleSearchViews(request):

    return render(request, "finance/purchases-sales-search.html")


def purSaleSearchViews_search(request):
    with connection.cursor() as cursor:
        cursor.execute(" SELECT IFNULL(ACDATE, ''), IFNULL(DAY(ACDATE), '') "
                       "    , IFNULL(SUM(ACAMTS), 0), IFNULL(ACIOGB, '') "
                       "    FROM OSBILL  "
                       "    WHERE ACIOGB = '2' "
                       "    GROUP BY DAY(ACDATE) ")
        mainresult = cursor.fetchall()

    return JsonResponse({"mainList": mainresult})