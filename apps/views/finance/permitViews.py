import datetime
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
def permitViews(request):

    return render(request, "finance/permit-reg.html")


def permitViews_search(request):
    perDate = request.POST.get('perDate')
    # 미시행 ''/ 시행 = 1
    permitGbn = request.POST.get('permitGbn','')
    custCode = request.POST.get('custCode','')
    # value = off
    offSet = request.POST.get('offSet','')
    user = request.session.get('userId')
    iCust = request.session.get('USER_ICUST')

    # if offSet and custCode:
    #     with connection.cursor() as cursor:
    #         cursor.execute("  SELECT IFNULL(A.IODATE, ''), IFNULL(A.ACTITLE, ''), IFNULL(A.ACAMTS, '') "
    #                        "        , IFNULL(B.EMP_NBR, ''), IFNULL(C.EMP_NME, ''), IFNULL(A.ACSEQN, ''), IFNULL(A.ACIOGB, '')"
    #                        "        , IFNULL(A.MCODE, ''), IFNULL(D.MCODENM, ''), IFNULL(A.ACACNUMBER, '') "
    #                        " FROM SISACCTT A "
    #                        " LEFT OUTER JOIN OSSIGN B "
    #                        " ON A.IODATE = B.ACDATE "
    #                        " AND A.ACSEQN = B.ACSEQN "
    #                        " AND A.ICUST = B.ICUST "
    #                        " AND A.FIN_OPT = 'N' "
    #                        " LEFT OUTER JOIN PIS1TB001 C "
    #                        " ON B.EMP_NBR = C.EMP_NBR "
    #                        " LEFT OUTER JOIN OSCODEM D "
    #                        " ON A.MCODE = D.MCODE "
    #                        " WHERE B.EMP_NBR = '" + user + "' "
    #                        " AND A.IODATE <= '" + perDate + "' "
    #                        " AND A.ACCUST = '" + custCode + "' "
    #                        " AND A.OFF_GBN = 'off'"
    #                        " AND A.ICUST = '" + iCust + "' "
    #                        " ORDER BY A.ACSEQN ASC ")
    #         mainresult = cursor.fetchall()
    #
    #     return JsonResponse({"mainList": mainresult})

    # elif custCode:
    #     with connection.cursor() as cursor:
    #         cursor.execute("  SELECT IFNULL(A.IODATE, ''), IFNULL(A.ACTITLE, ''), IFNULL(A.ACAMTS, '') "
    #                        "        , IFNULL(B.EMP_NBR, ''), IFNULL(C.EMP_NME, ''), IFNULL(A.ACSEQN, ''), IFNULL(A.ACIOGB, '')"
    #                        "        , IFNULL(A.MCODE, ''), IFNULL(D.MCODENM, ''), IFNULL(A.ACACNUMBER, '') "
    #                        " FROM SISACCTT A "
    #                        " LEFT OUTER JOIN OSSIGN B "
    #                        " ON A.IODATE = B.ACDATE "
    #                        " AND A.ACSEQN = B.ACSEQN "
    #                        " AND A.ICUST = B.ICUST "
    #                        " AND A.FIN_OPT = 'N' "
    #                        " LEFT OUTER JOIN PIS1TB001 C "
    #                        " ON B.EMP_NBR = C.EMP_NBR "
    #                        " LEFT OUTER JOIN OSCODEM D "
    #                        " ON A.MCODE = D.MCODE "
    #                        " WHERE B.EMP_NBR = '" + user + "' "
    #                        " AND A.IODATE <= '" + perDate + "' "
    #                        " AND A.ACCUST = '" + custCode + "' "
    #                        " AND A.ICUST = '" + iCust + "' "
    #                        " ORDER BY A.ACSEQN ASC ")
    #         mainresult = cursor.fetchall()
    #
    #     return JsonResponse({"mainList": mainresult})

    # 상계
    if offSet:
        if permitGbn == '':
            with connection.cursor() as cursor:
                cursor.execute("  SELECT IFNULL(A.IODATE, ''), IFNULL(A.ACTITLE, ''), IFNULL(A.ACAMTS, '') "
                               "        , IFNULL(B.EMP_NBR, ''), IFNULL(C.EMP_NME, ''), IFNULL(A.ACSEQN, ''), IFNULL(A.ACIOGB, '')"
                               "        , IFNULL(A.MCODE, ''), IFNULL(D.MCODENM, ''), IFNULL(A.ACACNUMBER, ''), IFNULL(B.OPT, ''), IFNULL(A.FIN_OPT, ''), IFNULL(A.ACINFO, '') "
                               " FROM SISACCTT A "
                               " LEFT OUTER JOIN OSSIGN B "
                               " ON A.IODATE = B.ACDATE "
                               " AND A.ACSEQN = B.ACSEQN "
                               " AND A.ICUST = B.ICUST "
                               " AND A.FIN_OPT = 'N' "
                               " LEFT OUTER JOIN PIS1TB001 C "
                               " ON B.EMP_NBR = C.EMP_NBR "
                               " LEFT OUTER JOIN OSCODEM D "
                               " ON A.MCODE = D.MCODE "
                               " WHERE B.EMP_NBR = '" + str(user) + "' "
                               " AND A.IODATE <= '" + str(perDate) + "' "
                               " AND A.OFF_GBN = 'off'"
                               " AND A.ICUST = '" + str(iCust) + "' "
                               " AND A.ACCUST like '%" + str(custCode) + "%' "
                               " ORDER BY A.ACSEQN ASC ")
                mainresult = cursor.fetchall()

            return JsonResponse({"mainList": mainresult})

        if permitGbn != '':
            with connection.cursor() as cursor:
                cursor.execute("  SELECT IFNULL(A.IODATE, ''), IFNULL(A.ACTITLE, ''), IFNULL(A.ACAMTS, '') "
                               "        , IFNULL(B.EMP_NBR, ''), IFNULL(C.EMP_NME, ''), IFNULL(A.ACSEQN, ''), IFNULL(A.ACIOGB, '')"
                               "        , IFNULL(A.MCODE, ''), IFNULL(D.MCODENM, ''), IFNULL(A.ACACNUMBER, ''), IFNULL(B.OPT, ''), IFNULL(A.FIN_OPT, ''), IFNULL(A.ACINFO, '') "
                               " FROM SISACCTT A "
                               " LEFT OUTER JOIN OSSIGN B "
                               " ON A.IODATE = B.ACDATE "
                               " AND A.ACSEQN = B.ACSEQN "
                               " AND A.ICUST = B.ICUST "
                               " AND A.FIN_OPT = 'Y' "
                               " LEFT OUTER JOIN PIS1TB001 C "
                               " ON B.EMP_NBR = C.EMP_NBR "
                               " LEFT OUTER JOIN OSCODEM D "
                               " ON A.MCODE = D.MCODE "
                               " WHERE B.EMP_NBR = '" + str(user) + "' "
                               " AND A.IODATE <= '" + str(perDate) + "' "
                               " AND A.OFF_GBN = 'off'"
                               " AND A.ICUST = '" + str(iCust) + "' "
                               " AND A.ACCUST like '%" + str(custCode) + "%' "
                               " ORDER BY A.ACSEQN ASC ")
                mainresult = cursor.fetchall()
            # " AND NOT EXISTS (SELECT OPT FROM OSSIGN WHERE OPT = 'N') "

            return JsonResponse({"mainList": mainresult})

    else:
        if permitGbn == '':
            with connection.cursor() as cursor:
                cursor.execute("  SELECT IFNULL(A.IODATE, ''), IFNULL(A.ACTITLE, ''), IFNULL(A.ACAMTS, '') "
                               "        , IFNULL(B.EMP_NBR, ''), IFNULL(C.EMP_NME, ''), IFNULL(A.ACSEQN, ''), IFNULL(A.ACIOGB, '')"
                               "        , IFNULL(A.MCODE, ''), IFNULL(D.MCODENM, ''), IFNULL(A.ACACNUMBER, ''), IFNULL(B.OPT, ''), IFNULL(A.FIN_OPT, ''), IFNULL(A.ACINFO, '') "
                               " FROM SISACCTT A "
                               " LEFT OUTER JOIN OSSIGN B "
                               " ON A.IODATE = B.ACDATE "
                               " AND A.ACSEQN = B.ACSEQN "
                               " AND A.ICUST = B.ICUST "
                               " AND A.FIN_OPT = 'N' "
                               " LEFT OUTER JOIN PIS1TB001 C "
                               " ON B.EMP_NBR = C.EMP_NBR "
                               " LEFT OUTER JOIN OSCODEM D "
                               " ON A.MCODE = D.MCODE "
                               " WHERE B.EMP_NBR = '" + str(user) + "' "                             
                               " AND A.IODATE <= '" + str(perDate) + "' "
                               " AND A.ICUST = '" + str(iCust) + "' "
                               " AND A.ACCUST like '%" + str(custCode) + "%' "
                               " ORDER BY A.ACSEQN ASC ")
                mainresult = cursor.fetchall()
            # " AND NOT EXISTS (SELECT OPT FROM OSSIGN WHERE OPT = 'N') "

            with connection.cursor() as cursor:
                cursor.execute(" SELECT CUST_NBR, CUST_NME FROM MIS1TB003 WHERE ICUST = '" + str(iCust) + "'")
                cboCust = cursor.fetchall()

            with connection.cursor() as cursor:
                cursor.execute(" SELECT ACNUMBER FROM ACNUMBER WHERE ICUST = '" + str(iCust) + "'")
                cboAct = cursor.fetchall()

            return JsonResponse({"mainList": mainresult, "cboCust": cboCust, "cboAct": cboAct})

        if permitGbn != '':
            with connection.cursor() as cursor:
                cursor.execute("  SELECT IFNULL(A.IODATE, ''), IFNULL(A.ACTITLE, ''), IFNULL(A.ACAMTS, '') "
                               "        , IFNULL(B.EMP_NBR, ''), IFNULL(C.EMP_NME, ''), IFNULL(A.ACSEQN, ''), IFNULL(A.ACIOGB, '')"
                               "        , IFNULL(A.MCODE, ''), IFNULL(D.MCODENM, ''), IFNULL(A.ACACNUMBER, ''), IFNULL(B.OPT, ''), IFNULL(A.FIN_OPT, ''), IFNULL(A.ACINFO, '') "
                               " FROM SISACCTT A "
                               " LEFT OUTER JOIN OSSIGN B "
                               " ON A.IODATE = B.ACDATE "
                               " AND A.ACSEQN = B.ACSEQN "
                               " AND A.ICUST = B.ICUST "
                               " AND A.FIN_OPT = 'Y' "
                               " LEFT OUTER JOIN PIS1TB001 C "
                               " ON B.EMP_NBR = C.EMP_NBR "
                               " LEFT OUTER JOIN OSCODEM D "
                               " ON A.MCODE = D.MCODE "
                               " WHERE B.EMP_NBR = '" + str(user) + "' "
                               " AND A.IODATE <= '" + str(perDate) + "' "
                               " AND A.ICUST = '" + str(iCust) + "' "
                               " AND A.ACCUST like '%" + str(custCode) + "%' "
                               " ORDER BY A.ACSEQN ASC ")
                mainresult = cursor.fetchall()
            # " AND NOT EXISTS (SELECT OPT FROM OSSIGN WHERE OPT = 'N') "

            with connection.cursor() as cursor:
                cursor.execute(" SELECT CUST_NBR, CUST_NME FROM MIS1TB003 WHERE ICUST = '" + str(iCust) + "'")
                cboCust = cursor.fetchall()

            with connection.cursor() as cursor:
                cursor.execute(" SELECT ACNUMBER FROM ACNUMBER WHERE ICUST = '" + str(iCust) + "'")
                cboAct = cursor.fetchall()

            return JsonResponse({"mainList": mainresult, "cboCust": cboCust, "cboAct": cboAct})









