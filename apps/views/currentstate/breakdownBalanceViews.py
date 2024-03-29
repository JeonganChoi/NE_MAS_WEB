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

# 내역별
def breakdownBalanceViews(request):
    userId = request.session.get('userId')
    if userId == '' or userId is None:
        return redirect("/page-404/")
    else:
        return render(request, "currentstate/breakdown-sheet.html")

def breakdownBalanceViews_search(request):
    date = request.POST.get('date')
    year = request.POST.get('year')
    iCust = request.session.get("USER_ICUST")

    with connection.cursor() as cursor:
        cursor.execute(" SELECT A.ACBKCD, B.RESNAM FROM ACNUMBER A LEFT OUTER JOIN OSREFCP B ON A.ACBKCD = B.RESKEY AND B.RECODE = 'BNK' AND A.ICUST = '" + str(iCust) + "' GROUP BY A.ACBKCD, B.RESNAM ORDER BY A.ACBKCD  ")
        headresult = cursor.fetchall()


    with connection.cursor() as cursor:
        cursor.execute(" SELECT B.ACBKCD, IFNULL(SUM(A.ACAMTS), 0) "
                       " FROM SISACCTT A "
                       " LEFT OUTER JOIN ACNUMBER B "
                       " ON A.ACACNUMBER = B.ACNUMBER "
                       " WHERE A.FIN_OPT = 'Y' AND A.ACDATE < '" + str(date) + "' AND A.ICUST = '" + str(iCust) + "' "
                       " GROUP BY B.ACBKCD "
                       " ORDER BY B.ACBKCD ASC ")
        mainresult = cursor.fetchall()

        with connection.cursor() as cursor:
            cursor.execute(" SELECT SUM(ACAMTS) FROM ACBALANCE WHERE ACDATE < '" + str(date) + "' AND ICUST = '" + str(iCust) + "' ")
            coderesult = cursor.fetchall()

        with connection.cursor() as cursor:
            cursor.execute(" SELECT MCODE, ACAMTS FROM SISACCTT WHERE FIN_OPT = 'Y' AND ACDATE < '" + str(date) + "' AND ICUST = '" + str(iCust) + "' ")
            coderesult2 = cursor.fetchall()

        # 매입51/매출43/출금53,55/입금41
        with connection.cursor() as cursor:
            cursor.execute(" SELECT IFNULL(SUM(TOTAL), 0) AS TOTAL, IFNULL(SUM(DEPOSIT), 0) AS DEPOSIT, IFNULL(SUM(SALE), 0) AS SALE "
                           "      , IFNULL(SUM(BUY), 0) AS BUY, IFNULL(SUM(WITHDROW), 0) AS WITHDROW "
                           "      , IFNULL(SUM(TOTAL + DEPOSIT + SALE - BUY - WITHDROW), 0) AS CAL FROM "
                           "     ( "
                           "     SELECT IFNULL(SUM(ACAMTS), 0) AS TOTAL, 0 AS BUY, 0 AS SALE, 0 AS WITHDROW, 0 AS DEPOSIT "
                           "     FROM ACBALANCE WHERE ACDATE < '" + str(date) + "' AND ICUST = '" + str(iCust) + "' "
                           " UNION ALL "
                           "     SELECT 0 AS TOTAL, IFNULL(SUM(ACAMTS), 0) AS BUY, 0 AS SALE, 0 AS WITHDROW, 0 AS DEPOSIT "
                           "     FROM SISACCTT WHERE YEAR(ACDATE) = '" + str(year) + "' AND ACDATE < '" + str(date) + "' AND FIN_OPT = 'Y' AND ACIOGB = '1' AND ICUST = '" + str(iCust) + "'  AND ACODE LIKE '51%' "
                           " UNION ALL "
                           "     SELECT 0 AS TOTAL, 0 AS BUY, IFNULL(SUM(ACAMTS), 0) AS SALE, 0 AS WITHDROW, 0 AS DEPOSIT "
                           "     FROM SISACCTT WHERE YEAR(ACDATE) = '" + str(year) + "' AND ACDATE < '" + str(date) + "' AND FIN_OPT = 'Y' AND ACIOGB = '2' AND ICUST = '" + str(iCust) + "' AND ACODE LIKE '43%' "
                           " UNION ALL "
                           "     SELECT 0 AS TOTAL, 0 AS BUY, 0 AS SALE, IFNULL(SUM(ACAMTS), 0) AS WITHDROW, 0 AS DEPOSIT "
                           "     FROM SISACCTT WHERE YEAR(ACDATE) = '" + str(year) + "' AND ACDATE < '" + str(date) + "' AND FIN_OPT = 'Y' AND ACIOGB = '1' AND ICUST = '" + str(iCust) + "'  AND ACODE IN ('53%', '55%') "
                           " UNION ALL "
                           "     SELECT 0 AS TOTAL, 0 AS BUY, 0 AS SALE, 0 AS WITHDROW, IFNULL(SUM(ACAMTS), 0) AS DEPOSIT "
                           "     FROM SISACCTT WHERE YEAR(ACDATE) = '" + str(year) + "' AND ACDATE < '" + str(date) + "' AND FIN_OPT = 'Y' AND ACIOGB = '2' AND ICUST = '" + str(iCust) + "'  AND ACODE LIKE '41%' "
                           " ) AA ")
            monthresult = cursor.fetchall()


        with connection.cursor() as cursor:
            cursor.execute(" SELECT IFNULL(SUM(TOTAL), 0) AS TOTAL, IFNULL(SUM(DEPOSIT), 0) AS DEPOSIT, IFNULL(SUM(SALE), 0) AS SALE "
                           "      , IFNULL(SUM(BUY), 0) AS BUY, IFNULL(SUM(WITHDROW), 0) AS WITHDROW, IFNULL(SUM(DEPOSIT - WITHDROW + (TOTAL + SALE) - BUY), 0) AS CAL FROM "
                           "      ( "
                           "      SELECT IFNULL(SUM(ACAMTS), 0) AS TOTAL, 0 AS BUY, 0 AS SALE, 0 AS WITHDROW, 0 AS DEPOSIT "
                           "      FROM ACBALANCE WHERE ACDATE < '" + str(date) + "' AND ICUST = '" + str(iCust) + "' "
                           "  UNION ALL "
                           "     SELECT 0 AS TOTAL, IFNULL(SUM(ACAMTS), 0) AS BUY, 0 AS SALE, 0 AS WITHDROW, 0 AS DEPOSIT "
                           "      FROM SISACCTT WHERE YEAR(ACDATE) = '" + str(year) + "' AND ACDATE < '" + str(date) + "' AND FIN_OPT = 'Y' AND ICUST = '" + str(iCust) + "' AND ACODE LIKE '51%' "
                           "  UNION ALL "
                           "     SELECT 0 AS TOTAL, 0 AS BUY, IFNULL(SUM(ACAMTS), 0) AS SALE, 0 AS WITHDROW, 0 AS DEPOSIT "
                           "      FROM SISACCTT WHERE YEAR(ACDATE) = '" + str(year) + "' AND ACDATE < '" + str(date) + "' AND FIN_OPT = 'Y' AND ICUST = '" + str(iCust) + "' AND ACODE LIKE '43%' "
                           "  UNION ALL "
                           "     SELECT 0 AS TOTAL, 0 AS BUY, 0 AS SALE, IFNULL(SUM(ACAMTS), 0) AS WITHDROW, 0 AS DEPOSIT "
                           "      FROM SISACCTT WHERE YEAR(ACDATE) = '" + str(year) + "' AND ACDATE < '" + str(date) + "' AND FIN_OPT = 'Y' AND ICUST = '" + str(iCust) + "' AND ACODE IN ('53%', '55%') "
                           "  UNION ALL "
                           "     SELECT 0 AS TOTAL, 0 AS BUY, 0 AS SALE, 0 AS WITHDROW, IFNULL(SUM(ACAMTS), 0) AS DEPOSIT "
                           "      FROM SISACCTT WHERE YEAR(ACDATE) = '" + str(year) + "' AND ACDATE < '" + str(date) + "' AND FIN_OPT = 'Y' AND ICUST = '" + str(iCust) + "' AND ACODE LIKE '41%' "
                           "  ) AA ")

            circleresult = cursor.fetchall()

        return JsonResponse({"headList": headresult, 'mainList': mainresult, 'codeList': coderesult
                                , 'codeList2': coderesult2, 'monthList': monthresult, 'circleList': circleresult})

    # for i in range(len(headresult)):
    #     bnkCode = headresult[i][0]
    #     with connection.cursor() as cursor:
    #         cursor.execute(" SELECT B.ACBKCD, IFNULL(SUM(A.ACAMTS), 0) "
    #                        " FROM SISACCTT A "
    #                        " LEFT OUTER JOIN ACNUMBER B "
    #                        " ON A.ACACNUMBER = B.ACNUMBER "
    #                        " WHERE B.ACBKCD = '" + bnkCode + "' "
    #                        " AND A.ACDATE > '" + date + "' "
    #                        " GROUP BY B.ACBKCD ")
    #         mainresult = cursor.fetchall()
    #         mainList += [mainresult]
    #         print(mainList)


