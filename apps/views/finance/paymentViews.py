import json
import os
from django.shortcuts import render, redirect
from django import template
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader
from django.urls import reverse
from django.contrib import messages
from django.http import JsonResponse
from django.db import connection
from django.core.files.storage import FileSystemStorage



# 출금-수불장
def withRegNewViews(request):

    return render(request, "finance/withdraw-reg-sheet.html")



def receivePay_search(request):
    strDate = request.POST.get('strDate')
    endDate = request.POST.get('endDate')
    cboCust = request.POST.get('cboCust')

    if strDate != '' and endDate != '' and cboCust == '':
        with connection.cursor() as cursor:
            cursor.execute(" SELECT IFNULL(SUM(ACAMTS), 0) FROM SISACCTT WHERE IODATE > '" + strDate + "' ")
            balresult = cursor.fetchall()

        with connection.cursor() as cursor:
            cursor.execute("  SELECT ACIOGB, IODATE, IN_ACAMTS, OUT_ACAMTS, ACCUST, CUST_NME, ACACNUMBER, ACNUM_NAME, MCODE FROM "
                           " ( "
                           "     SELECT A.ACIOGB, A.IODATE, A.ACAMTS AS IN_ACAMTS, 0 AS OUT_ACAMTS, A.ACCUST, B.CUST_NME, A.ACACNUMBER, C.ACNUM_NAME, A.MCODE, A.FIN_OPT "
                           "     FROM SISACCTT A "
                           "     LEFT OUTER JOIN MIS1TB003 B "
                           "     ON A.ACCUST = B.CUST_NBR "
                           "     LEFT OUTER JOIN ACNUMBER C "
                           "     ON A.ACACNUMBER = C.ACNUMBER "
                           "     WHERE A.ACIOGB = '2' "
                           "     UNION ALL "
                           "     SELECT A.ACIOGB, A.IODATE, 0 AS IN_ACAMTS, A.ACAMTS AS OUT_ACAMTS, A.ACCUST, B.CUST_NME, A.ACACNUMBER, C.ACNUM_NAME, A.MCODE, A.FIN_OPT "
                           "     FROM SISACCTT A "
                           "     LEFT OUTER JOIN MIS1TB003 B "
                           "     ON A.ACCUST = B.CUST_NBR "
                           "     LEFT OUTER JOIN ACNUMBER C "
                           "     ON A.ACACNUMBER = C.ACNUMBER "
                           "     WHERE A.ACIOGB = '1' "
                           " ) AA "
                           " WHERE AA.IODATE BETWEEN '" + strDate + "' AND '" + endDate + "' "
                           " ORDER BY AA.IODATE ")
            mainresult = cursor.fetchall()

            # 거래처
            with connection.cursor() as cursor:
                cursor.execute(" SELECT CUST_NBR, CUST_NME FROM MIS1TB003 ORDER BY CUST_NBR ")
                cboCust = cursor.fetchall()

            return JsonResponse({'balList': balresult, 'mainList': mainresult, 'cboCust': cboCust})

    elif cboCust:
        with connection.cursor() as cursor:
            cursor.execute(" SELECT IFNULL(SUM(ACAMTS), 0) FROM SISACCTT WHERE IODATE > '" + strDate + "' AND ACCUST = '" + cboCust + "' ")
            balresult = cursor.fetchall()

        with connection.cursor() as cursor:
            cursor.execute("  SELECT ACIOGB, IODATE, IN_ACAMTS, OUT_ACAMTS, ACCUST, CUST_NME, ACACNUMBER, ACNUM_NAME, MCODE FROM "
                           " ( "
                           "     SELECT A.ACIOGB, A.IODATE, A.ACAMTS AS IN_ACAMTS, 0 AS OUT_ACAMTS, A.ACCUST, B.CUST_NME, A.ACACNUMBER, C.ACNUM_NAME, A.MCODE "
                           "     FROM SISACCTT A "
                           "     LEFT OUTER JOIN MIS1TB003 B "
                           "     ON A.ACCUST = B.CUST_NBR "
                           "     LEFT OUTER JOIN ACNUMBER C "
                           "     ON A.ACACNUMBER = C.ACNUMBER "
                           "     WHERE A.ACIOGB = '2' "
                           "     UNION ALL "
                           "     SELECT A.ACIOGB, A.IODATE, 0 AS IN_ACAMTS, A.ACAMTS AS OUT_ACAMTS, A.ACCUST, B.CUST_NME, A.ACACNUMBER, C.ACNUM_NAME, A.MCODE "
                           "     FROM SISACCTT A "
                           "     LEFT OUTER JOIN MIS1TB003 B "
                           "     ON A.ACCUST = B.CUST_NBR "
                           "     LEFT OUTER JOIN ACNUMBER C "
                           "     ON A.ACACNUMBER = C.ACNUMBER "
                           "     WHERE A.ACIOGB = '1' "
                           " ) AA "
                           " WHERE AA.IODATE BETWEEN '" + strDate + "' AND '" + endDate + "' "
                           " AND AA.ACCUST = '" + cboCust + "' "
                           " ORDER BY AA.IODATE ")
            mainresult = cursor.fetchall()

        return JsonResponse({'balList': balresult, 'mainList': mainresult})

