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
    userId = request.session.get('userId')
    if userId == '' or userId is None:
        return redirect("/page-404/")
    else:
        return render(request, "base/base-actCode-reg.html")

def accountCodeViews_search(request):
    mainCode = request.POST.get('mainCode')
    codeType = request.POST.get('cboCodeType')
    iCust = request.session.get("USER_ICUST")

    if mainCode:
        with connection.cursor() as cursor:
            cursor.execute(" SELECT IFNULL(A.MCODE_M, ''), IFNULL(D.RESNAM, ''), IFNULL(A.MCODE, ''), IFNULL(A.MCODENM, ''), IFNULL(A.MDESC, ''), IFNULL(A.MSEQ, '')"
                           "    , IFNULL(A.GBN, ''), IFNULL(B.RESNAM, ''), IFNULL(A.GBN2, ''), IFNULL(C.RESNAM, ''), IFNULL(A.ACODE, ''), IFNULL(E.RESNAM, '')"
                           "    , IFNULL(A.OPT, ''), IFNULL(A.YUD, ''), IFNULL(F.RESNAM, '') "
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
                           "    LEFT OUTER JOIN OSREFCP F "
                           "    ON A.YUD = F.RESKEY "
                           "    AND F.RECODE = 'YUD' "
                           "    WHERE A.MCODE = '" + mainCode + "' "
                           "    AND A.ICUST = '" + str(iCust) + "'"
                           # "    WHERE MCODE = '" + mainCode + "' "
                           )
            mresult = cursor.fetchall()

        # 상위계정과목
        with connection.cursor() as cursor:
            cursor.execute(" SELECT RESKEY, RESNAM FROM OSREFCP WHERE RECODE = 'MCD' AND RESKEY LIKE '" + str(codeType) + "%' AND ICUST = '" + str(iCust) + "' ")
            cboMCode = cursor.fetchall()

        # 회계계정과목
        with connection.cursor() as cursor:
            cursor.execute(" SELECT RESKEY, RESNAM FROM OSREFCP WHERE RECODE = 'ACD' AND RESKEY LIKE '" + str(codeType) + "%' AND ICUST = '" + str(iCust) + "' ")
            cboACode = cursor.fetchall()

        if codeType != '':
            if codeType == '4':
                # 관리계정과목
                with connection.cursor() as cursor:
                    cursor.execute(" SELECT RESKEY, RESNAM FROM OSREFCP WHERE RECODE = 'REC' AND RESKEY LIKE '4%' AND ICUST = '" + str(iCust) + "' ")
                    cboRecCode = cursor.fetchall()
            if codeType == '5':
                # 관리계정과목
                with connection.cursor() as cursor:
                    cursor.execute(" SELECT RESKEY, RESNAM FROM OSREFCP WHERE RECODE = 'REC' AND RESKEY LIKE '5%' AND ICUST = '" + str(iCust) + "' ")
                    cboRecCode = cursor.fetchall()

        # 구분1
        with connection.cursor() as cursor:
            cursor.execute(" SELECT RESKEY, RESNAM FROM OSREFCP WHERE RECODE = 'CGB' AND ICUST = '" + str(iCust) + "' ")
            gbnesult = cursor.fetchall()

        # 구분2
        with connection.cursor() as cursor:
            cursor.execute(" SELECT RESKEY, RESNAM FROM OSREFCP WHERE RECODE = 'AGB' AND ICUST = '" + str(iCust) + "' ")
            gbn2result = cursor.fetchall()

        # 유동항목
        with connection.cursor() as cursor:
            cursor.execute(" SELECT RESKEY, RESNAM FROM OSREFCP WHERE RECODE = 'YUD' AND ICUST = '" + str(iCust) + "' ")
            cboYud = cursor.fetchall()


        return JsonResponse({"subMList": mresult, 'cboMCode': cboMCode, 'cboACode': cboACode, 'cboRecCode': cboRecCode, 'cboGbn': gbnesult, 'cboGbn2': gbn2result, "cboYud": cboYud})

    else:
        with connection.cursor() as cursor:
            cursor.execute(" SELECT IFNULL(A.MCODE_M, ''), IFNULL(D.RESNAM, ''), IFNULL(A.MCODE, ''), IFNULL(A.MCODENM, ''), IFNULL(A.MSEQ, ''), IFNULL(A.MDESC, '')"
                           "    , IFNULL(A.GBN, ''), IFNULL(B.RESNAM, ''), IFNULL(A.GBN2, ''), IFNULL(C.RESNAM, ''), IFNULL(A.ACODE, ''), IFNULL(E.RESNAM, '')"
                           "    , IFNULL(A.OPT, ''), IFNULL(A.YUD, ''), IFNULL(F.RESNAM, '') "
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
                           "    LEFT OUTER JOIN OSREFCP F "
                           "    ON A.YUD = F.RESKEY "
                           "    AND F.RECODE = 'YUD' "
                           "    WHERE A.MCODE LIKE '" + str(codeType) + "%' AND A.ICUST = '" + str(iCust) + "' ORDER BY MCODE ")
            mresult = cursor.fetchall()
            print(mresult)

        # 상위계정과목
        with connection.cursor() as cursor:
            cursor.execute(" SELECT RESKEY, RESNAM FROM OSREFCP WHERE RECODE = 'MCD' AND RESKEY LIKE '" + str(codeType) + "%' AND ICUST = '" + str(iCust) + "' ")
            cboMCode = cursor.fetchall()

        # 회계계정과목
        with connection.cursor() as cursor:
            cursor.execute(" SELECT RESKEY, RESNAM FROM OSREFCP WHERE RECODE = 'ACD' AND RESKEY LIKE '" + str(codeType) + "%' AND ICUST = '" + str(iCust) + "'")
            cboACode = cursor.fetchall()

        if codeType != '':
            if codeType == '4':
                # 관리계정과목
                with connection.cursor() as cursor:
                    cursor.execute(" SELECT RESKEY, RESNAM FROM OSREFCP WHERE RECODE = 'REC' AND RESKEY LIKE '4%' AND ICUST = '" + str(iCust) + "' ")
                    cboRecCode = cursor.fetchall()
            if codeType == '5':
                # 관리계정과목
                with connection.cursor() as cursor:
                    cursor.execute(" SELECT RESKEY, RESNAM FROM OSREFCP WHERE RECODE = 'REC' AND RESKEY LIKE '5%' AND ICUST = '" + str(iCust) + "' ")
                    cboRecCode = cursor.fetchall()
        # 구분1
        with connection.cursor() as cursor:
            cursor.execute(" SELECT RESKEY, RESNAM FROM OSREFCP WHERE RECODE = 'CGB' AND ICUST = '" + str(iCust) + "'")
            gbnesult = cursor.fetchall()

        # 구분2
        with connection.cursor() as cursor:
            cursor.execute(" SELECT RESKEY, RESNAM FROM OSREFCP WHERE RECODE = 'AGB' AND ICUST = '" + str(iCust) + "'")
            gbn2result = cursor.fetchall()

        # 유동항목
        with connection.cursor() as cursor:
            cursor.execute(" SELECT RESKEY, RESNAM FROM OSREFCP WHERE RECODE = 'YUD' AND ICUST = '" + str(iCust) + "'")
            cboYud = cursor.fetchall()

        return JsonResponse({"mList": mresult, 'cboMCode': cboMCode, 'cboACode': cboACode, 'cboRecCode': cboRecCode, 'cboGbn': gbnesult, 'cboGbn2': gbn2result, "cboYud": cboYud})

