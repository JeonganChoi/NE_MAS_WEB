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


def salesRegViews(request):

    return render(request, "finance/sales-reg.html")


def salesRegViews_search(request):
    strDate = request.POST.get('strDate')
    endDate = request.POST.get('endDate')

    with connection.cursor() as cursor:
        cursor.execute(" SELECT IFNULL(A.SADATE, ''), IFNULL(A.SASEQN, ''), IFNULL(A.SARECN, ''), IFNULL(A.SAITEM, '')"
                       "        , IFNULL(C.ITNAME, ''), IFNULL(A.SARCID, ''), IFNULL(D.RESNAM, '')"
                       "        , IFNULL(A.SAOTP, ''), IFNULL(E.RESNAM, '') "
                       "        , IFNULL(A.SAPRCE, 0), IFNULL(A.SAQTYS, 0), IFNULL(A.SAAMTS, 0), IFNULL(A.SAVATS, 0)"
                       "        , IFNULL(A.SADESC, ''), IFNULL(A.SACUST, ''), IFNULL(B.CUST_NME, '') "
                       "    FROM OSSALEP A "
                       "    LEFT OUTER JOIN MIS1TB003 B "
                       "    ON A.SACUST = B.CUST_NBR "
                       "    LEFT OUTER JOIN OSITEMP C "
                       "    ON A.SAITEM = C.ITITEM "
                       "    LEFT OUTER JOIN OSREFCP D "
                       "    ON A.SARCID = D.RESKEY "
                       "    AND D.RECODE = 'OTG' "
                       "    LEFT OUTER JOIN OSREFCP E "
                       "    ON A.SAOTP = E.RESKEY "
                       "    AND E.RECODE = 'OUB' "
                       "    WHERE SADATE BETWEEN '" + strDate + "' AND '" + endDate + "' "
                       "    ORDER BY SADATE ")

        saleresult = cursor.fetchall()

        with connection.cursor() as cursor:
            cursor.execute(" SELECT RESKEY, RESNAM FROM OSREFCP WHERE RECODE = 'OTG' ORDER BY RESNAM ")
            comboGbn = cursor.fetchall()

        # 결제방법
        with connection.cursor() as cursor:
            cursor.execute(" SELECT RESKEY, RESNAM FROM OSREFCP WHERE RECODE = 'OUB' ORDER BY RESNAM ")
            comboPay = cursor.fetchall()

    return JsonResponse({"saleList": saleresult, "comboGbn": comboGbn, "comboPay": comboPay})


def salesRegViews_save(request):
    if 'btnSave' in request.POST:
        # 출고일자, 출고순번, 출고행번, 출고거래처, 출고품목, 갯수, 단가, 공급가액, 부가세, 합계, 구분, 결제방법, 비고
        saDate = request.POST.get('txtOutDate').replace('-', '')
        saSeqn = request.POST.get('txtSaSeq')
        saRecn = request.POST.get('txtSaRecn')
        saCust = request.POST.get('cboOutCust')
        saItem = request.POST.get('txtSaItem')
        saPrce = request.POST.get('txtSaCost')
        saQtys = request.POST.get('txtSaQty')
        saAmts = request.POST.get('txtSaPrice')
        saVats = request.POST.get('txtSaTax')
        # saTotal = request.POST.get('txtSaTotal')
        saRcid = request.POST.get('cboSaGbn')
        saOtp = request.POST.get('cboPayGbn')
        saDesc = request.POST.get('cboSaRemark')

        with connection.cursor() as cursor:
            cursor.execute("INSERT INTO OSSALEP "
                           "   (    "
                           "     SADATE "
                           ",    SASEQN "
                           ",    SARECN "
                           ",    SAITEM "
                           ",    SARCID "
                           ",    SAOTP "
                           ",    SAPRCE "
                           ",    SAQTYS "
                           ",    SAAMTS "
                           ",    SAVATS "
                           ",    SADESC "
                           ",    SACUST "
                           "    ) "
                           "    VALUES "
                           "    (   "
                           "    '" + str(saDate) + "'"
                           ",   (SELECT IFNULL(MAX(SASEQN) + 1, 1) AS SASEQN FROM OSSALEP A WHERE SADATE = '" + str(saDate) + "' )"
                           ",   (SELECT IFNULL (MAX(SASEQN) + 1, 1) AS SASEQN FROM OSSALEP A WHERE SADATE = '" + str(saDate) + "' AND SASEQN = '" + str(saSeqn) + "')"
                           ",   '" + str(saItem) + "'"
                           ",   '" + str(saRcid) + "'"
                           ",   '" + str(saOtp) + "'"
                           ",   '" + str(saPrce) + "'"
                           ",   '" + str(saQtys) + "'"
                           ",   '" + str(saAmts) + "'"
                           ",   '" + str(saVats) + "'"
                           ",   '" + str(saDesc) + "'"
                           ",   '" + str(saCust) + "'"
                           "    )   "
                           "    ON DUPLICATE  KEY "
                           "    UPDATE "
                           "     SAOTP = '" + str(saOtp) + "' "
                           ",    SAPRCE = '" + str(saPrce) + "' "
                           ",    SAQTYS = '" + str(saQtys) + "' "
                           ",    SAAMTS = '" + str(saAmts) + "' "
                           ",    SAVATS = '" + str(saVats) + "' "
                           ",    SADESC = '" + str(saDesc) + "' "
                           ",    SACUST = '" + str(saCust) + "' "
                           )
            connection.commit()

            messages.success(request, '저장 되었습니다.')
            return render(request, 'finance/sales-reg.html')

    else:
        messages.warning(request, '입력 하신 정보를 확인 해주세요.')
        return redirect('/sales_reg')


def salesRegViews_dlt(request):
    if request.method == "POST":
        dataList = json.loads(request.POST.get('arrList'))
        print(dataList)
        for sale in dataList:
            acc_split_list = sale.split(',')
            with connection.cursor() as cursor:
                cursor.execute(" DELETE FROM OSSALEP WHERE SADATE = '" + acc_split_list[0] + "' "
                               "                        AND SASEQN = '" + acc_split_list[1] + "' "
                               "                        AND SARECN = '" + acc_split_list[2] + "' "
                               "                        AND SAITEM = '" + acc_split_list[3] + "' "
                               "                        AND SARCID = '" + acc_split_list[4] + "'")
                connection.commit()

        return JsonResponse({'sucYn': "Y"})

    else:
        return render(request, 'finance/sales-reg.html')