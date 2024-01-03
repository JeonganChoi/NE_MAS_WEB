import json
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.db import connection
from django.contrib import messages

def targetIndexViews(request):
    userId = request.session.get('userId')
    if userId == '' or userId is None:
        return redirect("/page-404/")
    else:
        return render(request, "base/base-targetIndex.html")


def targetIndexSearchViews(request):
    year = request.POST.get('Year')
    iCust = request.session.get('USER_ICUST')

    with connection.cursor() as cursor:
        cursor.execute("  SELECT "
                       "         A.RESNAM "
                       "         ,IFNULL(B.DATE01, 0) AS DAT "
                       "         ,IFNULL(B.DATE02, 0) AS DAT "
                       "         ,IFNULL(B.DATE03, 0) AS DAT "
                       "         ,IFNULL(B.DATE04, 0) AS DAT "
                       "         ,IFNULL(B.DATE05, 0) AS DAT "
                       "         ,IFNULL(B.DATE06, 0) AS DAT "
                       "         ,IFNULL(B.DATE07, 0) AS DAT "
                       "         ,IFNULL(B.DATE08, 0) AS DAT "
                       "         ,IFNULL(B.DATE09, 0) AS DAT "
                       "         ,IFNULL(B.DATE10, 0) AS DAT "
                       "         ,IFNULL(B.DATE11, 0) AS DAT "
                       "         ,IFNULL(B.DATE12, 0) AS DAT "
                       "         ,A.RESKEY "
                       "         ,B.YYMM "
                       " FROM osrefcp A "
                       " LEFT OUTER JOIN "
                       " ( "
                       "     SELECT "
                       "        ENTYPE "
                       "      , IFNULL(DATA01, 0) AS DATE01 "
                       "      , IFNULL(DATA02, 0) AS DATE02 "
                       "      , IFNULL(DATA03, 0) AS DATE03 "
                       "      , IFNULL(DATA04, 0) AS DATE04 "
                       "      , IFNULL(DATA05, 0) AS DATE05 "
                       "      , IFNULL(DATA06, 0) AS DATE06 "
                       "      , IFNULL(DATA07, 0) AS DATE07 "
                       "      , IFNULL(DATA08, 0) AS DATE08 "
                       "      , IFNULL(DATA09, 0) AS DATE09 "
                       "      , IFNULL(DATA10, 0) AS DATE10 "
                       "      , IFNULL(DATA11, 0) AS DATE11 "
                       "      , IFNULL(DATA12, 0) AS DATE12 "
                       "      , yymm AS YYMM "
                       "     FROM MIS1TB051 "
                       "     WHERE YYMM = '" + year + "' "
                       "       AND ICUST = '" + str(iCust) + "' "
                       " )B "
                       " ON A.RESKEY = B.ENTYPE "
                       " WHERE A.RECODE = 'EMD' ")
        result = cursor.fetchall()

    return JsonResponse({"targetList": result})

