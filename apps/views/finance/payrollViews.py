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

# 임금대장
def payrollViews(request):

    return render(request, "finance/payroll-reg-sheet.html")

def payrollViews_search(request):
    modal = request.POST.get('modal')
    yyyymm = request.POST.get('yyyymm')
    empType = request.POST.get('empType')
    user = request.session.get('userId')
    iCust = request.session.get('USER_ICUST')

    if modal:
        with connection.cursor() as cursor:
            cursor.execute(" SELECT ACNUMBER FROM ACNUMBER WHERE ICUST = '" + str(iCust) + "' ORDER BY ACNUMBER ")
            cboAct = cursor.fetchall()

        with connection.cursor() as cursor:
            cursor.execute(" SELECT MCODE, MCODENM FROM OSCODEM WHERE ICUST = '" + str(iCust) + "' ORDER BY MCODE ASC ")
            cboMCode = cursor.fetchall()

        return JsonResponse({"cboAct": cboAct, "cboMCode": cboMCode})

    else:
        with connection.cursor() as cursor:
            cursor.execute(" SELECT RESKEY, RESNAM FROM OSREFCP WHERE RECODE = 'PNM' AND ICUST = '" + str(iCust) + "' ORDER BY CAST(RESKEY AS UNSIGNED ) ASC ")
            headresult = cursor.fetchall()

        with connection.cursor() as cursor:
            cursor.execute(" SELECT EMP_NBR, EMP_NME FROM PIS1TB001 WHERE EMP_TESA  IS NULL OR EMP_TESA = '' AND ICUST = '" + str(iCust) + "' ")
            empresult = cursor.fetchall()


        # 날짜/사업장/사원번호/사원명/직책/기본시급/기본일급/기본시간/기본급/연장시간/휴계시간/휴일근로시간/휴일연장근로시간/주차지산/유급시간/
        # 심야시간/연장근로수당/휴계수당/휴일수당/휴일연장수당/심야수당/주차수당/유급수당/기타수당1,2,3,4,5/지급총액
        # 국민연급/의료보험/갑근세/주민세/고용보험/공제1,2,3/공제총액/실지급액
        with connection.cursor() as cursor:
            cursor.execute(" SELECT "
                           "     A.EMP_NBR, A.EMP_NME, IFNULL(B.PMYYMM,'') AS PMYYMM, IFNULL(B.ICUST,'') AS ICUST "
                           "    ,IFNULL(B.PMGRAD, '') AS PMGRAD, IFNULL(B.PMTPAY, '') AS PMTPAY, IFNULL(B.PMDPAY, '') AS PMDPAY "
                           "     , IFNULL(B.PMKBTM, '') AS PMKBTM, IFNULL(PMKBON, '') AS PMKBON "
                           "    ,IFNULL(B.PMOTTM, '') AS PMOTTM, IFNULL(B.PMOTOTM, '') AS PMOTOTM,IFNULL(B.PMHOTM, '') AS PMHOTM "
                           "     , IFNULL(B.PMHOOTM, '') AS PMHOOTM,IFNULL(B.PMOTOPY, '') AS PMOTOPY "
                           "    ,IFNULL(B.PMOTOPY,'') AS PMOTOPY,IFNULL(B.PMHOPY, '') AS PMHOPY,IFNULL(B.PMHOOPY, '') AS PMHOOPY "
                           "     , IFNULL(B.PMSYPY, '') AS PMSYPY, IFNULL(B.PMWWTM, '') AS PMWWTM "
                           "    ,IFNULL(B.PMWWPY, '') AS PMWWPY, IFNULL(PMYUTM, '') AS PMYUTM, IFNULL(PMYUPY, '') AS PMYUPY "
                           "     , IFNULL(B.PMGSU1, '') AS PMGSU1, IFNULL(B.PMGSU2, '') AS PMGSU2 "
                           "    ,IFNULL(B.PMGSU3, '') AS PMGSU3, IFNULL(B.PMGSU4, '') AS PMGSU4,  IFNULL(PMGSU5, '') AS PMGSU5 "
                           "     , IFNULL(B.PMPYTT, '') AS PMPYTT, IFNULL(B.PMKUPS, '') AS PMKUPS "
                           "    ,IFNULL(B.PMMEPS, '') AS PMMEPS, IFNULL(B.PMTAX1, '') AS PMTAX1, IFNULL(PMTAX3, '') AS PMTAX3 "
                           "     , IFNULL(B.PMGOPS, '') AS PMGOPS, IFNULL(B.PMGTG1, '') AS PMGTG1 "
                           "    ,IFNULL(B.PMGTG2, '') AS PMGTG2 , IFNULL(B.PMGTG3, '') AS PMGTG3 ,  IFNULL(PMGOTT, '') AS PMGOTT "
                           "     ,  IFNULL(PMJITT, '') AS PMJITT "
                           " FROM pis1tb001 A "
                           " LEFT OUTER JOIN "
                           "    ( "
                           "        SELECT "
                           "         PMYYMM, ICUST, PMGRAD, PMTPAY, PMDPAY, PMKBTM, PMKBON "
                           "        ,PMOTTM ,PMOTOTM ,PMHOTM ,PMHOOTM, PMSYTM ,PMOTPY ,PMOTOPY ,PMHOPY "
                           "        ,PMHOOPY, PMSYPY,PMWWTM,PMWWPY, PMYUTM,PMYUPY,PMGSU1, PMGSU2 "
                           "        ,PMGSU3,  PMGSU4, PMGSU5,PMPYTT, PMKUPS,PMMEPS, PMTAX1, PMTAX3 "
                           "        ,PMGOPS,  PMGTG1,  PMGTG2,  PMGTG3, PMGOTT, PMJITT, EMP_NBR "
                           "        FROM OSMONTHP "
                           "        WHERE PMYYMM = '" + str(yyyymm) + "' "
                           "    ) B "
                           " ON A.EMP_NBR = B.EMP_NBR "
                           " AND A.ICUST = B.ICUST "
                           " WHERE A.ICUST = '" + str(iCust) + "'")

            mainresult = cursor.fetchall()

        with connection.cursor() as cursor:
            cursor.execute(" SELECT RESKEY, RESNAM FROM OSREFCP WHERE RECODE = 'WOT' AND ICUST = '" + str(iCust) + "'  ")
            cboEmp = cursor.fetchall()

        return JsonResponse({"headList": headresult, "empList": empresult, "mainList": mainresult, "cboEmp": cboEmp})

