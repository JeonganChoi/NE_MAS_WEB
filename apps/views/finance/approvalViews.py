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
def approvalViews(request):

    return render(request, "finance/approval-reg.html")

def approvalViews_search(request):
    empNbr = request.session.get('userId')
    iCust = request.session.get('USER_ICUST')
    gbn = request.POST.get('gbn')
    ioDate = request.POST.get('ioDate').replace("-", "")
    acSeqn = request.POST.get('acSeqn')
    acIogb = request.POST.get('acIogb')

    # 미결재
    if gbn == '2':
        with connection.cursor() as cursor:
            cursor.execute(" SELECT IFNULL(A.IODATE, ''), IFNULL(A.ACTITLE, ''), IFNULL(A.ACAMTS, '')"
                           "        , IFNULL(B.EMP_NBR, ''), IFNULL(C.EMP_NME, ''), IFNULL(A.ACSEQN, ''), IFNULL(A.ACIOGB, '')  "
                           "        , IFNULL(B.OPT, ''), IFNULL(A.FIN_OPT, ''), IFNULL(A.CRE_USER, ''), IFNULL(D.EMP_NME, '')"
                           " FROM SISACCTT A "
                           " LEFT OUTER JOIN OSSIGN B "
                           " ON A.IODATE = B.ACDATE "
                           " AND A.ACSEQN = B.ACSEQN "
                           " AND A.ICUST = B.ICUST "
                           " LEFT OUTER JOIN PIS1TB001 C "
                           " ON B.EMP_NBR = C.EMP_NBR "
                           " LEFT OUTER JOIN PIS1TB001 D "
                           " ON A.CRE_USER = D.EMP_NBR "
                           " WHERE B.EMP_NBR = '" + str(empNbr) + "' "
                           " AND B.ACDATE <= '" + str(ioDate) + "' "
                           " AND B.ICUST = '" + str(iCust) + "' "
                           " AND B.OPT = 'N' AND B.RTNGBN != 'N' ")
            mainresult = cursor.fetchall()

        return JsonResponse({"mainList": mainresult})

    # 결재
    elif gbn == '3':
        with connection.cursor() as cursor:
            cursor.execute(" SELECT IFNULL(A.IODATE, ''), IFNULL(A.ACTITLE, ''), IFNULL(A.ACAMTS, '')"
                           "        , IFNULL(B.EMP_NBR, ''), IFNULL(C.EMP_NME, ''), IFNULL(A.ACSEQN, ''), IFNULL(A.ACIOGB, '')  "
                           "        , IFNULL(B.OPT, ''), IFNULL(A.FIN_OPT, ''), IFNULL(A.CRE_USER, ''), IFNULL(D.EMP_NME, '') "
                           " FROM SISACCTT A "
                           " LEFT OUTER JOIN OSSIGN B "
                           " ON A.IODATE = B.ACDATE "
                           " AND A.ACSEQN = B.ACSEQN "
                           " AND A.ICUST = B.ICUST "
                           " LEFT OUTER JOIN PIS1TB001 C "
                           " ON B.EMP_NBR = C.EMP_NBR "
                           " LEFT OUTER JOIN PIS1TB001 D "
                           " ON A.CRE_USER = D.EMP_NBR "
                           " WHERE B.EMP_NBR = '" + str(empNbr) + "' "
                           " AND B.ACDATE <= '" + str(ioDate) + "' "
                           " AND B.ICUST = '" + str(iCust) + "' "
                           " AND B.OPT = 'Y' ")
            mainresult = cursor.fetchall()

        return JsonResponse({"mainList": mainresult})

    # 미승인
    elif gbn == '4':
        with connection.cursor() as cursor:
            cursor.execute(" SELECT IFNULL(A.IODATE, ''), IFNULL(A.ACTITLE, ''), IFNULL(A.ACAMTS, '')"
                           "        , IFNULL(B.EMP_NBR, ''), IFNULL(C.EMP_NME, ''), IFNULL(A.ACSEQN, ''), IFNULL(A.ACIOGB, '')  "
                           "        , IFNULL(B.OPT, ''), IFNULL(A.FIN_OPT, ''), IFNULL(A.CRE_USER, ''), IFNULL(D.EMP_NME, '') "
                           " FROM SISACCTT A "
                           " LEFT OUTER JOIN OSSIGN B "
                           " ON A.IODATE = B.ACDATE "
                           " AND A.ACSEQN = B.ACSEQN "
                           " AND A.ICUST = B.ICUST "
                           " LEFT OUTER JOIN PIS1TB001 C "
                           " ON B.EMP_NBR = C.EMP_NBR "
                           " LEFT OUTER JOIN PIS1TB001 D "
                           " ON A.CRE_USER = D.EMP_NBR "
                           " WHERE B.EMP_NBR = '" + str(empNbr) + "' "
                           " AND B.ACDATE <= '" + str(ioDate) + "' "
                           " AND B.ICUST = '" + str(iCust) + "' "
                           " AND A.FIN_OPT = 'N' AND B.RTNGBN != 'N' ")
            mainresult = cursor.fetchall()

        return JsonResponse({"mainList": mainresult})

    # 승인
    elif gbn == '5':
        with connection.cursor() as cursor:
            cursor.execute(" SELECT IFNULL(A.IODATE, ''), IFNULL(A.ACTITLE, ''), IFNULL(A.ACAMTS, '')"
                           "        , IFNULL(B.EMP_NBR, ''), IFNULL(C.EMP_NME, ''), IFNULL(A.ACSEQN, ''), IFNULL(A.ACIOGB, '')"
                           "        , IFNULL(B.OPT, ''), IFNULL(A.FIN_OPT, ''), IFNULL(A.CRE_USER, ''), IFNULL(D.EMP_NME, '')  "
                           " FROM SISACCTT A "
                           " LEFT OUTER JOIN OSSIGN B "
                           " ON A.IODATE = B.ACDATE "
                           " AND A.ACSEQN = B.ACSEQN "
                           " AND A.ICUST = B.ICUST "
                           " LEFT OUTER JOIN PIS1TB001 C "
                           " ON B.EMP_NBR = C.EMP_NBR "
                           " LEFT OUTER JOIN PIS1TB001 D "
                           " ON A.CRE_USER = D.EMP_NBR "
                           " WHERE B.EMP_NBR = '" + str(empNbr) + "' "
                           " AND B.ACDATE <= '" + str(ioDate) + "' "
                           " AND B.ICUST = '" + str(iCust) + "' "
                           " AND A.FIN_OPT = 'Y' ")
            mainresult = cursor.fetchall()

        return JsonResponse({"mainList": mainresult})

    else:
        with connection.cursor() as cursor:
            cursor.execute(" SELECT IFNULL(A.IODATE, ''), IFNULL(A.ACTITLE, ''), IFNULL(A.ACAMTS, '')"
                           "        , IFNULL(B.EMP_NBR, ''), IFNULL(C.EMP_NME, ''), IFNULL(A.ACSEQN, ''), IFNULL(A.ACIOGB, '') "
                           "        , IFNULL(B.OPT, ''), IFNULL(A.FIN_OPT, ''), IFNULL(A.CRE_USER, ''), IFNULL(D.EMP_NME, '')  "
                           " FROM SISACCTT A "
                           " LEFT OUTER JOIN OSSIGN B "
                           " ON A.IODATE = B.ACDATE "
                           " AND A.ACSEQN = B.ACSEQN "
                           " AND A.ICUST = B.ICUST "
                           " LEFT OUTER JOIN PIS1TB001 C "
                           " ON B.EMP_NBR = C.EMP_NBR "
                           " LEFT OUTER JOIN PIS1TB001 D "
                           " ON A.CRE_USER = D.EMP_NBR "
                           " WHERE B.EMP_NBR = '" + str(empNbr) + "' "
                           " AND B.ACDATE <= '" + str(ioDate) + "' "
                           " AND B.ICUST = '" + str(iCust) + "' "
                           " AND B.OPT = 'N' AND B.RTNGBN != 'N' ")
            mainresult = cursor.fetchall()

        return JsonResponse({"mainList": mainresult})