def cboActNum_search(request):
    user = request.session.get('userId')
    iCust = request.session.get('USER_ICUST')

    with connection.cursor() as cursor:
        cursor.execute(" SELECT ACNUMBER, ACNUM_NAME FROM ACNUMBER WHERE ICUST = '" + iCust + "' ORDER BY ACNUMBER ")
        cboActNum = cursor.fetchall()

        return JsonResponse({'cboActNum': cboActNum})



def balanceChk(request):
    acNumber = request.POST.get('acNum')
    user = request.session.get('userId')
    iCust = request.session.get('USER_ICUST')

    with connection.cursor() as cursor:
        cursor.execute(" SELECT IFNULL(ACAMTS, 0) FROM ACBALANCE WHERE ACNUMBER = '" + acNumber + "' AND ICUST = '" + iCust + "' ")
        result = cursor.fetchall()

        if result:
            total = result[0][0]
        else:
            total = 0
    # 출금
    with connection.cursor() as cursor:
        cursor.execute(" SELECT IFNULL(SUM(ACAMTS), 0) FROM SISACCTT WHERE ACIOGB = '1' AND ACACNUMBER = '" + acNumber + "' AND ICUST = '" + iCust + "' ")
        result2 = cursor.fetchall()
        outTotal = result2[0][0]
        if result:
            outTotal = result2[0][0]
        else:
            outTotal = 0
    # 입금
    with connection.cursor() as cursor:
        cursor.execute(" SELECT IFNULL(SUM(ACAMTS), 0) FROM SISACCTT WHERE ACIOGB = '2' AND ACACNUMBER = '" + acNumber + "' AND ICUST = '" + iCust + "' ")
        result3 = cursor.fetchall()
        inTotal = result3[0][0]
        if result:
            inTotal = result3[0][0]
        else:
            inTotal = 0

        balance = (total - outTotal) + inTotal
        print(balance)

        return JsonResponse({'balance': balance, 'acNumber': acNumber})

