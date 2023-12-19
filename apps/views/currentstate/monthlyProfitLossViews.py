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

# 월별 자금 유동 현황
def montlyProfitLossViews(request):

    return render(request, "currentstate/profit-loss-sheet.html")


def montlyProfitLossViews_search(request):
    monthArray = json.loads(request.POST.get('monthArrList'))
    print(monthArray)
    strDate = request.POST.get('strDate')
    endDate = request.POST.get('endDate')
    user = request.session.get("userId")
    iCust = request.session.get("USER_ICUST")

    with connection.cursor() as cursor:
        cursor.execute(" SELECT RESKEY, RESNAM FROM OSREFCP WHERE RECODE = 'ACD' ")
        cboAcode = cursor.fetchall()

    with connection.cursor() as cursor:
        cursor.execute(" SELECT RESKEY, RESNAM FROM OSREFCP WHERE RECODE = 'MCD' ")
        mheadresult = cursor.fetchall()

    # with connection.cursor() as cursor:
    #     cursor.execute("  SELECT A.MCODE_M, B.RESNAM, A.MCODE, A.MCODENM, A.ACODE, C.RESNAM FROM OSCODEM A "
    #                    " LEFT OUTER JOIN OSREFCP B "
    #                    " ON A.MCODE_M = B.RESKEY "
    #                    " AND B.RECODE = 'MCD' "
    #                    " LEFT OUTER JOIN OSREFCP C "
    #                    " ON A.ACODE = C.RESKEY "
    #                    " AND C.RECODE = 'ACD' ")
    #     headresult = cursor.fetchall()
    # with connection.cursor() as cursor:
    #     cursor.execute("  SELECT A.MCODE_M, B.RESNAM, A.MCODE, A.MCODENM, A.ACODE, C.RESNAM FROM OSCODEM A "
    #                    " LEFT OUTER JOIN OSREFCP B "
    #                    " ON A.MCODE_M = B.RESKEY "
    #                    " AND B.RECODE = 'MCD' "
    #                    " LEFT OUTER JOIN OSREFCP C "
    #                    " ON A.ACODE = C.RESKEY "
    #                    " AND C.RECODE = 'ACD' ")
    #     headresult = cursor.fetchall()

    # 대분류별 총 금액
    with connection.cursor() as cursor:
        cursor.execute(" SELECT A.RESKEY, A.RESNAM, SUM(IFNULL(C.ACAMTS, 0)) "
                       " FROM OSREFCP A "
                       " LEFT OUTER JOIN OSCODEM B "
                       " ON A.RESKEY = B.MCODE_M "
                       " AND A.RECODE = 'MCD' "
                       " LEFT OUTER JOIN SISACCTT C "
                       " ON B.MCODE = C.MCODE "
                       " WHERE SUBSTRING(C.ACDATE, 1, 6) BETWEEN '" + str(strDate).replace("-", "") + "' AND '" + str(endDate).replace("-", "") + "'"
                       " GROUP BY A.RESKEY, A.RESNAM ORDER BY A.RESKEY ")
        mCoderesult = cursor.fetchall()

    with connection.cursor() as cursor:
        cursor.execute(" SELECT IFNULL(A.MCODE_M, ''), IFNULL(A.ACODE, ''), IFNULL(C.RESNAM, ''), SUM(IFNULL(B.ACAMTS, 0))"
                       " FROM OSCODEM A "
                       " LEFT OUTER JOIN SISACCTT B "
                       " ON A.MCODE = B.MCODE "
                       " LEFT OUTER JOIN OSREFCP C "
                       " ON A.ACODE = C.RESKEY "
                       " AND C.RECODE = 'ACD' "
                       " WHERE SUBSTRING(B.ACDATE, 1, 6) BETWEEN '" + str(strDate).replace("-", "") + "' AND '" + str(endDate).replace("-", "") + "' "
                       " GROUP BY A.MCODE_M, A.ACODE, C.RESNAM ")
        aCoderesult = cursor.fetchall()

    # 회계별 월별
    with connection.cursor() as cursor:
        cursor.execute(" SELECT IFNULL(A.MCODE_M, ''), IFNULL(A.ACODE, ''), IFNULL(C.RESNAM, ''), SUM(IFNULL(B.ACAMTS, 0)), SUBSTRING(B.ACDATE, 1, 6) "
                       " FROM OSCODEM A "
                       " LEFT OUTER JOIN SISACCTT B "
                       " ON A.MCODE = B.MCODE "
                       " LEFT OUTER JOIN OSREFCP C "
                       " ON A.ACODE = C.RESKEY "
                       " AND C.RECODE = 'ACD' "
                       " WHERE SUBSTRING(B.ACDATE, 1, 6) BETWEEN '" + str(strDate).replace("-", "") + "' AND '" + str(endDate).replace("-", "") + "' "
                       " GROUP BY A.MCODE_M, A.ACODE, C.RESNAM, SUBSTRING(B.ACDATE, 1, 6) ")
        itembomlist3 = cursor.fetchall()

    # 대분류 월별
    with connection.cursor() as cursor:
        cursor.execute(" SELECT A.RESKEY, A.RESNAM, SUM(IFNULL(C.ACAMTS, 0)), SUBSTRING(C.ACDATE, 1, 6) "
                       " FROM OSREFCP A "
                       " LEFT OUTER JOIN OSCODEM B "
                       " ON A.RESKEY = B.MCODE_M "
                       " AND A.RECODE = 'MCD' "
                       " LEFT OUTER JOIN SISACCTT C "
                       " ON B.MCODE = C.MCODE "
                       " WHERE SUBSTRING(C.ACDATE, 1, 6) BETWEEN '" + str(strDate).replace("-", "") + "' AND '" + str(endDate).replace("-", "") + "'"
                       " GROUP BY A.RESKEY, A.RESNAM, SUBSTRING(C.ACDATE, 1, 6)")
        itembomlist2 = cursor.fetchall()
        print(itembomlist2)


    return JsonResponse({'mheadList': mheadresult, "cboAcode": cboAcode, "mCodeList": mCoderesult
                            , "aCodeList": aCoderesult, "monthListM": itembomlist2, "monthListA": itembomlist3})