def approvalSubViews_search(request):
    empNbr = request.session.get('userId')
    iCust = request.session.get('USER_ICUST')
    gbn = request.POST.get('gbn')
    ioDate = request.POST.get('ioDate')
    acSeqn = request.POST.get('acSeqn')
    acIogb = request.POST.get('acIogb')

    if ioDate and acSeqn:
        with connection.cursor() as cursor:
            cursor.execute(" SELECT A.SEQ, A.EMP_NBR, B.EMP_NME, B.EMP_FOLDER, A.ACDATE, A.ACSEQN, A.ACIOGB "
                           " FROM OSSIGN A "
                           " LEFT OUTER JOIN PIS1TB001 B "
                           " ON A.EMP_NBR = B.EMP_NBR "
                           " WHERE A.ACDATE = '" + str(ioDate) + "' "
                           " AND A.ACSEQN = '" + str(acSeqn) + "' "
                           " AND A.ACIOGB = '" + str(acIogb) + "' "
                           " AND A.EMP_NBR = '" + empNbr + "' "
                           " AND A.ICUST = '" + str(iCust) + "' "
                           " ORDER BY SEQ ASC ")
            subresult = cursor.fetchall()

        with connection.cursor() as cursor:
            cursor.execute(" SELECT IFNULL(A.ACIOGB, ''), IFNULL(A.ACTITLE, ''), IFNULL(A.ACCUST, ''), IFNULL(A.IODATE, ''), IFNULL(A.MCODE, '') "
                           "        , IFNULL(A.EXDATE, ''), IFNULL(A.ACAMTS, ''), IFNULL(A.ACACNUMBER, ''), IFNULL(A.ACGUBN, ''), IFNULL(A.ACCARD, '') "
                           "        , IFNULL(A.ACDESC, ''), IFNULL(A.ACSEQN, '') "
                           " FROM SISACCTT A "
                           " LEFT OUTER JOIN OSSIGN B "
                           " ON A.IODATE = B.ACDATE "
                           " AND A.ACSEQN = B.ACSEQN "
                           " AND A.ICUST = B.ICUST "
                           " LEFT OUTER JOIN PIS1TB001 C "
                           " ON B.EMP_NBR = C.EMP_NBR "
                           " WHERE A.IODATE = '" + str(ioDate) + "' "
                           " AND A.ACSEQN = '" + str(acSeqn) + "' "
                           " AND A.ACIOGB = '" + str(acIogb) + "' "
                           " AND B.EMP_NBR = '" + str(empNbr) + "' "
                           " AND A.ICUST = '" + str(iCust) + "' ")
            mainresult = cursor.fetchall()

            # 거래처
        with connection.cursor() as cursor:
            cursor.execute(" SELECT CUST_NBR, CUST_NME FROM MIS1TB003 WHERE ICUST = '" + iCust + "' ")
            cboCust = cursor.fetchall()

            # 입출금구분
        with connection.cursor() as cursor:
            cursor.execute(" SELECT RESKEY, RESNAM FROM OSREFCP WHERE RECODE = 'OUA' AND ICUST = '" + iCust + "' ORDER BY RESKEY ")
            cboGgn = cursor.fetchall()

            # 관리계정
        with connection.cursor() as cursor:
            cursor.execute(" SELECT MCODE, MCODENM FROM OSCODEM WHERE ICUST = '" + iCust + "' ORDER BY MCODE ASC ")
            cboMCode = cursor.fetchall()

            # 결제방법
        with connection.cursor() as cursor:
            cursor.execute(" SELECT RESKEY, RESNAM FROM OSREFCP WHERE RECODE = 'PGB' AND ICUST = '" + iCust + "' ORDER BY RESNAM ")
            cboPay = cursor.fetchall()

            # 계좌번호
        with connection.cursor() as cursor:
            cursor.execute(" SELECT ACNUMBER FROM ACNUMBER WHERE ICUST = '" + iCust + "' ")
            cboAcnumber = cursor.fetchall()

        return JsonResponse({"subList": subresult, "mainList": mainresult, "cboCust": cboCust, "cboGgn": cboGgn, "cboMCode": cboMCode, "cboPay": cboPay, "cboAcnumber": cboAcnumber})



