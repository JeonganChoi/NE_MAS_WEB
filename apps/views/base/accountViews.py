import json
from django.shortcuts import render, redirect
from django import template
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from django.urls import reverse
from django.contrib import messages
from django.http import JsonResponse
from django.db import connection, transaction, IntegrityError


def accountViews(request):

    return render(request, "base/base-account.html")


def accountViews_search(request):
    bankCode = request.POST.get('bankCode')
    actCode = request.POST.get('actCode')

    if bankCode != '' and bankCode is not None:
        with connection.cursor() as cursor:
            cursor.execute(" SELECT A.ACBKCD, B.RESNAM, A.ACNUMBER, IFNULL(A.ACNUM_NAME, ''), IFNULL(A.ACINDTE, '') "
                           "    , IFNULL(A.ACENDTE, ''), IFNULL(A.ACPAY, ''), IFNULL(A.ACDESC, '') "
                           "    , IFNULL(A.INEPNO, ''), IFNULL(A.UEPNO, '') "
                           "    , IFNULL(A.INDATE, ''), IFNULL(A.UDATE, '') "
                           "    FROM ACNUMBER A "
                           "    LEFT OUTER JOIN OSREFCP B "
                           "    ON A.ACBKCD = B.RESKEY "
                           "    WHERE B.RECODE = 'BNK' "
                           "    AND ACBKCD LIKE '%" + bankCode + "%'")
            accountresult = cursor.fetchall()

        return JsonResponse({"accountList": accountresult})

    if actCode != '' and actCode is not None:
        with connection.cursor() as cursor:
            cursor.execute(" SELECT A.ACBKCD, B.RESNAM, A.ACNUMBER, IFNULL(A.ACNUM_NAME, ''), IFNULL(A.ACINDTE, '') "
                           "    , IFNULL(A.ACENDTE, ''), IFNULL(A.ACPAY, ''), IFNULL(A.ACDESC, '') "
                           "    , IFNULL(A.INEPNO, ''), IFNULL(A.UEPNO, '') "
                           "    , IFNULL(A.INDATE, ''), IFNULL(A.UDATE, '') "
                           "    FROM ACNUMBER A "
                           "    LEFT OUTER JOIN OSREFCP B "
                           "    ON A.ACBKCD = B.RESKEY "
                           "    WHERE B.RECODE = 'BNK' "
                           "    AND ACNUMBER LIKE '%" + actCode + "%'")
            accountresult = cursor.fetchall()

        # 은행명 - 콤보박스
        with connection.cursor() as cursor:
            cursor.execute(" SELECT RESKEY, RESNAM FROM OSREFCP WHERE RECODE = 'BNK' ")
            bankCombo = cursor.fetchall()

        print(bankCombo, accountresult)
        return JsonResponse({"bankCombo": bankCombo, "accountList": accountresult})
    # 테이블
    else:
        with connection.cursor() as cursor:
            cursor.execute(" SELECT A.ACBKCD, B.RESNAM, A.ACNUMBER, IFNULL(A.ACNUM_NAME, ''), IFNULL(A.ACINDTE, '') "
                           "    , IFNULL(A.ACENDTE, ''), IFNULL(A.ACPAY, ''), IFNULL(A.ACDESC, '') "
                           "    , IFNULL(A.INEPNO, ''), IFNULL(A.UEPNO, '') "
                           "    , IFNULL(A.INDATE, ''), IFNULL(A.UDATE, '') "
                           "    FROM ACNUMBER A "
                           "    LEFT OUTER JOIN OSREFCP B "
                           "    ON A.ACBKCD = B.RESKEY "
                           "    WHERE B.RECODE = 'BNK' ")
            accountresult = cursor.fetchall()

        # 은행명 - 콤보박스
        with connection.cursor() as cursor:
            cursor.execute(" SELECT RESKEY, RESNAM FROM OSREFCP WHERE RECODE = 'BNK' ")
            bankCombo = cursor.fetchall()

        return JsonResponse({"bankCombo": bankCombo, "accountList": accountresult})



def accountViews_save(request):
    accNum = request.POST.get('actCode')
    accName = request.POST.get('actNme')
    bankCode = request.POST.get('bankcode')
    strDate = request.POST.get('regDate').replace('-', '')
    endDate = request.POST.get('eprDate').replace('-', '')
    accPrc = request.POST.get('amts')
    remark = request.POST.get('remark')
    inepno = request.POST.get('user')
    # inepno = request.session['userid']
    # utepno = request.session['userid']
    if inepno is None or inepno == '':
        accPrc = 0
        with connection.cursor() as cursor:
            cursor.execute(" INSERT INTO ACNUMBER "
                           "   ("
                           "     ACNUMBER "
                           ",    ACNUM_NAME "
                           ",    ACBKCD "
                           ",    ACINDTE "
                           ",    ACENDTE "
                           ",    ACPAY "
                           ",    ACDESC "
                           ",    INEPNO "
                           ",    INDATE "
                           "    ) "
                           "    VALUES "
                           "    ("
                           "    '" + accNum + "' "
                           ",   '" + str(accName) + "' "
                           ",   '" + str(bankCode) + "' "
                           ",   '" + str(strDate) + "' "
                           ",   '" + str(endDate) + "' "
                           ",   '" + int(accPrc) + "' "
                           ",   '" + str(remark) + "' "
                           ",   '" + str(inepno) + "' "
                           ",   date_format(now(), '%Y%m%d') "
                           "    ) "
                           )
            connection.commit()

        return JsonResponse({'sucYn': "Y"})

    elif inepno:
        with connection.cursor() as cursor:
            cursor.execute("    UPDATE ACNUMBER SET"
                           "     ACNUM_NAME = '" + str(accName) + "' "
                           ",    ACBKCD = '" + str(bankCode) + "' "
                           ",    ACINDTE = '" + str(strDate) + "' "
                           ",    ACENDTE = '" + str(endDate) + "' "
                           ",    ACPAY = '" + int(accPrc) + "' "
                           ",    ACDESC = '" + str(remark) + "' "
                           ",    UEPNO = '" + str(user) + "' "
                           ",    UDATE = date_format(now(), '%Y%m%d') "
                           "     WHERE ACNUMBER = '" + str(accNum) + "' "
                           )
            connection.commit()

            return JsonResponse({'sucYn': "Y"})

    return render(request, 'base/base-account.html')


def accountViews_dlt(request):
    if request.method == "POST":
        dataList = json.loads(request.POST.get('arrList'))
        print(dataList)
        for act in dataList:
            acc_split_list = act.split(',')
            with connection.cursor() as cursor:
                cursor.execute(" DELETE FROM ACNUMBER WHERE ACBKCD = '" + acc_split_list[0] + "' "
                               "                        AND ACNUMBER = '" + acc_split_list[1] + "' ")
                connection.commit()

        return JsonResponse({'sucYn': "Y"})

    else:
        return render(request, 'base/base-account.html')