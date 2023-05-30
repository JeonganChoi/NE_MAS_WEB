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


    # if custCode is not None and custCode != '' or custType is not None and custType != '' or custYn is not None and custYn != '':
    #     with connection.cursor() as cursor:
    #         cursor.execute(
    #             " SELECT IFNULL(CUST_NME, ''), IFNULL(CUST_NBR, ''), IFNULL(CUST_CEO_NME, ''), IFNULL(CUST_ID_NBR, '') "
    #             "   , IFNULL(CUST_BSN_CON, ''), IFNULL(CUST_BSN_TYP, ''), IFNULL(CUST_POST_NBR, '') "
    #             "   , IFNULL(CUST_ADDR, ''), IFNULL(CUST_TEL_NBR, ''), IFNULL(CUST_FAX_NBR, '') "
    #             "   , IFNULL(CUST_EMP_NME, ''), IFNULL(CUST_EMP_PHN, ''), IFNULL(CUST_EMAIL, '') "
    #             "   , IFNULL(CUST_HOMEP, ''), IFNULL(CUST_GBN, ''), IFNULL(D.RESNAM, ''), IFNULL(CUST_BUNR, '')"
    #             "   , IFNULL(CUST_END_CHK, 'Y') "
    #             "   FROM MIS1TB003 A "
    #             "   LEFT OUTER JOIN OSREFCP D "
    #             "   ON A.CUST_GBN = D.RESKEY "
    #             "   AND D.RECODE = 'CGB' "
    #             "   WHERE CUST_NBR LIKE '%" + custCode + "%' "
    #             "   OR CUST_NME LIKE '%" + custCode + "%' "
    #             "   AND CUST_GBN LIKE '%" + custType + "%' "
    #             "   AND CUST_END_CHK LIKE '%" + custYn + "%' "
    #         )
    #         custresult = cursor.fetchall()
    #
    #     # 업체 구분 - 콤보박스
    #     with connection.cursor() as cursor:
    #         cursor.execute(" SELECT RESKEY, RESNAM FROM OSREFCP WHERE RECODE = 'CGB' ")
    #         inputCustType = cursor.fetchall()
    #
    #     # 사용여부 - 콤보박스
    #     with connection.cursor() as cursor:
    #         cursor.execute(" SELECT RESKEY, RESNAM FROM OSREFCP WHERE RECODE = 'UST' ")
    #         cboCustYn = cursor.fetchall()
    #
    #     # 업체 분류 - 콤보박스
    #     with connection.cursor() as cursor:
    #         cursor.execute(" SELECT RESKEY, RESNAM FROM OSREFCP WHERE RECODE = 'CGB' ")
    #         cboCustType = cursor.fetchall()
    #
    #     # 업체군 분류 - 콤보박스
    #     with connection.cursor() as cursor:
    #         cursor.execute(" SELECT RESKEY, RESNAM FROM OSREFCP WHERE RECODE = 'CGB' ")
    #         cboCustType2 = cursor.fetchall()
    #
    #     return JsonResponse({"inputCustType": inputCustType, "cboCustYn": cboCustYn, "cboCustType": cboCustType, "cboCustType2": cboCustType2
    #                             , "custList": custresult})

    if custCode is not None and custCode != '':
        with connection.cursor() as cursor:
            cursor.execute(
                " SELECT IFNULL(CUST_NME, ''), IFNULL(CUST_NBR, ''), IFNULL(CUST_CEO_NME, ''), IFNULL(CUST_ID_NBR, '') "
                "   , IFNULL(CUST_BSN_CON, ''), IFNULL(CUST_BSN_TYP, ''), IFNULL(CUST_POST_NBR, '') "
                "   , IFNULL(CUST_ADDR, ''), IFNULL(CUST_TEL_NBR, ''), IFNULL(CUST_FAX_NBR, '') "
                "   , IFNULL(CUST_EMP_NME, ''), IFNULL(CUST_EMP_PHN, ''), IFNULL(CUST_EMAIL, '') "
                "   , IFNULL(CUST_HOMEP, ''), IFNULL(CUST_GBN, ''), IFNULL(D.RESNAM, ''), IFNULL(CUST_BUNR, '')"
                "   , IFNULL(CUST_END_CHK, 'Y') "
                "   FROM MIS1TB003 A "
                "   LEFT OUTER JOIN OSREFCP D "
                "   ON A.CUST_GBN = D.RESKEY "
                "   AND D.RECODE = 'CGB' "
                "   WHERE CUST_NBR LIKE '%" + custCode + "%' "
                "   OR CUST_NME LIKE '%" + custCode + "%' "
            )
            custresult = cursor.fetchall()

        # 업체 구분 - 콤보박스
        with connection.cursor() as cursor:
            cursor.execute(" SELECT RESKEY, RESNAM FROM OSREFCP WHERE RECODE = 'CGB' ")
            inputCustType = cursor.fetchall()

        # 사용여부 - 콤보박스
        with connection.cursor() as cursor:
            cursor.execute(" SELECT RESKEY, RESNAM FROM OSREFCP WHERE RECODE = 'UST' ")
            cboCustYn = cursor.fetchall()

        # 업체 분류 - 콤보박스
        with connection.cursor() as cursor:
            cursor.execute(" SELECT RESKEY, RESNAM FROM OSREFCP WHERE RECODE = 'CGB' ")
            cboCustType = cursor.fetchall()

        # 업체군 분류 - 콤보박스
        with connection.cursor() as cursor:
            cursor.execute(" SELECT RESKEY, RESNAM FROM OSREFCP WHERE RECODE = 'CGB' ")
            cboCustType2 = cursor.fetchall()

        return JsonResponse({"inputCustType": inputCustType, "cboCustYn": cboCustYn, "cboCustType": cboCustType, "cboCustType2": cboCustType2
                                , "custList": custresult})
    else:
        with connection.cursor() as cursor:
            cursor.execute(
                " SELECT IFNULL(CUST_NBR, ''), IFNULL(CUST_NME, ''), IFNULL(CUST_CEO_NME, ''), IFNULL(CUST_ADDR, '') "
                "   , IFNULL(CUST_ID_NBR, ''), IFNULL(CUST_POST_NBR, ''), IFNULL(CUST_TEL_NBR, '')"
                "   , IFNULL(CUST_GBN, ''), IFNULL(CUST_END_CHK, 'Y') "
                "   FROM MIS1TB003"
            )
            custresult = cursor.fetchall()

        # 업체 구분 - 콤보박스
        with connection.cursor() as cursor:
            cursor.execute(" SELECT RESKEY, RESNAM FROM OSREFCP WHERE RECODE = 'CGB' ")
            inputCustType = cursor.fetchall()

        # 사용여부 - 콤보박스
        with connection.cursor() as cursor:
            cursor.execute(" SELECT RESKEY, RESNAM FROM OSREFCP WHERE RECODE = 'UST' ")
            cboCustYn = cursor.fetchall()

        # 업체 분류 - 콤보박스
        with connection.cursor() as cursor:
            cursor.execute(" SELECT RESKEY, RESNAM FROM OSREFCP WHERE RECODE = 'DPT' ")
            cboCustType = cursor.fetchall()

        # 업체군 분류 - 콤보박스
        with connection.cursor() as cursor:
            cursor.execute(" SELECT RESKEY, RESNAM FROM OSREFCP WHERE RECODE = 'POP' ")
            cboCustType2 = cursor.fetchall()

        return JsonResponse({"inputCustType": inputCustType, "cboCustYn": cboCustYn, "cboCustType": cboCustType
                                , "cboCustType2": cboCustType2, "custList": custresult})


