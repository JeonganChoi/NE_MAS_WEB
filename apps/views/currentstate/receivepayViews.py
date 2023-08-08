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

    return render(request, "currentstate/receive-pay-banksheet.html")


def receivepaySheetViews_search(request):
    cboBank = request.POST.get('cboBank')
    cboAccount = request.POST.get('cboAccount')
    strDate = request.POST.get('startDate')
    endDate = request.POST.get('endDate')

    if cboBank != '':
        with connection.cursor() as cursor:
            cursor.execute(" SELECT ACNUMBER FROM ACNUMBER WHERE ACBKCD = '" + str(cboBank) + "' ")

            cboAresult = cursor.fetchall()

        with connection.cursor() as cursor:
            cursor.execute(" SELECT MCODE, MCODENM FROM OSCODEM ")

            titleresult = cursor.fetchall()

        with connection.cursor() as cursor:
            cursor.execute(" SELECT IFNULL((BALANCE - OAMTS) + IAMTS, 0) AS TOTAL FROM( "
                           "         SELECT "
                           "          IFNULL(SUM(A.ACAMTS), 0) AS BALANCE "
                           "         ,(SELECT IFNULL(SUM(A.ACAMTS), 0) AS OAMTS FROM SISACCTT A LEFT OUTER JOIN ACNUMBER B ON A.ACACNUMBER = B.ACNUMBER WHERE A.ACIOGB = '1' AND A.ACDATE < '" + strDate + "' AND B.ACBKCD = '" + str(cboBank) + "') AS OAMTS "
                           "         ,(SELECT IFNULL(SUM(A.ACAMTS), 0) AS IAMTS FROM SISACCTT A LEFT OUTER JOIN ACNUMBER B ON A.ACACNUMBER = B.ACNUMBER WHERE A.ACIOGB = '2' AND A.ACDATE < '" + strDate + "' AND B.ACBKCD = '" + str(cboBank) + "') AS IAMTS "
                           "          FROM ACBALANCE A "
                           "          LEFT OUTER JOIN ACNUMBER B ON A.ACNUMBER = B.ACNUMBER "
                           "          WHERE A.ACDATE < '" + strDate + "' AND B.ACBKCD = '" + str(cboBank) + "' "
                           " ) A ")

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
                           "         ) UN "
                           " LEFT OUTER JOIN ACNUMBER CC "
                           " ON UN.ACACNUMBER = CC.ACNUMBER "
                           " WHERE UN.ACDATE BETWEEN '" + strDate + "' AND '" + endDate + "' AND CC.ACBKCD = '" + str(cboBank) + "'  ORDER BY UN.ACDATE ")

            mainresult = cursor.fetchall()

        with connection.cursor() as cursor:
            cursor.execute(" SELECT A.MCODE, B.MCODENM, SUM(A.ACAMTS) FROM SISACCTT A "
                           " LEFT OUTER JOIN OSCODEM B "
                           " ON A.MCODE = B.MCODE "
                           " LEFT OUTER JOIN ACNUMBER C "
                           " ON A.ACACNUMBER = C.ACNUMBER "
                           " WHERE A.ACDATE BETWEEN '" + strDate + "' AND '" + endDate + "' AND C.ACBKCD = '" + str(cboBank) + "' "
                           " GROUP BY A.MCODE, B.MCODENM ")

            subresult = cursor.fetchall()

        return JsonResponse({'cboAccount': cboAresult, 'titleList': titleresult, 'totalList': totalresult, 'mainList': mainresult, 'subList': subresult})

    if cboAccount != '':

        with connection.cursor() as cursor:
            cursor.execute(" SELECT IFNULL((BALANCE - OAMTS) + IAMTS, 0) AS TOTAL FROM( "
                           "         SELECT "
                           "          IFNULL(SUM(ACAMTS), 0) AS BALANCE "
                           "         ,(SELECT IFNULL(SUM(ACAMTS), 0) AS OAMTS FROM SISACCTT WHERE ACIOGB = '1' AND ACDATE < '" + strDate + "' AND ACACNUMBER = '" + str(cboAccount) + "') AS OAMTS "
                           "         ,(SELECT IFNULL(SUM(ACAMTS), 0) AS IAMTS FROM SISACCTT WHERE ACIOGB = '2' AND ACDATE < '" + strDate + "' AND ACACNUMBER = '" + str(cboAccount) + "') AS IAMTS "
                           "          FROM ACBALANCE"
                           "          WHERE ACDATE < '" + strDate + "' AND ACNUMBER = '" + str(cboAccount) + "' "
                           " ) A ")

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
                           "         ) UN "
                           " WHERE UN.ACDATE BETWEEN '" + strDate + "' AND '" + endDate + "' AND UN.ACACNUMBER = '" + str(cboAccount) + "'  ORDER BY UN.ACDATE ")

            mainresult = cursor.fetchall()

        with connection.cursor() as cursor:
            cursor.execute(" SELECT A.MCODE, B.MCODENM, SUM(A.ACAMTS) FROM SISACCTT A "
                           " LEFT OUTER JOIN OSCODEM B "
                           " ON A.MCODE = B.MCODE "
                           " WHERE A.ACDATE BETWEEN '" + strDate + "' AND '" + endDate + "' AND A.ACACNUMBER = '" + str(cboAccount) + "' "
                           " GROUP BY A.MCODE, B.MCODENM ")

        subresult = cursor.fetchall()

        return JsonResponse({'totalList': totalresult, 'mainList': mainresult, 'subList': subresult})

    else:
        with connection.cursor() as cursor:
            cursor.execute(" SELECT RESKEY, RESNAM FROM OSREFCP WHERE RECODE = 'BNK' ")
            bankresult = cursor.fetchall()
            bank = bankresult[0][0]

            cursor.execute(" SELECT ACNUMBER FROM ACNUMBER WHERE ACBKCD = '" + bank + "' ")

            cboAresult = cursor.fetchall()

        return JsonResponse({"cboBank": bankresult, 'cboAccount': cboAresult})




