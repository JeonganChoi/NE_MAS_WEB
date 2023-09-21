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

def accountCodeViews(request):

    return render(request, "base/base-actCode-reg.html")

def accountCodeViews_search(request):
    mainCode = request.POST.get('mainCode')
    codeType = request.POST.get('cboCodeType')

    if mainCode:
        with connection.cursor() as cursor:
            cursor.execute(" SELECT IFNULL(A.MCODE_M, ''), IFNULL(D.RESNAM, ''), IFNULL(A.MCODE, ''), IFNULL(A.MCODENM, ''), IFNULL(A.MDESC, ''), IFNULL(A.MSEQ, '')"
                           "    , IFNULL(A.GBN, ''), IFNULL(B.RESNAM, ''), IFNULL(A.GBN2, ''), IFNULL(C.RESNAM, ''), IFNULL(A.ACODE, ''), IFNULL(E.RESNAM, ''), IFNULL(A.OPT, '') "
                           "    FROM OSCODEM A "
                           "    LEFT OUTER JOIN OSREFCP B "
                           "    ON A.GBN = B.RESKEY "
                           "    AND B.RECODE = 'CGB' "
                           "    LEFT OUTER JOIN OSREFCP C "
                           "    ON A.GBN2 = C.RESKEY "
                           "    AND C.RECODE = 'AGB' "
                           "    LEFT OUTER JOIN OSREFCP D "
                           "    ON A.MCODE_M = D.RESKEY "
                           "    AND D.RECODE = 'MCD' "
                           "    LEFT OUTER JOIN OSREFCP E "
                           "    ON A.ACODE = E.RESKEY "
                           "    AND E.RECODE = 'ACD' "
                           "    WHERE MCODE = '400001' "
                           # "    WHERE MCODE = '" + mainCode + "' "
                           )
            mresult = cursor.fetchall()

        return JsonResponse({"subMList": mresult})

    else:
        with connection.cursor() as cursor:
            cursor.execute(" SELECT IFNULL(A.MCODE_M, ''), IFNULL(D.RESNAM, ''), IFNULL(A.MCODE, ''), IFNULL(A.MCODENM, ''), IFNULL(A.MSEQ, ''), IFNULL(A.MDESC, '')"
                           "    , IFNULL(A.GBN, ''), IFNULL(B.RESNAM, ''), IFNULL(A.GBN2, ''), IFNULL(C.RESNAM, ''), IFNULL(A.ACODE, ''), IFNULL(E.RESNAM, ''), IFNULL(A.OPT, '') "
                           "    FROM OSCODEM A "
                           "    LEFT OUTER JOIN OSREFCP B "
                           "    ON A.GBN = B.RESKEY "
                           "    AND B.RECODE = 'CGB' "
                           "    LEFT OUTER JOIN OSREFCP C "
                           "    ON A.GBN2 = C.RESKEY "
                           "    AND C.RECODE = 'AGB' "
                           "    LEFT OUTER JOIN OSREFCP D "
                           "    ON A.MCODE_M = D.RESKEY "
                           "    AND D.RECODE = 'MCD' "
                           "    LEFT OUTER JOIN OSREFCP E "
                           "    ON A.ACODE = E.RESKEY "
                           "    AND E.RECODE = 'ACD' "
                           "    WHERE MCODE LIKE '" + str(codeType) + "%' ORDER BY MCODE ")
            mresult = cursor.fetchall()
            print(mresult)

        # 상위계정과목
        with connection.cursor() as cursor:
            cursor.execute(" SELECT RESKEY, RESNAM FROM OSREFCP WHERE RECODE = 'MCD' ")
            cboMCode = cursor.fetchall()

        # 회계계정과목
        with connection.cursor() as cursor:
            cursor.execute(" SELECT RESKEY, RESNAM FROM OSREFCP WHERE RECODE = 'ACD' ")
            cboACode = cursor.fetchall()

        # 구분1
        with connection.cursor() as cursor:
            cursor.execute(" SELECT RESKEY, RESNAM FROM OSREFCP WHERE RECODE = 'CGB' ")
            gbnesult = cursor.fetchall()

        # 구분2
        with connection.cursor() as cursor:
            cursor.execute(" SELECT RESKEY, RESNAM FROM OSREFCP WHERE RECODE = 'AGB' ")
            gbn2result = cursor.fetchall()

        return JsonResponse({"mList": mresult, 'cboMCode': cboMCode, 'cboACode': cboACode, 'cboGbn': gbnesult, 'cboGbn2': gbn2result})

