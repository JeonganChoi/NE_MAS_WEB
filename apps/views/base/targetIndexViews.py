from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.db import connection
from django.contrib import messages

def targetIndexViews(request):

    return render(request, "base/base-targetIndex.html")


def targetIndexSearchViews(request):
    year = request.POST.get('Year')

    with connection.cursor() as cursor:
        cursor.execute(
                " SELECT "
                "         A.RESNAM "
                "         ,IFNULL(B.DATE01, 0) AS DATE01 "
                "         ,IFNULL(B.DATE02, 0) AS DATE02 "
                "         ,IFNULL(B.DATE03, 0) AS DATE03 "
                "         ,IFNULL(B.DATE04, 0) AS DATE04 "
                "         ,IFNULL(B.DATE05, 0) AS DATE05 "
                "         ,IFNULL(B.DATE06, 0) AS DATE06 "
                "         ,IFNULL(B.DATE07, 0) AS DATE07 "
                "         ,IFNULL(B.DATE08, 0) AS DATE08 "
                "         ,IFNULL(B.DATE09, 0) AS DATE09 "
                "         ,IFNULL(B.DATE10, 0) AS DATE10 "
                "         ,IFNULL(B.DATE11, 0) AS DATE11 "
                "         ,IFNULL(B.DATE12, 0) AS DATE12 "
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
                " )B "
                " ON A.RESKEY = B.ENTYPE "
                " WHERE RECODE = 'EMD'"
                " AND YYMM LIKE '%" + year + "%'"
        )
        result = cursor.fetchall()

    return JsonResponse({"targetList": result})

def targetIndexSaveViews(request):
    if request.method == "POST":
        entype_list = request.POST.getlist('index_code')
        yymm_list = request.POST.getlist('yymm')
        month01_list = request.POST.getlist('month01')
        month02_list = request.POST.getlist('month02')
        month03_list = request.POST.getlist('month03')
        month04_list = request.POST.getlist('month04')
        month05_list = request.POST.getlist('month05')
        month06_list = request.POST.getlist('month06')
        month07_list = request.POST.getlist('month07')
        month08_list = request.POST.getlist('month08')
        month09_list = request.POST.getlist('month09')
        month10_list = request.POST.getlist('month10')
        month11_list = request.POST.getlist('month11')
        month12_list = request.POST.getlist('month12')

        targetindexlist2 = []

        for i in range(len(entype_list)):
            targetindexlist = [yymm_list[i], month01_list[i], month02_list[i], month03_list[i], month04_list[i], month05_list[i], month06_list[i],
                         month07_list[i], month08_list[i], month09_list[i], month10_list[i], month11_list[i], month12_list[i], entype_list[i]]

            targetindexlist2 += [targetindexlist]

            with connection.cursor() as cursor:
                cursor.execute(
                          " INSERT INTO MIS1TB051 "
                          "(  "
                          "     yymm "
                          ",    DATA01 "
                          ",    DATA02 "
                          ",    DATA03 "
                          ",    DATA04 "
                          ",    DATA05 "
                          ",    DATA06 "
                          ",    DATA07 "
                          ",    DATA08 "
                          ",    DATA09 "
                          ",    DATA10 "
                          ",    DATA11 "
                          ",    DATA12 "
                          ",    ENTYPE "
                          ",    COMP "
                          "    )   "
                          "    VALUES "
                          "    (   "
                          "    '" + str(targetindexlist2[i][0]) + "'"
                          ",   '" + str(targetindexlist2[i][1]) + "'"
                          ",   '" + str(targetindexlist2[i][2]) + "'"
                          ",   '" + str(targetindexlist2[i][3]) + "'"
                          ",   '" + str(targetindexlist2[i][4]) + "'"
                          ",   '" + str(targetindexlist2[i][5]) + "'"
                          ",   '" + str(targetindexlist2[i][6]) + "'"
                          ",   '" + str(targetindexlist2[i][7]) + "'"
                          ",   '" + str(targetindexlist2[i][8]) + "'"
                          ",   '" + str(targetindexlist2[i][9]) + "'"
                          ",   '" + str(targetindexlist2[i][10]) + "'"
                          ",   '" + str(targetindexlist2[i][11]) + "'"
                          ",   '" + str(targetindexlist2[i][12]) + "'"
                          ",   '" + str(targetindexlist2[i][13]) + "'"
                          ",   '1'"
                          "    )   "
                          "    ON DUPLICATE  KEY "
                          "    UPDATE "
                          "     DATA01 = '" + str(targetindexlist2[i][1]) + "' "
                          ",    DATA02 = '" + str(targetindexlist2[i][2]) + "' "
                          ",    DATA03 = '" + str(targetindexlist2[i][3]) + "' "
                          ",    DATA04 = '" + str(targetindexlist2[i][4]) + "' "
                          ",    DATA05 = '" + str(targetindexlist2[i][5]) + "' "
                          ",    DATA06 = '" + str(targetindexlist2[i][6]) + "' "
                          ",    DATA07 = '" + str(targetindexlist2[i][7]) + "' "
                          ",    DATA08 = '" + str(targetindexlist2[i][8]) + "' "
                          ",    DATA09 = '" + str(targetindexlist2[i][9]) + "' "
                          ",    DATA10 = '" + str(targetindexlist2[i][10]) + "' "
                          ",    DATA11 = '" + str(targetindexlist2[i][11]) + "' "
                          ",    DATA12 = '" + str(targetindexlist2[i][12]) + "' "
                      )
                connection.commit()
        messages.success(request, '저장 되었습니다.')
        return render(request, 'base/base-targetIndex.html')
    else:
        messages.warning(request, '입력 하신 정보를 확인 해주세요.')
        return redirect('/base_targetIndex')
