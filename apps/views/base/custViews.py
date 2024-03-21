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
    userId = request.session.get('userId')
    if userId == '' or userId is None:
        return redirect("/page-404/")
    else:
        return render(request, "base/base-cust.html")

def custViews_search(request):
    custType = request.POST.get('custType')
    custCode = request.POST.get('custCode')
    # custYn = request.POST.get('custYn')
    iCust = request.session.get('USER_ICUST')

    if custCode != '' and custType != '':
        with connection.cursor() as cursor:
            cursor.execute(" SELECT IFNULL(A.CUST_NME, ''), IFNULL(A.CUST_NBR, ''), IFNULL(A.CUST_CEO_NME, ''), IFNULL(A.CUST_ADDR, '') "
                           "   , IFNULL(A.CUST_ID_NBR, ''), IFNULL(A.CUST_POST_NBR, ''), IFNULL(A.CUST_TEL_NBR, '')"
                           "   , IFNULL(A.CUST_EMP_PHN, ''), IFNULL(A.CUST_END_CHK, 'Y'), IFNULL(A.CUST_PAY_DAY, '')"
                           "   , IFNULL(A.CUST_ADDR, ''), IFNULL(A.CUST_TEL_NBR, ''), IFNULL(A.CUST_FAX_NBR, '') "
                           "   , IFNULL(A.CUST_EMP_NME, ''), IFNULL(A.CUST_GBN, ''), IFNULL(D.RESNAM, ''), IFNULL(A.CUST_EMAIL, '')"
                           "   , IFNULL(A.CRE_USER, ''), IFNULL(A.CRE_DT, ''), IFNULL(D.RESNAM, '')"
                           "   , IFNULL(A.CUST_PAY_DAY, '') , IFNULL(A.CUST_PAY, ''), IFNULL(B.RESNAM, '') "
                           "   FROM MIS1TB003 A "
                           "   LEFT OUTER JOIN OSREFCP D "
                           "   ON A.CUST_GBN = D.RESKEY "
                           "   AND D.RECODE = 'BGB' "
                           "   LEFT OUTER JOIN OSREFCP B "
                           "   ON A.CUST_PAY = B.RESKEY "
                           "   AND B.RECODE = 'MOP' "
                           "   WHERE A.CUST_NBR LIKE '%" + custCode + "%' "
                           "    OR A.CUST_NME LIKE '%" + custCode + "%'"
                           "    AND A.CUST_GBN LIKE '%" + custType + "%' "
                           "    AND A.ICUST = '" + str(iCust) + "' ")
            custresult = cursor.fetchall()

        return JsonResponse({"custList": custresult})

    elif custCode != '' and custType == '':
        with connection.cursor() as cursor:
            cursor.execute(" SELECT IFNULL(A.CUST_NME, ''), IFNULL(A.CUST_NBR, ''), IFNULL(A.CUST_CEO_NME, ''), IFNULL(A.CUST_ADDR, '') "
                           "   , IFNULL(A.CUST_ID_NBR, ''), IFNULL(A.CUST_POST_NBR, ''), IFNULL(A.CUST_TEL_NBR, '')"
                           "   , IFNULL(A.CUST_EMP_PHN, ''), IFNULL(A.CUST_END_CHK, 'Y'), IFNULL(A.CUST_PAY_DAY, '')"
                           "   , IFNULL(A.CUST_ADDR, ''), IFNULL(A.CUST_TEL_NBR, ''), IFNULL(A.CUST_FAX_NBR, '') "
                           "   , IFNULL(A.CUST_EMP_NME, ''), IFNULL(A.CUST_GBN, ''), IFNULL(D.RESNAM, ''), IFNULL(A.CUST_EMAIL, '')"
                           "   , IFNULL(A.CRE_USER, ''), IFNULL(A.CRE_DT, ''), IFNULL(D.RESNAM, '')"
                           "   , IFNULL(A.CUST_PAY_DAY, '') , IFNULL(A.CUST_PAY, ''), IFNULL(B.RESNAM, '')"
                           "   , IFNULL(A.CUST_BSN_CON, ''), IFNULL(A.CUST_BSN_TYP, ''), IFNULL(A.CUST_HOMEP, '') "
                           "   FROM MIS1TB003 A "
                           "   LEFT OUTER JOIN OSREFCP D "
                           "   ON A.CUST_GBN = D.RESKEY "
                           "   AND D.RECODE = 'BGB' "
                           "   LEFT OUTER JOIN OSREFCP B "
                           "   ON A.CUST_PAY = B.RESKEY "
                           "   AND B.RECODE = 'MOP' "
                           "   WHERE A.CUST_NBR LIKE '%" + custCode + "%' "
                           "   OR A.CUST_NME LIKE '%" + custCode + "%' "
                           "   AND A.ICUST = '" + str(iCust) + "' ")
            custresult = cursor.fetchall()

        #  거래처 계좌번호 테이블
        with connection.cursor() as cursor:
            cursor.execute(
                " SELECT CUST_BKCD, CUST_ACNUM, SEQ "
                " FROM MIS1TB003_D "
                " WHERE CUST_NBR = '" + str(custCode) + "' AND ICUST = '" + str(iCust) + "' ")
            custBank = cursor.fetchall()

            # 업체 분류 - 콤보박스
        with connection.cursor() as cursor:
            cursor.execute(" SELECT RESKEY, RESNAM FROM OSREFCP WHERE RECODE = 'BGB' AND ICUST = '" + str(iCust) + "' ")
            cboCustType = cursor.fetchall()

        # 거래처 은행 - 콤보박스
        with connection.cursor() as cursor:
            cursor.execute(
                " SELECT RESKEY, RESNAM FROM OSREFCP WHERE RECODE = 'BNK' AND ICUST = '" + str(iCust) + "' ")
            cboBank = cursor.fetchall()

        # 결제(달선택) - 콤보박스
        with connection.cursor() as cursor:
            cursor.execute(
                " SELECT RESKEY, RESNAM FROM OSREFCP WHERE RECODE = 'MOP' AND ICUST = '" + str(iCust) + "' ")
            cboPay = cursor.fetchall()

            # 업체군 분류 - 콤보박스
        # with connection.cursor() as cursor:
        #     cursor.execute(" SELECT RESKEY, RESNAM FROM OSREFCP WHERE RECODE = 'CGB' ")
        #     cboCustType2 = cursor.fetchall()

        return JsonResponse({"cboCustType": cboCustType, "custBank": custBank, "cboBank": cboBank, "cboPay": cboPay, "custList": custresult})

    # elif custCode != '':
    #     with connection.cursor() as cursor:
    #         cursor.execute(
    #             " SELECT IFNULL(A.CUST_NME, ''), IFNULL(A.CUST_NBR, ''), IFNULL(A.CUST_CEO_NME, ''), IFNULL(A.CUST_ID_NBR, '') "
    #             "   , IFNULL(A.CUST_BSN_CON, ''), IFNULL(A.CUST_BSN_TYP, ''), IFNULL(A.CUST_POST_NBR, '') "
    #             "   , IFNULL(A.CUST_ADDR, ''), IFNULL(A.CUST_TEL_NBR, ''), IFNULL(A.CUST_FAX_NBR, '') "
    #             "   , IFNULL(A.CUST_EMP_NME, ''), IFNULL(A.CUST_EMP_PHN, ''), IFNULL(A.CUST_EMAIL, '') "
    #             "   , IFNULL(A.CUST_HOMEP, ''), IFNULL(A.CUST_GBN, ''), IFNULL(D.RESNAM, ''), IFNULL(A.CUST_BUNR, '')"
    #             "   , IFNULL(A.CUST_END_CHK, 'Y'), IFNULL(A.CRE_USER, ''), IFNULL(A.CRE_DT, ''), IFNULL(A.CUST_PAY_DAY, '')"
    #             "   , IFNULL(A.CUST_PAY, ''), IFNULL(B.RESNAM, '') "
    #             "   FROM MIS1TB003 A "
    #             "   LEFT OUTER JOIN OSREFCP D "
    #             "   ON A.CUST_GBN = D.RESKEY "
    #             "   AND D.RECODE = 'BGB' "
    #             "   LEFT OUTER JOIN OSREFCP B "
    #             "   ON A.CUST_PAY = B.RESKEY "
    #             "   AND B.RECODE = 'MOP' "
    #             "   WHERE A.CUST_NBR LIKE '%" + custCode + "%' "
    #             "   OR A.CUST_NME LIKE '%" + custCode + "%' "
    #             "   AND A.ICUST = '" + str(iCust) + "' "
    #         )
    #         custresult = cursor.fetchall()
    #
    #     #  거래처 계좌번호 테이블
    #     with connection.cursor() as cursor:
    #         cursor.execute(
    #             " SELECT CUST_BKCD, CUST_ACNUM, SEQ "
    #             " FROM MIS1TB003_D "
    #             " WHERE CUST_NBR LIKE '%" + custCode + "%' AND ICUST = '" + str(iCust) + "' ")
    #         custBank = cursor.fetchall()
    #
    #         # 업체 분류 - 콤보박스
    #     with connection.cursor() as cursor:
    #         cursor.execute(" SELECT RESKEY, RESNAM FROM OSREFCP WHERE RECODE = 'BGB' AND ICUST = '" + str(iCust) + "' ")
    #         cboCustType = cursor.fetchall()
    #
    #     # 거래처 은행 - 콤보박스
    #     with connection.cursor() as cursor:
    #         cursor.execute(
    #             " SELECT RESKEY, RESNAM FROM OSREFCP WHERE RECODE = 'BNK' AND ICUST = '" + str(iCust) + "' ")
    #         cboBank = cursor.fetchall()
    #
    #     # 결제(달선택) - 콤보박스
    #     with connection.cursor() as cursor:
    #         cursor.execute(
    #             " SELECT RESKEY, RESNAM FROM OSREFCP WHERE RECODE = 'MOP' AND ICUST = '" + str(iCust) + "' ")
    #         cboPay = cursor.fetchall()
    #
    #         # 업체군 분류 - 콤보박스
    #     # with connection.cursor() as cursor:
    #     #     cursor.execute(" SELECT RESKEY, RESNAM FROM OSREFCP WHERE RECODE = 'CGB' ")
    #     #     cboCustType2 = cursor.fetchall()
    #
    #     return JsonResponse({"cboCustType": cboCustType, "custBank": custBank, "cboBank": cboBank, "cboPay": cboPay, "custList": custresult})

    # elif custYn != '':
    #     with connection.cursor() as cursor:
    #         cursor.execute(
    #             " SELECT IFNULL(A.CUST_NME, ''), IFNULL(A.CUST_NBR, ''), IFNULL(A.CUST_CEO_NME, ''), IFNULL(A.CUST_ID_NBR, '') "
    #             "   , IFNULL(A.CUST_BSN_CON, ''), IFNULL(A.CUST_BSN_TYP, ''), IFNULL(A.CUST_POST_NBR, '') "
    #             "   , IFNULL(A.CUST_ADDR, ''), IFNULL(A.CUST_TEL_NBR, ''), IFNULL(A.CUST_FAX_NBR, '') "
    #             "   , IFNULL(A.CUST_EMP_NME, ''), IFNULL(A.CUST_EMP_PHN, ''), IFNULL(A.CUST_EMAIL, '') "
    #             "   , IFNULL(A.CUST_HOMEP, ''), IFNULL(A.CUST_GBN, ''), IFNULL(D.RESNAM, ''), IFNULL(A.CUST_BUNR, '')"
    #             "   , IFNULL(A.CUST_END_CHK, 'Y'), IFNULL(A.CRE_USER, ''), IFNULL(A.CRE_DT, '')"
    #             "   , IFNULL(A.CUST_PAY_DAY, ''), IFNULL(A.CUST_PAY, ''), IFNULL(B.RESNAM, '') "
    #             "   FROM MIS1TB003 A "
    #             "   LEFT OUTER JOIN OSREFCP D "
    #             "   ON A.CUST_GBN = D.RESKEY "
    #             "   AND D.RECODE = 'BGB' "
    #             "   LEFT OUTER JOIN OSREFCP B "
    #             "   ON A.CUST_PAY = B.RESKEY "
    #             "   AND B.RECODE = 'MOP' "
    #             "   WHERE A.CUST_END_CHK LIKE '%" + custYn + "%' AND A.ICUST = '" + str(iCust) + "' "
    #         )
    #         custresult = cursor.fetchall()
    #
    #
    #     return JsonResponse({"custList": custresult})

    elif custType != '' and custCode == '':
        with connection.cursor() as cursor:
            cursor.execute(" SELECT IFNULL(A.CUST_NME, ''), IFNULL(A.CUST_NBR, ''), IFNULL(A.CUST_CEO_NME, ''), IFNULL(A.CUST_ADDR, '') "
                           "   , IFNULL(A.CUST_ID_NBR, ''), IFNULL(A.CUST_POST_NBR, ''), IFNULL(A.CUST_TEL_NBR, '')"
                           "   , IFNULL(A.CUST_EMP_PHN, ''), IFNULL(A.CUST_END_CHK, 'Y'), IFNULL(A.CUST_PAY_DAY, '')"
                           "   , IFNULL(A.CUST_ADDR, ''), IFNULL(A.CUST_TEL_NBR, ''), IFNULL(A.CUST_FAX_NBR, '') "
                           "   , IFNULL(A.CUST_EMP_NME, ''), IFNULL(A.CUST_GBN, ''), IFNULL(D.RESNAM, ''), IFNULL(A.CUST_EMAIL, '')"
                           "   , IFNULL(A.CRE_USER, ''), IFNULL(A.CRE_DT, ''), IFNULL(D.RESNAM, '')"
                           "   , IFNULL(A.CUST_PAY_DAY, '') , IFNULL(A.CUST_PAY, ''), IFNULL(B.RESNAM, '') "
                           "   FROM MIS1TB003 A "
                           "   LEFT OUTER JOIN OSREFCP D "
                           "   ON A.CUST_GBN = D.RESKEY "
                           "   AND D.RECODE = 'BGB' "
                           "   LEFT OUTER JOIN OSREFCP B "
                           "   ON A.CUST_PAY = B.RESKEY "
                           "   AND B.RECODE = 'MOP' "
                           "   WHERE A.CUST_GBN LIKE '%" + custType + "%' AND A.ICUST = '" + str(iCust) + "' ")

            custresult = cursor.fetchall()


        return JsonResponse({"custList": custresult})

    else:
        with connection.cursor() as cursor:
            cursor.execute(" SELECT IFNULL(A.CUST_NME, ''), IFNULL(A.CUST_NBR, ''), IFNULL(A.CUST_CEO_NME, ''), IFNULL(A.CUST_ADDR, '') "
                           "   , IFNULL(A.CUST_ID_NBR, ''), IFNULL(A.CUST_POST_NBR, ''), IFNULL(A.CUST_TEL_NBR, '')"
                           "   , IFNULL(A.CUST_EMP_PHN, ''), IFNULL(A.CUST_END_CHK, 'Y'), IFNULL(A.CUST_PAY_DAY, '')"
                           "   , IFNULL(A.CUST_ADDR, ''), IFNULL(A.CUST_TEL_NBR, ''), IFNULL(A.CUST_FAX_NBR, '') "
                           "   , IFNULL(A.CUST_EMP_NME, ''), IFNULL(A.CUST_GBN, ''), IFNULL(D.RESNAM, ''), IFNULL(A.CUST_EMAIL, '')"
                           "   , IFNULL(A.CRE_USER, ''), IFNULL(A.CRE_DT, ''), IFNULL(D.RESNAM, '')"
                           "   , IFNULL(A.CUST_PAY_DAY, '') , IFNULL(A.CUST_PAY, ''), IFNULL(B.RESNAM, '') "
                           "   FROM MIS1TB003 A "
                           "   LEFT OUTER JOIN OSREFCP D "
                           "   ON A.CUST_GBN = D.RESKEY "
                           "   AND D.RECODE = 'BGB' "
                           "   LEFT OUTER JOIN OSREFCP B "
                           "   ON A.CUST_PAY = B.RESKEY "
                           "   AND B.RECODE = 'MOP' "
                           "   WHERE A.ICUST = '" + str(iCust) + "' "
                            )
            custresult = cursor.fetchall()

        # 업체 구분 - 콤보박스
        with connection.cursor() as cursor:
            cursor.execute(" SELECT RESKEY, RESNAM FROM OSREFCP WHERE RECODE = 'BGB' AND ICUST = '" + str(iCust) + "' ")
            inputCustType = cursor.fetchall()

        # 사용여부 - 콤보박스
        with connection.cursor() as cursor:
            cursor.execute(" SELECT RESKEY, RESNAM FROM OSREFCP WHERE RECODE = 'UST' AND ICUST = '" + str(iCust) + "' ")
            cboCustYn = cursor.fetchall()

        # 거래처 은행 - 콤보박스
        with connection.cursor() as cursor:
            cursor.execute(" SELECT RESKEY, RESNAM FROM OSREFCP WHERE RECODE = 'BNK' AND ICUST = '" + str(iCust) + "' ")
            cboBank = cursor.fetchall()

        # 결제(달선택) - 콤보박스
        with connection.cursor() as cursor:
            cursor.execute(" SELECT RESKEY, RESNAM FROM OSREFCP WHERE RECODE = 'MOP' AND ICUST = '" + str(iCust) + "' ")
            cboPay = cursor.fetchall()

        # 업체 분류 - 콤보박스
        # with connection.cursor() as cursor:
        #     cursor.execute(" SELECT RESKEY, RESNAM FROM OSREFCP WHERE RECODE = 'DPT' ")
        #     cboCustType = cursor.fetchall()

        # 업체군 분류 - 콤보박스
        # with connection.cursor() as cursor:
        #     cursor.execute(" SELECT RESKEY, RESNAM FROM OSREFCP WHERE RECODE = 'POP' ")
        #     cboCustType2 = cursor.fetchall()

        return JsonResponse({"inputCustType": inputCustType, "cboCustYn": cboCustYn, "cboBank": cboBank, "cboPay": cboPay, "custList": custresult})