def custViews_save(request):
    if 'btnSave' in request.POST:
        custName = request.POST.get('txtCustName')
        custName = request.POST.get('txtCustCode')
        custCeo = request.POST.get('txtCeo')
        custRegNum = request.POST.get('txtRegNum')
        custCat = request.POST.get('txtCustCat')
        custType = request.POST.get('txtCustType')
        custPostCode = request.POST.get('txtPostCode')
        custAddress = request.POST.get('txtAddress')
        custTelPhone = request.POST.get('txtTelePhone')
        custFax = request.POST.get('txtFax')
        custEmp = request.POST.get('txtEmp')
        custEmpPhone = request.POST.get('txtEmpPhone')
        # custRegDate = request.POST.get('txtRegDate').replace('-', '')
        custEmail = request.POST.get('txtEMail')
        custWeb = request.POST.get('txtWebAddress')
        custType = request.POST.get('cboCustType')
        custType2 = request.POST.get('cboCustType2')

        with connection.cursor() as cursor:
            cursor.execute("INSERT INTO PIS1TB001 "
                           "   ("
                           "     EMP_NBR "
                           ",    EMP_NME "
                           ",    EMP_PASS "
                           ",    EMP_DEPT "
                           ",    EMP_GBN "
                           ",    EMP_JO "
                           ",    EMP_COM "
                           ",    EMP_TEL "
                           ",    EMP_IPSA "
                           ",    EMP_TESA "
                           ",    EMP_PRC "
                           ",    EMP_PRC1 "
                           ",    EMP_PRC2 "
                           ",    EMP_PRC3 "
                           ",    CRE_DT "
                           ",    CRE_USER "
                           ") "
                           "    VALUES "
                           "    ("
                           "    '" + empNbr + "'"
                           ",   '" + str(empNme) + "'"
                           ",   '" + str(empPass) + "'"
                           ",   '" + str(empDept) + "'"
                           ",   '" + str(empGbn) + "'"
                           ",   '" + str(empJo) + "'"
                           ",   '" + str(empCom) + "'"
                           ",   '" + str(empTel) + "'"
                           ",   '" + str(empIpsa) + "'"
                           ",   '" + str(empTesa) + "'"
                           ",   '" + str(empBom) + "'"
                           ",   '" + str(empBom1) + "'"
                           ",   '" + str(empBom2) + "'"
                           ",   '" + str(empBom3) + "'"
                           ",   '" + str(inepno) + "'"
                           ",   date_format(now(), '%Y%m%d')"
                           "    ) "
                           "    ON DUPLICATE  KEY "
                           "    UPDATE "
                           "     EMP_NME  = '" + str(empNme) + "' "
                           ",    EMP_PASS = '" + str(empPass) + "' "
                           ",    EMP_DEPT = '" + str(empDept) + "' "
                           ",    EMP_GBN  = '" + str(empGbn) + "' "
                           ",    EMP_JO  = '" + str(empJo) + "' "
                           ",    EMP_COM  = '" + str(empCom) + "' "
                           ",    EMP_TEL  = '" + str(empTel) + "' "
                           ",    EMP_IPSA = '" + str(empIpsa) + "' "
                           ",    EMP_TESA = '" + str(empTesa) + "'  "
                           ",    EMP_PRC  = '" + str(empBom) + "' "
                           ",    EMP_PRC1  = '" + str(empBom1) + "' "
                           ",    EMP_PRC2 = '" + str(empBom2) + "' "
                           ",    EMP_PRC3 = '" + str(empBom3) + "'  "
                           ",    UPD_DT = '" + str(utepno) + "' "
                           ",    UPD_USER = date_format(now(), '%Y%m%d') "
                           )
            connection.commit()

            messages.success(request, '저장 되었습니다.')
            return render(request, 'base/base-cust.html')

    else:
        messages.warning(request, '입력 하신 정보를 확인 해주세요.')
        return redirect('/base_cust')


def custViews_dlt(request):
    if request.method == "POST":
        dataList = json.loads(request.POST.get('arrList'))
        print(dataList)
        for cust in dataList:
            acc_split_list = cust.split(',')
            with connection.cursor() as cursor:
                cursor.execute(" DELETE FROM MIS1TB003 WHERE CUST_NBR = '" + acc_split_list[0] + "'"
                           "                                 CUST_GBN = '" + acc_split_list[1] + "' ")
                connection.commit()

        return JsonResponse({'sucYn': "Y"})

    else:
        return render(request, 'base/base-cust.html')