# 계정별 내역서
def receivepayCodeSheetViews(request):

    return render(request, "currentstate/receive-pay-codesheet.html")

def receivepayCodeSheetViews_search(request):
    strDate = request.POST.get('startDate')
    endDate = request.POST.get('endDate')

    with connection.cursor() as cursor:
        cursor.execute(" SELECT ACNUM_NAME, ACBKCD FROM ACNUMBER ORDER BY ACNUMBER ")
        headresult = cursor.fetchall()
        itembomlist2 = []

        for i in range(len(headresult)):
            itembomlist = [headresult[i][1]]
            itembomlist2 += [itembomlist]

    with connection.cursor() as cursor:
        cursor.execute(" SELECT IFNULL((BALANCE - OAMTS) + IAMTS, 0) AS TOTAL, BANK FROM( "
                       "         SELECT "
                       "          IFNULL(SUM(A.ACAMTS), 0) AS BALANCE "
                       "         ,IFNULL(B.ACNUM_NAME, '') AS BANK "
                       "         ,(SELECT IFNULL(SUM(A.ACAMTS), 0) AS OAMTS FROM SISACCTT A LEFT OUTER JOIN ACNUMBER B ON A.ACACNUMBER = B.ACNUMBER WHERE A.ACIOGB = '1' AND A.ACDATE < '" + strDate + "') AS OAMTS "
                       "         ,(SELECT IFNULL(SUM(A.ACAMTS), 0) AS IAMTS FROM SISACCTT A LEFT OUTER JOIN ACNUMBER B ON A.ACACNUMBER = B.ACNUMBER WHERE A.ACIOGB = '2' AND A.ACDATE < '" + strDate + "') AS IAMTS "
                       "          FROM ACBALANCE A "
                       "          LEFT OUTER JOIN ACNUMBER B "
                       "          ON A.ACNUMBER = B.ACNUMBER "
                       "          WHERE A.ACDATE < '" + strDate + "' "
                       "          GROUP BY BANK "
                       " ) A ")

        mainresult = cursor.fetchall()

    with connection.cursor() as cursor:
        cursor.execute(" SELECT MCODE FROM SISACCTT GROUP BY MCODE ")
        coderesult = cursor.fetchall()

    itembomlist2 = sum(itembomlist2, [])
    if itembomlist2:
        if int(max(itembomlist2)) < 10:
            for i in range(10 - int(max(itembomlist2))):
                itembomlist2 += ['']
            print(itembomlist2)
        with connection.cursor() as cursor:
            cursor.execute(" SELECT SUM(1ACMTS), SUM(2ACMTS), SUM(3ACMTS) "
                           "    , SUM(4ACMTS), SUM(5ACMTS), SUM(6ACMTS), SUM(7ACMTS) "
                           "    , SUM(8ACMTS), SUM(9ACMTS), SUM(10ACMTS), MCODE, MCODENM "
                           "    , SUM(1ACMTS + 2ACMTS + 3ACMTS + 4ACMTS + 5ACMTS + 6ACMTS + 7ACMTS + 8ACMTS +  9ACMTS + 10ACMTS) FROM ( "
                           "    SELECT MCODE, MCODENM, 1ACMTS, 2ACMTS, 3ACMTS, 4ACMTS, 5ACMTS, 6ACMTS, 7ACMTS, 8ACMTS, 9ACMTS, 10ACMTS "
                           "     FROM( "
                           "         SELECT A.MCODE, C.MCODENM, B.ACBKCD, SUM(A.ACAMTS) AS 1ACMTS, 0 AS 2ACMTS, 0 AS 3ACMTS, 0 AS 4ACMTS, 0 AS 5ACMTS, 0 AS 6ACMTS, 0 AS 7ACMTS, 0 AS 8ACMTS, 0 AS 9ACMTS, 0 AS 10ACMTS "
                           "         FROM SISACCTT A "
                           "         LEFT OUTER JOIN ACNUMBER B "
                           "         ON A.ACACNUMBER = B.ACNUMBER "
                           "         LEFT OUTER JOIN OSCODEM C "
                           "         ON A.MCODE = C.MCODE "
                           "         WHERE B.ACBKCD = '" + itembomlist2[0] + "' AND A.ACDATE BETWEEN '" + strDate + "' AND '" + endDate + "' "
                           "         GROUP BY A.MCODE, C.MCODENM, B.ACBKCD "
                           "         UNION ALL "
                           "         SELECT A.MCODE, C.MCODENM, B.ACBKCD, 0 AS 1ACMTS, SUM(A.ACAMTS) AS 2ACAMTS,  0 AS 3ACMTS, 0 AS 4ACMTS, 0 AS 5ACMTS, 0 AS 6ACMTS, 0 AS 7ACMTS, 0 AS 8ACMTS, 0 AS 9ACMTS, 0 AS 10ACMTS "
                           "         FROM SISACCTT A "
                           "         LEFT OUTER JOIN ACNUMBER B "
                           "         ON A.ACACNUMBER = B.ACNUMBER "
                           "         LEFT OUTER JOIN OSCODEM C "
                           "         ON A.MCODE = C.MCODE "
                           "         WHERE B.ACBKCD = '" + itembomlist2[1] + "' AND A.ACDATE BETWEEN '" + strDate + "' AND '" + endDate + "' "
                           "         GROUP BY A.MCODE, C.MCODENM, B.ACBKCD "
                           "         UNION ALL "
                           "         SELECT A.MCODE, C.MCODENM, B.ACBKCD, 0 AS 1ACMTS, 0 AS 2ACAMTS, SUM(A.ACAMTS) AS 3ACMTS, 0 AS 4ACMTS, 0 AS 5ACMTS, 0 AS 6ACMTS, 0 AS 7ACMTS, 0 AS 8ACMTS, 0 AS 9ACMTS, 0 AS 10ACMTS "
                           "         FROM SISACCTT A "
                           "         LEFT OUTER JOIN ACNUMBER B "
                           "         ON A.ACACNUMBER = B.ACNUMBER "
                           "         LEFT OUTER JOIN OSCODEM C "
                           "         ON A.MCODE = C.MCODE "
                           "         WHERE B.ACBKCD = '" + itembomlist2[2] + "'  AND A.ACDATE BETWEEN '" + strDate + "' AND '" + endDate + "' "
                           "         GROUP BY A.MCODE, C.MCODENM, B.ACBKCD "
                           "         UNION ALL "
                           "         SELECT A.MCODE, C.MCODENM, B.ACBKCD, 0 AS 1ACMTS, 0 AS 2ACAMTS, 0 AS 3ACMTS, SUM(A.ACAMTS) AS 4ACMTS, 0 AS 5ACMTS, 0 AS 6ACMTS, 0 AS 7ACMTS, 0 AS 8ACMTS, 0 AS 9ACMTS, 0 AS 10ACMTS "
                           "         FROM SISACCTT A "
                           "         LEFT OUTER JOIN ACNUMBER B "
                           "         ON A.ACACNUMBER = B.ACNUMBER "
                           "         LEFT OUTER JOIN OSCODEM C "
                           "         ON A.MCODE = C.MCODE "
                           "         WHERE B.ACBKCD = '" + itembomlist2[3] + "'  AND A.ACDATE BETWEEN '" + strDate + "' AND '" + endDate + "' "
                           "         GROUP BY A.MCODE, C.MCODENM, B.ACBKCD "
                           "         UNION ALL "
                           "         SELECT A.MCODE, C.MCODENM, B.ACBKCD, 0 AS 1ACMTS,0 AS 2ACAMTS, 0 AS 3ACMTS, 0 AS 4ACMTS, SUM(A.ACAMTS) AS 5ACMTS, 0 AS 6ACMTS, 0 AS 7ACMTS, 0 AS 8ACMTS, 0 AS 9ACMTS, 0 AS 10ACMTS "
                           "         FROM SISACCTT A "
                           "         LEFT OUTER JOIN ACNUMBER B "
                           "         ON A.ACACNUMBER = B.ACNUMBER "
                           "         LEFT OUTER JOIN OSCODEM C "
                           "         ON A.MCODE = C.MCODE "
                           "         WHERE B.ACBKCD = '" + itembomlist2[4] + "'  AND A.ACDATE BETWEEN '" + strDate + "' AND '" + endDate + "' "
                           "         GROUP BY A.MCODE, C.MCODENM, B.ACBKCD "
                           "         UNION ALL "
                           "         SELECT A.MCODE, C.MCODENM, B.ACBKCD, 0 AS 1ACMTS, 0 AS 2ACAMTS,0 AS 3ACMTS, 0 AS 4ACMTS, 0 AS 5ACMTS, SUM(A.ACAMTS) AS 6ACMTS, 0 AS 7ACMTS, 0 AS 8ACMTS, 0 AS 9ACMTS, 0 AS 10ACMTS "
                           "         FROM SISACCTT A "
                           "         LEFT OUTER JOIN ACNUMBER B "
                           "         ON A.ACACNUMBER = B.ACNUMBER "
                           "         LEFT OUTER JOIN OSCODEM C "
                           "         ON A.MCODE = C.MCODE "
                           "         WHERE B.ACBKCD = '" + itembomlist2[5] + "'  AND A.ACDATE BETWEEN '" + strDate + "' AND '" + endDate + "' "
                           "         GROUP BY A.MCODE, C.MCODENM, B.ACBKCD "
                           "         UNION ALL "
                           "         SELECT A.MCODE, C.MCODENM, B.ACBKCD, 0 AS 1ACMTS, 0 AS 2ACAMTS,0 AS 3ACMTS, 0 AS 4ACMTS, 0 AS 5ACMTS, 0 AS 6ACMTS, SUM(A.ACAMTS) AS 7ACMTS, 0 AS 8ACMTS, 0 AS 9ACMTS, 0 AS 10ACMTS "
                           "         FROM SISACCTT A "
                           "         LEFT OUTER JOIN ACNUMBER B "
                           "         ON A.ACACNUMBER = B.ACNUMBER "
                           "         LEFT OUTER JOIN OSCODEM C "
                           "         ON A.MCODE = C.MCODE "
                           "         WHERE B.ACBKCD = '" + itembomlist2[6] + "'  AND A.ACDATE BETWEEN '" + strDate + "' AND '" + endDate + "' "
                           "         GROUP BY A.MCODE, C.MCODENM, B.ACBKCD "
                           "         UNION ALL "
                           "         SELECT A.MCODE, C.MCODENM, B.ACBKCD, 0 AS 1ACMTS, 0 AS 2ACAMTS, 0 AS 3ACMTS, 0 AS 4ACMTS, 0 AS 5ACMTS, 0 AS 6ACMTS, 0 AS 7ACMTS, SUM(A.ACAMTS) AS 8ACMTS, 0 AS 9ACMTS, 0 AS 10ACMTS "
                           "         FROM SISACCTT A "
                           "         LEFT OUTER JOIN ACNUMBER B "
                           "         ON A.ACACNUMBER = B.ACNUMBER "
                           "         LEFT OUTER JOIN OSCODEM C "
                           "         ON A.MCODE = C.MCODE "
                           "         WHERE B.ACBKCD = '" + itembomlist2[7] + "'  AND A.ACDATE BETWEEN '" + strDate + "' AND '" + endDate + "' "
                           "         GROUP BY A.MCODE, C.MCODENM, B.ACBKCD "
                           "         UNION ALL "
                           "         SELECT A.MCODE, C.MCODENM, B.ACBKCD, 0 AS 1ACMTS, 0 AS 2ACAMTS, 0 AS 3ACMTS, 0 AS 4ACMTS, 0 AS 5ACMTS, 0 AS 6ACMTS, 0 AS 7ACMTS, 0 AS 8ACMTS, SUM(A.ACAMTS) AS 9ACMTS, 0 AS 10ACMTS "
                           "         FROM SISACCTT A "
                           "         LEFT OUTER JOIN ACNUMBER B "
                           "         ON A.ACACNUMBER = B.ACNUMBER "
                           "         LEFT OUTER JOIN OSCODEM C "
                           "         ON A.MCODE = C.MCODE "
                           "         WHERE B.ACBKCD = '" + itembomlist2[8] + "'  AND A.ACDATE BETWEEN '" + strDate + "' AND '" + endDate + "' "
                           "         GROUP BY A.MCODE, C.MCODENM, B.ACBKCD "
                           "         UNION ALL "
                           "         SELECT A.MCODE, C.MCODENM, B.ACBKCD, 0 AS 1ACMTS, 0 AS 2ACAMTS, 0 AS 3ACMTS, 0 AS 4ACMTS, 0 AS 5ACMTS, 0 AS 6ACMTS, 0 AS 7ACMTS, 0 AS 8ACMTS, 0 AS 9ACMTS, SUM(A.ACAMTS) AS 10ACMTS "
                           "         FROM SISACCTT A "
                           "         LEFT OUTER JOIN ACNUMBER B "
                           "         ON A.ACACNUMBER = B.ACNUMBER "
                           "         LEFT OUTER JOIN OSCODEM C "
                           "         ON A.MCODE = C.MCODE "
                           "         WHERE B.ACBKCD = '" + itembomlist2[9] + "'  AND A.ACDATE BETWEEN '" + strDate + "' AND '" + endDate + "' "
                           "         GROUP BY A.MCODE, C.MCODENM, B.ACBKCD "
                           "         ) TMP GROUP BY MCODE, MCODENM, 1ACMTS, 2ACMTS, 3ACMTS, 4ACMTS, 5ACMTS, 6ACMTS, 7ACMTS, 8ACMTS, 9ACMTS, 10ACMTS "
                           "     ) BB "
                           " GROUP BY MCODE, MCODENM ")

            tbresult = cursor.fetchall()
            print(tbresult)

        return JsonResponse({"headList": headresult, 'mainList': mainresult,'tbList': tbresult})