def chkCust(request):
    regNum = request.POST.get('regNum')
    iCust = request.session.get('USER_ICUST')

    with connection.cursor() as cursor:
        cursor.execute(" SELECT COUNT(CUST_NBR) FROM MIS1TB003 WHERE CUST_ID_NBR = '" + str(regNum) + "' AND ICUST = '" + str(iCust) + "' ")
        chkCust = cursor.fetchall()
        return JsonResponse({"chkCust": chkCust})

def custViews_save(request):
    # custArray = json.loads(request.POST.get('custArrList'))
    custName = request.POST.get('txtCustName')
    custCode = request.POST.get('txtCustCode')
    custCeo = request.POST.get('txtCeo')
    custRegNum = request.POST.get('txtRegNum')
    custCat = request.POST.get('txtCustCat')
    custPostCode = request.POST.get('txtPostCode')
    custAddress = request.POST.get('txtAddress')
    custTelPhone = request.POST.get('txtTelePhone')
    custFax = request.POST.get('txtFax')
    creDt = request.POST.get('txtRegDate').replace('-', '')
    custEmail = request.POST.get('txtEMail')
    custWeb = request.POST.get('txtWebAddress')
    custType = request.POST.get('cboCustType')
    cboApv = request.POST.get('cboApv')
    cboDay = request.POST.get('cboDay')
    creUser = request.POST.get('txtUser')
    custBank = request.POST.get('custBank')
    custAct = request.POST.get('custAct')
    custSeq = request.POST.get('custSeq')

    user = request.session.get('userId')
    iCust = request.session.get('USER_ICUST')


    with connection.cursor() as cursor:
        cursor.execute(" SELECT COUNT(CUST_NBR) FROM MIS1TB003 WHERE CUST_NBR = '" + str(custCode) + "' AND ICUST = '" + str(iCust) + "' ")
        result = cursor.fetchall()
        count = int(result[0][0])

    if count > 0:
        with connection.cursor() as cursor:
            cursor.execute(
                " SELECT COUNT(CUST_NBR) FROM MIS1TB003 WHERE CUST_NBR = '" + str(custCode) + "' AND ICUST = '" + str(iCust) + "' ")
            result = cursor.fetchall()
            count = int(result[0][0])

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
                           "    , CUST_EMAIL = '" + str(custEmail) + "' "
                           "    , CUST_HOMEP = '" + str(custWeb) + "'  "
                           "    , CUST_GBN = '" + str(custType) + "' "
                           "    , CUST_PAY = '" + str(cboApv) + "' "
                           "    , CUST_PAY_DAY = '" + str(cboDay) + "' "
                           "    , UPD_DT = '" + str(creDt) + "' "
                           "    , UPD_USER = '" + str(user) + "' "
                           "    WHERE ICUST = '" + str(iCust) + "' "
                           "      AND CUST_NBR = '" + str(custCode) + "'"
                           )
            connection.commit()

            with connection.cursor() as cursor:
                cursor.execute(" SELECT COUNT(SEQ) FROM MIS1TB003_D WHERE CUST_NBR = '" + str(custCode) + "' AND ICUST = '" + str(iCust) + "' ")
                connection.commit()
                result = cursor.fetchall()
                seqCount = int(result[0][0])

            # if (len(result) != 0):
            if seqCount > 0:
                with connection.cursor() as cursor:
                    cursor.execute(" DELETE FROM MIS1TB003_D WHERE CUST_NBR = '" + str(custCode) + "' "
                                   "    AND SEQ = '" + str(custSeq) + "' AND ICUST = '" + str(iCust) + "' ")
                    connection.commit()

            if custAct != '':
                with connection.cursor() as cursor:
                    cursor.execute(" INSERT INTO MIS1TB003_D "
                                   "("
                                   "    CUST_NBR "
                                   "   ,CUST_BKCD "
                                   "   ,CUST_ACNUM "
                                   "   ,SEQ "
                                   "   ,ICUST"
                                   ") "
                                   "VALUES "
                                   "("
                                   "    '" + str(custCode) + "' "
                                   "    ,'" + str(custBank) + "' "
                                   "    ,'" + str(custAct) + "' "
                                   "    ,'1'"
                                   "    ,'" + str(iCust) + "' "
                                   ") ")
                    connection.commit()

        # custArrayLists = list(filter(len, custArray))
        # for data in range(len(custArrayLists)):
        #     if str(custArrayLists[data]["custSeq"]) != '' and str(custArrayLists[data]["custBank"]) == '' and str(custArrayLists[data]["custActNum"]) == '':
        #         with connection.cursor() as cursor:
        #             cursor.execute(" DELETE FROM MIS1TB003_D WHERE CUST_NBR = '" + str(custCode) + "' "
        #                            "    AND SEQ = '" + str(custArrayLists[data]["custSeq"]) + "' AND ICUST = '" + str(iCust) + "' ")
        #             connection.commit()
        #
        #     else:
        #         with connection.cursor() as cursor:
        #             cursor.execute(" SELECT CUST_NBR, SEQ FROM MIS1TB003_D WHERE CUST_NBR = '" + str(custCode) + "' "
        #                            "    AND SEQ = '" + str(custArrayLists[data]["custSeq"]) + "' AND ICUST = '" + str(iCust) + "' ")
        #             result = cursor.fetchall()
        #
        #         if result:
        #             custNbr = result[0][0]
        #             custSeq = result[0][1]
        #             with connection.cursor() as cursor:
        #                 cursor.execute(" UPDATE MIS1TB003_D SET "
        #                                "        CUST_BKCD = '" + str(custArrayLists[data]["custBank"]) + "' "
        #                                "       , CUST_ACNUM = '" + str(custArrayLists[data]["custActNum"]) + "' "
        #                                " WHERE CUST_NBR = '" + custNbr + "'"
        #                                " AND ICUST = '" + str(iCust) + "'"
        #                                " AND SEQ = '" + str(custSeq) + "'")
        #                 connection.commit()
        #         else:
        #             with connection.cursor() as cursor:
        #                 cursor.execute(" INSERT INTO MIS1TB003_D "
        #                                "("
        #                                "    CUST_NBR "
        #                                "   ,CUST_BKCD "
        #                                "   ,CUST_ACNUM "
        #                                "   ,SEQ "
        #                                "   ,ICUST"
        #                                ") "
        #                                "VALUES "
        #                                "("
        #                                "    '" + str(custResult) + "' "
        #                                "    ,'" + str(custArrayLists[data]["custBank"]) + "' "
        #                                "    ,'" + str(custArrayLists[data]["custActNum"]) + "' "
        #                                "    , (SELECT IFNULL (MAX(SEQ) + 1,1) AS COUNTED FROM MIS1TB003_D A WHERE CUST_NBR = '" + str(custCode) + "' AND ICUST = '" + str(iCust) + "') "
        #                                "    ,'" + str(iCust) + "' "
        #                                ") ")
        #                 connection.commit()

        return JsonResponse({'sucYn': "Y"})

    else:

        with connection.cursor() as cursor:
            cursor.execute(" SELECT IFNULL(MAX(CUST_NBR) + 1, 0) AS COUNTED FROM MIS1TB003 A "
                           "    WHERE CUST_NBR LIKE '" + str(custType) + "%' AND ICUST = '" + str(iCust) + "' ")
            custresult = cursor.fetchall()
            cust = int(custresult[0][0])

        if len(str(cust)) < 5:
            custnumber = str(custType) + '0001'
            print(custnumber)
        else:
            custnumber = cust

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
                           ",    CUST_EMAIL "
                           ",    CUST_HOMEP "
                           ",    CUST_GBN "
                           ",    CUST_PAY "
                           ",    CUST_PAY_DAY "
                           ",    CRE_DT "
                           ",    CRE_USER "
                           ",    ICUST "
                           ") "
                           "    VALUES "
                           "    ("
                           "    '" + str(custName) + "'"
                           ",   '" + str(custnumber) + "'"
                           ",   '" + str(custCeo) + "'"
                           ",   '" + str(custRegNum) + "'"
                           ",   '" + str(custCat) + "'"
                           ",   '" + str(custType) + "'"
                           ",   '" + str(custPostCode) + "'"
                           ",   '" + str(custAddress) + "'"
                           ",   '" + str(custTelPhone) + "'"
                           ",   '" + str(custFax) + "'"
                           ",   '" + str(custEmail) + "'"
                           ",   '" + str(custWeb) + "'"
                           ",   '" + str(custType) + "'"
                           ",   '" + str(cboApv) + "'"
                           ",   '" + str(cboDay) + "'"
                           ",   '" + str(creDt) + "'"
                           ",   '" + str(user) + "'"
                           ",   '" + str(iCust) + "'"
                           "    ) "
                           )

            connection.commit()

        with connection.cursor() as cursor:
            cursor.execute(" SELECT COUNT(SEQ) FROM MIS1TB003_D WHERE CUST_NBR = '" + str(custCode) + "' AND ICUST = '" + str(iCust) + "' ")
            connection.commit()
            result = cursor.fetchall()
            custCount = int(result[0][0])

        if custCount > 0:
            with connection.cursor() as cursor:
                cursor.execute(" DELETE FROM MIS1TB003_D WHERE CUST_NBR = '" + str(custCode) + "' "
                               "    AND SEQ = '" + str(custSeq) + "' AND ICUST = '" + str(iCust) + "' ")
                connection.commit()
        if custAct != '':
            with connection.cursor() as cursor:
                cursor.execute(" INSERT INTO MIS1TB003_D "
                               "("
                               "    CUST_NBR "
                               "   ,CUST_BKCD "
                               "   ,CUST_ACNUM "
                               "   ,SEQ "
                               "   ,ICUST"
                               ") "
                               "VALUES "
                               "("
                               "    '" + str(custnumber) + "' "
                               "    ,'" + str(custBank) + "' "
                               "    ,'" + str(custAct) + "' "
                               "    ,'1'"
                               "    ,'" + str(iCust) + "' "
                               ") ")
                connection.commit()

        return JsonResponse({'sucYn': "Y"})



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