def chkcodeM(request):
    codeType = request.POST.get('codeType')
    iCust = request.session.get("USER_ICUST")

    with connection.cursor() as cursor:
        cursor.execute(" SELECT RESKEY, RESNAM FROM OSREFCP WHERE RECODE = 'ACD' AND RESKEY LIKE '" + str(codeType) + "%' AND ICUST = '" + str(iCust) + "' ")
        cboACode = cursor.fetchall()

    return JsonResponse({"cboACode": cboACode})

def chkMCode(request):
    txtCode_M = request.POST.get('txtCode_M')
    iCust = request.session.get("USER_ICUST")

    with connection.cursor() as cursor:
        cursor.execute(" SELECT RESNAM FROM OSREFCP WHERE RECODE = 'ACD' AND RESKEY LIKE '" + str(txtCode_M) + "%' AND ICUST = '" + str(iCust) + "' ")
        cboMCode = cursor.fetchall()

    return JsonResponse({"cboMCode": cboMCode})

def chkCodeViews_search(request):
    mCode = request.POST.get("mCode")

    with connection.cursor() as cursor:
        cursor.execute(" SELECT MCODE FROM OSCODEM WHERE MCODE = '" + mCode + "' ")
        result = cursor.fetchall()
        print(result)

        return JsonResponse({"key": result})


