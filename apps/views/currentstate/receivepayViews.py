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


def receivepaySheetViews(request):

    return render(request, "currentstate/receive-pay-banksheet.html")


def receivepaySheetViews_search(request):
    with connection.cursor() as cursor:
        cursor.execute(" SELECT RESKEY, RESNAM FROM OSREFCP WHERE RECODE = 'BNK' ")
        bankresult = cursor.fetchall()
        bank = bankresult[0][0]

        cursor.execute(" SELECT ACNUMBER FROM ACNUMBER WHERE ACBKCD = '" + bank + "' ")

        cboAresult = cursor.fetchall()

    return JsonResponse({"cboBank": bankresult, 'cboAccount': cboAresult})