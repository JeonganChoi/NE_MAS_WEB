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
from django.core.files.storage import FileSystemStorage


def cardViews(request):

    return render(request, "base/base-card.html")

def cardViews_search(request):
    cardNum = request.POST.get('cardNum')
    actNum = request.POST.get('actNum')
    bankCode = request.POST.get('bankCode')
    user = request.session.get("userId")
    iCust = request.session.get("USER_ICUST")

    if cardNum and actNum:
        with connection.cursor() as cursor:
            cursor.execute(" SELECT IFNULL(A.CARDNUM, ''), IFNULL(A.ACNUMBER, ''), IFNULL(A.ACBKCD, ''), IFNULL(B.RESNAM, '') "
                           "        , IFNULL(A.ACPAYDTE, ''), IFNULL(A.ACDESC, ''), IFNULL(A.CRE_USER, '') "
                           "        , IFNULL(A.GBN, ''), IFNULL(C.RESNAM, '') "
                           " FROM ACCARD A "
                           " LEFT OUTER JOIN OSREFCP B "
                           " ON A.ACBKCD = B.RESKEY "
                           " AND B.RECODE = 'BNK' "
                           " LEFT OUTER JOIN OSREFCP C "
                           " ON A.GBN = C.RESKEY "
                           " AND C.RECODE = 'COT' "
                           " WHERE A.CARDNUM = '" + str(cardNum) + "' "
                           "   AND A.ACNUMBER = '" + str(actNum) + "' "
                           "   AND A.ACBKCD = '" + str(bankCode) + "' "
                           "   AND A.ICUST = '" + str(iCust) + "' ")
            cardresult = cursor.fetchall()

        with connection.cursor() as cursor:
            cursor.execute(" SELECT RESKEY, RESNAM FROM OSREFCP WHERE RECODE = 'BNK' AND ICUST = '" + str(iCust) + "'")
            cboBank = cursor.fetchall()

        with connection.cursor() as cursor:
            cursor.execute(" SELECT ACNUMBER FROM ACNUMBER WHERE ICUST = '" + str(iCust) + "' ")
            cboAct = cursor.fetchall()

        with connection.cursor() as cursor:
            cursor.execute(" SELECT RESKEY, RESNAM FROM OSREFCP WHERE RECODE = 'COT' AND ICUST = '" + str(iCust) + "' ")
            cboType = cursor.fetchall()

        return JsonResponse({'cardList': cardresult, 'cboBank': cboBank, 'cboAct': cboAct, 'cboType': cboType})

    elif bankCode:
        with connection.cursor() as cursor:
            cursor.execute(" SELECT IFNULL(A.CARDNUM, ''), IFNULL(A.ACNUMBER, ''), IFNULL(A.ACBKCD, ''), IFNULL(B.RESNAM, '') "
                           "        , IFNULL(A.ACPAYDTE, ''), IFNULL(A.ACDESC, ''), IFNULL(A.CRE_USER, '') "
                           "        , IFNULL(A.GBN, ''), IFNULL(C.RESNAM, '') "
                           " FROM ACCARD A "
                           " LEFT OUTER JOIN OSREFCP B "
                           " ON A.ACBKCD = B.RESKEY "
                           " AND B.RECODE = 'BNK' "
                           " LEFT OUTER JOIN OSREFCP C "
                           " ON A.GBN = C.RESKEY "
                           " AND C.RECODE = 'COT' "
                           " WHERE A.ACBKCD = '" + str(bankCode) + "' "
                           " AND A.ICUST = '" + str(iCust) + "' ")
            cardresult = cursor.fetchall()

        with connection.cursor() as cursor:
            cursor.execute(" SELECT ACNUMBER FROM ACNUMBER WHERE ACBKCD = '" + str(bankCode) + "' AND ICUST = '" + str(iCust) + "' ")
            cboAct = cursor.fetchall()

        return JsonResponse({'cardList': cardresult, 'cboAct': cboAct})

    else:
        with connection.cursor() as cursor:
            cursor.execute(" SELECT IFNULL(A.CARDNUM, ''), IFNULL(A.ACNUMBER, ''), IFNULL(A.ACBKCD, '')"
                           "        , IFNULL(B.RESNAM, ''), IFNULL(A.ACPAYDTE, ''), IFNULL(A.ACDESC, ''), IFNULL(A.CRE_USER, '')"
                           "        , IFNULL(A.GBN, ''), IFNULL(C.RESNAM, '')  "
                           " FROM ACCARD A "
                           " LEFT OUTER JOIN OSREFCP B "
                           " ON A.ACBKCD = B.RESKEY "
                           " AND B.RECODE = 'BNK' "
                           " LEFT OUTER JOIN OSREFCP C "
                           " ON A.GBN = C.RESKEY "
                           " AND C.RECODE = 'COT' "
                           " WHERE A.ICUST = '" + str(iCust) + "' ")
            cardresult = cursor.fetchall()

        with connection.cursor() as cursor:
            cursor.execute(" SELECT RESKEY, RESNAM FROM OSREFCP WHERE RECODE = 'BNK' AND ICUST = '" + str(iCust) + "' ")
            cboBank = cursor.fetchall()

        with connection.cursor() as cursor:
            cursor.execute(" SELECT ACNUMBER FROM ACNUMBER WHERE ICUST = '" + str(iCust) + "' ")
            cboAct = cursor.fetchall()

        with connection.cursor() as cursor:
            cursor.execute(" SELECT RESKEY, RESNAM FROM OSREFCP WHERE RECODE = 'COT' AND ICUST = '" + str(iCust) + "' ")
            cboType = cursor.fetchall()

        return JsonResponse({'cardList': cardresult, 'cboBank': cboBank, 'cboAct': cboAct, 'cboType': cboType})


