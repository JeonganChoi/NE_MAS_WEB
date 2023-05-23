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

        print(accountresult)
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

        print(bankCombo, accountresult)
        return JsonResponse({"bankCombo": bankCombo, "accountList": accountresult})



def accountViews_save(request):
    if 'btnSave' in request.POST:
        accNum = request.POST.get('accNum')
        accName = request.POST.get('accName')
        bankCode = request.POST.get('bankCode')
        strDate = request.POST.get('strDate').replace('-', '')
        endDate = request.POST.get('endDate').replace('-', '')
        accPrc = request.POST.get('accPrc')
        remark = request.POST.get('remark')
        inepno = request.session['userid']
        utepno = request.session['userid']

        with connection.cursor() as cursor:
            cursor.execute("INSERT INTO ACNUMBER "
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
                           ") "
                           "    VALUES "
                           "    ("
                           "    '" + accNum + "'"
                           ",   '" + str(accName) + "'"
                           ",   '" + str(bankCode) + "'"
                           ",   '" + str(strDate) + "'"
                           ",   '" + str(endDate) + "'"
                           ",   '" + str(accPrc) + "'"
                           ",   '" + str(remark) + "'"
                           ",   '" + str(inepno) + "'"
                           ",   date_format(now(), '%Y%m%d')"
                           "    ) "
                           "    ON DUPLICATE  KEY "
                           "    UPDATE "
                           "     ACNUM_NAME = '" + str(accName) + "' "
                           ",    ACBKCD = '" + str(bankCode) + "' "
                           ",    ACINDTE = '" + str(strDate) + "' "
                           ",    ACENDTE = '" + str(endDate) + "' "
                           ",    ACPAY = '" + str(accPrc) + "' "
                           ",    ACDESC = '" + str(remark) + "' "
                           ",    UEPNO = '" + str(utepno) + "' "
                           ",    UDATE = date_format(now(), '%Y%m%d') "
                           )
            connection.commit()

            messages.success(request, '저장 되었습니다.')
            return render(request, 'home/base-account.html')

    else:
        messages.warning(request, '입력 하신 정보를 확인 해주세요.')
        return redirect('/base_account')