def accountCodeViews_saveM(request):
    codeType = request.POST.get("cboCodeType")
    mCode_M = request.POST.get("mCode_M")
    mCode_A = request.POST.get("mCode_A")
    mCode = request.POST.get("txtCode_M")
    # mCodeNme = request.POST.get("txtCodeNme_M")
    mSeq = request.POST.get("txtSeq_M")
    mDesc = request.POST.get("txtDesc_M")
    gbn = request.POST.get("cboGbn_M")
    gbn2 = request.POST.get("cboGbn2_M")
    opt = request.POST.get("cboOpt")
    yud = request.POST.get("cboYud")
    iCust = request.session.get("USER_ICUST")
    user = request.session.get("userId")

    # 수익4/ 비용5
    with connection.cursor() as cursor:
        cursor.execute(" SELECT COUNT(MCODE) FROM OSCODEM WHERE MCODE = '" + str(mCode) + "' AND ICUST = '" + str(iCust) + "'")
        result = cursor.fetchall()
        count = int(result[0][0])

    if count > 0:
        with connection.cursor() as cursor:
            cursor.execute(" SELECT RESNAM FROM OSREFCP WHERE RECODE = 'REC' AND RESKEY = '" + str(mCode) + "%' AND ICUST = '" + str(iCust) + "'")
            result2 = cursor.fetchall()
            mCodeNme = result2[0][0]

        with connection.cursor() as cursor:
            cursor.execute("    UPDATE OSCODEM SET"
                           "     MCODE_M = '" + str(mCode_M) + "' "
                           "    , ACODE = '" + str(mCode_A) + "' "
                           "    , MCODENM = '" + str(mCodeNme) + "' "
                           "    , MDESC = '" + str(mDesc) + "' "
                           "    , GBN = '" + str(gbn) + "' "
                           "    , GBN2 = '" + str(gbn2) + "' "
                           "    , OPT = '" + str(opt) + "' "
                           "    , YUD = '" + str(yud) + "' "
                           "    , UPD_USER = '" + str(user) + "' "
                           "    , UPD_DT = date_format(now(), '%Y%m%d') "
                           "      WHERE MCODE = '" + str(mCode) + "' "
                           "      AND MSEQ = '" + str(mSeq) + "' "
                           "      AND ICUST = '" + str(iCust) + "' "
                           )
            connection.commit()

            return JsonResponse({'sucYn': "Y"})

    else:

        # for문으로 회계코드 기준으로 만들게 해야함.
        # if mCode_A.startswith('41'):
        #     with connection.cursor() as cursor:
        #         cursor.execute(" SELECT IFNULL(MAX(A.MCODE) + 1, 41001) FROM OSCODEM A WHERE MCODE LIKE '41%' AND ICUST = '" + str(iCust) + "' ")
        #         result = cursor.fetchall()
        #         code = int(result[0][0])
        #         mCode = code
        #
        # if mCode_A.startswith('43'):
        #     with connection.cursor() as cursor:
        #         cursor.execute(" SELECT IFNULL(MAX(A.MCODE) + 1, 43001) FROM OSCODEM A WHERE MCODE LIKE '43%' AND ICUST = '" + str(iCust) + "' ")
        #         result = cursor.fetchall()
        #         code = int(result[0][0])
        #         mCode = code
        #
        # if mCode_A.startswith('51'):
        #     with connection.cursor() as cursor:
        #         cursor.execute(" SELECT IFNULL(MAX(A.MCODE) + 1, 51001) FROM OSCODEM A WHERE MCODE LIKE '51%' AND ICUST = '" + str(iCust) + "' ")
        #         result = cursor.fetchall()
        #         code = int(result[0][0])
        #         mCode = code
        #
        # if mCode_A.startswith('53') or mCode_A.startswith('55'):
        #     with connection.cursor() as cursor:
        #         cursor.execute(" SELECT IFNULL(MAX(A.MCODE) + 1, 53001) FROM OSCODEM A WHERE MCODE LIKE '53%' AND ICUST = '" + str(iCust) + "' ")
        #         result = cursor.fetchall()
        #         code = int(result[0][0])
        #         mCode = code

        # if mCode == '':
        # 비어있으면 튕기게 해야함.
        with connection.cursor() as cursor:
            cursor.execute(" SELECT RESNAM FROM OSREFCP WHERE RECODE = 'REC' AND RESKEY = '" + str(mCode) + "%' AND ICUST = '" + str(iCust) + "'")
            result2 = cursor.fetchall()
            mCodeNme = result2[0][0]

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
                             ",    YUD "
                             ",    CRE_USER "
                             ",    CRE_DT "
                             ",    ICUST "
                             "    ) "
                             "    VALUES "
                             "    (   "
                             "    '" + str(mCode) + "' "
                             ",   '" + str(mCode_M) + "' "
                             ",   '" + str(mCode_A) + "' "
                             ",   (SELECT IFNULL(MAX(A.MSEQ) + 1, 1) AS COUNTED FROM OSCODEM A ) "
                             ",   '" + str(mCodeNme) + "' "
                             ",   '" + str(mDesc) + "' "
                             ",   '" + str(gbn) + "' "
                             ",   '" + str(gbn2) + "' "
                             ",   '" + str(opt) + "' "
                             ",   '" + str(yud) + "' "
                             ",   '" + str(user) + "' "
                             ",   date_format(now(), '%Y%m%d') "
                             ",   '" + str(iCust) + "' "
                             "    )   "
                             )
              connection.commit()

              return JsonResponse({'sucYn': "Y"})




def accountCodeViews_dltM(request):
    iCust = request.session.get("USER_ICUST")

    if request.method == "POST":
        dataList = json.loads(request.POST.get('arrList'))
        print(dataList)
        for code in dataList:
            acc_split_list = code.split(',')
            with connection.cursor() as cursor:
                cursor.execute(" DELETE FROM OSCODEM WHERE MCODE = '" + acc_split_list[0] + "' "
                               "                       AND MSEQ = '" + acc_split_list[1] + "' "
                               "                       AND ICUST = '" + str(iCust) + "'")
                connection.commit()

        return JsonResponse({'sucYn': "Y"})

    else:
        return render(request, 'base/base-actCode-reg.html')