def targetIndexSaveViews(request):
    payArray = json.loads(request.POST.get('payArrList'))
    year = request.POST.get('year')
    user = request.session.get('userId')
    iCust = request.session.get('USER_ICUST')

    payArrayLists = list(filter(len, payArray))
    for data in range(len(payArrayLists)):

        if (payArrayLists[data]["month01"] == ''):
            payArrayLists[data]["month01"] = 0
        if (payArrayLists[data]["month02"] == ''):
            payArrayLists[data]["month02"] = 0
        if (payArrayLists[data]["month03"] == ''):
            payArrayLists[data]["month03"] = 0
        if (payArrayLists[data]["month04"] == ''):
            payArrayLists[data]["month04"] = 0
        if (payArrayLists[data]["month05"] == ''):
            payArrayLists[data]["month05"] = 0
        if (payArrayLists[data]["month06"] == ''):
            payArrayLists[data]["month06"] = 0
        if (payArrayLists[data]["month07"] == ''):
            payArrayLists[data]["month07"] = 0
        if (payArrayLists[data]["month08"] == ''):
            payArrayLists[data]["month08"] = 0
        if (payArrayLists[data]["month09"] == ''):
            payArrayLists[data]["month09"] = 0
        if (payArrayLists[data]["month10"] == ''):
            payArrayLists[data]["month10"] = 0
        if (payArrayLists[data]["month11"] == ''):
            payArrayLists[data]["month11"] = 0
        if (payArrayLists[data]["month12"] == ''):
            payArrayLists[data]["month12"] = 0


        with connection.cursor() as cursor:
            cursor.execute(" SELECT ENTYPE FROM MIS1TB051 WHERE yymm = '" + year + "' AND ENTYPE = '" + payArrayLists[data]["iCode"] + "' ")
            result = cursor.fetchall()

        if result:
            with connection.cursor() as cursor:
                cursor.execute("    UPDATE MIS1TB051 SET"
                              "     DATA01 = '" + payArrayLists[data]["month01"].replace(',', '') + "' "
                              ",    DATA02 = '" + payArrayLists[data]["month02"].replace(',', '') + "' "
                              ",    DATA03 = '" + payArrayLists[data]["month03"].replace(',', '') + "' "
                              ",    DATA04 = '" + payArrayLists[data]["month04"].replace(',', '') + "' "
                              ",    DATA05 = '" + payArrayLists[data]["month05"].replace(',', '') + "' "
                              ",    DATA06 = '" + payArrayLists[data]["month06"].replace(',', '') + "' "
                              ",    DATA07 = '" + payArrayLists[data]["month07"].replace(',', '') + "' "
                              ",    DATA08 = '" + payArrayLists[data]["month08"].replace(',', '') + "' "
                              ",    DATA09 = '" + payArrayLists[data]["month09"].replace(',', '') + "' "
                              ",    DATA10 = '" + payArrayLists[data]["month10"].replace(',', '') + "' "
                              ",    DATA11 = '" + payArrayLists[data]["month11"].replace(',', '') + "' "
                              ",    DATA12 = '" + payArrayLists[data]["month12"].replace(',', '') + "' "
                              ",    UPD_USER = '" + str(user) + "' "
                              ",    UPD_DT = date_format(now(), '%Y%m%d') "
                              "     WHERE yymm = '" + year + "' "
                              "      AND ENTYPE = '" + payArrayLists[data]["iCode"] + "'"
                              "      AND ICUST = '" + str(iCust) + "'"
                      )
                connection.commit()

        else:
            with connection.cursor() as cursor:
                cursor.execute("    INSERT INTO MIS1TB051 "
                               "("
                               "   yymm"
                               " , ENTYPE  "
                               " , DATA01 "
                               " , DATA02 "
                               " , DATA03 "
                               " , DATA04 "
                               " , DATA05 "
                               " , DATA06 "
                               " , DATA07 "
                               " , DATA08 "
                               " , DATA09 "
                               " , DATA10 "
                               " , DATA11 "
                               " , DATA12 "
                               " , CRE_USER "
                               " , CRE_DT "
                               " , ICUST "
                               ")"
                               "VALUES"
                               "("
                               " '" + year + "' "
                               " ,'" + payArrayLists[data]["iCode"] + "'"
                               " , '" + payArrayLists[data]["month01"].replace(',', '') + "'"
                               " , '" + payArrayLists[data]["month02"].replace(',', '') + "'"
                               " , '" + payArrayLists[data]["month03"].replace(',', '') + "'"
                               " , '" + payArrayLists[data]["month04"].replace(',', '') + "'"
                               " , '" + payArrayLists[data]["month05"].replace(',', '') + "'"
                               " , '" + payArrayLists[data]["month06"].replace(',', '') + "'"
                               " , '" + payArrayLists[data]["month07"].replace(',', '') + "'"
                               " , '" + payArrayLists[data]["month08"].replace(',', '') + "'"
                               " , '" + payArrayLists[data]["month09"].replace(',', '') + "'"
                               " , '" + payArrayLists[data]["month10"].replace(',', '') + "'"
                               " , '" + payArrayLists[data]["month11"].replace(',', '') + "'"
                               " , '" + payArrayLists[data]["month12"].replace(',', '') + "'"
                               " , '" + str(user) + "' "
                               " , date_format(now(), '%Y%m%d') "
                               " , '" + str(iCust) + "' "
                               ")"
                  )
                connection.commit()

    return JsonResponse({'arrList': "Y"})

    #         with connection.cursor() as cursor:
    #             cursor.execute("    UPDATE MIS1TB051 SET"
    #                           "     DATA01 = '" + str(targetindexlist2[i][1]) + "' "
    #                           ",    DATA02 = '" + str(targetindexlist2[i][2]) + "' "
    #                           ",    DATA03 = '" + str(targetindexlist2[i][3]) + "' "
    #                           ",    DATA04 = '" + str(targetindexlist2[i][4]) + "' "
    #                           ",    DATA05 = '" + str(targetindexlist2[i][5]) + "' "
    #                           ",    DATA06 = '" + str(targetindexlist2[i][6]) + "' "
    #                           ",    DATA07 = '" + str(targetindexlist2[i][7]) + "' "
    #                           ",    DATA08 = '" + str(targetindexlist2[i][8]) + "' "
    #                           ",    DATA09 = '" + str(targetindexlist2[i][9]) + "' "
    #                           ",    DATA10 = '" + str(targetindexlist2[i][10]) + "' "
    #                           ",    DATA11 = '" + str(targetindexlist2[i][11]) + "' "
    #                           ",    DATA12 = '" + str(targetindexlist2[i][12]) + "' "
    #                   )
    #             connection.commit()
    #     messages.success(request, '저장 되었습니다.')
    #     return render(request, 'base/base-targetIndex.html')
    # else:
    #     messages.warning(request, '입력 하신 정보를 확인 해주세요.')
    #     return redirect('/base_targetIndex')
