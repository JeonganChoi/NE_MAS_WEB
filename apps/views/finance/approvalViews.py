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
    userId = request.session.get('userId')
    if userId == '' or userId is None:
        return redirect("/page-404/")
    else:
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
            cursor.execute("SELECT IFNULL(A.IODATE, ''), IFNULL(A.ACTITLE, ''), IFNULL(A.ACAMTS, '')"
                           "        , IFNULL(B.EMP_NBR, ''), IFNULL(C.EMP_NME, ''), IFNULL(A.ACSEQN, ''), IFNULL(A.ACIOGB, '') "
                           "        , IFNULL(B.OPT, ''), IFNULL(A.FIN_OPT, ''), IFNULL(A.CRE_USER, ''), IFNULL(D.EMP_NME, ''), IFNULL(B.SEQ, ''), IFNULL(A.APPLYDT, '')  "
                           " FROM SISACCTT A "
                           " LEFT OUTER JOIN OSSIGN B "
                           " ON A.IODATE = B.ACDATE "
                           " AND A.ACSEQN = B.ACSEQN "
                           " AND A.ACIOGB = B.ACIOGB "
                           " AND A.ICUST = B.ICUST "
                           " LEFT OUTER JOIN PIS1TB001 C "
                           " ON B.EMP_NBR = C.EMP_NBR "
                           " LEFT OUTER JOIN PIS1TB001 D "
                           " ON A.CRE_USER = D.EMP_NBR "
                           " WHERE B.EMP_NBR = '" + str(empNbr) + "' "
                           " AND B.ICUST = '" + str(iCust) + "' "
                           " AND B.OPT = 'N' AND B.RTNGBN = 'N' AND A.MID_OPT = 'N' ")
            mainresult = cursor.fetchall()

        return JsonResponse({"mainList": mainresult})

    # 결재
    elif gbn == '3':
        with connection.cursor() as cursor:
            cursor.execute(" SELECT IFNULL(A.IODATE, ''), IFNULL(A.ACTITLE, ''), IFNULL(A.ACAMTS, '')"
                           "        , IFNULL(B.EMP_NBR, ''), IFNULL(C.EMP_NME, ''), IFNULL(A.ACSEQN, ''), IFNULL(A.ACIOGB, '')  "
                           "        , IFNULL(B.OPT, ''), IFNULL(A.FIN_OPT, ''), IFNULL(A.CRE_USER, ''), IFNULL(D.EMP_NME, ''), IFNULL(B.SEQ, ''), IFNULL(A.APPLYDT, '') "
                           " FROM SISACCTT A "
                           " LEFT OUTER JOIN OSSIGN B "
                           " ON A.IODATE = B.ACDATE "
                           " AND A.ACSEQN = B.ACSEQN "
                           " AND A.ACIOGB = B.ACIOGB "
                           " AND A.ICUST = B.ICUST "
                           " LEFT OUTER JOIN PIS1TB001 C "
                           " ON B.EMP_NBR = C.EMP_NBR "
                           " LEFT OUTER JOIN PIS1TB001 D "
                           " ON A.CRE_USER = D.EMP_NBR "
                           " WHERE B.EMP_NBR = '" + str(empNbr) + "' "
                           " AND B.ICUST = '" + str(iCust) + "' "
                           " AND B.OPT = 'Y' AND A.MID_OPT = 'Y' ")
            mainresult = cursor.fetchall()

        return JsonResponse({"mainList": mainresult})

    # 미승인
    # elif gbn == '4':
    #     with connection.cursor() as cursor:
    #         cursor.execute(" SELECT IFNULL(A.IODATE, ''), IFNULL(A.ACTITLE, ''), IFNULL(A.ACAMTS, '')"
    #                        "        , IFNULL(B.EMP_NBR, ''), IFNULL(C.EMP_NME, ''), IFNULL(A.ACSEQN, ''), IFNULL(A.ACIOGB, '')  "
    #                        "        , IFNULL(B.OPT, ''), IFNULL(A.FIN_OPT, ''), IFNULL(A.CRE_USER, ''), IFNULL(D.EMP_NME, ''), IFNULL(B.SEQ, ''), IFNULL(A.APPLYDT, '') "
    #                        " FROM SISACCTT A "
    #                        " LEFT OUTER JOIN OSSIGN B "
    #                        " ON A.IODATE = B.ACDATE "
    #                        " AND A.ACSEQN = B.ACSEQN "
    #                        " AND A.ACIOGB = B.ACIOGB "
    #                        " AND A.ICUST = B.ICUST "
    #                        " LEFT OUTER JOIN PIS1TB001 C "
    #                        " ON B.EMP_NBR = C.EMP_NBR "
    #                        " LEFT OUTER JOIN PIS1TB001 D "
    #                        " ON A.CRE_USER = D.EMP_NBR "
    #                        " WHERE B.EMP_NBR = '" + str(empNbr) + "' "
    #                        " AND B.ICUST = '" + str(iCust) + "' "
    #                        " AND A.FIN_OPT = 'N' AND A.MID_OPT = 'Y' AND B.RTNGBN != 'N' ")
    #         mainresult = cursor.fetchall()
    #
    #     return JsonResponse({"mainList": mainresult})

    # 승인
    # elif gbn == '5':
    #     with connection.cursor() as cursor:
    #         cursor.execute(" SELECT IFNULL(A.IODATE, ''), IFNULL(A.ACTITLE, ''), IFNULL(A.ACAMTS, '')"
    #                        "        , IFNULL(B.EMP_NBR, ''), IFNULL(C.EMP_NME, ''), IFNULL(A.ACSEQN, ''), IFNULL(A.ACIOGB, '')"
    #                        "        , IFNULL(B.OPT, ''), IFNULL(A.FIN_OPT, ''), IFNULL(A.CRE_USER, ''), IFNULL(D.EMP_NME, ''), IFNULL(B.SEQ, ''), IFNULL(A.APPLYDT, '')  "
    #                        " FROM SISACCTT A "
    #                        " LEFT OUTER JOIN OSSIGN B "
    #                        " ON A.IODATE = B.ACDATE "
    #                        " AND A.ACSEQN = B.ACSEQN "
    #                        " AND A.ACIOGB = B.ACIOGB "
    #                        " AND A.ICUST = B.ICUST "
    #                        " LEFT OUTER JOIN PIS1TB001 C "
    #                        " ON B.EMP_NBR = C.EMP_NBR "
    #                        " LEFT OUTER JOIN PIS1TB001 D "
    #                        " ON A.CRE_USER = D.EMP_NBR "
    #                        " WHERE B.EMP_NBR = '" + str(empNbr) + "' "
    #                        " AND B.ICUST = '" + str(iCust) + "' "
    #                        " AND A.FIN_OPT = 'Y' "
    #                        " AND A.MID_OPT = 'Y' ")
    #         mainresult = cursor.fetchall()
    #
    #     return JsonResponse({"mainList": mainresult})

    else:
        with connection.cursor() as cursor:
            cursor.execute("SELECT IFNULL(A.IODATE, ''), IFNULL(A.ACTITLE, ''), IFNULL(A.ACAMTS, '')"
                           "        , IFNULL(B.EMP_NBR, ''), IFNULL(C.EMP_NME, ''), IFNULL(A.ACSEQN, ''), IFNULL(A.ACIOGB, '') "
                           "        , IFNULL(B.OPT, ''), IFNULL(A.FIN_OPT, ''), IFNULL(A.CRE_USER, ''), IFNULL(D.EMP_NME, ''), IFNULL(B.SEQ, ''), IFNULL(A.APPLYDT, '')  "
                           " FROM SISACCTT A "
                           " LEFT OUTER JOIN OSSIGN B "
                           " ON A.IODATE = B.ACDATE "
                           " AND A.ACSEQN = B.ACSEQN "
                           " AND A.ACIOGB = B.ACIOGB "
                           " AND A.ICUST = B.ICUST "
                           " LEFT OUTER JOIN PIS1TB001 C "
                           " ON B.EMP_NBR = C.EMP_NBR "
                           " LEFT OUTER JOIN PIS1TB001 D "
                           " ON A.CRE_USER = D.EMP_NBR "
                           " WHERE B.EMP_NBR = '" + str(empNbr) + "' "
                           " AND B.ICUST = '" + str(iCust) + "' "
                           " AND B.OPT = 'N' AND B.RTNGBN = 'N' AND A.MID_OPT = 'N' ")
            mainresult = cursor.fetchall()

        return JsonResponse({"mainList": mainresult})
        # cursor.execute("SELECT IODATE, ACTITLE, ACAMTS, EMP_NBR, EMP_NME, ACSEQN, ACIOGB, OPT, FIN_OPT, CRE_USER, WRITER, SEQ, APPLYDT FROM "
        #                 "            ( "
        #                 " SELECT IFNULL(A.IODATE, '') AS IODATE, IFNULL(A.ACTITLE, '') AS ACTITLE, IFNULL(A.ACAMTS, '') AS ACAMTS "
        #                 "        , IFNULL(B.EMP_NBR, '') AS EMP_NBR, IFNULL(C.EMP_NME, '') AS EMP_NME, IFNULL(A.ACSEQN, '') AS ACSEQN, IFNULL(A.ACIOGB, '') AS ACIOGB "
        #                 "        , IFNULL(B.OPT, '') AS OPT, IFNULL(A.FIN_OPT, '') AS FIN_OPT, IFNULL(A.CRE_USER, '') AS CRE_USER, IFNULL(D.EMP_NME, '') AS WRITER "
        #                 "        , IFNULL(B.SEQ, '') AS SEQ, IFNULL(A.APPLYDT, '') AS APPLYDT "
        #                 " FROM SISACCTT A "
        #                 " LEFT OUTER JOIN OSSIGN B "
        #                 " ON A.IODATE = B.ACDATE "
        #                 " AND A.ACSEQN = B.ACSEQN "
        #                 " AND A.ACIOGB = B.ACIOGB "
        #                 " AND A.ICUST = B.ICUST "
        #                 " LEFT OUTER JOIN PIS1TB001 C "
        #                 " ON B.EMP_NBR = C.EMP_NBR "
        #                 " LEFT OUTER JOIN PIS1TB001 D "
        #                 " ON A.CRE_USER = D.EMP_NBR "
        #                 " WHERE B.EMP_NBR = '" + str(empNbr) + "' "
        #                 " AND B.ICUST = '" + str(iCust) + "' "
        #                 " AND B.OPT = 'N' "
        #                 " AND B.SEQ  > (SELECT MAX(SEQ) FROM OSSIGN S WHERE S.ACDATE = B.ACDATE AND S.ACSEQN = B.ACSEQN AND S.ACIOGB = B.ACIOGB AND S.ICUST = B.ICUST AND S.OPT = 'Y' AND S.RTNGBN = 'N') "
        #                 " UNION ALL "
        #                 " SELECT IFNULL(A.IODATE, ''), IFNULL(A.ACTITLE, ''), IFNULL(A.ACAMTS, '') "
        #                 "        , IFNULL(B.EMP_NBR, ''), IFNULL(C.EMP_NME, ''), IFNULL(A.ACSEQN, ''), IFNULL(A.ACIOGB, '') "
        #                 "        , IFNULL(B.OPT, ''), IFNULL(A.FIN_OPT, ''), IFNULL(A.CRE_USER, ''), IFNULL(D.EMP_NME, ''), IFNULL(B.SEQ, ''), IFNULL(A.APPLYDT, '') "
        #                 " FROM SISACCTT A "
        #                 " LEFT OUTER JOIN OSSIGN B "
        #                 " ON A.IODATE = B.ACDATE "
        #                 " AND A.ACSEQN = B.ACSEQN "
        #                 " AND A.ACIOGB = B.ACIOGB "
        #                 " AND A.ICUST = B.ICUST "
        #                 " LEFT OUTER JOIN PIS1TB001 C "
        #                 " ON B.EMP_NBR = C.EMP_NBR "
        #                 " LEFT OUTER JOIN PIS1TB001 D "
        #                 " ON A.CRE_USER = D.EMP_NBR "
        #                 " WHERE B.EMP_NBR = '" + str(empNbr) + "' "
        #                 " AND B.ICUST = '" + str(iCust) + "' "
        #                 " AND B.OPT = 'N' "
        #                 " AND B.SEQ  = '1' AND B.RTNGBN = 'N') AA ORDER BY IODATE ")
        # mainresult = cursor.fetchall()



        #     sublist2 = []
        #
        #     for i in range(len(mainresult)):
        #         sublist = [mainresult[i][0], mainresult[i][5], mainresult[i][6], mainresult[i][11]]
        #         sublist2 += [sublist]
        #
        #     sublist4 = []
        #     for j in range(len(sublist2)):
        #         with connection.cursor() as cursor:
        #             cursor.execute("  SELECT IFNULL(A.IODATE, ''), IFNULL(A.ACTITLE, ''), IFNULL(A.ACAMTS, '')"
        #                            "        , IFNULL(B.EMP_NBR, ''), IFNULL(C.EMP_NME, ''), IFNULL(A.ACSEQN, ''), IFNULL(A.ACIOGB, '') "
        #                            "        , IFNULL(B.OPT, ''), IFNULL(A.FIN_OPT, ''), IFNULL(A.CRE_USER, ''), IFNULL(D.EMP_NME, ''), IFNULL(B.SEQ, '')  "
        #                            " FROM SISACCTT A "
        #                            " LEFT OUTER JOIN OSSIGN B "
        #                            " ON A.IODATE = B.ACDATE "
        #                            " AND A.ACSEQN = B.ACSEQN "
        #                            " AND A.ICUST = B.ICUST "
        #                            " AND A.ACIOGB = B.ACIOGB "
        #                            " LEFT OUTER JOIN PIS1TB001 C "
        #                            " ON B.EMP_NBR = C.EMP_NBR "
        #                            " LEFT OUTER JOIN PIS1TB001 D "
        #                            " ON A.CRE_USER = D.EMP_NBR "
        #                            " WHERE B.SEQ < '" + str(sublist2[j][3]) + "' "
        #                            " AND B.OPT = 'Y' "
        #                            " AND A.IODATE = '" + str(sublist2[j][0]) + "' "
        #                            " AND A.ACSEQN = '" + str(sublist2[j][1]) + "' "
        #                            " AND A.ICUST = '" + str(iCust) + "' "
        #                            " AND A.ACIOGB = '" + str(sublist2[j][2]) + "' ")
        #             subresult = cursor.fetchall()
        #             print(subresult)
        #             for data in range(len(subresult)):
        #                 itembomlist3 = [subresult[data][0], subresult[data][1], subresult[data][2], subresult[data][3],
        #                                 subresult[data][4], subresult[data][5], subresult[data][6], subresult[data][7],
        #                                 subresult[data][8], subresult[data][9], subresult[data][10]]
        #                 sublist4 += [itembomlist3]
        #
        # return JsonResponse({"mainList": mainresult, "subList": sublist4})


