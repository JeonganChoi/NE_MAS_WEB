import json
import os
from django.shortcuts import render, redirect
from django import template
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect, FileResponse
from django.template import loader
from django.urls import reverse
from django.contrib import messages
from django.http import JsonResponse
from django.db import connection
from django.core.files.storage import FileSystemStorage
from urllib.parse import quote

def cboJJoEmp(request):
    iCust = request.session.get('USER_ICUST')

    with connection.cursor() as cursor:
        cursor.execute(
            " SELECT RESKEY, RESNAM FROM OSREFCP WHERE RECODE = 'JJO' AND ICUST = '" + str(iCust) + "' ")
        result = cursor.fetchall()

        return JsonResponse({"cboJJoEmp": result})


def cboBankList(request):
    iCust = request.session.get('USER_ICUST')

    with connection.cursor() as cursor:
        cursor.execute(
            " SELECT RESKEY, RESNAM FROM OSREFCP WHERE RECODE = 'BNK' AND ICUST = '" + str(iCust) + "' ")
        result = cursor.fetchall()

        return JsonResponse({"cboBank": result})

def cboUseBank(request):
    iCust = request.session.get('USER_ICUST')

    with connection.cursor() as cursor:
        cursor.execute(
            " SELECT A.ACBKCD, B.RESNAM FROM ACNUMBER A "
            " LEFT OUTER JOIN OSREFCP B ON A.ACBKCD = B.RESKEY AND B.RECODE = 'BNK' AND A.ICUST = '" + str(iCust) + "' "
            " GROUP BY A.ACBKCD, B.RESNAM ORDER BY A.ACBKCD  ")
        result = cursor.fetchall()

        return JsonResponse({"cboBank": result})


def cboAct(request):
    cboBank = request.POST.get('cboBank')
    iCust = request.session.get('USER_ICUST')

    if cboBank != '':
        with connection.cursor() as cursor:
            cursor.execute(" SELECT ACNUMBER FROM ACNUMBER WHERE ACBKCD = '" + str(cboBank) + "' AND ICUST = '" + str(iCust) + "' ")
            result = cursor.fetchall()

            return JsonResponse({"cboAct": result})
    else:
        with connection.cursor() as cursor:
            cursor.execute(
                " SELECT A.ACBKCD, B.RESNAM FROM ACNUMBER A "
                " LEFT OUTER JOIN OSREFCP B ON A.ACBKCD = B.RESKEY AND B.RECODE = 'BNK' AND A.ICUST = '" + str(iCust) + "' "
                " GROUP BY A.ACBKCD, B.RESNAM ORDER BY A.ACBKCD  ")
            result = cursor.fetchall()

            return JsonResponse({"cboBank": result})


def cboCard(request):
    cboCard = request.POST.get('cboCard')
    iCust = request.session.get('USER_ICUST')

    with connection.cursor() as cursor:
        cursor.execute(" SELECT A.CARDNUM FROM ACCARD A LEFT OUTER JOIN OSREFCP B ON A.CARDTYPE = B.RESKEY AND B.RECODE = 'COC' WHERE A.ICUST = '" + str(iCust) + "' AND CARDTYPE = '" + str(cboCard) + "' ")
        result = cursor.fetchall()

        return JsonResponse({"cboCard": result})

def cboCardAct(request):
    cardNum = request.POST.get('cardNum')
    iCust = request.session.get('USER_ICUST')

    with connection.cursor() as cursor:
        cursor.execute(
            " SELECT ACNUMBER FROM ACCARD WHERE ICUST = '" + str(iCust) + "' AND CARDNUM = '" + str(cardNum) + "' ")
        result = cursor.fetchall()

        return JsonResponse({"cboAct": result})




def cboMcode(request):
    iCust = request.session.get('USER_ICUST')

    with connection.cursor() as cursor:
        cursor.execute(" SELECT MCODE, MCODENM FROM OSCODEM WHERE ICUST = '" + str(iCust) + "' ")
        result = cursor.fetchall()

        return JsonResponse({"cboMcode": result})