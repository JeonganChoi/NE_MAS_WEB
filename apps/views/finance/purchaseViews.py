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


def purchaseRegViews(request):

    return render(request, "finance/purchases-reg.html")

def purchaseRegViews_search(request):
    strDate = request.POST.get('strDate')
    endDate = request.POST.get('endDate')

    with connection.cursor() as cursor:
        cursor.execute(" SELECT IFNULL(A.TRDATE, ''), IFNULL(A.TRSEQN, ''), IFNULL(A.TRRECN, ''), IFNULL(A.TRITEM, '')"
                       "    , IFNULL(C.ITNAME, ''), IFNULL(A.TRRCID, ''), IFNULL(D.RESNAM, '')"
                       "    , IFNULL(A.TROTP, ''), IFNULL(E.RESNAM, ''), IFNULL(A.TRPRCE, 0), IFNULL(A.TRQTYS, 0)"
                       "    , IFNULL(A.TRAMTS, 0), IFNULL(A.TRVATS, 0)"
                       "    , IFNULL(A.TRDESC, ''), IFNULL(A.TRCUST, ''), IFNULL(B.CUST_NME, '') "
                       "    FROM OSTRNSP A "
                       "    LEFT OUTER JOIN MIS1TB003 B "
                       "    ON A.TRCUST = B.CUST_NBR "
                       "    LEFT OUTER JOIN OSITEMP C "
                       "    ON A.TRITEM = C.ITITEM "
                       "    LEFT OUTER JOIN OSREFCP D "
                       "    ON A.TRRCID = D.RESKEY "
                       "    AND D.RECODE = 'IPG' "
                       "    LEFT OUTER JOIN OSREFCP E "
                       "    ON A.TROTP = E.RESKEY "
                       "    AND E.RECODE = 'OUB' "
                       "    WHERE TRDATE BETWEEN '" + strDate + "' AND '" + endDate + "' "
                       "    ORDER BY TRDATE "
                       )

        buyresult = cursor.fetchall()

        # 구분
        with connection.cursor() as cursor:
            cursor.execute(" SELECT RESKEY, RESNAM FROM OSREFCP WHERE RECODE = 'IPG' ORDER BY RESNAM ")
            comboGbn = cursor.fetchall()

        # 결제방법
        with connection.cursor() as cursor:
            cursor.execute(" SELECT RESKEY, RESNAM FROM OSREFCP WHERE RECODE = 'OUB' ORDER BY RESNAM ")
            comboPay = cursor.fetchall()

    return JsonResponse({"buyList": buyresult, "comboGbn": comboGbn, "comboPay": comboPay})



def purchaseRegViews_save(request):
    if 'btnSave' in request.POST:
        # 입고일자, 입고순번, 입고행번, 입고거래처, 입고품목, 갯수, 단가, 공급가액, 부가세, 합계, 구분, 결제방법, 비고
        trDate = request.POST.get('txtInDate').replace('-', '')
        trSeqn = request.POST.get('txtSeq')
        trRecn = request.POST.get('txtRecn')
        trCust = request.POST.get('cboInCust')
        trItem = request.POST.get('txtItem')
        trPrce = request.POST.get('txtBaseCost')
        trQtys = request.POST.get('txtQty')
        ttAmts = request.POST.get('txtPrice')
        trVats = request.POST.get('txtTax')
        # buyTotal = request.POST.get('txtTotal')
        trRcid = request.POST.get('cboBuyGbn')
        trOtp = request.POST.get('cboPayGbn')
        trDesc = request.POST.get('txtRemark')
        trIocd = 'I'

        with connection.cursor() as cursor:
            cursor.execute("INSERT INTO OSTRNSP "
                           "   (    "
                           "     TRDATE "
                           ",    TRSEQN "
                           ",    TRRECN "
                           ",    TRITEM "
                           ",    TRRCID "
                           ",    TROTP "
                           ",    TRPRCE "
                           ",    TRQTYS "
                           ",    TRAMTS "
                           ",    TRVATS "
                           ",    TRDESC "
                           ",    TRCUST "
                           ",    TRIOCD "
                           "    ) "
                           "    VALUES "
                           "    (   "
                           "    '" + str(trDate) + "'"
                           ",   (SELECT IFNULL(MAX(TRSEQN) + 1, 1) AS TRSEQN FROM OSTRNSP A WHERE TRDATE = '" + str(trDate) + "' )"
                           ",   (SELECT IFNULL (MAX(TRRECN) + 1, 1) AS TRRECN FROM OSTRNSP A WHERE TRDATE = '" + str(trDate) + "' AND TRSEQN = '" + str(trSeqn) + "')"
                           ",   '" + str(trItem) + "'"
                           ",   '" + str(trRcid) + "'"
                           ",   '" + str(trOtp) + "'"
                           ",   '" + str(trPrce) + "'"
                           ",   '" + str(trQtys) + "'"
                           ",   '" + str(ttAmts) + "'"
                           ",   '" + str(trVats) + "'"
                           ",   '" + str(trDesc) + "'"
                           ",   '" + str(trCust) + "'"
                           ",   '" + str(trIocd) + "'"
                           "    )   "
                           "    ON DUPLICATE  KEY "
                           "    UPDATE "
                           "     TROTP = '" + str(trOtp) + "' "
                           ",    TRPRCE = '" + str(trPrce) + "' "
                           ",    TRQTYS = '" + str(trQtys) + "' "
                           ",    TRAMTS = '" + str(ttAmts) + "' "
                           ",    TRVATS = '" + str(trVats) + "' "
                           ",    TRDESC = '" + str(trDesc) + "' "
                           ",    TRCUST = '" + str(trCust) + "' "
                           )
            connection.commit()

            messages.success(request, '저장 되었습니다.')
            return render(request, 'finance/purchases_reg.html')

    else:
        messages.warning(request, '입력 하신 정보를 확인 해주세요.')
        return redirect('/purchase_reg')


def purchaseRegViews_dlt(request):
    if request.method == "POST":
        dataList = json.loads(request.POST.get('arrList'))
        print(dataList)
        for buy in dataList:
            acc_split_list = buy.split(',')
            with connection.cursor() as cursor:
                cursor.execute(" DELETE FROM OSTRNSP WHERE TRDATE = '" + acc_split_list[0] + "' "
                               "                        AND TRSEQN = '" + acc_split_list[1] + "' "
                               "                        AND TRRECN = '" + acc_split_list[2] + "' "
                               "                        AND TRITEM = '" + acc_split_list[3] + "' "
                               "                        AND TRRCID = '" + acc_split_list[4] + "'")
                connection.commit()

        return JsonResponse({'sucYn': "Y"})

    else:
        return render(request, 'finance/purchase-reg.html')