def payrollViews_save(request):
    payArray = json.loads(request.POST.get('payArrList'))
    user = request.session.get('userId')
    iCust = request.session.get('USER_ICUST')


    payArrayLists = list(filter(len, payArray))
    for data in range(len(payArrayLists)):
        with connection.cursor() as cursor:
            cursor.execute("SELECT PMYYMM, EMP_NBR, ICUST FROM OSMONTHP WHERE PMYYMM = '" + payArrayLists[data]["pmYymm"] + "' "
                           "    AND EMP_NBR = '" + payArrayLists[data]["pmEmpNbr"] + "' AND ICUST = '" + str(iCust) + "' ")
            payresult = cursor.fetchall()

            if (payArrayLists[data]["pmTpay"] == ''):
                payArrayLists[data]["pmTpay"] = 0
            if (payArrayLists[data]["pmDpay"] == ''):
                payArrayLists[data]["pmDpay"] = 0
            if (payArrayLists[data]["pmKbon"] == ''):
                payArrayLists[data]["pmKbon"] = 0
            if (payArrayLists[data]["pmKbtm"] == ''):
                payArrayLists[data]["pmKbtm"] = 0
            if (payArrayLists[data]["pmOttm"] == ''):
                payArrayLists[data]["pmOttm"] = 0
            if (payArrayLists[data]["pmPtptm"] == ''):
                payArrayLists[data]["pmPtptm"] = 0
            if (payArrayLists[data]["pmHotm"] == ''):
                payArrayLists[data]["pmHotm"] = 0
            if (payArrayLists[data]["pmHootm"] == ''):
                payArrayLists[data]["pmHootm"] = 0
            if (payArrayLists[data]["pmWwtm"] == ''):
                payArrayLists[data]["pmWwtm"] = 0
            if (payArrayLists[data]["pmYutm"] == ''):
                payArrayLists[data]["pmYutm"] = 0
            if (payArrayLists[data]["pmSytm"] == ''):
                payArrayLists[data]["pmSytm"] = 0
            if (payArrayLists[data]["pmOtpy"] == ''):
                payArrayLists[data]["pmOtpy"] = 0
            if (payArrayLists[data]["pmOtopy"] == ''):
                payArrayLists[data]["pmOtopy"] = 0
            if (payArrayLists[data]["pmHopy"] == ''):
                payArrayLists[data]["pmHopy"] = 0
            if (payArrayLists[data]["pmHoopy"] == ''):
                payArrayLists[data]["pmHoopy"] = 0
            if (payArrayLists[data]["pmSypy"] == ''):
                payArrayLists[data]["pmSypy"] = 0
            if (payArrayLists[data]["pmWwpy"] == ''):
                payArrayLists[data]["pmWwpy"] = 0
            if (payArrayLists[data]["pmYupy"] == ''):
                payArrayLists[data]["pmYupy"] = 0
            if (payArrayLists[data]["pmPytt"] == ''):
                payArrayLists[data]["pmPytt"] = 0
            if (payArrayLists[data]["pmKups"] == ''):
                payArrayLists[data]["pmKups"] = 0
            if (payArrayLists[data]["pmMeps"] == ''):
                payArrayLists[data]["pmMeps"] = 0
            if (payArrayLists[data]["pmTax1"] == ''):
                payArrayLists[data]["pmTax1"] = 0
            if (payArrayLists[data]["pmTax3"] == ''):
                payArrayLists[data]["pmTax3"] = 0
            if (payArrayLists[data]["pmGops"] == ''):
                payArrayLists[data]["pmGops"] = 0
            if (payArrayLists[data]["pmGott"] == ''):
                payArrayLists[data]["pmGott"] = 0
            if (payArrayLists[data]["pmJitt"] == ''):
                payArrayLists[data]["pmJitt"] = 0

            pmGsu_data = payArrayLists[data]["pmGsu"]
            pmGsu_list = [0 for i in range(5)]
            for u in range(len(pmGsu_data)):
                pmGsu_list[u] = pmGsu_data[u]

            pmGtg_data = payArrayLists[data]["pmGtg"]
            pmGtg_list = [0 for j in range(3)]
            for g in range(len(pmGtg_data)):
                pmGtg_list[g] = pmGtg_data[g]

            if payresult:

                yyyymm = payresult[0][0]
                empCode = payresult[0][1]

                with connection.cursor() as cursor:
                    cursor.execute(" UPDATE OSMONTHP SET "
                                    "   PMGRAD = '" + str(payArrayLists[data]["pmGrad"]) + "' "
                                    " , PMTPAY = '" + str(payArrayLists[data]["pmTpay"]) + "' "
                                    " , PMDPAY = '" + str(payArrayLists[data]["pmDpay"]) + "' "
                                    " , PMKBON = '" + str(payArrayLists[data]["pmKbon"]) + "' "
                                    " , PMKBTM = '" + str(payArrayLists[data]["pmKbtm"]) + "' "
                                    " , PMOTTM = '" + str(payArrayLists[data]["pmOttm"]) + "' "
                                    " , PMOTOTM = '" + str(payArrayLists[data]["pmPtptm"]) + "' "
                                    " , PMHOTM = '" + str(payArrayLists[data]["pmHotm"]) + "' "
                                    " , PMHOOTM = '" + str(payArrayLists[data]["pmHootm"]) + "' "
                                    " , PMWWTM = '" + str(payArrayLists[data]["pmWwtm"]) + "' "
                                    " , PMYUTM = '" + str(payArrayLists[data]["pmYutm"]) + "' "
                                    " , PMSYTM = '" + str(payArrayLists[data]["pmSytm"]) + "' "
                                    " , PMOTPY = '" + str(payArrayLists[data]["pmOtpy"]) + "' "
                                    " , PMOTOPY = '" + str(payArrayLists[data]["pmOtopy"]) + "' "
                                    " , PMHOPY = '" + str(payArrayLists[data]["pmHopy"]) + "' "
                                    " , PMHOOPY = '" + str(payArrayLists[data]["pmHoopy"]) + "' "
                                    " , PMSYPY = '" + str(payArrayLists[data]["pmSypy"]) + "' "
                                    " , PMWWPY = '" + str(payArrayLists[data]["pmWwpy"]) + "' "
                                    " , PMYUPY = '" + str(payArrayLists[data]["pmYupy"]) + "' "
                                    " , PMGSU1 = '" + str(pmGsu_list[0]) + "' "                                                              
                                    " , PMGSU2 = '" + str(pmGsu_list[1]) + "' "
                                    " , PMGSU3 = '" + str(pmGsu_list[2]) + "' "
                                    " , PMGSU4 = '" + str(pmGsu_list[3]) + "' "
                                    " , PMGSU5 = '" + str(pmGsu_list[4]) + "' "
                                    " , PMPYTT = '" + str(payArrayLists[data]["pmPytt"]) + "' "
                                    " , PMKUPS = '" + str(payArrayLists[data]["pmKups"]) + "' "
                                    " , PMMEPS = '" + str(payArrayLists[data]["pmMeps"]) + "' "
                                    " , PMTAX1 = '" + str(payArrayLists[data]["pmTax1"]) + "' "
                                    " , PMTAX3 = '" + str(payArrayLists[data]["pmTax3"]) + "' "
                                    " , PMGOPS = '" + str(payArrayLists[data]["pmGops"]) + "' "
                                    " , PMGTG1 = '" + str(pmGtg_list[0]) + "' "
                                    " , PMGTG2 = '" + str(pmGtg_list[1]) + "' "
                                    " , PMGTG3 = '" + str(pmGtg_list[2]) + "' "
                                    " , PMGOTT = '" + str(payArrayLists[data]["pmGott"]) + "' "
                                    " , PMJITT = '" + str(payArrayLists[data]["pmJitt"]) + "' "
                                    " , UPD_USER = '" + str(user) + "' "
                                    " , UPD_DT = date_format(now(), '%Y%m%d') "
                                    " WHERE PMYYMM = '" + str(yyyymm) + "' "
                                    "   AND EMP_NBR = '" + str(empCode) + "' "
                                    "   AND ICUST = '" + str(iCust) + "'"
                    )
                    connection.commit()

            else:
                with connection.cursor() as cursor:
                    cursor.execute(" INSERT INTO OSMONTHP "
                                    " ( "
                                    "   PMYYMM "
                                    " , EMP_NBR "
                                    " , EMP_NME "
                                    " , ICUST "
                                    " , PMGRAD "
                                    " , PMTPAY "
                                    " , PMDPAY "
                                    " , PMKBON "
                                    " , PMKBTM "
                                    " , PMOTTM "
                                    " , PMOTOTM "
                                    " , PMHOTM "
                                    " , PMHOOTM "
                                    " , PMWWTM "
                                    " , PMYUTM "
                                    " , PMSYTM "
                                    " , PMOTPY "
                                    " , PMOTOPY "
                                    " , PMHOPY "
                                    " , PMHOOPY "
                                    " , PMSYPY "
                                    " , PMWWPY "
                                    " , PMYUPY "
                                    " , PMGSU1 "
                                    " , PMGSU2 "
                                    " , PMGSU3 "
                                    " , PMGSU4 "
                                    " , PMGSU5 "
                                    " , PMPYTT "
                                    " , PMKUPS "
                                    " , PMMEPS "
                                    " , PMTAX1 "
                                    " , PMTAX3 "
                                    " , PMGOPS "
                                    " , PMGTG1 "
                                    " , PMGTG2 "
                                    " , PMGTG3 "
                                    " , PMGOTT "
                                    " , PMJITT "
                                    " , CRE_USER "
                                    " , CRE_DT "
                                    " ) "
                                    "  VALUES "
                                    " ( "
                                    "  '" + str(payArrayLists[data]["pmYymm"].replace("-", "")) + "' "
                                    " ,'" + str(payArrayLists[data]["pmEmpNbr"]) + "' "
                                    " ,'" + str(payArrayLists[data]["pmEmpNme"]) + "' "
                                    " ,'" + str(iCust) + "' "
                                    " ,'" + str(payArrayLists[data]["pmGrad"]) + "' "
                                    " ,'" + str(payArrayLists[data]["pmTpay"]) + "' "
                                    " ,'" + str(payArrayLists[data]["pmDpay"]) + "' "
                                    " ,'" + str(payArrayLists[data]["pmKbon"]) + "' "
                                    " ,'" + str(payArrayLists[data]["pmKbtm"]) + "' "
                                    " ,'" + str(payArrayLists[data]["pmOttm"]) + "' "
                                    " ,'" + str(payArrayLists[data]["pmPtptm"]) + "' "
                                    " ,'" + str(payArrayLists[data]["pmHotm"]) + "' "
                                    " ,'" + str(payArrayLists[data]["pmHootm"]) + "' "
                                    " ,'" + str(payArrayLists[data]["pmWwtm"]) + "' "
                                    " ,'" + str(payArrayLists[data]["pmYutm"]) + "' "
                                    " ,'" + str(payArrayLists[data]["pmSytm"]) + "' "
                                    " ,'" + str(payArrayLists[data]["pmOtpy"]) + "' "
                                    " ,'" + str(payArrayLists[data]["pmOtopy"]) + "' "
                                    " ,'" + str(payArrayLists[data]["pmHopy"]) + "' "
                                    " ,'" + str(payArrayLists[data]["pmHoopy"]) + "' "
                                    " ,'" + str(payArrayLists[data]["pmSypy"]) + "' "
                                    " ,'" + str(payArrayLists[data]["pmWwpy"]) + "' "
                                    " ,'" + str(payArrayLists[data]["pmYupy"]) + "' "
                                    " ,'" + str(pmGsu_list[0]) + "' "
                                    " ,'" + str(pmGsu_list[1]) + "' "
                                    " ,'" + str(pmGsu_list[2]) + "' "
                                    " ,'" + str(pmGsu_list[3]) + "' "
                                    " ,'" + str(pmGsu_list[4]) + "' "
                                    " ,'" + str(payArrayLists[data]["pmPytt"]) + "' "
                                    " ,'" + str(payArrayLists[data]["pmKups"]) + "' "
                                    " ,'" + str(payArrayLists[data]["pmMeps"]) + "' "
                                    " ,'" + str(payArrayLists[data]["pmTax1"]) + "' "
                                    " ,'" + str(payArrayLists[data]["pmTax3"]) + "' "
                                    " ,'" + str(payArrayLists[data]["pmGops"]) + "' "
                                    " ,'" + str(pmGtg_list[0]) + "' "
                                    " ,'" + str(pmGtg_list[1]) + "' "
                                    " ,'" + str(pmGtg_list[2]) + "' "
                                    " ,'" + str(payArrayLists[data]["pmGott"]) + "' "
                                    " ,'" + str(payArrayLists[data]["pmJitt"]) + "' "
                                    " ,'" + str(user) + "' "
                                    " ,date_format(now(), '%Y%m%d') "
                                    " ) "
                    )
                    connection.commit()

    return JsonResponse({'arrList': "Y"})