def chkCard_search(request):
    cardNum = request.POST.get('txtCardNum')
    iCust = request.session.get("USER_ICUST")
    with connection.cursor() as cursor:
        cursor.execute(" SELECT CARDNUM FROM ACCARD WHERE CARDNUM = '" + str(cardNum) + "' AND ICUST = '" + str(iCust) + "' ")
        card = cursor.fetchall()

    return JsonResponse({'card': card})

def cardViews_save(request):
    cboBank = request.POST.get('cboBank')
    cardNum = request.POST.get('txtCardNum')
    actNum = request.POST.get('cboActNum')
    payDate = request.POST.get('cboDay')
    acRemark = request.POST.get('txtRemark')
    cardType = request.POST.get('cboType')
    user = request.session.get("userId")
    iCust = request.session.get("USER_ICUST")

    with connection.cursor() as cursor:
        cursor.execute(" SELECT CARDNUM FROM ACCARD WHERE CARDNUM = '" + cardNum + "' AND ICUST = '" + str(iCust) + "' ")
        result = cursor.fetchall()

    if result:
        with connection.cursor() as cursor:
            cursor.execute("    UPDATE ACCARD SET"
                           "     ACNUMBER = '" + str(actNum) + "' "
                           ",    GBN = '" + str(cardType) + "' "
                           ",    ACBKCD = '" + str(cboBank) + "' "
                           ",    ACPAYDTE = '" + str(payDate) + "' "
                           ",    ACDESC = '" + str(acRemark) + "' "
                           ",    UPD_USER = '" + str(user) + "' "
                           ",    UPD_DT = date_format(now(), '%Y%m%d') "
                           "     WHERE CARDNUM = '" + str(cardNum) + "' "
                           "     AND ICUST = '" + str(iCust) + "' "
                           )
            connection.commit()

        return JsonResponse({'sucYn': "Y"})

    else:
        with connection.cursor() as cursor:
            cursor.execute("    INSERT INTO ACCARD "
                           "   ("
                           "     CARDNUM "
                           ",    ACNUMBER "
                           ",    GBN "
                           ",    ACBKCD "
                           ",    ACPAYDTE "
                           ",    ACDESC "
                           ",    CRE_USER " 
                           ",    CRE_DT "
                           ",    ICUST "
                           "    ) "
                           "    VALUES "
                           "    ("
                           "    '" + cardNum + "' "
                           ",   '" + str(actNum) + "' "
                           ",   '" + str(cardType) + "' "
                           ",   '" + str(cboBank) + "' "
                           ",   '" + str(payDate) + "' "
                           ",   '" + str(acRemark) + "' "
                           ",   '" + user + "' "
                           ",   date_format(now(), '%Y%m%d') "
                           ",   '" + str(iCust) + "' "
                           "    ) "
                           )
            connection.commit()

        return JsonResponse({'sucYn': "Y"})


def cardViews_dlt(request):
    iCust = request.session.get('USER_ICUST')

    if request.method == "POST":
        dataList = json.loads(request.POST.get('arrList'))
        print(dataList)
        for act in dataList:
            acc_split_list = act.split(',')
            with connection.cursor() as cursor:
                cursor.execute(" DELETE FROM ACCARD WHERE CARDNUM = '" + acc_split_list[0] + "' "
                               "                        AND ACBKCD = '" + acc_split_list[1] + "' "
                               "                        AND ICUST = '" + str(iCust) + "'")
                connection.commit()

        return JsonResponse({'sucYn': "Y"})

    else:
        return render(request, 'base/base-card.html')