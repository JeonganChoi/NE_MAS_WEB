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

# 감가상각비명세서
def depreciationViews(request):

    return render(request, "finance/depreciation-reg-sheet.html")

def dptViews_search(request):
    yymm = request.POST.get('yymm')
    yymm = yymm + '00'

    with connection.cursor() as cursor:
        cursor.execute(" SELECT IFNULL(A.FIX_NO, ''), IFNULL(A.FIX_NME, ''), IFNULL(A.FIX_GRD, ''), IFNULL(A.FIX_QTY, 0) "
                       "    , IFNULL(A.FIX_GDATE, ''), IFNULL(A.FIX_YEARS, ''), IFNULL(A.FIX_GAMTS, 0) "
                       "    , IFNULL(B.FIX_FUND, 0), IFNULL(B.FIX_REPAY, 0), IFNULL(B.FIX_TAXC, 0) "
                       "    FROM OSREPAY A "
                       "    LEFT OUTER JOIN OSREPAY_D B "
                       "    ON A.FIX_NO = B.FIX_NO "
                       "    WHERE B.FIX_YYMM = '" + yymm + "' ")
        mainresult = cursor.fetchall()

    return JsonResponse({"mainList": mainresult})

def dptViews_save(request):
    fixArray = json.loads(request.POST.get('fixArrList'))

    fixArrayLists = list(filter(len, fixArray))
    for data in range(len(fixArrayLists)):
        print(fixArrayLists[data]["fixCode"])
        with connection.cursor() as cursor:
            cursor.execute("SELECT FIX_NO, FIX_GRD, ICUST FROM OSREPAY WHERE FIX_NO = '" + fixArrayLists[data]["fixCode"] + "' ")
            fixresult = cursor.fetchall()

        with connection.cursor() as cursor:
            cursor.execute(
                "SELECT FIX_NO, FIX_YYMM FROM OSREPAY_D WHERE FIX_NO = '" + fixArrayLists[data]["fixCode"] + "' ")
            fixresult_d = cursor.fetchall()

            if(fixArrayLists[data]["fixAmts"] ==''):
                fixArrayLists[data]["fixAmts"] = 0
            if (fixArrayLists[data]["fixFund"] == ''):
                fixArrayLists[data]["fixFund"] = 0
            if (fixArrayLists[data]["fixRepay"] == ''):
                fixArrayLists[data]["fixRepay"] = 0
            if (fixArrayLists[data]["fixTaxc"] == ''):
                fixArrayLists[data]["fixTaxc"] = 0


            if fixresult:
                # 마스터 테이블 자산 확인
                fixCode = fixresult[0][0]
                iCust = fixresult[0][2]
                # 디테일 테이블 자산 확인
                fixCode_d = fixresult_d[0][0]
                fixyymm_d = fixresult_d[0][1]

                if fixCode == fixCode_d and fixCode_d:
                    with connection.cursor() as cursor:
                        cursor.execute(
                                " UPDATE OSREPAY SET "
                                "   FIX_NME = '" + fixArrayLists[data]["fixNme"] + "' "
                                " , FIX_GRD = '" + fixArrayLists[data]["fixGrd"] + "' "
                                " , FIX_QTY = '" + fixArrayLists[data]["fixQty"] + "' "
                                " , FIX_GDATE = '" + fixArrayLists[data]["fixGdt"].replace("-", "") + "' "
                                " , FIX_YEARS = '" + fixArrayLists[data]["fixYYYY"] + "' "
                                " , FIX_GAMTS = '" + str(fixArrayLists[data]["fixAmts"]) + "' "
                                " , UPD_USER = '101' "
                                " , UPD_DT = date_format(now(), '%Y%m%d') "
                                " WHERE FIX_NO = '" + fixCode + "' "
                                "   AND ICUST = '" + iCust + "' "
                        )
                        connection.commit()

                        cursor.execute(
                                " UPDATE OSREPAY_D SET "
                                "   FIX_FUND = '" + str(fixArrayLists[data]["fixFund"]) + "' "
                                " , FIX_REPAY = '" + str(fixArrayLists[data]["fixRepay"]) + "' "
                                " , FIX_TAXC = '" + str(fixArrayLists[data]["fixTaxc"]) + "' "
                                " WHERE FIX_NO = '" + fixCode_d + "' "
                                "   AND FIX_YYMM = '" + fixyymm_d + "' "
                        )
                        connection.commit()
            else:
                with connection.cursor() as cursor:
                    cursor.execute(
                            " INSERT INTO OSREPAY "
                            " ( "
                            "   FIX_NO "
                            " , FIX_NME "
                            " , FIX_GRD "
                            " , FIX_QTY "
                            " , FIX_GDATE "
                            " , FIX_YEARS "
                            " , FIX_GAMTS "
                            " , CRE_USER "
                            " , CRE_DT "
                            " , ICUST "
                            " ) "
                            "  VALUES "
                            " ( "
                            "  (SELECT IFNULL (LPAD(MAX(A.FIX_NO + 1), '4', '0'), 0001) AS COUNTED FROM OSREPAY A) "
                            " ,'" + fixArrayLists[data]["fixNme"] + "' "
                            " ,'" + fixArrayLists[data]["fixGrd"] + "' "
                            " ,'" + fixArrayLists[data]["fixQty"] + "' "
                            " ,'" + fixArrayLists[data]["fixGdt"].replace("-", "") + "' "
                            " ,'" + fixArrayLists[data]["fixYYYY"] + "' "
                            " ,'" + str(fixArrayLists[data]["fixAmts"]) + "' "
                            " ,'101' "
                            " ,date_format(now(), '%Y%m%d') "
                            " ,'101' "
                            " ) "
                    )
                    connection.commit()

                    print(fixArrayLists[data]["fixYYMM"] + '00')
                    cursor.execute(
                            " INSERT INTO OSREPAY_D "
                            " ( "
                            "   FIX_NO "
                            " , FIX_YYMM "
                            " , FIX_FUND "
                            " , FIX_REPAY "
                            " , FIX_TAXC "
                            " ) "
                            "  VALUES "
                            " ( "
                            "  (SELECT IFNULL (LPAD(MAX(A.FIX_NO + 1), '4', '0'), 0001) AS COUNTED FROM OSREPAY_D A) "
                            " ,'" + str(fixArrayLists[data]["fixYYMM"]) + "' "
                            " ,'" + str(fixArrayLists[data]["fixFund"]) + "' "
                            " ,'" + str(fixArrayLists[data]["fixRepay"]) + "' "
                            " ,'" + str(fixArrayLists[data]["fixTaxc"]) + "' "
                            " ) "
                    )
                    connection.commit()

    return JsonResponse({'arrList': "Y"})

    # return render(request, 'finance/depreciation-reg-sheet.html')