def accountCodeViews_saveM(request):
    codeType = request.POST.get("cboCodeType")
    mCode_M = request.POST.get("mCode_M")
    mCode_A = request.POST.get("mCode_A")
    mCode = request.POST.get("txtCode_M")
    mCodeNme = request.POST.get("txtCodeNme_M")
    mSeq = request.POST.get("txtSeq_M")
    mDesc = request.POST.get("txtDesc_M")
    gbn = request.POST.get("cboGbn_M")
    gbn2 = request.POST.get("cboGbn2_M")
    opt = request.POST.get("cboOpt")
    iCust = request.session.get("USER_ICUST")
    user = request.session.get("userId")

    # 수익4/ 비용5


    if mSeq == '' or mSeq is None:
        # with connection.cursor() as cursor:
        #     cursor.execute(" SELECT IFNULL(MAX(MCODE), 0) FROM OSCODEM WHERE MCODE LIKE '" + codeType + "%'")
        #     subresult = cursor.fetchall()
        #     x = int(subresult[0][0])
        #     x = str(x)
        #     if codeType == str(x[0]):
        #         subCode = int(x) + 1
        #     else:
        #         subCode = int(codeType + str(x).zfill(5)) + 1
        #         print(subCode)

        with connection.cursor() as cursor:
              cursor.execute(" INSERT INTO OSCODEM "
                             "   (    "
                             "     MCODE "
                             ",    MCODE_M "
                             ",    ACODE "
                             ",    MSEQ "
                             ",    MCODENM "
                             ",    MDESC "
                             ",    GBN "
                             ",    GBN2 "
                             ",    OPT "
                             ",    ICUST "
                             ",    CRE_USER "
                             ",    CRE_DT "
                             "    ) "
                             "    VALUES "
                             "    (   "
                             "    '" + str(mCode) + "' "
                             ",   '" + str(mCode_M) + "' "
                             ",   '" + str(mCode_A) + "' "
                             ",   (SELECT IFNULL(MAX(A.MSEQ) + 1, 1) AS COUNTED FROM OSCODEM A) "
                             ",   '" + str(mCodeNme) + "' "
                             ",   '" + str(mDesc) + "' "
                             ",   '" + str(gbn) + "' "
                             ",   '" + str(gbn2) + "' "
                             ",   '" + str(opt) + "' "
                             ",   '" + str(iCust) + "' "
                             ",   '" + str(user) + "' "
                             ",   date_format(now(), '%Y%m%d') "
                             "    )   "
                             )
              connection.commit()

              return JsonResponse({'sucYn': "Y"})

    elif mSeq:
        with connection.cursor() as cursor:
            cursor.execute("    UPDATE OSCODEM SET"
                           "     MCODE_M = '" + str(mCode_M) + "' "
                           ",    ACODE = '" + str(mCode_A) + "' "
                           ",    MCODENM = '" + str(mCodeNme) + "' "
                           ",    MDESC = '" + str(mDesc) + "' "
                           ",    GBN = '" + str(gbn) + "' "
                           ",    GBN2 = '" + str(gbn2) + "' "
                           ",    OPT = '" + str(opt) + "' "
                           ",    UPD_USER = '" + str(user) + "' "
                           ",    UPD_DT = date_format(now(), '%Y%m%d') "
                           "     WHERE MCODE = '" + str(mCode) + "' "
                           "     AND MSEQ = '" + str(mSeq) + "' "
                           )
            connection.commit()

            return JsonResponse({'sucYn': "Y"})

    return render(request, 'base/base-actCode-reg.html')


def accountCodeViews_dltM(request):
    if request.method == "POST":
        dataList = json.loads(request.POST.get('arrList'))
        print(dataList)
        for code in dataList:
            acc_split_list = code.split(',')
            with connection.cursor() as cursor:
                cursor.execute(" DELETE FROM OSCODEM WHERE MCODE_M = '" + acc_split_list[0] + "'"
                               "                       AND MSEQ = '" + acc_split_list[2] + "'")
                connection.commit()

        return JsonResponse({'sucYn': "Y"})

    else:
        return render(request, 'base/base-actCode-reg.html')
