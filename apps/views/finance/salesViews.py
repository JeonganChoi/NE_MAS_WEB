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
    serial = request.POST.get('serial')
    regDate = request.POST.get('regDate')

    if serial != '' and serial is not None:
        with connection.cursor() as cursor:
            cursor.execute(" SELECT IFNULL(A.SERIAL_NUM, ''), IFNULL(A.GUBUN, ''), IFNULL(A.BAL_DD, '') "
                           "    , IFNULL(A.ITEM, ''), IFNULL(A.QTY, 0), IFNULL(A.DANGA, 0), IFNULL(A.SUPPLY, 0) "
                           "    , IFNULL(A.TAX, 0), IFNULL(A.AMTS, 0), IFNULL(A.REMARK, '')"
                           "    , IFNULL(A.UP_CODE, ''), IFNULL(B.CUST_NME, '') "
                           "    FROM OSBILL A "
                           "    LEFT OUTER JOIN MIS1TB003 B "
                           "    ON A.UP_CODE = B.CUST_NBR "
                           "    WHERE A.BAL_DD = '" + regDate + "' "
                           "    AND A.GUBUN = '2' "
                           "    AND A.SERIAL_NUM = '" + serial + "' ")
            modalresult = cursor.fetchall()

        with connection.cursor() as cursor:
            cursor.execute(" SELECT CUST_NBR, CUST_NME FROM MIS1TB003 WHERE CUST_GBN = '2' ORDER BY CUST_NBR ")
            cboCust = cursor.fetchall()

        return JsonResponse({"modalList": modalresult, 'cboCust': cboCust})

    elif strDate and endDate:
        with connection.cursor() as cursor:
            cursor.execute(" SELECT IFNULL(A.SERIAL_NUM, ''), IFNULL(A.GUBUN, ''), IFNULL(A.BAL_DD, '') "
                           "    , IFNULL(A.ITEM, ''), IFNULL(A.QTY, 0), IFNULL(A.DANGA, 0), IFNULL(A.SUPPLY, 0) "
                           "    , IFNULL(A.TAX, 0), IFNULL(A.AMTS, 0), IFNULL(A.UP_CODE, ''), IFNULL(B.CUST_NME, '') "
                           "    FROM OSBILL A "
                           "    LEFT OUTER JOIN MIS1TB003 B "
                           "    ON A.UP_CODE = B.CUST_NBR "
                           "    WHERE A.BAL_DD BETWEEN '" + strDate + "' AND '" + endDate + "' "
                           "    AND A.GUBUN = '2' "
                           "    ORDER BY BAL_DD ")

            saleresult = cursor.fetchall()

        with connection.cursor() as cursor:
            cursor.execute(" SELECT CUST_NBR, CUST_NME FROM MIS1TB003 WHERE CUST_GBN = '2' ORDER BY CUST_NBR ")
            cboCust = cursor.fetchall()

        return JsonResponse({"saleList": saleresult, 'cboCust': cboCust})

    else:
        with connection.cursor() as cursor:
            cursor.execute(" SELECT CUST_NBR, CUST_NME FROM MIS1TB003 WHERE CUST_GBN = '2' ORDER BY CUST_NBR ")
            cboCust = cursor.fetchall()

        return JsonResponse({'cboCust': cboCust})

def salesRegViews_save(request):
    if 'btnSave' in request.POST:
        gubun = '2'
        serial_num = request.POST.get('txtSerial')
        bal_dd = request.POST.get('txtDate').replace('-', '')
        up_code = request.POST.get('cboCust')
        item = request.POST.get('txtItem')
        qty = request.POST.get('txtQty')
        danga = request.POST.get('txtDanga')
        supply = request.POST.get('txtSupply')
        tax = request.POST.get('txtVat')
        amts = request.POST.get('txtAmts')
        remark = request.POST.get('txtRemark')

        if serial_num == '':
            with connection.cursor() as cursor:
                cursor.execute("INSERT INTO OSBILL "
                               "   (    "
                               "     GUBUN "
                               ",    SERIAL_NUM "
                               ",    BAL_DD "
                               ",    UP_CODE "
                               ",    ITEM "
                               ",    QTY "
                               ",    DANGA "
                               ",    SUPPLY "
                               ",    TAX "
                               ",    AMTS "
                               ",    REMARK "
                               "    ) "
                               "    VALUES "
                               "    (   "
                               "    '" + str(gubun) + "'"
                               ",   (SELECT IFNULL(MAX(SERIAL_NUM) + 1, 1) AS SERIAL_NUM FROM OSBILL A WHERE SERIAL_NUM = (SELECT A.SERIAL_NUM FROM OSBILL A ORDER BY A.SERIAL_NUM DESC LIMIT 1))"
                               ",   '" + str(bal_dd) + "'"
                               ",   '" + str(up_code) + "'"
                               ",   '" + str(item) + "'"
                               ",   '" + str(qty) + "'"
                               ",   '" + str(danga) + "'"
                               ",   '" + str(supply) + "'"
                               ",   '" + str(tax) + "'"
                               ",   '" + str(amts) + "'"
                               ",   '" + str(remark) + "'"
                               "    )   "
                               )
                connection.commit()

            messages.success(request, '저장 되었습니다.')
            return redirect('/sales_reg')

        elif serial_num:
            with connection.cursor() as cursor:
                cursor.execute(" UPDATE OSBILL SET "
                               "     GUBUN = '" + str(gubun) + "' "
                               ",    BAL_DD = '" + str(bal_dd) + "' "
                               ",    UP_CODE = '" + str(up_code) + "' "
                               ",    ITEM = '" + str(item) + "' "
                               ",    QTY = '" + str(qty) + "' "
                               ",    DANGA = '" + str(danga) + "' "
                               ",    SUPPLY = '" + str(supply) + "' "
                               ",    TAX = '" + str(tax) + "' "
                               ",    AMTS = '" + str(amts) + "' "
                               ",    REMARK = '" + str(remark) + "' "
                               "     WHERE SERIAL_NUM = '" + str(serial_num) + "' "
                               )
                connection.commit()
            messages.success(request, '저장 되었습니다.')
            return redirect('/sales_reg')

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
                cursor.execute(" DELETE FROM OSBILL WHERE SERIAL_NUM = '" + acc_split_list[0] + "' "
                               "                    AND GUBUN = '" + acc_split_list[1] + "' "
                               "                    AND BAL_DD = '" + acc_split_list[2] + "'")
                connection.commit()

        return JsonResponse({'sucYn': "Y"})

    else:
        return render(request, 'finance/sales-reg.html')