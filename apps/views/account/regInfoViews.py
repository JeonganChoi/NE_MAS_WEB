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

def regCustomers(request):

    return render(request, "account/reg-customers.html")


def regCustomers_list(request):
    custCode = request.POST.get('custCode')

    if custCode != '':
        with connection.cursor() as cursor:
            cursor.execute(
                " SELECT IFNULL(CUST_NBR, ''), IFNULL(CUST_NME, ''), IFNULL(CUST_GBN, ''), IFNULL(CEO_NAME, '') "
                "       , IFNULL(CUST_ADS, ''), IFNULL(CUST_ID_NUM, ''), IFNULL(POST_CODE, ''), IFNULL(CUST_TEL, '') "
                "       , IFNULL(CUST_FAX, ''), IFNULL(REG_DATE, ''), IFNULL(FIN_DATE, ''), IFNULL(CUST_INDUSTRY, '')"
                "       , IFNULL(CUST_TYPE, ''), IFNULL(CUST_PMK, ''), IFNULL(CUST_EMAIL, ''), IFNULL(CUST_ACCOUNT, '')"
                " FROM ACCOMLIST "
                " WHERE CUST_NBR = '" + str(custCode) + "' "
                "    OR CUST_NME = '" + str(custCode) + "' "
                " ORDER BY CUST_NBR ")
            cust = cursor.fetchall()

        return JsonResponse({"custList": cust})

    else:
        with connection.cursor() as cursor:
            cursor.execute(" SELECT IFNULL(CUST_NBR, ''), IFNULL(CUST_NME, ''), IFNULL(CUST_GBN, ''), IFNULL(CEO_NAME, '') "
                           "        , IFNULL(CUST_ADS, ''), IFNULL(CUST_ID_NUM, ''), IFNULL(POST_CODE, ''), IFNULL(CUST_TEL, '') "
                           "        , IFNULL(CUST_FAX, ''), IFNULL(REG_DATE, ''), IFNULL(FIN_DATE, '') "
                           " FROM ACCOMLIST ORDER BY CUST_NBR ")
            cust = cursor.fetchall()

        return JsonResponse({"custList": cust})


# def regCustomers_save(request):
#     regDate = request.POST.get("txtRegDate").replace('-', '')
#     expDate = request.POST.get("txtExpDate")
#     custCode = request.POST.get("txtCustCode")
#     custName = request.POST.get("txtCustName")
#     custCeo = request.POST.get("txtCeo")
#     regNum = request.POST.get("txtRegNum")
#     # 업태/ 업종
#     custCat = request.POST.get("txtCustCat")
#     custType = request.POST.get("txtCustType")
#     postCode = request.POST.get("txtPostCode")
#     custAds = request.POST.get("txtAddress")
#     custTel = request.POST.get("txtTelePhone")
#     custFax = request.POST.get("txtFax")
#     custGbn = request.POST.get("txtCustGbn")
#     custEmail = request.POST.get("txtEMail")
#     custBank = request.POST.get("txtBank")
#     custAct = request.POST.get("txtAct")
#     masterUser = request.session.get("userId")
#     masterIcust = request.session.get("USER_ICUST")
#
#     with connection.cursor() as cursor:
#         cursor.execute(" SELECT CUST_NBR FROM ACCOMLIST WHERE CUST_NBR = '" + str(custCode) + "' ")
#         result = cursor.fetchall()  # 계좌 은행
#
#     if result:
#         with connection.cursor() as cursor:
#             iCust = request.session.get("USER_ICUST")
#             cursor.execute("    UPDATE  SISACCTT SET"
#                            "     ACGUBN = '" + str(acGubn) + "' "
#                            ",    MCODE = '" + str(mCode) + "' "
#                            ",    GBN = (SELECT GBN FROM OSCODEM A WHERE MCODE = '" + str(mCode) + "' AND ICUST = '" + str(iCust) + "') "
#                            ",    ACTITLE = '" + str(acTitle) + "' "
#                            ",    ACAMTS = '" + str(acAmts) + "' "
#                            ",    ACACNUMBER = '" + str(acAcnumber) + "' "
#                            ",    ACDESC = '" + str(acDesc) + "' "
#                            ",    ACGUNO_BK = '" + str(acBank) + "' "
#                            ",    ACFOLDER = '" + str(uploaded_file) + "' "
#                            ",    EXDATE = '" + str(exDate) + "' "
#                            ",    ACDATE = '" + str(acDate) + "' "
#                            ",    ACCARD = '" + str(acCard) + "' "
#                            ",    ACUSE = '" + str(acUse) + "' "
#                            ",    ACINFO = '" + str(acInfo) + "' "
#                            ",    ACCUST = '" + str(acCust) + "' "
#                            ",    UPD_USER = '" + str(creUser) + "' "
#                            ",    UPD_DT = date_format(now(), '%Y%m%d') "
#                            "     WHERE IODATE = '" + str(ioDate) + "' "
#                            "     AND ACIOGB = '" + str(acIogb) + "' "
#                            "     AND ACSEQN = '" + str(acSeqn) + "' "
#                            "     AND ICUST = '" + str(iCust) + "' "
#                            )
#
#             connection.commit()
#     else:
