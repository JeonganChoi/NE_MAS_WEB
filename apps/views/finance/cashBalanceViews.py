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


def cashBalRegViews(request):

    return render(request, "finance/cash-reg.html")

def cashBalRegBankViews(request):
    with connection.cursor() as cursor:
        cursor.execute(" SELECT RESKEY, RESNAM FROM OSREFCP WHERE RECODE = 'BNK' ")
        banks = cursor.fetchall()

        return JsonResponse({"bankList": banks})

def cashBalRegSearchViews(request):
    SearchBank = request.POST.get('bankCode')
    user = request.session.get('userId')
    iCust = request.session.get('USER_ICUST')

    # 은행명 선택 시 조회
    if SearchBank:
        # 은행 계좌 잔액 등록 - 은행명 콤보박스
        with connection.cursor() as cursor:
            cursor.execute(" SELECT RESKEY, RESNAM FROM OSREFCP WHERE RECODE = 'BNK' AND RESKEY = '" + SearchBank + "' ")
            bankselected = cursor.fetchall()

        with connection.cursor() as cursor:
            cursor.execute(" SELECT IFNULL(C.RESKEY,'') AS RECODE "
                           "        ,IFNULL(C.RESNAM,'') AS BANKNM "
                           "        ,IFNULL(A.ACNUM_NAME,'') AS ACNUM_NAME "
                           "        ,IFNULL(A.ACNUMBER,'') AS ACNUMBER "
                           "        ,IFNULL(B.ACDATE,'') AS ACDATE "
                           "        ,IFNULL(B.ACAMTS, 0) AS ACAMTS "
                           "        ,IFNULL(B.ACDESC, '') AS ACDESC "
                           " FROM ACNUMBER A "
                           " LEFT OUTER JOIN ACCASHP  B "
                           " ON A.ACNUMBER = B.ACNUMBER "
                           " LEFT OUTER JOIN OSREFCP C "
                           " ON A.ACBKCD = C.RESKEY "
                           " AND C.RECODE = 'BNK' "
                           " WHERE A.ICUST = '" + str(iCust) + "' "
                           " AND C.RESKEY = '" + str(SearchBank) + "' "
                           " ORDER BY B.ACDATE "
                            )
            acResult = cursor.fetchall()

        return JsonResponse({'acList': acResult, "bankCombo2": bankselected})

    else:
        # 은행 계좌 잔액 등록 - 은행명 콤보박스
        with connection.cursor() as cursor:
            cursor.execute(" SELECT RESKEY, RESNAM FROM OSREFCP WHERE RECODE = 'BNK' ")
            bankresult = cursor.fetchall()

        # 은행 계좌 잔액 테이블
        with connection.cursor() as cursor:
            cursor.execute(" SELECT IFNULL(C.RESKEY,'') AS RECODE "
                           "        ,IFNULL(C.RESNAM,'') AS BANKNM "
                           "        ,IFNULL(A.ACNUM_NAME,'') AS ACNUM_NAME "
                           "        ,IFNULL(A.ACNUMBER,'') AS ACNUMBER "
                           "        ,IFNULL(B.ACDATE,'') AS ACDATE "
                           "        ,IFNULL(B.ACAMTS, 0) AS ACAMTS "
                           "        ,IFNULL(B.ACDESC, '') AS ACDESC "
                           " FROM ACNUMBER A "
                           " LEFT OUTER JOIN ACCASHP  B "
                           " ON A.ACNUMBER = B.ACNUMBER "
                           " LEFT OUTER JOIN OSREFCP C "
                           " ON A.ACBKCD = C.RESKEY "
                           " AND C.RECODE = 'BNK' "
                           " WHERE A.ICUST = '" + str(iCust) + "' "
                           " ORDER BY B.ACDATE "
                )
            allAcResult = cursor.fetchall()

        return JsonResponse({"bankCombo": bankresult, "acList": allAcResult})





def cashBalRegSearchScndViews(request):
    SearchBank = request.POST.get('bankCode')
    user = request.session.get('userId')
    iCust = request.session.get('USER_ICUST')

    # 은행명 선택 시 조회
    with connection.cursor() as cursor:
        cursor.execute(
            " SELECT "
            "         IFNULL(C.RESKEY,'') AS RECODE"
            "        ,IFNULL(C.RESNAM,'') AS BANKNM "
            "        ,IFNULL(B.ACNUM_NAME,'') AS ACNUM_NAME "
            "        ,IFNULL(A.ACNUMBER,'') AS ACNUMBER "
            "        ,IFNULL(A.ACDATE,'') AS ACDATE "
            "        ,IFNULL(A.ACAMTS, 0) AS ACAMTS "
            "        ,IFNULL(A.ACDESC, '') AS ACDESC "
            " FROM ACCASHP A "
            " LEFT OUTER JOIN ACNUMBER B "
            " ON A.ACNUMBER = B.ACNUMBER "
            " LEFT OUTER JOIN OSREFCP C "
            " ON B.ACBKCD = C.RESKEY "
            " WHERE C.RECODE = 'BNK' "
            " AND C.RESKEY = '" + SearchBank + "'"
            " AND A.ICUST = '" + str(iCust) + "'"
            " ORDER BY A.ACDATE "

            )
        acResult = cursor.fetchall()

    return JsonResponse({'acListScnd': acResult})