def apvLine_modal_search(request):
    empList = json.loads(request.POST.get('empList'))
    cboDpt = request.POST.get('cboDpt')

    if empList:
        for emp in empList:
            acc_split_list = emp.split(',')
            with connection.cursor() as cursor:
                cursor.execute(" SELECT EMP_DEPT, EMP_GBN, EMP_NBR, EMP_NME "
                               " FROM PIS1TB001 "
                               " WHERE EMP_DEPT = '" + acc_split_list[0] + "' AND EMP_GBN = '" + acc_split_list[1] + "' AND EMP_NBR = '" + acc_split_list[2] + "' ")
                subresult = cursor.fetchall()

                return JsonResponse({'subList': subresult})

    if cboDpt:
        with connection.cursor() as cursor:
            cursor.execute(" SELECT A.EMP_DEPT, B.RESNAM, A.EMP_GBN, C.RESNAM, A.EMP_NBR, A.EMP_NME "
                           " FROM PIS1TB001 A "
                           " LEFT OUTER JOIN OSREFCP B "
                           " ON A.EMP_DEPT = B.RESKEY "
                           " AND B.RECODE = 'DPT' "
                           " LEFT OUTER JOIN OSREFCP C "
                           " ON A.EMP_GBN = C.RESKEY "
                           " AND C.RECODE = 'JJO' "
                           " WHERE C.RESKEY LIKE '3%' "
                           " AND A.EMP_DEPT = '" + cboDpt + "' ")
            mainresult = cursor.fetchall()

            return JsonResponse({'mainList': mainresult})

    else:
        with connection.cursor() as cursor:
            cursor.execute(" SELECT A.EMP_DEPT, B.RESNAM, A.EMP_GBN, C.RESNAM, A.EMP_NBR, A.EMP_NME "
                           " FROM PIS1TB001 A "
                           " LEFT OUTER JOIN OSREFCP B "
                           " ON A.EMP_DEPT = B.RESKEY "
                           " AND B.RECODE = 'DPT' "
                           " LEFT OUTER JOIN OSREFCP C "
                           " ON A.EMP_GBN = C.RESKEY "
                           " AND C.RECODE = 'JJO' "
                           " WHERE C.RESKEY LIKE '3%' ")
            mainresult = cursor.fetchall()

            with connection.cursor() as cursor:
                cursor.execute(" SELECT RESKEY, RESNAM FROM OSREFCP WHERE RECODE = 'DPT' ORDER BY RESKEY ")
                cboDpt = cursor.fetchall()

            return JsonResponse({'mainList': mainresult, "cboDpt": cboDpt})

