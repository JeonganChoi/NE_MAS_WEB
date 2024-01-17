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

# 은행내역서
def receivepaySheetViews(request):
    userId = request.session.get('userId')
    if userId == '' or userId is None:
        return redirect("/page-404/")
    else:
        return render(request, "currentstate/receive-pay-banksheet.html")


def receivepaySheetViews_search(request):
    cboBank = request.POST.get('cboBank')
    cboAccount = request.POST.get('cboAccount')
    strDate = request.POST.get('startDate').replace("-", "")
    endDate = request.POST.get('endDate').replace("-", "")
    creUser = request.session.get("userId")
    iCust = request.session.get("USER_ICUST")

    if cboBank != '' and cboAccount == '':
        with connection.cursor() as cursor:
            cursor.execute(" SELECT ACNUMBER FROM ACNUMBER WHERE ACBKCD = '" + str(cboBank) + "' AND ICUST = '" + str(iCust) + "' ")

            cboAresult = cursor.fetchall()

        with connection.cursor() as cursor:
            cursor.execute(" SELECT MCODE, MCODENM FROM OSCODEM WHERE ICUST = '" + str(iCust) + "' ")

            titleresult = cursor.fetchall()

        with connection.cursor() as cursor:
            cursor.execute(" SELECT IFNULL(SUM(BAL), 0), IFNULL(SUM(INTOTAL), 0), IFNULL(SUM(OUTTOTAL), 0), IFNULL(SUM(BAL + INTOTAL - OUTTOTAL), 0) FROM "
                           "        (SELECT SUM(IFNULL(A.ACAMTS, 0)) AS BAL, 0 AS INTOTAL, 0 AS OUTTOTAL, B.ACBKCD FROM ACBALANCE A "
                           "        LEFT OUTER JOIN ACNUMBER B ON A.ACACNUMBER = B.ACNUMBER "
                           "        WHERE A.ACDATE < '" + str(strDate) + "' AND A.ICUST = '" + str(iCust) + "' AND B.ACBKCD = '" + str(cboBank) + "' "
                           " UNION ALL "
                           "        SELECT 0 AS BAL, SUM(IFNULL(A.ACAMTS, 0)) AS INTOTAL, 0 AS OUTTOTAL, B.ACBKCD FROM SISACCTT A "
                           "        LEFT OUTER JOIN ACNUMBER B ON A.ACACNUMBER = B.ACNUMBER "
                           "        WHERE A.ACIOGB = '2' AND A.FIN_OPT = 'Y' AND A.ICUST = '" + str(iCust) + "' AND A.ACDATE < '" + str(strDate) + "' AND B.ACBKCD = '" + str(cboBank) + "' "
                           " UNION ALL "
                           "        SELECT 0 AS BAL, 0 AS INTOTAL, SUM(IFNULL(A.ACAMTS, 0)) AS OUTTOTAL, B.ACBKCD FROM SISACCTT A "
                           "        LEFT OUTER JOIN ACNUMBER B ON A.ACACNUMBER = B.ACNUMBER "
                           "        WHERE A.ACIOGB = '1' AND A.FIN_OPT = 'Y' AND A.ICUST = '" + str(iCust) + "' AND A.ACDATE < '" + str(strDate) + "' AND B.ACBKCD = '" + str(cboBank) + "' "
                           " ) AA ")

            totalresult = cursor.fetchall()

        with connection.cursor() as cursor:
            cursor.execute(" SELECT IFNULL(UN.ACDATE, ''), IFNULL(UN.ACIOGB, ''), IFNULL(UN.RESNAM, ''), IFNULL(UN.OACAMTS, 0), IFNULL(UN.IACAMTS, 0) "
                           "        , IFNULL(UN.ACCUST, ''), IFNULL(UN.CUST_NME, ''), IFNULL(UN.ACACNUMBER, ''), IFNULL(UN.ACNUM_NAME, ''), IFNULL(UN.MCODE, ''), IFNULL(UN.MCODENM, '')"
                           "        , IFNULL(UN.ACDESC, ''), IFNULL(UN.GBN, ''), IFNULL(UN.RESNAM2, '') "
                           " FROM( "
                           "         SELECT IFNULL(A.ACDATE, '') AS ACDATE, IFNULL(A.ACIOGB, '') AS ACIOGB, IFNULL(B.RESNAM, '') AS RESNAM, IFNULL(A.ACAMTS, 0) AS OACAMTS, 0 AS IACAMTS "
                           "                , IFNULL(A.ACCUST, '') AS ACCUST, IFNULL(C.CUST_NME, '') AS CUST_NME "
                           "                , IFNULL(A.ACACNUMBER, '') AS ACACNUMBER, IFNULL(D.ACNUM_NAME, '') AS ACNUM_NAME, IFNULL(A.MCODE, '') AS MCODE, IFNULL(E.MCODENM, '') AS MCODENM"
                           "                , IFNULL(A.ACDESC, '') AS ACDESC, IFNULL(A.GBN, '') AS GBN, IFNULL(F.RESNAM, '') AS RESNAM2 "
                           "         FROM SISACCTT A "
                           "         LEFT OUTER JOIN OSREFCP B "
                           "         ON A.ACIOGB = B.RESKEY "
                           "         AND B.RECODE = 'OUA' "
                           "         LEFT OUTER JOIN MIS1TB003 C "
                           "         ON A.ACCUST = C.CUST_NBR "
                           "         LEFT OUTER JOIN ACNUMBER D "
                           "         ON A.ACACNUMBER = D.ACNUMBER "
                           "         LEFT OUTER JOIN OSCODEM E "
                           "         ON A.MCODE = E.MCODE "
                           "         LEFT OUTER JOIN OSREFCP F "
                           "         ON A.GBN = F.RESKEY "
                           "         AND F.RECODE = 'PGB' "
                           "         WHERE A.ACIOGB = '1' "
                           "         AND A.FIN_OPT = 'Y' "
                           "          AND A.ICUST = '" + str(iCust) + "'"
                           "         UNION ALL "
                           "         SELECT IFNULL(A.ACDATE, ''), IFNULL(A.ACIOGB, ''), IFNULL(B.RESNAM, ''), 0 AS OACAMTS, IFNULL(A.ACAMTS, 0) AS IACAMTS "
                           "                , IFNULL(A.ACCUST, ''), IFNULL(C.CUST_NME, ''), IFNULL(A.ACACNUMBER, ''), IFNULL(D.ACNUM_NAME, ''), IFNULL(A.MCODE, ''), IFNULL(E.MCODENM, '')"
                           "                , IFNULL(A.ACDESC, ''), IFNULL(A.GBN, ''), IFNULL(F.RESNAM, '')"
                           "         FROM SISACCTT A "
                           "         LEFT OUTER JOIN OSREFCP B "
                           "         ON A.ACIOGB = B.RESKEY "
                           "         AND B.RECODE = 'OUA' "
                           "         LEFT OUTER JOIN MIS1TB003 C "
                           "         ON A.ACCUST = C.CUST_NBR "
                           "         LEFT OUTER JOIN ACNUMBER D "
                           "         ON A.ACACNUMBER = D.ACNUMBER "
                           "         LEFT OUTER JOIN OSCODEM E "
                           "         ON A.MCODE = E.MCODE "
                           "         LEFT OUTER JOIN OSREFCP F "
                           "         ON A.GBN = F.RESKEY "
                           "         AND F.RECODE = 'PGB' "
                           "         WHERE A.ACIOGB = '2' "
                           "         AND A.FIN_OPT = 'Y' "
                           "          AND A.ICUST = '" + str(iCust) + "'"
                           "         ) UN "
                           " LEFT OUTER JOIN ACNUMBER CC "
                           " ON UN.ACACNUMBER = CC.ACNUMBER "
                           " WHERE UN.ACDATE BETWEEN '" + str(strDate) + "' AND '" + str(endDate) + "' AND CC.ACBKCD = '" + str(cboBank) + "'  ORDER BY UN.ACDATE ")

            mainresult = cursor.fetchall()

        with connection.cursor() as cursor:
            cursor.execute(" SELECT IFNULL(A.MCODE, ''), IFNULL(B.MCODENM, ''), IFNULL(SUM(A.ACAMTS), 0) FROM SISACCTT A "
                           " LEFT OUTER JOIN OSCODEM B "
                           " ON A.MCODE = B.MCODE "
                           " LEFT OUTER JOIN ACNUMBER C "
                           " ON A.ACACNUMBER = C.ACNUMBER "
                           " WHERE A.ACDATE BETWEEN '" + str(strDate) + "' AND '" + str(endDate) + "' AND A.FIN_OPT = 'Y' AND C.ACBKCD = '" + str(cboBank) + "' AND A.ICUST = '" + str(iCust) + "' "
                           " GROUP BY A.MCODE, B.MCODENM ")

            subresult = cursor.fetchall()

        return JsonResponse({'cboAccount': cboAresult, 'titleList': titleresult, 'totalList': totalresult, 'mainList': mainresult, 'subList': subresult})

    if cboAccount != '':

        with connection.cursor() as cursor:
            cursor.execute(" SELECT IFNULL(SUM(BAL), 0), IFNULL(SUM(INTOTAL), 0), IFNULL(SUM(OUTTOTAL), 0), IFNULL(SUM(BAL + INTOTAL - OUTTOTAL), 0) FROM "
                           "        (SELECT SUM(IFNULL(ACAMTS, 0)) AS BAL, 0 AS INTOTAL, 0 AS OUTTOTAL FROM ACBALANCE WHERE ACDATE < '" + str(strDate) + "' AND ICUST = '" + str(iCust) + "' AND ACNUMBER = '" + str(cboAccount) + "'"
                           " UNION ALL "
                           "        SELECT 0 AS BAL, SUM(IFNULL(ACAMTS, 0)) AS INTOTAL, 0 AS OUTTOTAL FROM SISACCTT "
                           "        WHERE ACIOGB = '2' AND FIN_OPT = 'Y' AND ICUST = '" + str(iCust) + "' AND ACDATE < '" + str(strDate) + "' AND ACACNUMBER = '" + str(cboAccount) + "' "
                           " UNION ALL "
                           "        SELECT 0 AS BAL, 0 AS INTOTAL, SUM(IFNULL(ACAMTS, 0)) AS OUTTOTAL FROM SISACCTT "
                           "        WHERE ACIOGB = '1' AND FIN_OPT = 'Y' AND ICUST = '" + str(iCust) + "' AND ACDATE < '" + str(strDate) + "' AND ACACNUMBER = '" + str(cboAccount) + "' "
                           " ) AA ")

            totalresult = cursor.fetchall()

        with connection.cursor() as cursor:
            cursor.execute(" SELECT IFNULL(UN.ACDATE, ''), IFNULL(UN.ACIOGB, ''), IFNULL(UN.RESNAM, ''), IFNULL(UN.OACAMTS, 0), IFNULL(UN.IACAMTS, 0) "
                           "      , IFNULL(UN.ACCUST, ''), IFNULL(UN.CUST_NME, ''), IFNULL(UN.ACACNUMBER, ''), IFNULL(UN.ACNUM_NAME, ''), IFNULL(UN.MCODE, ''), IFNULL(UN.MCODENM, '') "
                           "        , IFNULL(UN.ACDESC, ''), IFNULL(UN.GBN, ''), IFNULL(UN.RESNAM2, '') "
                           " FROM( "
                           "         SELECT IFNULL(A.ACDATE, '') AS ACDATE, IFNULL(A.ACIOGB, '') AS ACIOGB, IFNULL(B.RESNAM, '') AS RESNAM, IFNULL(A.ACAMTS, 0) AS OACAMTS, 0 AS IACAMTS "
                           "                , IFNULL(A.ACCUST, '') AS ACCUST, IFNULL(C.CUST_NME, '') AS CUST_NME "
                           "                , IFNULL(A.ACACNUMBER, '') AS ACACNUMBER, IFNULL(D.ACNUM_NAME, '') AS ACNUM_NAME, IFNULL(A.MCODE, '') AS MCODE, IFNULL(E.MCODENM, '') AS MCODENM "
                           "                , IFNULL(A.ACDESC, '') AS ACDESC, IFNULL(A.GBN, '') AS GBN, IFNULL(F.RESNAM, '') AS RESNAM2 "
                           "         FROM SISACCTT A "
                           "         LEFT OUTER JOIN OSREFCP B "
                           "         ON A.ACIOGB = B.RESKEY "
                           "         AND B.RECODE = 'OUA' "
                           "         LEFT OUTER JOIN MIS1TB003 C "
                           "         ON A.ACCUST = C.CUST_NBR "
                           "         LEFT OUTER JOIN ACNUMBER D "
                           "         ON A.ACACNUMBER = D.ACNUMBER "
                           "         LEFT OUTER JOIN OSCODEM E "
                           "         ON A.MCODE = E.MCODE "
                           "         LEFT OUTER JOIN OSREFCP F "
                           "         ON A.GBN = F.RESKEY "
                           "         AND F.RECODE = 'PGB' "
                           "         WHERE A.ACIOGB = '1' "
                           "         AND A.FIN_OPT = 'Y' "
                           "         AND A.ICUST = '" + str(iCust) + "' "
                           "         UNION ALL "
                           "         SELECT IFNULL(A.ACDATE, ''), IFNULL(A.ACIOGB, ''), IFNULL(B.RESNAM, ''), 0 AS OACAMTS, IFNULL(A.ACAMTS, 0) AS IACAMTS "
                           "                , IFNULL(A.ACCUST, ''), IFNULL(C.CUST_NME, ''), IFNULL(A.ACACNUMBER, ''), IFNULL(D.ACNUM_NAME, ''), IFNULL(A.MCODE, ''), IFNULL(E.MCODENM, '') "
                           "                , IFNULL(A.ACDESC, ''), IFNULL(A.GBN, ''), IFNULL(F.RESNAM, '') "
                           "         FROM SISACCTT A "
                           "         LEFT OUTER JOIN OSREFCP B "
                           "         ON A.ACIOGB = B.RESKEY "
                           "         AND B.RECODE = 'OUA' "
                           "         LEFT OUTER JOIN MIS1TB003 C "
                           "         ON A.ACCUST = C.CUST_NBR "
                           "         LEFT OUTER JOIN ACNUMBER D "
                           "         ON A.ACACNUMBER = D.ACNUMBER "
                           "         LEFT OUTER JOIN OSCODEM E "
                           "         ON A.MCODE = E.MCODE "
                           "         LEFT OUTER JOIN OSREFCP F "
                           "         ON A.GBN = F.RESKEY "
                           "         AND F.RECODE = 'PGB' "
                           "         WHERE A.ACIOGB = '2' "
                           "         AND A.FIN_OPT = 'Y' "
                           "         AND A.ICUST = '" + str(iCust) + "' "
                           "         ) UN "
                           " WHERE UN.ACDATE BETWEEN '" + str(strDate) + "' AND '" + str(endDate) + "' AND UN.ACACNUMBER = '" + str(cboAccount) + "'  ORDER BY UN.ACDATE ")

            mainresult = cursor.fetchall()

        with connection.cursor() as cursor:
            cursor.execute(" SELECT IFNULL(A.MCODE, ''), IFNULL(B.MCODENM, ''), IFNULL(SUM(A.ACAMTS), 0) FROM SISACCTT A "
                           " LEFT OUTER JOIN OSCODEM B "
                           " ON A.MCODE = B.MCODE "
                           " WHERE A.ACDATE BETWEEN '" + str(strDate) + "' AND '" + str(endDate) + "' AND A.FIN_OPT = 'Y' AND A.ACACNUMBER = '" + str(cboAccount) + "' AND A.ICUST = '" + str(iCust) + "' "
                           " GROUP BY A.MCODE, B.MCODENM ")

        subresult = cursor.fetchall()

        return JsonResponse({'totalList': totalresult, 'mainList': mainresult, 'subList': subresult})

    else:
        with connection.cursor() as cursor:
            cursor.execute(" SELECT A.ACBKCD, B.RESNAM FROM ACNUMBER A LEFT OUTER JOIN OSREFCP B ON A.ACBKCD = B.RESKEY AND B.RECODE = 'BNK' AND A.ICUST = '" + str(iCust) + "' GROUP BY A.ACBKCD, B.RESNAM ORDER BY A.ACBKCD  ")
            bankresult = cursor.fetchall()

        with connection.cursor() as cursor:
            cursor.execute(" SELECT ACNUMBER FROM ACNUMBER WHERE ICUST = '" + str(iCust) + "' ")
            cboAresult = cursor.fetchall()

        return JsonResponse({"cboBank": bankresult, 'cboAccount': cboAresult})