def permitViews_save(request):
    pmtArray = json.loads(request.POST.get('pmtArrList'))
    iCust = request.session.get('USER_ICUST')
    offSet = request.POST.get('offSet')
    actNum = request.POST.get('actNum')
    perDate = request.POST.get('perDate')
    permit = 'Y'

    if offSet:
        balance = 0;
        pmtArrayLists = list(filter(len, pmtArray))
        for data in range(len(pmtArrayLists)):
            if pmtArrayLists[data]["acIogb"]:
                with connection.cursor() as cursor:
                    cursor.execute(" UPDATE SISACCTT SET "
                                   "    ACDATE = '" + pmtArrayLists[data]["perDate"] + "'"
                                   "  , FIN_OPT = '" + str(permit) + "' "
                                   "  , FIN_AMTS = '" + pmtArrayLists[data]["acAmts"] + "' "
                                   "  , OFF_GBN = 'Y' "
                                   "  , OFF_DATE = '" + pmtArrayLists[data]["perDate"] + "' "
                                   "     WHERE IODATE = '" + pmtArrayLists[data]["ioDate"] + "' "
                                   "     AND ACIOGB = '" + pmtArrayLists[data]["acIogb"] + "' "
                                   "     AND ACSEQN = '" + pmtArrayLists[data]["acSeqn"] + "' "
                                   "     AND ICUST = '" + str(iCust) + "' "
                    )
                    connection.commit()

                if pmtArrayLists[data]["acIogb"] == '1':
                    balance -= pmtArrayLists[data]["acAmts"]
                if pmtArrayLists[data]["acIogb"] == '2':
                    balance += pmtArrayLists[data]["acAmts"]

        if balance < 0:
            finalacIogb = '2'
            finalTitle = '상계 매입'
        if balance >= 0:
            finalacIogb = '1'
            finalTitle = '상계 매출'

        # mCode, aCode 계정코드를 어떻게 저장하면 되는지 물어보

        # 입금 or 출금 전표 저장
        now = datetime.date
        with connection.cursor() as cursor:
            cursor.execute("INSERT INTO SISACCTT "
                           "   (    "
                           "     IODATE "
                           ",    ACSEQN "
                           ",    ACIOGB "
                           ",    ACTITLE "
                           ",    ACAMTS "
                           ",    ACACNUMBER "
                           ",    ICUST "
                           ",    EXDATE "
                           ",    ACDATE "
                           ",    FIN_OPT "
                           ",    FIN_AMTS "
                           ",    OFF_GBN "
                           ",    OFF_AMTS "
                           ",    OFF_DATE "
                           "    ) "
                           "    VALUES "
                           "    (   "
                           "    '" + str(perDate) + "' "
                           ",   (SELECT IFNULL (MAX(ACSEQN) + 1,1) AS COUNTED FROM SISACCTT A WHERE IODATE = '" + str(perDate) + "' AND ACIOGB = '" + str(finalacIogb) + "') "
                           ",   '" + str(finalacIogb) + "'"
                           ",   '" + str(finalTitle) + "'"
                           ",   '" + str(balance) + "'"
                           ",   '" + str(actNum) + "'"
                           ",   '" + str(iCust) + "'"
                           ",   '" + str(perDate) + "' "
                           ",   '" + str(perDate) + "' "
                           ",   'Y' "
                           ",   '" + str(balance) + "' "
                           ",   'Y' "
                           ",   '" + str(balance) + "' "
                           ",   '" + str(perDate) + "' "
                           "    )   "
                           )
            connection.commit()

        return JsonResponse({'sucYn': "Y"})

    else:
        pmtArrayLists = list(filter(len, pmtArray))
        for data in range(len(pmtArrayLists)):
            if pmtArrayLists[data]["acIogb"]:
                amts = pmtArrayLists[data]["acAmts"]
                acAmts = amts.replace(",", "")
                print(acAmts)
                with connection.cursor() as cursor:
                    cursor.execute(" UPDATE SISACCTT SET "
                                   "    ACDATE = '" + pmtArrayLists[data]["perDate"] + "'"
                                   "  , FIN_OPT = '" + str(permit) + "' "
                                   "  , FIN_AMTS = '" + str(acAmts) + "' "
                                   "  , ACACNUMBER = '" + str(actNum) + "' "
                                   "     WHERE IODATE = '" + pmtArrayLists[data]["ioDate"] + "' "
                                   "     AND ACIOGB = '" + pmtArrayLists[data]["acIogb"] + "' "
                                   "     AND ACSEQN = '" + pmtArrayLists[data]["acSeqn"] + "' "
                                   "     AND ICUST = '" + str(iCust) + "' "
                    )
                    connection.commit()

        return JsonResponse({'sucYn': "Y"})