# def apvLine_modal_save(request):
#     empArray = json.loads(request.POST.get('empArrList'))
#
#     empArrayLists = list(filter(len, empArray))
#     for data in range(len(empArrayLists)):
#         with connection.cursor() as cursor:
#             cursor.execute("SELECT SEQ FROM tmpsign WHERE EMP_GBN = '" + empArrayLists[data]["fixCode"] + "' AND EMP_NBR = '" + empArrayLists[data]["empNbr"] + "' ")
#             empresult = cursor.fetchall()
#
#             if empresult:
#                 seq = empresult[0][0]
#
#                 with connection.cursor() as cursor:
#                     cursor.execute(" UPDATE tmpsign SET "
#                                     "   EMP_DPT = '" + empArrayLists[data]["empDpt"] + "' "
#                                     " , EMP_GBN = '" + empArrayLists[data]["empGbn"] + "' "
#                                     " , EMP_NBR = '" + empArrayLists[data]["empNbr"] + "' "
#                                     " , EMP_NME = '" + empArrayLists[data]["empNme"] + "' "
#                                     " WHERE SEQ = '" + seq + "' ")
#                     connection.commit()
#
#             else:
#                 with connection.cursor() as cursor:
#                     cursor.execute(" INSERT INTO tmpsign "
#                                   " ( "
#                                   "   SEQ "
#                                   " , EMP_DPT "
#                                   " , EMP_GBN "
#                                   " , EMP_NBR "
#                                   " , EMP_NME "
#                                   " ) "
#                                   "  VALUES "
#                                   " ( "
#                                   "  (SELECT IFNULL (LPAD(MAX(A.SEQ + 1), '4', '0'), 0001) AS COUNTED FROM tmpsign A) "
#                                   " ,'" + empArrayLists[data]["empDpt"] + "' "
#                                   " ,'" + empArrayLists[data]["empGbn"] + "' "
#                                   " ,'" + empArrayLists[data]["empNbr"] + "' "
#                                   " ,'" + empArrayLists[data]["empNme"] + "' "
#                                   " ) "
#                                   )
#                     connection.commit()
#
#     with connection.cursor() as cursor:
#         cursor.execute("SELECT SEQ, EMP_DPT, EMP_GBN, EMP_NBR, EMP_NME FROM tmpsign ORDER BY SEQ ASC ")
#         empresult = cursor.fetchall()
#
#     return JsonResponse({'arrList': "Y", 'empList': empresult})


