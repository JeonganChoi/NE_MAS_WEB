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

def custViews(request):

    return render(request, "base/base-cust.html")

def custViews_search(request):
    custType = request.POST.get('custType')
    custCode = request.POST.get('custCode')
    custYn = request.POST.get('custYn')
    iCust = request.session.get('USER_ICUST')

    if custCode is not None and custCode != '' and custType is not None and custType != '':
        with connection.cursor() as cursor:
            cursor.execute(
                " SELECT IFNULL(A.CUST_NME, ''), IFNULL(A.CUST_NBR, ''), IFNULL(A.CUST_CEO_NME, ''), IFNULL(A.CUST_ID_NBR, '') "
                "   , IFNULL(A.CUST_BSN_CON, ''), IFNULL(A.CUST_BSN_TYP, ''), IFNULL(A.CUST_POST_NBR, '') "
                "   , IFNULL(A.CUST_ADDR, ''), IFNULL(A.CUST_TEL_NBR, ''), IFNULL(A.CUST_FAX_NBR, '') "
                "   , IFNULL(A.CUST_EMP_NME, ''), IFNULL(A.CUST_EMP_PHN, ''), IFNULL(A.CUST_EMAIL, '') "
                "   , IFNULL(A.CUST_HOMEP, ''), IFNULL(A.CUST_GBN, ''), IFNULL(D.RESNAM, ''), IFNULL(A.CUST_BUNR, '')"
                "   , IFNULL(A.CUST_END_CHK, 'Y'), IFNULL(A.CRE_DT, '') "
                "   FROM MIS1TB003 A "
                "   LEFT OUTER JOIN OSREFCP D "
                "   ON A.CUST_GBN = D.RESKEY "
                "   AND D.RECODE = 'BGB' "
                "   WHERE A.CUST_NBR LIKE '%" + custCode + "%' "
                "   OR A.CUST_NME LIKE '%" + custCode + "%' "
                "   AND A.CUST_GBN = '" + custType + "' "
                "   AND A.ICUST = '" + str(iCust) + "'"
            )
            custresult = cursor.fetchall()

        return JsonResponse({"custList": custresult})

    elif custCode is not None and custCode != '':
        with connection.cursor() as cursor:
            cursor.execute(
                " SELECT IFNULL(A.CUST_NME, ''), IFNULL(A.CUST_NBR, ''), IFNULL(A.CUST_CEO_NME, ''), IFNULL(A.CUST_ID_NBR, '') "
                "   , IFNULL(A.CUST_BSN_CON, ''), IFNULL(A.CUST_BSN_TYP, ''), IFNULL(A.CUST_POST_NBR, '') "
                "   , IFNULL(A.CUST_ADDR, ''), IFNULL(A.CUST_TEL_NBR, ''), IFNULL(A.CUST_FAX_NBR, '') "
                "   , IFNULL(A.CUST_EMP_NME, ''), IFNULL(A.CUST_EMP_PHN, ''), IFNULL(A.CUST_EMAIL, '') "
                "   , IFNULL(A.CUST_HOMEP, ''), IFNULL(A.CUST_GBN, ''), IFNULL(D.RESNAM, ''), IFNULL(A.CUST_BUNR, '')"
                "   , IFNULL(A.CUST_END_CHK, 'Y'), IFNULL(A.CRE_USER, ''), IFNULL(A.CRE_DT, ''), IFNULL(A.CUST_PAY_DAY, '') "
                "   FROM MIS1TB003 A "
                "   LEFT OUTER JOIN OSREFCP D "
                "   ON A.CUST_GBN = D.RESKEY "
                "   AND D.RECODE = 'BGB' "
                "   WHERE A.CUST_NBR LIKE '%" + custCode + "%' "
                "   OR A.CUST_NME LIKE '%" + custCode + "%' "
                "   AND A.ICUST = '" + str(iCust) + "' "
            )
            custresult = cursor.fetchall()
            print(custresult)

            # 업체 분류 - 콤보박스
        with connection.cursor() as cursor:
            cursor.execute(" SELECT RESKEY, RESNAM FROM OSREFCP WHERE RECODE = 'BGB' ")
            cboCustType = cursor.fetchall()

            # 업체군 분류 - 콤보박스
        # with connection.cursor() as cursor:
        #     cursor.execute(" SELECT RESKEY, RESNAM FROM OSREFCP WHERE RECODE = 'CGB' ")
        #     cboCustType2 = cursor.fetchall()

        return JsonResponse({"cboCustType": cboCustType, "custList": custresult})

    elif custYn is not None and custYn != '':
        with connection.cursor() as cursor:
            cursor.execute(
                " SELECT IFNULL(A.CUST_NME, ''), IFNULL(A.CUST_NBR, ''), IFNULL(A.CUST_CEO_NME, ''), IFNULL(A.CUST_ID_NBR, '') "
                "   , IFNULL(A.CUST_BSN_CON, ''), IFNULL(A.CUST_BSN_TYP, ''), IFNULL(A.CUST_POST_NBR, '') "
                "   , IFNULL(A.CUST_ADDR, ''), IFNULL(A.CUST_TEL_NBR, ''), IFNULL(A.CUST_FAX_NBR, '') "
                "   , IFNULL(A.CUST_EMP_NME, ''), IFNULL(A.CUST_EMP_PHN, ''), IFNULL(A.CUST_EMAIL, '') "
                "   , IFNULL(A.CUST_HOMEP, ''), IFNULL(A.CUST_GBN, ''), IFNULL(D.RESNAM, ''), IFNULL(A.CUST_BUNR, '')"
                "   , IFNULL(A.CUST_END_CHK, 'Y'), IFNULL(A.CRE_DT, ''), IFNULL(A.CUST_PAY_DAY, '') "
                "   FROM MIS1TB003 A "
                "   LEFT OUTER JOIN OSREFCP D "
                "   ON A.CUST_GBN = D.RESKEY "
                "   AND D.RECODE = 'BGB' "
                "   WHERE A.CUST_END_CHK LIKE '%" + custYn + "%' AND A.ICUST = '" + str(iCust) + "' "
            )
            custresult = cursor.fetchall()


        return JsonResponse({"custList": custresult})

    elif custType is not None and custType != '':
        with connection.cursor() as cursor:
            cursor.execute(
                " SELECT IFNULL(A.CUST_NME, ''), IFNULL(A.CUST_NBR, ''), IFNULL(A.CUST_CEO_NME, ''), IFNULL(A.CUST_ID_NBR, '') "
                "   , IFNULL(A.CUST_BSN_CON, ''), IFNULL(A.CUST_BSN_TYP, ''), IFNULL(A.CUST_POST_NBR, '') "
                "   , IFNULL(A.CUST_ADDR, ''), IFNULL(A.CUST_TEL_NBR, ''), IFNULL(A.CUST_FAX_NBR, '') "
                "   , IFNULL(A.CUST_EMP_NME, ''), IFNULL(A.CUST_EMP_PHN, ''), IFNULL(A.CUST_EMAIL, '') "
                "   , IFNULL(A.CUST_HOMEP, ''), IFNULL(A.CUST_GBN, ''), IFNULL(D.RESNAM, ''), IFNULL(A.CUST_BUNR, '')"
                "   , IFNULL(A.CUST_END_CHK, 'Y'), IFNULL(A.CRE_DT, ''), IFNULL(A.CUST_PAY_DAY, '') "
                "   FROM MIS1TB003 A "
                "   LEFT OUTER JOIN OSREFCP D "
                "   ON A.CUST_GBN = D.RESKEY "
                "   AND D.RECODE = 'BGB' "
                "   WHERE A.CUST_GBN LIKE '%" + custType + "%' AND A.ICUST = '" + str(iCust) + "'"
            )
            custresult = cursor.fetchall()


        return JsonResponse({"custList": custresult})

    else:
        with connection.cursor() as cursor:
            cursor.execute(
                " SELECT IFNULL(CUST_NME, ''), IFNULL(CUST_NBR, ''), IFNULL(CUST_CEO_NME, ''), IFNULL(CUST_ADDR, '') "
                "   , IFNULL(CUST_ID_NBR, ''), IFNULL(CUST_POST_NBR, ''), IFNULL(CUST_TEL_NBR, '')"
                "   , IFNULL(CUST_GBN, ''), IFNULL(CUST_END_CHK, 'Y'), IFNULL(CUST_PAY_DAY, '') "
                "   FROM MIS1TB003 WHERE ICUST = '" + str(iCust) + "'"
            )
            custresult = cursor.fetchall()

        # 업체 구분 - 콤보박스
        with connection.cursor() as cursor:
            cursor.execute(" SELECT RESKEY, RESNAM FROM OSREFCP WHERE RECODE = 'BGB' ")
            inputCustType = cursor.fetchall()

        # 사용여부 - 콤보박스
        with connection.cursor() as cursor:
            cursor.execute(" SELECT RESKEY, RESNAM FROM OSREFCP WHERE RECODE = 'UST' ")
            cboCustYn = cursor.fetchall()

        # 업체 분류 - 콤보박스
        # with connection.cursor() as cursor:
        #     cursor.execute(" SELECT RESKEY, RESNAM FROM OSREFCP WHERE RECODE = 'DPT' ")
        #     cboCustType = cursor.fetchall()

        # 업체군 분류 - 콤보박스
        # with connection.cursor() as cursor:
        #     cursor.execute(" SELECT RESKEY, RESNAM FROM OSREFCP WHERE RECODE = 'POP' ")
        #     cboCustType2 = cursor.fetchall()

        return JsonResponse({"inputCustType": inputCustType, "cboCustYn": cboCustYn, "custList": custresult})