def cashBalRegCboSearchViews(request):
    bank = request.POST.get('bankCode')
    user = request.session.get('userId')
    iCust = request.session.get('USER_ICUST')

    # 은행명 선택 시 계좌번호 란에 콤보박스에 바인딩
    with connection.cursor() as cursor:
        cursor.execute(" SELECT "
                       "         IFNULL(C.RESKEY,'') AS RESKEY "
                       "        ,IFNULL(B.ACNUM_NAME,'') AS ACNUM_NAME "
                       "        ,IFNULL(B.ACNUMBER,'') AS ACNUMBER "
                       " FROM ACNUMBER B "
                       " LEFT OUTER JOIN OSREFCP C "
                       " ON B.ACBKCD = C.RESKEY "
                       " WHERE C.RECODE = 'BNK' "
                       " AND B.ACBKCD = '" + bank + "' "
                       " AND B.ICUST = '" + str(iCust) + "' "
                       " GROUP BY C.RESKEY, B.ACNUM_NAME, B.ACNUMBER "
            )
        acnumlist = cursor.fetchall()

    return JsonResponse({'acnumlist': acnumlist})

def cashBalRegAcNmSearchViews(request):
    actNum = request.POST.get('acnumcode')
    iCust = request.session.get('USER_ICUST')

    # 은행명 선택 시 계좌번호 란에 콤보박스에 바인딩
    with connection.cursor() as cursor:
        cursor.execute(
            " SELECT ACNUM_NAME FROM ACNUMBER WHERE ACNUMBER = '" + actNum + "' AND ICUST = '" + str(iCust) + "' "
            )
        acnamelist = cursor.fetchall()

    return JsonResponse({'acnamelist': acnamelist})



def cashBalRegSaveViews(request):
    ActNum = request.POST.get("cboActNum")
    RAcNum = ActNum[0:]
    RegDate = request.POST.get("txtRegDate").replace('-', '')
    Amount = request.POST.get("txtAmount").replace(',', '')
    Bigo = request.POST.get("txtBigo")
    user = request.session.get('userId')
    iCust = request.session.get('USER_ICUST')

    with connection.cursor() as cursor:
        cursor.execute(" SELECT ACNUMBER FROM ACCASHP WHERE ACNUMBER = '" + ActNum + "' AND ACDATE = '" + str(RegDate) + "' AND ICUST = '" + str(iCust) + "' ")
        chkresult = cursor.fetchall()

        if chkresult:
            acNum = chkresult[0][0]
            with connection.cursor() as cursor:
                cursor.execute(" UPDATE ACCASHP SET "
                               "     ACAMTS = '" + str(Amount) + "' "
                               ",    ACDESC = '" + str(Bigo) + "' "
                               ",    UPD_USER = '" + str(user) + "' "
                               ",    UPD_DT = date_format(now(), '%Y%m%d') "
                               "     WHERE ACNUMBER = '" + str(acNum) + "' "
                               "     AND ACDATE = '" + str(RegDate) + "' "
                               "     AND ICUST = '" + str(iCust) + "'"
                               )
                connection.commit()

                return JsonResponse({'sucYn': "Y"})

        else:
            with connection.cursor() as cursor:
                cursor.execute("INSERT INTO ACCASHP "
                               "   ("
                               "     ACNUMBER "
                               ",    ACDATE "
                               ",    ACAMTS "
                               ",    ACDESC "
                               ",    CRE_USER "
                               ",    CRE_DT "
                               ",    ICUST "
                               ") "
                               "    VALUES "
                               "    ("
                               "    '" + str(RAcNum) + "' "
                               ",   '" + str(RegDate) + "' "
                               ",   '" + str(Amount) + "'"
                               ",   '" + str(Bigo) + "'"
                               ",   '" + str(user) + "' "
                               ",   date_format(now(), '%Y%m%d')"
                               ",   '" + str(iCust) + "'"
                               "    ) "
                               )

                connection.commit()

            return JsonResponse({'sucYn': "Y"})


def cashViews_dlt(request):
    iCust = request.session.get('USER_ICUST')

    if request.method == "POST":
        dataList = json.loads(request.POST.get('arrList'))
        print(dataList)
        for act in dataList:
            acc_split_list = act.split(',')
            with connection.cursor() as cursor:
                cursor.execute(" DELETE FROM ACCASHP WHERE ACNUMBER = '" + acc_split_list[1] + "' "
                               "                        AND ACDATE = '" + acc_split_list[2] + "' "
                               "                        AND ICUST = '" + iCust + "'")
                connection.commit()

        return JsonResponse({'sucYn': "Y"})

    else:
        return render(request, 'base/base-card.html')