# 계정별 내역서
def receivepayCodeSheetViews(request):

    return render(request, "currentstate/receive-pay-codesheet.html")

def receivepayCodeSheetViews_search(request):
    strDate = request.POST.get('startDate').replace("-", "")
    endDate = request.POST.get('endDate').replace("-", "")
    creUser = request.session.get("userId")
    iCust = request.session.get("USER_ICUST")

    with connection.cursor() as cursor:
        cursor.execute(" SELECT IFNULL(A.MCODE_M, ''), IFNULL(D.RESNAM, ''), IFNULL(A.MCODE, ''), IFNULL(A.MCODENM, '')"
                       "        , IFNULL(A.ACODE, ''), IFNULL(C.RESNAM, ''), SUM(IFNULL(B.ACAMTS, 0)) "
                       " FROM OSCODEM A "
                       " LEFT OUTER JOIN SISACCTT B "
                       " ON B.MCODE = A.MCODE "
                       " LEFT OUTER JOIN OSREFCP C "
                       " ON A.ACODE = C.RESKEY "
                       " AND C.RECODE = 'ACD' "
                       " LEFT OUTER JOIN OSREFCP D "
                       " ON A.MCODE_M = D.RESKEY "
                       " AND D.RECODE = 'MCD' "
                       " WHERE A.ICUST = '" + str(iCust) + "' AND B.FIN_OPT = 'Y' AND B.ACDATE BETWEEN '" + str(strDate) + "' AND '" + str(endDate) + "' "
                       " GROUP BY A.MCODE_M, D.RESNAM, A.MCODE, A.MCODENM, A.ACODE , C.RESNAM")
        coderesult = cursor.fetchall()
        print(coderesult)

    with connection.cursor() as cursor:
        # cursor.execute(" SELECT IFNULL(A.ACBKCD, ''), IFNULL(B.RESNAM, '') FROM ACNUMBER A LEFT OUTER JOIN OSREFCP B ON A.ACBKCD = B.RESKEY AND B.RECODE = 'BNK' WHERE A.ICUST = '" + str(iCust) + "' ")
        cursor.execute(" SELECT IFNULL(A.ACBKCD, ''), IFNULL(B.RESNAM, '') FROM ACNUMBER A LEFT OUTER JOIN OSREFCP B ON A.ACBKCD = B.RESKEY AND B.RECODE = 'BNK' "
                       "        WHERE A.ICUST = '" + str(iCust) + "' GROUP BY A.ACBKCD, B.RESNAM ORDER BY A.ACBKCD ")
        headresult = cursor.fetchall()


    with connection.cursor() as cursor:
        cursor.execute(" SELECT IFNULL(SUM(BAL), 0), IFNULL(SUM(INTOTAL), 0), IFNULL(SUM(OUTTOTAL), 0), IFNULL(SUM(BAL + INTOTAL - OUTTOTAL), 0), AA.ACBKCD FROM "
                       " (SELECT SUM(IFNULL(A.ACAMTS, 0)) AS BAL, 0 AS INTOTAL, 0 AS OUTTOTAL, B.ACBKCD FROM ACBALANCE A "
                       "     LEFT OUTER JOIN ACNUMBER B ON A.ACNUMBER= B.ACNUMBER  WHERE A.ACDATE < '202401101' AND A.ICUST = '111' GROUP BY B.ACBKCD "
                       " UNION ALL "
                       "        SELECT 0 AS BAL, SUM(IFNULL(A.ACAMTS, 0)) AS INTOTAL, 0 AS OUTTOTAL, B.ACBKCD FROM SISACCTT A "
                       "        LEFT OUTER JOIN ACNUMBER B ON A.ACACNUMBER = B.ACNUMBER "
                       "        WHERE A.FIN_OPT = 'Y' AND A.ICUST = '111' AND A.ACDATE < '202401101' AND A.MCODE LIKE '53%' OR A.MCODE LIKE '55%' GROUP BY B.ACBKCD "
                       " UNION ALL "
                       "        SELECT 0 AS BAL, 0 AS INTOTAL, SUM(IFNULL(A.ACAMTS, 0)) AS OUTTOTAL, B.ACBKCD FROM SISACCTT A "
                       "        LEFT OUTER JOIN ACNUMBER B ON A.ACACNUMBER = B.ACNUMBER "
                       "        WHERE A.FIN_OPT = 'Y' AND A.ICUST = '111' AND A.ACDATE < '202401101' AND A.MCODE LIKE '43%' GROUP BY B.ACBKCD "
                       " ) AA GROUP BY AA.ACBKCD ")
        mainresult = cursor.fetchall()

    with connection.cursor() as cursor:
        cursor.execute(" SELECT MCODE FROM OSCODEM WHERE ICUST = '" + str(iCust) + "' ORDER BY MCODE ")
        headresult2 = cursor.fetchall()
        itembomlist2 = []

        itembomlist4 = []
        for i in range(len(headresult2)):
            itembomlist = [headresult2[i][0]]
            itembomlist2 += [itembomlist]

        # 관리계정코드, 관리계정명, 금액, 은행코드, 은행명
        for j in range(len(itembomlist2)):
            with connection.cursor() as cursor:
                cursor.execute(" SELECT IFNULL(A.MCODE, ''), IFNULL(B.MCODENM, ''), SUM(A.ACAMTS), IFNULL(C.ACBKCD, ''), IFNULL(D.RESNAM, ''), IFNULL(B.MCODE_M, '')"
                               "        , IFNULL(B.ACODE, ''), IFNULL(E.RESNAM, ''), IFNULL(F.RESNAM, '')  "
                               " FROM SISACCTT A "
                               " LEFT OUTER JOIN ACNUMBER C "
                               " ON A.ACACNUMBER = C.ACNUMBER "
                               " LEFT OUTER JOIN OSCODEM B "
                               " ON A.MCODE = B.MCODE "
                               " LEFT OUTER JOIN OSREFCP D "
                               " ON C.ACBKCD = D.RESKEY "
                               " AND D.RECODE = 'BNK' "
                               " LEFT OUTER JOIN OSREFCP E "
                               " ON B.ACODE = E.RESKEY "
                               " AND E.RECODE = 'ACD' "
                               " LEFT OUTER JOIN OSREFCP F "
                               " ON B.MCODE_M = F.RESKEY "
                               " AND F.RECODE = 'MCD' "
                               " WHERE A.FIN_OPT = 'Y' AND A.MCODE = '" + str(itembomlist2[j][0]) + "' AND A.ICUST = '" + str(iCust) + "' AND A.ACDATE BETWEEN '" + str(strDate) + "' AND '" + str(endDate) + "' "
                               " GROUP BY A.MCODE, B.MCODENM, C.ACBKCD, D.RESNAM, B.MCODE_M, F.RESNAM, B.ACODE, E.RESNAM ORDER BY ACBKCD ")
                subresult = cursor.fetchall()

                for data in range(len(subresult)):
                    itembomlist3 = [subresult[data][0], subresult[data][1], subresult[data][2], subresult[data][3], subresult[data][4], subresult[data][5]]
                    itembomlist4 += [itembomlist3]

                    print(itembomlist4)


    itembomlist2 = sum(itembomlist2, [])
    if itembomlist2:
        if int(max(itembomlist2)) < 10:
            for i in range(10 - int(max(itembomlist2))):
                itembomlist2 += ['']

        with connection.cursor() as cursor:
            cursor.execute(
                " SELECT IFNULL(A.MCODE_M, ''), IFNULL(A.MCODE, ''), IFNULL(A.MCODENM, ''), IFNULL(A.ACODE, ''), SUM(IFNULL(B.ACAMTS, 0)) "
                " FROM OSCODEM A "
                " LEFT OUTER JOIN SISACCTT B "
                " ON B.MCODE = A.MCODE "
                " LEFT OUTER JOIN OSREFCP C "
                " ON A.ACODE = C.RESKEY "
                " AND C.RECODE = 'ACD' "
                " LEFT OUTER JOIN OSREFCP D "
                " ON A.MCODE_M = D.RESKEY "
                " AND D.RECODE = 'MCD' "
                " WHERE B.FIN_OPT = 'Y' AND A.ICUST = '" + str(iCust) + "'"
                " GROUP BY A.MCODE_M, A.MCODE, A.MCODENM, A.ACODE ")
            tbresult = cursor.fetchall()

        return JsonResponse({"headList": headresult, 'mainList': mainresult, 'tbList': tbresult, "codeList": coderesult, "itembomlist4": itembomlist4})



    # with connection.cursor() as cursor:
    #     cursor.execute(" SELECT SUM(ACAMTS) FROM SISACCTT WHERE MCODE LIKE '4%' AND ACDATE BETWEEN '" + strDate + "' AND '" + endDate + "' AND ICUST = '" + str(iCust) + "' ")
    #     inTotalresult = cursor.fetchall()
    #     inTotal = inTotalresult[0][0]
    #
    #
    # with connection.cursor() as cursor:
    #     cursor.execute(" SELECT SUM(ACAMTS) FROM SISACCTT WHERE MCODE LIKE '5%' AND ACDATE BETWEEN '" + strDate + "' AND '" + endDate + "' AND ICUST = '" + str(iCust) + "' ")
    #     outTotalresult = cursor.fetchall()
    #     outTotal = outTotalresult[0][0]

    # cursor.execute(" SELECT SUM(1ACMTS), SUM(2ACMTS), SUM(3ACMTS) "
    #                "    , SUM(4ACMTS), SUM(5ACMTS), SUM(6ACMTS), SUM(7ACMTS) "
    #                "    , SUM(8ACMTS), SUM(9ACMTS), SUM(10ACMTS), MCODE, MCODENM "
    #                "    , SUM(1ACMTS + 2ACMTS + 3ACMTS + 4ACMTS + 5ACMTS + 6ACMTS + 7ACMTS + 8ACMTS +  9ACMTS + 10ACMTS) FROM ( "
    #                "    SELECT MCODE, MCODENM, 1ACMTS, 2ACMTS, 3ACMTS, 4ACMTS, 5ACMTS, 6ACMTS, 7ACMTS, 8ACMTS, 9ACMTS, 10ACMTS "
    #                "     FROM( "
    #                "         SELECT A.MCODE, C.MCODENM, B.ACBKCD, SUM(A.ACAMTS) AS 1ACMTS, 0 AS 2ACMTS, 0 AS 3ACMTS, 0 AS 4ACMTS, 0 AS 5ACMTS, 0 AS 6ACMTS, 0 AS 7ACMTS, 0 AS 8ACMTS, 0 AS 9ACMTS, 0 AS 10ACMTS "
    #                "         FROM SISACCTT A "
    #                "         LEFT OUTER JOIN ACNUMBER B "
    #                "         ON A.ACACNUMBER = B.ACNUMBER "
    #                "         LEFT OUTER JOIN OSCODEM C "
    #                "         ON A.MCODE = C.MCODE "
    #                "         WHERE B.ACBKCD = '" + itembomlist2[0] + "' AND A.ACDATE BETWEEN '" + strDate + "' AND '" + endDate + "' AND A.ICUST = '" + str(iCust) + "'"
    #                "         GROUP BY A.MCODE, C.MCODENM, B.ACBKCD "
    #                "         UNION ALL "
    #                "         SELECT A.MCODE, C.MCODENM, B.ACBKCD, 0 AS 1ACMTS, SUM(A.ACAMTS) AS 2ACAMTS,  0 AS 3ACMTS, 0 AS 4ACMTS, 0 AS 5ACMTS, 0 AS 6ACMTS, 0 AS 7ACMTS, 0 AS 8ACMTS, 0 AS 9ACMTS, 0 AS 10ACMTS "
    #                "         FROM SISACCTT A "
    #                "         LEFT OUTER JOIN ACNUMBER B "
    #                "         ON A.ACACNUMBER = B.ACNUMBER "
    #                "         LEFT OUTER JOIN OSCODEM C "
    #                "         ON A.MCODE = C.MCODE "
    #                "         WHERE B.ACBKCD = '" + itembomlist2[1] + "' AND A.ACDATE BETWEEN '" + strDate + "' AND '" + endDate + "' AND A.ICUST = '" + str(iCust) + "'"
    #                "         GROUP BY A.MCODE, C.MCODENM, B.ACBKCD "
    #                "         UNION ALL "
    #                "         SELECT A.MCODE, C.MCODENM, B.ACBKCD, 0 AS 1ACMTS, 0 AS 2ACAMTS, SUM(A.ACAMTS) AS 3ACMTS, 0 AS 4ACMTS, 0 AS 5ACMTS, 0 AS 6ACMTS, 0 AS 7ACMTS, 0 AS 8ACMTS, 0 AS 9ACMTS, 0 AS 10ACMTS "
    #                "         FROM SISACCTT A "
    #                "         LEFT OUTER JOIN ACNUMBER B "
    #                "         ON A.ACACNUMBER = B.ACNUMBER "
    #                "         LEFT OUTER JOIN OSCODEM C "
    #                "         ON A.MCODE = C.MCODE "
    #                "         WHERE B.ACBKCD = '" + itembomlist2[2] + "'  AND A.ACDATE BETWEEN '" + strDate + "' AND '" + endDate + "' AND A.ICUST = '" + str(iCust) + "'"
    #                "         GROUP BY A.MCODE, C.MCODENM, B.ACBKCD "
    #                "         UNION ALL "
    #                "         SELECT A.MCODE, C.MCODENM, B.ACBKCD, 0 AS 1ACMTS, 0 AS 2ACAMTS, 0 AS 3ACMTS, SUM(A.ACAMTS) AS 4ACMTS, 0 AS 5ACMTS, 0 AS 6ACMTS, 0 AS 7ACMTS, 0 AS 8ACMTS, 0 AS 9ACMTS, 0 AS 10ACMTS "
    #                "         FROM SISACCTT A "
    #                "         LEFT OUTER JOIN ACNUMBER B "
    #                "         ON A.ACACNUMBER = B.ACNUMBER "
    #                "         LEFT OUTER JOIN OSCODEM C "
    #                "         ON A.MCODE = C.MCODE "
    #                "         WHERE B.ACBKCD = '" + itembomlist2[3] + "'  AND A.ACDATE BETWEEN '" + strDate + "' AND '" + endDate + "' AND A.ICUST = '" + str(iCust) + "'"
    #                "         GROUP BY A.MCODE, C.MCODENM, B.ACBKCD "
    #                "         UNION ALL "
    #                "         SELECT A.MCODE, C.MCODENM, B.ACBKCD, 0 AS 1ACMTS,0 AS 2ACAMTS, 0 AS 3ACMTS, 0 AS 4ACMTS, SUM(A.ACAMTS) AS 5ACMTS, 0 AS 6ACMTS, 0 AS 7ACMTS, 0 AS 8ACMTS, 0 AS 9ACMTS, 0 AS 10ACMTS "
    #                "         FROM SISACCTT A "
    #                "         LEFT OUTER JOIN ACNUMBER B "
    #                "         ON A.ACACNUMBER = B.ACNUMBER "
    #                "         LEFT OUTER JOIN OSCODEM C "
    #                "         ON A.MCODE = C.MCODE "
    #                "         WHERE B.ACBKCD = '" + itembomlist2[4] + "'  AND A.ACDATE BETWEEN '" + strDate + "' AND '" + endDate + "' AND A.ICUST = '" + str(iCust) + "'"
    #                "         GROUP BY A.MCODE, C.MCODENM, B.ACBKCD "
    #                "         UNION ALL "
    #                "         SELECT A.MCODE, C.MCODENM, B.ACBKCD, 0 AS 1ACMTS, 0 AS 2ACAMTS,0 AS 3ACMTS, 0 AS 4ACMTS, 0 AS 5ACMTS, SUM(A.ACAMTS) AS 6ACMTS, 0 AS 7ACMTS, 0 AS 8ACMTS, 0 AS 9ACMTS, 0 AS 10ACMTS "
    #                "         FROM SISACCTT A "
    #                "         LEFT OUTER JOIN ACNUMBER B "
    #                "         ON A.ACACNUMBER = B.ACNUMBER "
    #                "         LEFT OUTER JOIN OSCODEM C "
    #                "         ON A.MCODE = C.MCODE "
    #                "         WHERE B.ACBKCD = '" + itembomlist2[5] + "'  AND A.ACDATE BETWEEN '" + strDate + "' AND '" + endDate + "' AND A.ICUST = '" + str(iCust) + "'"
    #                "         GROUP BY A.MCODE, C.MCODENM, B.ACBKCD "
    #                "         UNION ALL "
    #                "         SELECT A.MCODE, C.MCODENM, B.ACBKCD, 0 AS 1ACMTS, 0 AS 2ACAMTS,0 AS 3ACMTS, 0 AS 4ACMTS, 0 AS 5ACMTS, 0 AS 6ACMTS, SUM(A.ACAMTS) AS 7ACMTS, 0 AS 8ACMTS, 0 AS 9ACMTS, 0 AS 10ACMTS "
    #                "         FROM SISACCTT A "
    #                "         LEFT OUTER JOIN ACNUMBER B "
    #                "         ON A.ACACNUMBER = B.ACNUMBER "
    #                "         LEFT OUTER JOIN OSCODEM C "
    #                "         ON A.MCODE = C.MCODE "
    #                "         WHERE B.ACBKCD = '" + itembomlist2[6] + "'  AND A.ACDATE BETWEEN '" + strDate + "' AND '" + endDate + "' AND A.ICUST = '" + str(iCust) + "'"
    #                "         GROUP BY A.MCODE, C.MCODENM, B.ACBKCD "
    #                "         UNION ALL "
    #                "         SELECT A.MCODE, C.MCODENM, B.ACBKCD, 0 AS 1ACMTS, 0 AS 2ACAMTS, 0 AS 3ACMTS, 0 AS 4ACMTS, 0 AS 5ACMTS, 0 AS 6ACMTS, 0 AS 7ACMTS, SUM(A.ACAMTS) AS 8ACMTS, 0 AS 9ACMTS, 0 AS 10ACMTS "
    #                "         FROM SISACCTT A "
    #                "         LEFT OUTER JOIN ACNUMBER B "
    #                "         ON A.ACACNUMBER = B.ACNUMBER "
    #                "         LEFT OUTER JOIN OSCODEM C "
    #                "         ON A.MCODE = C.MCODE "
    #                "         WHERE B.ACBKCD = '" + itembomlist2[7] + "'  AND A.ACDATE BETWEEN '" + strDate + "' AND '" + endDate + "' AND A.ICUST = '" + str(iCust) + "'"
    #                "         GROUP BY A.MCODE, C.MCODENM, B.ACBKCD "
    #                "         UNION ALL "
    #                "         SELECT A.MCODE, C.MCODENM, B.ACBKCD, 0 AS 1ACMTS, 0 AS 2ACAMTS, 0 AS 3ACMTS, 0 AS 4ACMTS, 0 AS 5ACMTS, 0 AS 6ACMTS, 0 AS 7ACMTS, 0 AS 8ACMTS, SUM(A.ACAMTS) AS 9ACMTS, 0 AS 10ACMTS "
    #                "         FROM SISACCTT A "
    #                "         LEFT OUTER JOIN ACNUMBER B "
    #                "         ON A.ACACNUMBER = B.ACNUMBER "
    #                "         LEFT OUTER JOIN OSCODEM C "
    #                "         ON A.MCODE = C.MCODE "
    #                "         WHERE B.ACBKCD = '" + itembomlist2[8] + "'  AND A.ACDATE BETWEEN '" + strDate + "' AND '" + endDate + "' AND A.ICUST = '" + str(iCust) + "'"
    #                "         GROUP BY A.MCODE, C.MCODENM, B.ACBKCD "
    #                "         UNION ALL "
    #                "         SELECT A.MCODE, C.MCODENM, B.ACBKCD, 0 AS 1ACMTS, 0 AS 2ACAMTS, 0 AS 3ACMTS, 0 AS 4ACMTS, 0 AS 5ACMTS, 0 AS 6ACMTS, 0 AS 7ACMTS, 0 AS 8ACMTS, 0 AS 9ACMTS, SUM(A.ACAMTS) AS 10ACMTS "
    #                "         FROM SISACCTT A "
    #                "         LEFT OUTER JOIN ACNUMBER B "
    #                "         ON A.ACACNUMBER = B.ACNUMBER "
    #                "         LEFT OUTER JOIN OSCODEM C "
    #                "         ON A.MCODE = C.MCODE "
    #                "         WHERE B.ACBKCD = '" + itembomlist2[9] + "'  AND A.ACDATE BETWEEN '" + strDate + "' AND '" + endDate + "' AND A.ICUST = '" + str(iCust) + "'"
    #                "         GROUP BY A.MCODE, C.MCODENM, B.ACBKCD "
    #                "         ) TMP GROUP BY MCODE, MCODENM, 1ACMTS, 2ACMTS, 3ACMTS, 4ACMTS, 5ACMTS, 6ACMTS, 7ACMTS, 8ACMTS, 9ACMTS, 10ACMTS "
    #                "     ) BB "
    #                " GROUP BY MCODE, MCODENM ")

    # cursor.execute(
    #     " SELECT IFNULL(A.ACODE, ''), IFNULL(B.RESNAM, ''), SUM(A.ACAMTS), IFNULL(C.ACBKCD, ''), IFNULL(D.RESNAM, '') "
    #     " FROM SISACCTT A "
    #     " LEFT OUTER JOIN ACNUMBER C "
    #     " ON A.ACACNUMBER = C.ACNUMBER "
    #     " LEFT OUTER JOIN OSREFCP B "
    #     " ON A.ACODE = B.RESKEY "
    #     " AND B.RECODE = 'ACD' "
    #     " LEFT OUTER JOIN OSREFCP D "
    #     " ON C.ACBKCD = D.RESKEY "
    #     " AND D.RECODE = 'BNK' "
    #     " WHERE A.MCODE = '" + str(itembomlist2[j][0]) + "' AND A.ICUST = '" + str(iCust) + "'"
    #                                                                                         " GROUP BY A.ACODE, B.RESNAM, C.ACBKCD ORDER BY ACBKCD ")