def custViews_save(request):
    custName = request.POST.get('txtCustName')
    custCode = request.POST.get('txtCustCode')
    custCeo = request.POST.get('txtCeo')
    custRegNum = request.POST.get('txtRegNum')
    custCat = request.POST.get('txtCustCat')
    custPostCode = request.POST.get('txtPostCode')
    custAddress = request.POST.get('txtAddress')
    custTelPhone = request.POST.get('txtTelePhone')
    custFax = request.POST.get('txtFax')
    custEmp = request.POST.get('txtEmp')
    custEmpPhone = request.POST.get('txtEmpPhone')
    creDt = request.POST.get('txtRegDate').replace('-', '')
    custEmail = request.POST.get('txtEMail')
    custWeb = request.POST.get('txtWebAddress')
    custType = request.POST.get('cboCustType')
    cboDay = request.POST.get('cboDay')
    creUser = request.POST.get('txtUser')
    user = request.session.get('userId')
    iCust = request.session.get('USER_ICUST')

    if creUser is None or creUser == '':
        with connection.cursor() as cursor:
            cursor.execute("INSERT INTO MIS1TB003 "
                           "   ("
                           "     CUST_NME "
                           ",    CUST_NBR "
                           ",    CUST_CEO_NME "
                           ",    CUST_ID_NBR "
                           ",    CUST_BSN_CON "
                           ",    CUST_BSN_TYP "
                           ",    CUST_POST_NBR "
                           ",    CUST_ADDR "
                           ",    CUST_TEL_NBR "
                           ",    CUST_FAX_NBR "
                           ",    CUST_EMP_NME "
                           ",    CUST_EMP_TEL "
                           ",    CUST_EMAIL "
                           ",    CUST_HOMEP "
                           ",    CUST_GBN "
                           ",    CRE_DT "
                           ",    CRE_USER "
                           ",    CRE_USER "
                           ") "
                           "    VALUES "
                           "    ("
                           "    '" + custName + "'"
                           ",   '" + str(custCode) + "'"
                           ",   '" + str(custCeo) + "'"
                           ",   '" + str(custRegNum) + "'"
                           ",   '" + str(custCat) + "'"
                           ",   '" + str(custType) + "'"
                           ",   '" + str(custPostCode) + "'"
                           ",   '" + str(custAddress) + "'"
                           ",   '" + str(custTelPhone) + "'"
                           ",   '" + str(custFax) + "'"
                           ",   '" + str(custEmp) + "'"
                           ",   '" + str(custEmpPhone) + "'"
                           ",   '" + str(custEmail) + "'"
                           ",   '" + str(custWeb) + "'"
                           ",   '" + str(custType) + "'"
                           ",   '" + str(creDt) + "'"
                           ",   '" + str(user) + "'"
                           ",   '" + str(iCust) + "'"
                           "    ) "
                           )

            connection.commit()

        return JsonResponse({'sucYn': "Y"})

    elif creUser:
        with connection.cursor() as cursor:
            cursor.execute(" UPDATE MIS1TB003 SET "
                           "      CUST_NME  = '" + str(custName) + "' "
                           "    , CUST_CEO_NME = '" + str(custCeo) + "' "
                           "    , CUST_ID_NBR = '" + str(custRegNum) + "' "
                           "    , CUST_BSN_CON  = '" + str(custCat) + "' "
                           "    , CUST_BSN_TYP  = '" + str(custType) + "' "
                           "    , CUST_POST_NBR  = '" + str(custPostCode) + "' "
                           "    , CUST_ADDR  = '" + str(custAddress) + "' "
                           "    , CUST_TEL_NBR = '" + str(custTelPhone) + "' "
                           "    , CUST_FAX_NBR = '" + str(custFax) + "'  "
                           "    , CUST_EMP_NME  = '" + str(custEmp) + "' "
                           "    , CUST_EMP_TEL  = '" + str(custEmpPhone) + "' "
                           "    , CUST_EMAIL = '" + str(custEmail) + "' "
                           "    , CUST_HOMEP = '" + str(custWeb) + "'  "
                           "    , CUST_GBN = '" + str(custType) + "' "
                           "    , UPD_DT = '" + str(creDt) + "' "
                           "    , UPD_USER = '" + str(user) + "' "
                           "    WHERE ICUST = '" + str(iCust) + "' "
                           "      AND CUST_NBR = '" + str(custCode) + "'"
                           )
            connection.commit()

            return JsonResponse({'sucYn': "Y"})

        return render(request, 'base/base-cust.html')


def custViews_dlt(request):
    iCust = request.session.get('USER_ICUST')

    if request.method == "POST":
        dataList = json.loads(request.POST.get('arrList'))
        print(dataList)
        for cust in dataList:
            acc_split_list = cust.split(',')
            with connection.cursor() as cursor:
                cursor.execute(" DELETE FROM MIS1TB003 WHERE CUST_NBR = '" + acc_split_list[0] + "'"
                           "                            AND CUST_GBN = '" + acc_split_list[1] + "' "
                           "                            AND ICUST = '" + str(iCust) + "' ")
                connection.commit()

        return JsonResponse({'sucYn': "Y"})

    else:
        return render(request, 'base/base-cust.html')