def paymentViews_search(request):
    acIogb = request.POST.get('acIogb')
    ioDate = request.POST.get('ioDate')
    acNum = request.POST.get('acNum')
    acCust = request.POST.get('acCust')
    acMcode = request.POST.get('acMcode')
    cboGbn = request.POST.get('cboGbn')
    cboCard = request.POST.get('cboCard')

    if cboCard:
        # 거래처
        with connection.cursor() as cursor:
            cursor.execute(" SELECT ACNUMBER FROM ACCARD WHERE CARDNUM = '" + cboCard + "' ")
            cboActNum = cursor.fetchall()

            return JsonResponse({'cboActNum': cboActNum})

    if acIogb:
        with connection.cursor() as cursor:
            # 거래처구분/명/행/결제방법명/결제방법코드/입출금구분/계정/금액/순번/날짜/계좌번호
            cursor.execute(" SELECT IFNULL(A.ACSEQN,''), IFNULL(A.ACCUST, ''), IFNULL(B.CUST_NME, '') "
                           "    , IFNULL(A.ACRECN,''), IFNULL(A.ACGUBN,''), IFNULL(C.RESNAM,'') "
                           "    , IFNULL(A.ACIOGB,''), IFNULL(E.RESNAM, ''), IFNULL(A.MCODE,''), IFNULL(D.MCODENM, '') "
                           "    , IFNULL(A.ACAMTS, 0), IFNULL(A.IODATE,''), IFNULL(A.ACACNUMBER,'') "
                           "    , IFNULL(A.ACGUNO_BK,''), IFNULL(F.RESNAM, '') , IFNULL(A.ACBUNHO,''), IFNULL(A.ACGUNO_DT,'')"
                           "    , IFNULL(A.ACCODE,''), IFNULL(G.ACODENM, ''), IFNULL(A.ACDESC, ''), IFNULL(A.EXDATE,''), IFNULL(A.ACTITLE,'')"
                           "    , IFNULL(A.ACFOLDER,''), IFNULL(A.ACCARD, '') "
                           "    FROM SISACCTT A "
                           "    LEFT OUTER JOIN MIS1TB003 B "
                           "    ON A.ACCUST = B.CUST_NBR "
                           "    LEFT OUTER JOIN OSREFCP C "
                           "    ON A.ACGUBN = C.RESKEY "
                           "    AND C.RECODE = 'OUB' "
                           "    LEFT OUTER JOIN OSCODEM D "
                           "    ON A.MCODE = D.MCODE "
                           "    LEFT OUTER JOIN OSCODEA G "
                           "    ON A.ACCODE = G.ACODE "
                           "    LEFT OUTER JOIN OSREFCP E "
                           "    ON A.ACIOGB = E.RESKEY "
                           "    AND E.RECODE = 'OUA' "
                           "    LEFT OUTER JOIN OSREFCP F "
                           "    ON A.ACGUNO_BK = F.RESKEY "
                           "    AND F.RECODE = 'BNK' "
                           "    WHERE A.IODATE = '" + ioDate + "' "
                           "    AND A.ACIOGB = '" + acIogb + "' "
                           "    AND A.ACACNUMBER = '" + acNum + "' "
                           "    AND A.ACCUST = '" + acCust + "'"
                           "    AND A.MCODE = '" + acMcode + "' ")
            subresult = cursor.fetchall()
            print(subresult)

            # 거래처
            with connection.cursor() as cursor:
                cursor.execute(" SELECT CUST_NBR, CUST_NME FROM MIS1TB003 ")
                cboCust = cursor.fetchall()

            # 입출금구분
            with connection.cursor() as cursor:
                cursor.execute(" SELECT RESKEY, RESNAM FROM OSREFCP WHERE RECODE = 'OUA' ORDER BY RESKEY ")
                cboGgn = cursor.fetchall()

            # 관리계정
            with connection.cursor() as cursor:
                cursor.execute(" SELECT MCODE, MCODENM FROM OSCODEM ORDER BY MCODE ASC ")
                cboMCode = cursor.fetchall()

            # 회계게정
            with connection.cursor() as cursor:
                cursor.execute(" SELECT ACODE, ACODENM FROM OSCODEA ORDER BY ACODE ASC ")
                cboACode = cursor.fetchall()

            # 결제방법
            with connection.cursor() as cursor:
                cursor.execute(" SELECT RESKEY, RESNAM FROM OSREFCP WHERE RECODE = 'PGB' ORDER BY RESNAM ")
                cboPay = cursor.fetchall()

            # 계좌번호
            with connection.cursor() as cursor:
                cursor.execute(" SELECT ACNUMBER FROM ACNUMBER ")
                cboAcnumber = cursor.fetchall()

            # 카드번호
            with connection.cursor() as cursor:
                cursor.execute(" SELECT CARDNUM FROM ACCARD ")
                cboCard = cursor.fetchall()

        return JsonResponse({'subList': subresult, 'cboCust': cboCust, 'cboGgn': cboGgn
                                , 'cboMCode': cboMCode, 'cboPay': cboPay, 'cboAcnumber': cboAcnumber, 'cboCard': cboCard})

    # 출금
    if cboGbn == '1':
        # 거래처
        with connection.cursor() as cursor:
            cursor.execute(" SELECT CUST_NBR, CUST_NME FROM MIS1TB003 WHERE CUST_GBN LIKE '1' AND '3'")
            cboCust = cursor.fetchall()

        # 입출금구분
        with connection.cursor() as cursor:
            cursor.execute(" SELECT RESKEY, RESNAM FROM OSREFCP WHERE RECODE = 'OUA' ORDER BY RESKEY ")
            cboGgn = cursor.fetchall()

        # 관리계정
        with connection.cursor() as cursor:
            cursor.execute(" SELECT MCODE, MCODENM FROM OSCODEM WHERE MCODE LIKE '5%' ORDER BY MCODE ASC ")
            cboMCode = cursor.fetchall()

        # 회계게정
        with connection.cursor() as cursor:
            cursor.execute(" SELECT ACODE, ACODENM FROM OSCODEA ORDER BY ACODE ASC ")
            cboACode = cursor.fetchall()

        # 결제방법
        with connection.cursor() as cursor:
            cursor.execute(" SELECT RESKEY, RESNAM FROM OSREFCP WHERE RECODE = 'PGB' ORDER BY RESNAM ")
            cboPay = cursor.fetchall()

        # 계좌번호
        with connection.cursor() as cursor:
            cursor.execute(" SELECT ACNUMBER FROM ACNUMBER ")
            cboAcnumber = cursor.fetchall()

        # 카드번호
        with connection.cursor() as cursor:
            cursor.execute(" SELECT CARDNUM FROM ACCARD ")
            cboCard = cursor.fetchall()

        return JsonResponse(
            {'cboCust': cboCust, 'cboGgn': cboGgn, 'cboMCode': cboMCode, 'cboPay': cboPay, 'cboAcnumber': cboAcnumber, 'cboCard': cboCard})

    # 입금
    else:
        # 거래처
        with connection.cursor() as cursor:
            cursor.execute(" SELECT CUST_NBR, CUST_NME FROM MIS1TB003 WHERE CUST_GBN LIKE '2' AND '3' ")
            cboCust = cursor.fetchall()

        # 입출금구분
        with connection.cursor() as cursor:
            cursor.execute(" SELECT RESKEY, RESNAM FROM OSREFCP WHERE RECODE = 'OUA' ORDER BY RESKEY ")
            cboGgn = cursor.fetchall()

        # 관리계정
        with connection.cursor() as cursor:
            cursor.execute(" SELECT MCODE, MCODENM FROM OSCODEM WHERE MCODE LIKE '4%' ORDER BY MCODE ASC ")
            cboMCode = cursor.fetchall()

        # 회계게정
        with connection.cursor() as cursor:
            cursor.execute(" SELECT ACODE, ACODENM FROM OSCODEA ORDER BY ACODE ASC ")
            cboACode = cursor.fetchall()

        # 결제방법
        with connection.cursor() as cursor:
            cursor.execute(" SELECT RESKEY, RESNAM FROM OSREFCP WHERE RECODE = 'PGB' ORDER BY RESNAM ")
            cboPay = cursor.fetchall()

        # 계좌번호
        with connection.cursor() as cursor:
            cursor.execute(" SELECT ACNUMBER FROM ACNUMBER ")
            cboAcnumber = cursor.fetchall()

        # 카드번호
        with connection.cursor() as cursor:
            cursor.execute(" SELECT CARDNUM FROM ACCARD ")
            cboCard = cursor.fetchall()

        return JsonResponse({'cboCust': cboCust, 'cboGgn': cboGgn, 'cboMCode': cboMCode, 'cboPay': cboPay, 'cboAcnumber': cboAcnumber, 'cboCard': cboCard})