# " SELECT IFNULL(SUM(TOTAL), 0) AS TOTAL, IFNULL(SUM(DEPOSIT), 0) AS DEPOSIT, IFNULL(SUM(SALE), 0) AS SALE "
# "      , IFNULL(SUM(BUY), 0) AS BUY, IFNULL(SUM(WITHDROW), 0) AS WITHDROW"
# "      , IFNULL(SUM(TOTAL + DEPOSIT + SALE - BUY - WITHDROW), 0) AS CAL FROM "
# "     ( "
# "     SELECT IFNULL(SUM(ACAMTS), 0) AS TOTAL, 0 AS BUY, 0 AS SALE, 0 AS WITHDROW, 0 AS DEPOSIT  "
# "     FROM ACBALANCE WHERE ACDATE < '" + date + "' "
# " UNION ALL "
# "     SELECT 0 AS TOTAL, IFNULL(SUM(AMTS), 0) AS BUY, 0 AS SALE, 0 AS WITHDROW, 0 AS DEPOSIT  "
# "     FROM SISACCTT WHERE YEAR(BAL_DD) = '" + year + "' AND BAL_DD < '" + date + "' AND GUBUN = '1' "
# " UNION ALL "
# "     SELECT 0 AS TOTAL, 0 AS BUY, IFNULL(SUM(AMTS), 0) AS SALE, 0 AS WITHDROW, 0 AS DEPOSIT  "
# "     FROM SISACCTT WHERE YEAR(BAL_DD) = '" + year + "' AND BAL_DD < '" + date + "' AND GUBUN = '2' "
# " UNION ALL "
# "     SELECT 0 AS TOTAL, 0 AS BUY, 0 AS SALE, IFNULL(SUM(ACAMTS), 0) AS WITHDROW, 0 AS DEPOSIT  "
# "     FROM SISACCTT WHERE YEAR(ACDATE) = '" + year + "' AND ACDATE < '" + date + "' AND ACIOGB = '1' "
# " UNION ALL "
# "     SELECT 0 AS TOTAL, 0 AS BUY, 0 AS SALE, 0 AS WITHDROW, IFNULL(SUM(ACAMTS), 0) AS DEPOSIT  "
# "     FROM SISACCTT WHERE YEAR(ACDATE) = '" + year + "' AND ACDATE < '" + date + "' AND ACIOGB = '2' "
# " ) AA "