def approvalSubViews_search(request):
    empNbr = request.session.get('userId')
    iCust = request.session.get('USER_ICUST')
    gbn = request.POST.get('gbn')
    ioDate = request.POST.get('ioDate')
    acSeqn = request.POST.get('acSeqn')
    acIogb = request.POST.get('acIogb')

    if ioDate and acSeqn:
        with connection.cursor() as cursor:
            cursor.execute(" SELECT A.SEQ, A.EMP_NBR, B.EMP_NME, B.EMP_FOLDER, A.ACDATE, A.ACSEQN, A.ACIOGB, A.OPT "
                           " FROM OSSIGN A "
                           " LEFT OUTER JOIN PIS1TB001 B "
                           " ON A.EMP_NBR = B.EMP_NBR "
                           " WHERE A.ACDATE = '" + str(ioDate) + "' "
                           " AND A.ACSEQN = '" + str(acSeqn) + "' "
                           " AND A.ACIOGB = '" + str(acIogb) + "' "
                           " AND A.ICUST = '" + str(iCust) + "' "
                           " ORDER BY SEQ ASC ")
            subresult = cursor.fetchall()

        with connection.cursor() as cursor:
            cursor.execute(" SELECT IFNULL(A.ACIOGB, ''), IFNULL(A.ACTITLE, ''), IFNULL(A.ACCUST, ''), IFNULL(A.IODATE, ''), IFNULL(A.MCODE, '') "
                           "        , IFNULL(A.EXDATE, ''), IFNULL(A.ACAMTS, ''), IFNULL(A.ACACNUMBER, ''), IFNULL(A.ACGUBN, ''), IFNULL(A.ACCARD, '') "
                           "        , IFNULL(A.ACDESC, ''), IFNULL(A.ACSEQN, ''), IFNULL(A.ACFOLDER, ''), IFNULL(B.SEQ, '') "
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
            cursor.execute(" SELECT CUST_NBR, CUST_NME FROM MIS1TB003 WHERE ICUST = '" + str(iCust) + "' ")
            cboCust = cursor.fetchall()

            # 입출금구분
        with connection.cursor() as cursor:
            cursor.execute(" SELECT RESKEY, RESNAM FROM OSREFCP WHERE RECODE = 'OUA' AND ICUST = '" + str(iCust) + "' ORDER BY RESKEY ")
            cboGgn = cursor.fetchall()

            # 관리계정
        with connection.cursor() as cursor:
            cursor.execute(" SELECT MCODE, MCODENM FROM OSCODEM WHERE ICUST = '" + str(iCust) + "' ORDER BY MCODE ASC ")
            cboMCode = cursor.fetchall()

            # 결제방법
        with connection.cursor() as cursor:
            cursor.execute(" SELECT RESKEY, RESNAM FROM OSREFCP WHERE RECODE = 'PGB' AND ICUST = '" + str(iCust) + "' ORDER BY RESNAM ")
            cboPay = cursor.fetchall()

            # 계좌번호
        with connection.cursor() as cursor:
            cursor.execute(" SELECT ACNUMBER FROM ACNUMBER WHERE ICUST = '" + str(iCust) + "' ")
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
    user = request.session.get('userId')
    iCust = request.session.get('USER_ICUST')
    gbn = request.POST.get('gbn')
    opt = 'Y'

    if gbn == '1':
        rtnGbn = 'N'
        with connection.cursor() as cursor:
            cursor.execute(" SELECT EMP_NBR FROM OSSIGN WHERE ACDATE = '" + str(ioDate) + "' "
                           "  AND ACSEQN = '" + str(seq) + "' AND ACIOGB = '" + str(acIogb) + "' AND ICUST = '" + str(iCust) + "' "
                           "  AND SEQ = (SELECT MAX(SEQ) FROM OSSIGN WHERE ACDATE = '" + str(ioDate) + "' AND ACSEQN = '" + str(seq) + "' AND ACIOGB = '" + str(acIogb) + "' AND ICUST = '" + str(iCust) + "') ")
            result = cursor.fetchall()
            emp = str(result[0][0])

        # 예결
        if emp == str(user):
            with connection.cursor() as cursor:
                cursor.execute(" UPDATE OSSIGN SET "
                               "     OPT = '" + str(opt) + "' "
                               "   , GBN = '" + str(gbn) + "' "
                               "   , RTNGBN = '" + str(rtnGbn) + "' "
                               "     WHERE ACDATE = '" + str(ioDate).replace("-", "") + "' "
                               "     AND ACSEQN = '" + str(seq) + "' "
                               "     AND SEQ = '" + str(acSeqn) + "' "
                               "     AND EMP_NBR = '" + str(user) + "' "
                               "     AND ACIOGB = '" + str(acIogb) + "' "
                               "     AND ICUST = '" + str(iCust) + "'"
                               )
                connection.commit()

            with connection.cursor() as cursor:
                cursor.execute(" UPDATE SISACCTT SET "
                               "     MID_OPT = 'Y' "
                               "     WHERE IODATE = '" + str(ioDate).replace("-", "") + "' "
                               "     AND ACSEQN = '" + str(seq) + "' "
                               "     AND ACIOGB = '" + str(acIogb) + "' "
                               "     AND ICUST = '" + str(iCust) + "'"
                               )
                connection.commit()

            return JsonResponse({'sucYn': "Y"})

        # 일반결재
        else:
            with connection.cursor() as cursor:
                cursor.execute(" UPDATE OSSIGN SET "
                               "     OPT = '" + str(opt) + "' "
                               "   , GBN = '" + str(gbn) + "' "
                               "   , RTNGBN = '" + str(rtnGbn) + "' "
                               "     WHERE ACDATE = '" + str(ioDate).replace("-", "") + "' "
                               "     AND ACSEQN = '" + str(seq) + "' "
                               "     AND SEQ = '" + str(acSeqn) + "' "
                               "     AND EMP_NBR = '" + str(user) + "' "
                               "     AND ACIOGB = '" + str(acIogb) + "' "
                               "     AND ICUST = '" + str(iCust) + "'"
                               )
                connection.commit()

            # 모두 결재 했는지 체크 후, 모두 했으면 SISACCTT 처리
            with connection.cursor() as cursor:
                cursor.execute(" SELECT COUNT(*) FROM OSSIGN WHERE ACDATE = '" + str(ioDate).replace("-", "") + "' "
                               "        AND ACSEQN = '" + str(seq) + "' AND ACIOGB = '" + str(acIogb) + "' AND ICUST = '" + str(iCust) + "' "
                               "        AND OPT = 'N' ")
                result = cursor.fetchall()
                chk = int(result[0][0])

                if chk == 0:
                    with connection.cursor() as cursor:
                        cursor.execute(" UPDATE SISACCTT SET "
                                       "     MID_OPT = 'Y' "
                                       "     WHERE IODATE = '" + str(ioDate).replace("-", "") + "' "
                                       "     AND ACSEQN = '" + str(seq) + "' "
                                       "     AND ACIOGB = '" + str(acIogb) + "' "
                                       "     AND ICUST = '" + str(iCust) + "'"
                                       )
                        connection.commit()

            return JsonResponse({'sucYn': "Y"})

    elif gbn == '2':
        rtnGbn = 'N'
        with connection.cursor() as cursor:
            cursor.execute(" SELECT EMP_NBR, SEQ FROM OSSIGN WHERE ACDATE = '" + str(ioDate).replace("-", "") + "' AND ACSEQN = '" + str(seq) + "' "
                           "                             AND SEQ >= '" + str(acSeqn) + "' AND ACIOGB = '" + str(acIogb) + "' AND ICUST = '" + str(iCust) + "' ")
            empresult = cursor.fetchall()

        payArrayLists = list(filter(len, empresult))
        for data in range(len(payArrayLists)):
            with connection.cursor() as cursor:
                cursor.execute("    UPDATE OSSIGN SET "
                                   "     OPT = '" + str(opt) + "' "
                                   "   , GBN = '" + str(gbn) + "' "
                                   "   , RTNGBN = '" + str(rtnGbn) + "' "
                                   "     WHERE ACDATE = '" + str(ioDate).replace("-", "") + "' "
                                   "     AND ACSEQN = '" + str(seq) + "' "
                                   "     AND SEQ = '" + str(payArrayLists[data][1]) + "' "
                                   "     AND EMP_NBR = '" + str(payArrayLists[data][0]) + "' "
                                   "     AND ACIOGB = '" + str(acIogb) + "' "
                                   "     AND ICUST = '" + str(iCust) + "'"
                                   )
                connection.commit()

        # 모두 결재 했는지 체크 후, 모두 했으면 SISACCTT 처리
        with connection.cursor() as cursor:
            cursor.execute(" SELECT COUNT(*) FROM OSSIGN WHERE ACDATE = '" + str(ioDate).replace("-", "") + "' "
                           "        AND ACSEQN = '" + str(seq) + "' AND ACIOGB = '" + str(acIogb) + "' AND ICUST = '" + str(iCust) + "' "
                           "        AND OPT = 'N' ")
            result2 = cursor.fetchall()
            chk = int(result2[0][0])

            if chk == 0:
                with connection.cursor() as cursor:
                    cursor.execute(" UPDATE SISACCTT SET "
                                   "     MID_OPT = 'Y' "
                                   "     WHERE IODATE = '" + str(ioDate).replace("-", "") + "' "
                                   "     AND ACSEQN = '" + str(seq) + "' "
                                   "     AND ACIOGB = '" + str(acIogb) + "' "
                                   "     AND ICUST = '" + str(iCust) + "'"
                                   )
                    connection.commit()

            return JsonResponse({'sucYn': "Y"})

    elif gbn == '3':
        opt = 'N'
        rtnGbn = 'Y'
        with connection.cursor() as cursor:
            cursor.execute("    UPDATE OSSIGN SET "
                               "     RETURNS = '" + str(reason) + "' "
                               "   , OPT = '" + str(opt) + "' "
                               "   , GBN = '" + str(gbn) + "' "
                               "   , RTNGBN = '" + str(rtnGbn) + "' "
                               "     WHERE ACDATE = '" + str(ioDate).replace("-", "") + "' "
                               "     AND ACSEQN = '" + str(seq) + "' "
                               "     AND SEQ = '" + str(acSeqn) + "' "
                               "     AND EMP_NBR = '" + str(user) + "' "
                               "     AND ACIOGB = '" + str(acIogb) + "' "
                               "     AND ICUST = '" + str(iCust) + "'"
                               )
            connection.commit()

        return JsonResponse({'sucYn': "Y"})