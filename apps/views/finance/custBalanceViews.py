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


def custBalRegViews(request):

    return render(request, "finance/custBalance-reg.html")



def custBalRegViews_search(request):
    startDate = request.POST.get('startDate')
    endDate = request.POST.get('endDate')
    regDate = request.POST.get('regDate')
    custCode = request.POST.get('custCode')

    if regDate is not None and regDate != '' and custCode is not None and custCode != '':
        with connection.cursor() as cursor:
            cursor.execute(
                " SELECT IFNULL(A.MOdate,''), IFNULL(A.MOCUST, ''), IFNULL(B.CUST_NME,'') "
                "    , IFNULL(A.MOIWOL, 0), IFNULL(A.MOIWOL2, 0), IFNULL(A.MODESC, ''), IFNULL(B.CUST_GBN, '') "
                "    FROM SIOMONTT A "
                "    LEFT OUTER JOIN MIS1TB003 B "
                "    ON A.MOCUST = B.CUST_NBR "
                "    WHERE A.MOdate LIKE '%" + regDate + "%' "
                "    AND A.MOCUST LIKE '%" + custCode + "%' "
                "    ORDER BY A.MOdate ")

            custBalresult = cursor.fetchall()

        # 거래처 - 콤보박스
        with connection.cursor() as cursor:
            cursor.execute(" SELECT CUST_NBR, CUST_NME, CUST_GBN FROM MIS1TB003 "
                           "        WHERE CUST_GBN = '1' "
                           "        OR CUST_GBN = '2' "
                           "        OR CUST_GBN = '3' ")
            cboCustType = cursor.fetchall()

        return JsonResponse({"cboCustType": cboCustType, "custBalList": custBalresult})

    else:
        with connection.cursor() as cursor:
            cursor.execute(
                " SELECT IFNULL(A.MOdate,''), IFNULL(A.MOCUST, ''), IFNULL(B.CUST_NME,'') "
                "    , IFNULL(A.MOIWOL, 0), IFNULL(A.MOIWOL2, 0), IFNULL(A.MODESC, ''), IFNULL(B.CUST_GBN, '') "
                "    FROM SIOMONTT A "
                "    LEFT OUTER JOIN MIS1TB003 B "
                "    ON A.MOCUST = B.CUST_NBR "
                "    WHERE A.MOdate BETWEEN '" + startDate + "' AND '" + endDate + "' "
                "    AND A.MOCUST LIKE '%" + custCode + "%'"
                "    ORDER BY A.MOdate ")

            custBalresult = cursor.fetchall()

        # 거래처 - 콤보박스
        with connection.cursor() as cursor:
            cursor.execute(" SELECT CUST_NBR, CUST_NME, CUST_GBN FROM MIS1TB003 "
                           "        WHERE CUST_GBN = '1' "
                           "        OR CUST_GBN = '2' "
                           "        OR CUST_GBN = '3' ")
            inputCustType = cursor.fetchall()

        return JsonResponse({"inputCustType": inputCustType, "custBalList": custBalresult})


def custBalRegViews_save(request):
    if 'btnSave' in request.POST:
        moCust = request.POST.get('cboCustCode')
        moDate = request.POST.get('txtRegDate').replace('-', '')
        moIwol = request.POST.get('txtNonGet')
        moIwol2 = request.POST.get('txtNonPay')
        moDesc = request.POST.get('txtRemark')
        # iUser = request.POST.get('txtDate')
        # uUser = request.POST.get('txtBalance')

        with connection.cursor() as cursor:
            cursor.execute("INSERT INTO ACBALANCE "
                           "   ("
                           "     MOCUST "
                           ",    MOdate "
                           ",    MOIWOL "
                           ",    MOIWOL2 "
                           ",    MODESC "
                           ") "
                           "    VALUES "
                           "    ("
                           "    '" + moCust + "' "
                           ",   date_format(now(), '%Y%m%d') "
                           ",   '" + str(moIwol) + "' "
                           ",   '" + str(moIwol2) + "' "
                           ",   '" + str(moDesc) + "' "
                           "    ) "
                           "    ON DUPLICATE  KEY "
                           "    UPDATE "
                           "     MOIWOL  = '" + str(moIwol) + "' "
                           ",    MOIWOL2 = '" + str(moIwol2) + "' "
                           ",    MODESC = '" + str(moDesc) + "' "
                           )
            connection.commit()

            messages.success(request, '저장 되었습니다.')
            return render(request, 'finance/custBalance-reg.html')

    else:
        messages.warning(request, '입력 하신 정보를 확인 해주세요.')
        return redirect('/custBalance_reg')



def custBalRegViews_dlt(request):
    if request.method == "POST":
        dataList = json.loads(request.POST.get('arrList'))
        print(dataList)
        for cust in dataList:
            acc_split_list = cust.split(',')
            with connection.cursor() as cursor:
                cursor.execute(" DELETE FROM SIOMONTT WHERE MOdate = '" + acc_split_list[0] + "' "
                               "                        AND MOCUST = '" + acc_split_list[1] + "' ")
                connection.commit()

        return JsonResponse({'sucYn': "Y"})

    else:
        return render(request, 'finance/custBalance-reg.html')