# cursor.execute(" SELECT IFNULL(SUM(TOTAL), 0) AS TOTAL, IFNULL(SUM(DEPOSIT), 0) AS DEPOSIT, IFNULL(SUM(SALE), 0) AS SALE "
#                "     , IFNULL(SUM(BUY), 0) AS BUY, IFNULL(SUM(WITHDROW), 0) AS WITHDROW, IFNULL(SUM(DEPOSIT - WITHDROW + (TOTAL + SALE) - BUY), 0) AS CAL FROM "
#                "     ( "
#                "     SELECT IFNULL(SUM(ACAMTS), 0) AS TOTAL, 0 AS BUY, 0 AS SALE, 0 AS WITHDROW, 0 AS DEPOSIT "
#                "     FROM ACBALANCE WHERE ACDATE < '" + date + "' "
#                " UNION ALL "
#                "    SELECT 0 AS TOTAL, IFNULL(SUM(AMTS), 0) AS BUY, 0 AS SALE, 0 AS WITHDROW, 0 AS DEPOSIT "
#                "     FROM OSBILL WHERE YEAR(BAL_DD) = '" + year + "' AND BAL_DD < '" + date + "' AND GUBUN = '1' "
#                " UNION ALL "
#                "    SELECT 0 AS TOTAL, 0 AS BUY, IFNULL(SUM(AMTS), 0) AS SALE, 0 AS WITHDROW, 0 AS DEPOSIT "
#                "     FROM OSBILL WHERE YEAR(BAL_DD) = '" + year + "' AND BAL_DD < '" + date + "' AND GUBUN = '2' "
#                " UNION ALL "
#                "    SELECT 0 AS TOTAL, 0 AS BUY, 0 AS SALE, IFNULL(SUM(ACAMTS), 0) AS WITHDROW, 0 AS DEPOSIT "
#                "     FROM SISACCTT WHERE YEAR(ACDATE) = '" + year + "' AND ACDATE < '" + date + "' AND ACIOGB = '1' "
#                " UNION ALL "
#                "    SELECT 0 AS TOTAL, 0 AS BUY, 0 AS SALE, 0 AS WITHDROW, IFNULL(SUM(ACAMTS), 0) AS DEPOSIT "
#                "     FROM SISACCTT WHERE YEAR(ACDATE) = '" + year + "' AND ACDATE < '" + date + "' AND ACIOGB = '2' "
#                " ) AA ")