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


def actBalRegViews(request):

    return render(request, "finance/accountBalance-reg.html")

def actBalRegViews_search(request):
    actCode = request.POST.get('actCode')
    actNum = request.POST.get('actNum')
    bankCode = request.POST.get('bankCode')
    user = request.session.get('userId')
    iCust = request.session.get('USER_ICUST')

    if actNum is not None and actNum != '' and bankCode is not None and bankCode != '':
        with connection.cursor() as cursor:
            cursor.execute(
                " SELECT IFNULL(A.ACNUMBER,''), IFNULL(B.ACNUM_NAME,''), IFNULL(B.ACBKCD, ''), IFNULL(C.RESNAM,'') "
                "        ,IFNULL(A.ACDATE,''), IFNULL(A.ACAMTS, 0), IFNULL(A.ACDESC, '') "
                "       FROM ACBALANCE A "
                "       LEFT OUTER JOIN ACNUMBER B "
                "       ON A.ACNUMBER = B.ACNUMBER "
                "       LEFT OUTER JOIN OSREFCP C "
                "       ON B.ACBKCD = C.RESKEY "
                "       AND C.RECODE = 'BNK' "
                "       WHERE A.ACNUMBER LIKE '%" + actNum + "%'"
                "       AND B.ACBKCD LIKE '%" + bankCode + "%' "
                "       AND A.ICUST = '" + str(iCust) + "' "
                "       ORDER BY A.ACDATE"
            )
            actBalresult = cursor.fetchall()

        # 은행명 - 콤보박스
        with connection.cursor() as cursor:
            cursor.execute(" SELECT RESKEY, RESNAM FROM OSREFCP WHERE RECODE = 'BNK' AND ICUST = '" + str(iCust) + "' ")
            cboBankName = cursor.fetchall()

        # 계좌번호 - 콤보박스
        with connection.cursor() as cursor:
            cursor.execute(" SELECT ACNUMBER FROM ACNUMBER WHERE ICUST = '" + str(iCust) + "' ")
            cboActNum = cursor.fetchall()

        return JsonResponse({"cboActNum": cboActNum, "cboBankName": cboBankName, "actBalList": actBalresult})


    elif actCode is not None and actCode != '' or bankCode is not None and bankCode != '':
        # 계좌명 - 콤보박스
        with connection.cursor() as cursor:
            cursor.execute(" SELECT A.ACNUMBER, A.ACNUM_NAME, A.ACBKCD, B.RESNAM FROM ACNUMBER A "
                           "    LEFT OUTER JOIN OSREFCP B "
                           "    ON A.ACBKCD = B.RESKEY "
                           "    AND B.RECODE = 'BNK' "
                           "    WHERE A.ACNUMBER LIKE '%" + actCode + "%' "
                           "    AND A.ACBKCD LIKE '%" + bankCode + "%' "
                           "    AND A.ICUST = '" + str(iCust) + "' ")
            actResult = cursor.fetchall()
            print(actResult)

        return JsonResponse({"actList": actResult})

    else:
        with connection.cursor() as cursor:
            cursor.execute(
                " SELECT IFNULL(A.ACNUMBER,''), IFNULL(B.ACNUM_NAME,''), IFNULL(B.ACBKCD, ''), IFNULL(C.RESNAM,'') "
                "        ,IFNULL(A.ACDATE,''), IFNULL(A.ACAMTS, 0), IFNULL(A.ACDESC, '') "
                "       FROM ACBALANCE A "
                "       LEFT OUTER JOIN ACNUMBER B "
                "       ON A.ACNUMBER = B.ACNUMBER "
                "       LEFT OUTER JOIN OSREFCP C "
                "       ON B.ACBKCD = C.RESKEY "
                "       AND C.RECODE = 'BNK' "
                "       WHERE A.ICUST = '" + str(iCust) + "'"
                "       ORDER BY A.ACDATE"
            )
            actBalresult = cursor.fetchall()

            print(actBalresult)

        # 은행명 - 콤보박스
        with connection.cursor() as cursor:
            cursor.execute(" SELECT RESKEY, RESNAM FROM OSREFCP WHERE RECODE = 'BNK' AND ICUST = '" + str(iCust) + "' ")
            inputBankType = cursor.fetchall()

        # 계좌번호 - 콤보박스
        with connection.cursor() as cursor:
            cursor.execute(" SELECT ACNUMBER FROM ACNUMBER WHERE ICUST = '" + str(iCust) + "' ")
            cboActNum = cursor.fetchall()

        return JsonResponse({"inputBankType": inputBankType, "actBalList": actBalresult, "cboActNum": cboActNum})


def actBalRegViews_save(request):
    actNum = request.POST.get('cboActNum')
    actDate = request.POST.get('txtDate').replace('-', '')
    actAmts = request.POST.get('txtBalance').replace(',', '')
    actDesc = request.POST.get('txtRemark')
    user = request.session.get('userId')
    iCust = request.session.get('USER_ICUST')

    with connection.cursor() as cursor:
        cursor.execute(" SELECT ACNUMBER FROM ACBALANCE WHERE ACNUMBER = '" + actNum + "' AND ICUST = '" + str(iCust) + "' ")
        chkresult = cursor.fetchall()
        if chkresult:
            with connection.cursor() as cursor:
                cursor.execute("    UPDATE ACBALANCE SET "
                               "     ACAMTS  = '" + str(actAmts) + "' "
                               ",    ACDESC = '" + str(actDesc) + "' "
                               ",    UPD_USER = '" + str(user) + "' "
                               ",    UPD_DT = date_format(now(), '%Y%m%d') "
                               "     WHERE ACNUMBER = '" + str(actNum) + "' "
                               "       AND ICUST = '" + str(iCust) + "'"
                               )
                connection.commit()

                return JsonResponse({'sucYn': "Y"})

            return render(request, 'finance/accountBalance-reg.html')

        else:
            with connection.cursor() as cursor:
                cursor.execute("INSERT INTO ACBALANCE "
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
                               "    '" + actNum + "' "
                               ",   '" + str(actDate) + "' "
                               ",   '" + str(actAmts) + "' "
                               ",   '" + str(actDesc) + "' "
                               ",   '" + str(user) + "' "
                               ",   date_format(now(), '%Y%m%d') "
                               ",   '" + str(iCust) + "' "
                               "    ) "
                               )
                connection.commit()

            return JsonResponse({'sucYn': "Y"})


def actBalRegViews_dlt(request):
    iCust = request.session.get('USER_ICUST')

    if request.method == "POST":
        dataList = json.loads(request.POST.get('arrList'))
        print(dataList)
        for act in dataList:
            acc_split_list = act.split(',')
            with connection.cursor() as cursor:
                cursor.execute(" DELETE FROM ACBALANCE WHERE ACNUMBER = '" + acc_split_list[0] + "' "
                               "                        AND ACDATE = '" + acc_split_list[1] + "' "
                               "                        AND ICUST = '" + str(iCust) + "' ")
                connection.commit()

        return JsonResponse({'sucYn': "Y"})

    else:
        return render(request, 'finance/accountBalance-reg.html')