def paymentViews_save(request):
    empArray = json.loads(request.POST.get('empArrList'))
    ioDate = request.POST.get("txtWitRegDate").replace('-', '') # 등록일자
    exDate = request.POST.get("txtExDate").replace('-', '')
    acSeqn = request.POST.get("txtWitSeq")               # 순번
    acTitle = request.POST.get("txtTitle")
    acRecn = request.POST.get("txtWitRecn")
    acCust = request.POST.get("cboWitCust")     # 거래처
    acIogb = request.POST.get("cboWitGbn")  # 구분(입금2/출금1)
    mCode = request.POST.get("cboAdminCode")  # 관리계정
    acCode = request.POST.get("cboActCode")  # 회계계정
    acAmts = request.POST.get("txtWitPrice")      # 금액
    acAcnumber = request.POST.get("cboWitActNum")     # 계좌번호
    acGubn = request.POST.get("cboWitMethod")     # 결제방법
    acCard = request.POST.get("cboWitCard")
    acDesc = request.POST.get("txtWitRemark")     # 비고
    creUser = request.session.get("userId")
    iCust = request.session.get("USER_ICUST")

    file = request.FILES.get('file')

    if (file is None):
        file = ''
    url = '/media/'

    if file is None or not None:
        if len(request.FILES) != 0:
            myfile = request.FILES['file']
            fs = FileSystemStorage()
            filename = fs.save(myfile.name, myfile)
            Rfilenameloc = url + filename

        else:
            Rfilenameloc = file


    with connection.cursor() as cursor:
        cursor.execute(" SELECT ACBKCD FROM ACNUMBER WHERE ACNUMBER = '" + acAcnumber + "' ")
        result = cursor.fetchall()  # 계좌 은행

        bnk = result[0][0]

    if exDate == '' or exDate is None:
        exDate = ioDate

    if acSeqn == '' or acSeqn is None:
        with connection.cursor() as cursor:
            cursor.execute("INSERT INTO SISACCTT "
                           "   (    "
                           "     IODATE "
                           ",    ACSEQN "
                           ",    ACIOGB "
                           ",    ACTITLE "
                           ",    ACCUST "
                           ",    ACGUBN "
                           ",    MCODE "
                           ",    ACCODE "
                           ",    ACAMTS "
                           ",    ACACNUMBER "
                           ",    ACRECN "
                           ",    ACDESC "
                           ",    CRE_USER "
                           ",    CRE_DT "
                           ",    ICUST "
                           ",    ACGUNO_BK "
                           ",    ACFOLDER "
                           ",    EXDATE "
                           ",    ACCARD "
                           "    ) "
                           "    VALUES "
                           "    (   "
                           "    '" + str(ioDate) + "'"
                           ",   (SELECT IFNULL (MAX(ACSEQN) + 1,1) AS COUNTED FROM SISACCTT A WHERE ACDATE = '" + ioDate + "' AND ACIOGB = '" + acIogb + "') "
                           ",   '" + str(acIogb) + "'"
                           ",   '" + str(acTitle) + "'"
                           ",   '" + str(acCust) + "'"
                           ",   '" + str(acGubn) + "'"
                           ",   '" + str(mCode) + "'"
                           ",   '" + str(acCode) + "'"
                           ",   '" + str(acAmts) + "'"
                           ",   '" + str(acAcnumber) + "'"
                           ",   (SELECT IFNULL (MAX(ACRECN) + 1,1) AS COUNTED FROM SISACCTT A WHERE ACDATE = '" + ioDate + "' AND ACIOGB = '" + acIogb + "' AND ACSEQN = '" + acSeqn + "' ) "
                           ",   '" + str(acDesc) + "'"
                           ",   '" + str(creUser) + "'"
                           ",   date_format(now(), '%Y%m%d') "
                           ",   '" + str(iCust) + "'"
                           ",   '" + str(bnk) + "'"
                           ",   '" + str(Rfilenameloc) + "'"
                           "    '" + str(exDate) + "'"
                           "    '" + str(acCard) + "'"
                           "    )   "
                           )
            connection.commit()

            with connection.cursor() as cursor:
                cursor.execute(" SELECT MAX(ACSEQN) FROM SISACCTT WHERE IODATE = '" + str(ioDate).replace('-', '') + "' AND ACIOGB = '" + str(acIogb) + "' ")
                result2 = cursor.fetchall()  # 계좌 은행

                seq = result2[0][0]

            # 들어오는 순서대로 emp_nbr(순번)으로 데이터 넣어주기
            opt = 'N'
            empArrayLists = list(filter(len, empArray))
            for data in range(len(empArrayLists)):
                with connection.cursor() as cursor:
                    cursor.execute(" INSERT INTO OSSIGN "
                                   "    ( "
                                   "     ACDATE "
                                   "   , ACSEQN "
                                   "   , SEQ "
                                   "   , EMP_NBR "
                                   "   , OPT "
                                   "   , ACIOGB "
                                   "   , ICUST "                                                    
                                   "    ) "
                                   "    VALUES "
                                   "    ( "
                                   "     '" + str(exDate) + "' "
                                   "     , '" + str(seq) + "' "
                                   "     , ( SELECT IFNULL (MAX(SEQ) + 1,1) AS COUNTED FROM OSSIGN A WHERE ACDATE = '" + str(ioDate) + "' AND ACSEQN = '" + str(seq) + "' ) "
                                   "     , '" + empArrayLists[data]["empNbr"] + "' "
                                   "     , '" + opt + "' "
                                   "     , '" + str(acIogb) + "' "
                                   "     , '" + str(iCust) + "' "
                                   "     ) "
                    )
                    connection.commit()

        return JsonResponse({'sucYn': "Y"})

    elif acSeqn:
        with connection.cursor() as cursor:
            cursor.execute("    UPDATE  SISACCTT SET"
                           "     ACGUBN = '" + str(acGubn) + "' "
                           ",    MCODE = '" + str(mCode) + "' "
                           ",    ACCODE = '" + str(acCode) + "' "
                           ",    ACTITLE = '" + str(acTitle) + "' "
                           ",    ACAMTS = '" + str(acAmts) + "' "
                           ",    ACACNUMBER = '" + str(acAcnumber) + "' "
                           ",    ACDESC = '" + str(acDesc) + "' "
                           ",    ACGUNO_BK = '" + str(bnk) + "' "
                           ",    ACFOLDER = '" + str(Rfilenameloc) + "' "
                           ",    EXDATE = '" + str(exDate) + "' "
                           ",    ACCARD = '" + str(acCard) + "' "
                           ",    UPD_USER = '" + str(creUser) + "' "
                           ",    UPD_DT = date_format(now(), '%Y%m%d') "
                           "     WHERE acdate = '" + str(ioDate) + "' "
                           "     AND ACIOGB = '" + str(acIogb) + "' "
                           "     AND ACCUST = '" + str(acCust) + "' "
                           "     AND ACSEQN = '" + str(acSeqn) + "' "
                           "     AND ICUST = '" + str(iCust) + "' "
                           )
            connection.commit()

        return JsonResponse({'sucYn': "Y"})