# cursor.execute(" SELECT IFNULL(AA.MCODE_M, ''), IFNULL(AA.RESNAM, '')"
#                "        , IFNULL(AA.OPT, ''), IFNULL(AA.MCODENM, '')"
#                "        , IFNULL(SUM(AA.TOTAL), 0), IFNULL(AVG(AA.AVG), 0)  "
#                " FROM ( "
#                "     SELECT B.MCODE_M, C.RESNAM, A.MCODE, B.MCODENM, SUM(A.ACAMTS) AS TOTAL, AVG(A.ACAMTS) AS AVG "
#                "     FROM SISACCTT A "
#                "     LEFT OUTER JOIN OSCODEM B "
#                "     ON A.MCODE = B.MCODE "
#                "     LEFT OUTER JOIN OSREFCP C "
#                "     ON B.MCODE_M = C.RESKEY "
#                "     AND C.RECODE = 'MCD' "
#                "     WHERE A.MCODE LIKE '5%' "
#                # "     AND YEAR(A.BAL_DD) = '" + yyyy + "' AND MONTH(A.BAL_DD) = '" + mm + "' "
#                "     GROUP BY A.OPT, B.MCODE_M, C.RESNAM, B.MCODENM "
#                "     UNION ALL "
#                "     SELECT B.MCODE_M, C.RESNAM, A.MCODE, B.MCODENM, SUM(A.ACAMTS) AS TOTAL, AVG(A.ACAMTS) AS AVG "
#                "     FROM SISACCTT A "
#                "     LEFT OUTER JOIN OSCODEM B "
#                "     ON A.MCODE = B.MCODE "
#                "     LEFT OUTER JOIN OSREFCP C "
#                "     ON B.MCODE_M = C.RESKEY "
#                "     AND C.RECODE = 'MCD' "
#                "     WHERE A.MCODE LIKE '5%' "
#                # "     AND YEAR(A.BAL_DD) = '" + yyyy + "' AND MONTH(A.BAL_DD) = '" + mm + "' "
#                "     GROUP BY A.OPT, B.MCODE_M, C.RESNAM, B.MCODENM "
#                "     UNION ALL "
#                "     SELECT B.MCODE_M, C.RESNAM, A.MCODE, B.MCODENM, SUM(A.ACAMTS) AS TOTAL, AVG(A.ACAMTS) AS AVG "
#                "     FROM SISACCTT A "
#                "     LEFT OUTER JOIN OSCODEM B "
#                "     ON A.MCODE = B.MCODE "
#                "     LEFT OUTER JOIN OSREFCP C "
#                "     ON B.MCODE_M = C.RESKEY "
#                "     AND C.RECODE = 'MCD' "
#                "     WHERE A.MCODE LIKE '5%' "
#                # "     AND YEAR(A.ACDATE) = '" + yyyy + "' AND MONTH(A.ACDATE) = '" + mm + "' "
#                "     GROUP BY A.MCODE, B.MCODE_M, C.RESNAM, B.MCODENM "
#                "     UNION ALL "
#                "     SELECT B.MCODE_M, C.RESNAM, A.MCODE, B.MCODENM, SUM(A.ACAMTS) AS TOTAL, AVG(A.ACAMTS) AS AVG "
#                "     FROM SISACCTT A "
#                "     LEFT OUTER JOIN OSCODEM B "
#                "     ON A.MCODE = B.MCODE "
#                "     LEFT OUTER JOIN OSREFCP C "
#                "     ON B.MCODE_M = C.RESKEY "
#                "     AND C.RECODE = 'MCD' "
#                "     WHERE A.MCODE LIKE '4%' "
#                # "     AND YEAR(A.ACDATE) = '" + yyyy + "' AND MONTH(A.ACDATE) = '" + mm + "' "
#                "     GROUP BY A.MCODE, B.MCODE_M, C.RESNAM, B.MCODENM "
#                "    ) AA  "
#                " GROUP BY AA.MCODE_M, AA.RESNAM, AA.OPT, AA.MCODENM ")

# 회계코드별
# "  SELECT IFNULL(A.MCODE_M, ''), IFNULL(B.RESNAM, ''), IFNULL(A.MCODE, ''), IFNULL(A.MCODENM, '') "
# "       , IFNULL(A.ACODE, ''), IFNULL(C.RESNAM, ''), SUM(IFNULL(D.ACAMTS, 0)), SUBSTRING(D.ACDATE, 1, 6) "
# "  FROM OSCODEM A "
# "  LEFT OUTER JOIN SISACCTT D "
# "  ON A.ACODE = D.ACODE "
# "  LEFT OUTER JOIN OSREFCP B "
# "  ON A.MCODE_M = B.RESKEY "
# "  AND B.RECODE = 'MCD' "
# "  LEFT OUTER JOIN OSREFCP C "
# "  ON A.ACODE = C.RESKEY "
# "  AND C.RECODE = 'ACD' "
# "  WHERE SUBSTRING(D.ACDATE, 1, 6) BETWEEN '"
# "  GROUP BY A.MCODE_M, B.RESNAM, A.MCODE, A.MCODENM, A.ACODE, C.RESNAM, D.ACDATE