def approvalViews_save(request):
    seq = request.POST.get("seq")
    empNbr = request.POST.get("empNbr")
    folder = request.POST.get("folder")
    reason = request.POST.get("reason")
    ioDate = request.POST.get("ioDate")
    acSeqn = request.POST.get("acSeqn")
    acIogb = request.POST.get("acIogb")
    iCust = request.session.get('USER_ICUST')
    gbn = request.POST.get('gbn')
    opt = 'Y'

    if gbn == '1':
        rtnGbn = ''
        with connection.cursor() as cursor:
            cursor.execute(" UPDATE OSSIGN SET "
                           "     OPT = '" + str(opt) + "' "
                           "   , GBN = '" + str(gbn) + "' "
                           "   , RTNGBN = '" + str(rtnGbn) + "' "
                           "   , FOLDER = '" + str(folder) + "' "
                           "     WHERE ACDATE = '" + str(ioDate) + "' "
                           "     AND ACSEQN = '" + str(acSeqn) + "' "
                           "     AND SEQ = '" + str(seq) + "' "
                           "     AND EMP_NBR = '" + str(empNbr) + "' "
                           "     AND ACIOGB = '" + str(acIogb) + "' "
                           "     AND ICUST = '" + str(iCust) + "'"
                           )
            connection.commit()

        # 모두 결재 했는지 체크 후, 모두 했으면 SISACCTT 처리
        # with connection.cursor() as cursor:
        #     cursor.execute(" SELECT * FROM OSSIGN WHERE ACDATE = '" + str(ioDate) + "' "
        #                    "        AND ACSEQN = '" + str(acSeqn) + "' AND ACIOGB = '" + str(acIogb) + "' AND ICUST = '" + str(iCust) + "' "
        #                    "        AND OPT = 'N' ")
        #     chk = cursor.fetchall()
        #
        #     if chk is '' or chk is None:
        #         with connection.cursor() as cursor:
        #             cursor.execute(" UPDATE SISACCTT SET "
        #                            "     FIN_OPT = 'Y' "
        #                            "     WHERE ACDATE = '" + str(ioDate) + "' "
        #                            "     AND ACSEQN = '" + str(acSeqn) + "' "
        #                            "     AND ACIOGB = '" + str(acIogb) + "' "
        #                            "     AND ICUST = '" + str(iCust) + "'"
        #                            )
        #             connection.commit()

        return JsonResponse({'sucYn': "Y"})

    elif gbn == '2':
        rtnGbn = ''
        with connection.cursor() as cursor:
            cursor.execute(" SELECT EMP_NBR, SEQ FROM OSSIGN WHERE ACDATE = '" + str(ioDate) + "' AND ACSEQN = '" + str(acSeqn) + "' "
                           "                             AND SEQ >= '" + str(seq) + "' AND ACIOGB = '" + str(acIogb) + "' AND ICUST = '" + str(iCust) + "' ")
            empresult = cursor.fetchall()

            payArrayLists = list(filter(len, empresult))
            for data in range(len(payArrayLists)):
                with connection.cursor() as cursor:
                    cursor.execute("    UPDATE OSSIGN SET "
                                       "     OPT = '" + str(opt) + "' "
                                       "   , GBN = '" + str(gbn) + "' "
                                       "   , RTNGBN = '" + str(rtnGbn) + "' "
                                       "   , FOLDER = '" + str(folder) + "' "
                                       "     WHERE ACDATE = '" + str(ioDate) + "' "
                                       "     AND ACSEQN = '" + str(acSeqn) + "' "
                                       "     AND SEQ = '" + str(payArrayLists[data][1]) + "' "
                                       "     AND EMP_NBR = '" + str(payArrayLists[data][0]) + "' "
                                       "     AND ACIOGB = '" + str(acIogb) + "' "
                                       "     AND ICUST = '" + str(iCust) + "'"
                                       )
                    connection.commit()

            return JsonResponse({'sucYn': "Y"})

    elif gbn == '3':
        opt = 'N'
        rtnGbn = 'N'
        with connection.cursor() as cursor:
            cursor.execute("    UPDATE OSSIGN SET "
                               "     RETURNS = '" + str(reason) + "' "
                               "   , OPT = '" + str(opt) + "' "
                               "   , GBN = '" + str(gbn) + "' "
                               "   , RTNGBN = '" + str(rtnGbn) + "' "
                               "   , FOLDER = '" + str(folder) + "' "
                               "     WHERE ACDATE = '" + str(ioDate) + "' "
                               "     AND ACSEQN = '" + str(acSeqn) + "' "
                               "     AND SEQ = '" + str(seq) + "' "
                               "     AND EMP_NBR = '" + str(empNbr) + "' "
                               "     AND ACIOGB = '" + str(acIogb) + "' "
                               "     AND ICUST = '" + str(iCust) + "'"
                               )
            connection.commit()

        return JsonResponse({'sucYn': "Y"})