#
# return render(request, 'finance/withdraw-reg-sheet.html')


def paymentViews_dlt(request):
    if request.method == "POST":
        dataList = json.loads(request.POST.get('arrList'))
        print(dataList)
        for cust in dataList:
            acc_split_list = cust.split(',')
            with connection.cursor() as cursor:
                cursor.execute(" DELETE FROM SISACCTT WHERE ACSEQN = '" + acc_split_list[0] + "'"
                               "                      AND ACIOGB = '" + acc_split_list[1] + "' "
                               "                      AND IODATE = '" + acc_split_list[2] + "'"
                               "                      AND ACACNUMBER = '" + acc_split_list[3] + "' "
                               "                      AND ACCUST = '" + acc_split_list[4] + "' "
                               "                      AND MCODE = '" + acc_split_list[5] + "' ")
                connection.commit()

        return JsonResponse({'sucYn': "Y"})

    else:
        return render(request, 'finance/withdraw-reg-sheet.html')


def checkLimit_search(request):
    price = request.POST.get('price')
    date = request.POST.get('date')
    userId = request.session.get('userId')
    iCust = request.session.get('USER_ICUST')

    with connection.cursor() as cursor:
        cursor.execute(" SELECT EMP_LIMIT FROM PIS1TB001 WHERE EMP_NBR = '" + userId + "' AND ICUST = '" + iCust + "' ")
        result = cursor.fetchall()

        limit = result[0][0]

    with connection.cursor() as cursor:
        cursor.execute(" SELECT IFNULL(SUM(ACAMTS), 0) FROM SISACCTT WHERE CRE_USER = '" + userId + "' AND SUBSTRING(IODATE, 0, 6) = '" + date + "' AND ACIOGB = '1' AND ICUST = '" + iCust + "' ")
        result2 = cursor.fetchall()

        spent = result2[0][0]

        if int(limit) >= int(price) + int(spent):
            YN = 'Y'

        elif int(limit) < int(price) + int(spent):
            YN = 'N'

        return JsonResponse({'YN': YN})