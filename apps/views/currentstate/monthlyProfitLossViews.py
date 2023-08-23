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

    with connection.cursor() as cursor:
        cursor.execute(" SELECT RESKEY, RESNAM FROM OSREFCP WHERE RECODE = 'AGB' ")
        headerresult = cursor.fetchall()
        print(headerresult)

    return JsonResponse({"headerList": headerresult})