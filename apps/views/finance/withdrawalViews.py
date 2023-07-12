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


def withRegViews(request):

    return render(request, "finance/withdrawal-reg.html")

def withRegViews_search(request):
    date = request.POST.get('date')
    year = request.POST.get('inputYear')
    month = request.POST.get('inputMonth')

    if date != '' and date is not None:
        with connection.cursor() as cursor:
            # 거래처구분/명/행/결제방법명/결제방법코드/입출금구분/계정/금액/순번/날짜/계좌번호
            cursor.execute(" SELECT IFNULL(A.ACSEQN,''), IFNULL(A.ACCUST, ''), IFNULL(B.CUST_NME, '') "
                           "    , IFNULL(A.ACRECN,''), IFNULL(A.ACGUBN,''), IFNULL(C.RESNAM,'') "
                           "    , IFNULL(A.ACIOGB,''), IFNULL(E.RESNAM, ''), IFNULL(A.ACCODE,''), IFNULL(D.RESNAM, '') "
                           "    , IFNULL(A.ACAMTS, 0), IFNULL(A.ACDATE,''), IFNULL(A.ACACNUMBER,'') "
                           "    , IFNULL(A.ACGUNO_BK,''), IFNULL(F.RESNAM, '') , IFNULL(A.ACBUNHO,''), IFNULL(A.ACGUNO_DT,'') "
                           "    FROM SISACCTT A "
                           "    LEFT OUTER JOIN MIS1TB003 B "
                           "    ON A.ACCUST = B.CUST_NBR "
                           "    LEFT OUTER JOIN OSREFCP C "
                           "    ON A.ACGUBN = C.RESKEY "
                           "    AND C.RECODE = 'OUB' "
                           "    LEFT OUTER JOIN OSREFCP D "
                           "    ON A.ACCODE = D.RESKEY "
                           "    AND D.RECODE = 'ACC' "
                           "    LEFT OUTER JOIN OSREFCP E "
                           "    ON A.ACIOGB = E.RESKEY "
                           "    AND E.RECODE = 'OUA' "
                           "    LEFT OUTER JOIN OSREFCP F "
                           "    ON A.ACGUNO_BK = F.RESKEY "
                           "    AND F.RECODE = 'BNK' "
                           "    WHERE A.ACDATE = '" + str(date) + "'"
                           "    AND A.ACIOGB = '1' "
                           "    ORDER BY A.ACSEQN ")
            subresult = cursor.fetchall()
        return JsonResponse({"subList": subresult})

    else:
        with connection.cursor() as cursor:
            cursor.execute(" SELECT IFNULL(ACDATE, ''), IFNULL(DAY(ACDATE), '') "
                           "    , IFNULL(SUM(ACAMTS), 0), IFNULL(ACIOGB, '') "
                           "    FROM SISACCTT  "
                           "    WHERE ACIOGB = '1' "
                           "    AND YEAR(ACDATE) = '" + str(year) + "' "
                           "    AND MONTH(ACDATE) = '" + str(month) + "' "
                           "    GROUP BY DAY(ACDATE) ")
            mainresult = cursor.fetchall()

        return JsonResponse({"mainList": mainresult})


def withRegViews_save(request):
    if 'btnSave' in request.POST:
        acDate = request.POST.get("txtWitRegDate").replace('-', '')   # 등록일자
        acSeqn = request.POST.get("txtWitSeq")               # 순번
        acRecn = '1' # 행
        acCust = request.POST.get("cboWitCust")     # 거래처
        acIogb = request.POST.get("cboWitGbn")     # 구분(출금)
        acCode = request.POST.get("cboWitCode")  # 계정과목
        acAmts = request.POST.get("txtWitPrice")      # 금액
        acAcnumber = request.POST.get("cboWitActNum")     # 계좌번호
        acGubn = request.POST.get("cboWitMethod")     # 결제방법
        acDesc = request.POST.get("txtWitRemark")     # 비고
        acbunho = request.POST.get("txtWitCashNum")     # 어음번호
        acguno_dt = request.POST.get("txtWitCashNum")     # 만기일자
        acIuser = '101'
        acIdate = acDate.replace('-', '')
        acUuser = '101'

        with connection.cursor() as cursor:
            cursor.execute(" SELECT ACBKCD FROM ACNUMBER WHERE ACNUMBER = '" + acAcnumber + "' ")
            result = cursor.fetchall()  # 계좌 은행

            bnk = result[0][0]

        if acSeqn == '' or acSeqn is None:
            with connection.cursor() as cursor:
                cursor.execute("INSERT INTO SISACCTT "
                               "   (    "
                               "     ACDATE "
                               ",    ACSEQN "
                               ",    ACIOGB "
                               ",    ACCUST "
                               ",    ACGUBN "
                               ",    ACCODE "
                               ",    ACAMTS "
                               ",    ACACNUMBER "
                               ",    ACRECN "
                               ",    ACDESC "
                               ",    IUSER "
                               ",    IDATE "
                               ",    ACBUNHO "
                               ",    ACGUNO_DT "
                               ",    ACGUNO_BK "
                               "    ) "
                               "    VALUES "
                               "    (   "
                               "    '" + str(acDate).replace('-', '') + "'"
                               ",   (SELECT IFNULL (MAX(ACSEQN) + 1,1) AS COUNTED FROM SISACCTT A WHERE ACDATE = '" + acDate + "' AND ACIOGB = '" + acIogb + "')"
                               ",   '1'"
                               ",   '" + str(acCust) + "'"
                               ",   '" + str(acGubn) + "'"
                               ",   '" + str(acCode) + "'"
                               ",   '" + str(acAmts) + "'"
                               ",   '" + str(acAcnumber) + "'"
                               ",   '" + str(acRecn) + "'"
                               ",   '" + str(acDesc) + "'"
                               ",   '" + str(acIuser) + "'"
                               ",   '" + str(acIdate) + "'"
                               ",   '" + str(acbunho) + "'"
                               ",   '" + str(acguno_dt) + "'"
                               ",   '" + str(bnk) + "'"
                               "    )   "
                               )
                connection.commit()

                messages.success(request, '저장 되었습니다.')
                return redirect('/with_reg')

        elif acSeqn:
            with connection.cursor() as cursor:
                cursor.execute("    UPDATE  SISACCTT SET"
                               "     ACCUST = '" + str(acCust) + "' "
                               ",    ACGUBN = '" + str(acGubn) + "' "
                               ",    ACCODE = '" + str(acCode) + "' "
                               ",    ACAMTS = '" + str(acAmts) + "' "
                               ",    ACACNUMBER = '" + str(acAcnumber) + "' "
                               ",    ACRECN = '" + str(acRecn) + "' "
                               ",    ACDESC = '" + str(acDesc) + "' "
                               ",    ACBUNHO = '" + str(acbunho) + "' "
                               ",    ACGUNO_DT = '" + str(acguno_dt) + "' "
                               ",    ACGUNO_BK = '" + str(bnk) + "' "
                               ",    UUSER = '" + str(acUuser) + "' "
                               ",    UDATE = date_format(now(), '%Y%m%d') "
                               "     WHERE ACDATE = '" + str(acDate) + "' "
                               "     AND ACSEQN = '" + str(acSeqn) + "' "
                               "     AND ACIOGB = '" + str(acIogb) + "' "
                               )
                connection.commit()

                messages.success(request, '수정 되었습니다.')
                return redirect('/with_reg')

        else:
            messages.warning(request, '입력 하신 정보를 확인 해주세요.')
            return redirect('/with_reg')

    return render(request, 'finance/withdrawal-reg.html')



def withRegViews_dlt(request):
    if request.method == "POST":
        date = request.POST.get("date")
        seq = request.POST.get("seq")
        custCode = request.POST.get("custCode")
        iogb = request.POST.get("iogb")

        with connection.cursor() as cursor:
            cursor.execute(" DELETE FROM SISACCTT WHERE ACDATE = '" + date+ "' "
                           "                        AND ACSEQN = '" + seq + "' "
                           "                        AND ACIOGB = '" + iogb + "' "
                           "                        AND ACCUST = '" + custCode + "' ")
            connection.commit()

        return JsonResponse({'sucYn': "Y"})

    else:
        return render(request, 'finance/withdrawal-reg.html')


# 모달 조회
def withRegOutList_search(request):
    year = request.POST.get('inputYear')
    month = request.POST.get('inputMonth')
    upCode = request.POST.get('custCode')
    seq = request.POST.get('seq')
    date = request.POST.get('date')

    if seq != '' and seq is not None:
        # 순번, 거래처, 거래처명, 행번, 결제발벙, 입/출금구분, 계정과목, 금액, 등록일자, 계좌번호, 은행번호, 어음번호, 어음만료일, 비고
        with connection.cursor() as cursor:
            cursor.execute(" SELECT IFNULL(A.ACSEQN,''), IFNULL(A.ACCUST, ''), IFNULL(B.CUST_NME, '') "
                           "    , IFNULL(A.ACRECN,''), IFNULL(A.ACGUBN,''), IFNULL(C.RESNAM,'') "
                           "    , IFNULL(A.ACIOGB,''), IFNULL(E.RESNAM, ''), IFNULL(A.MCODE,''), IFNULL(D.MCODENM, '') "
                           "    , IFNULL(A.ACAMTS, 0), IFNULL(A.ACDATE,''), IFNULL(A.ACACNUMBER,'')"
                           "    , IFNULL(A.ACGUNO_BK,''), IFNULL(F.RESNAM, '') , IFNULL(A.ACBUNHO,''), IFNULL(A.ACGUNO_DT,'')"
                           "    , IFNULL(A.ACDESC,''), IFNULL(A.ACCODE,''), IFNULL(D.ACODENM, '')  "
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
                           "    WHERE A.ACIOGB = '1' "
                           "    AND A.ACCUST = '" + str(upCode) + "'"
                           "    AND A.ACDATE = '" + str(date) + "'"
                           "    AND A.ACSEQN = '" + str(seq) + "'")
            modalform = cursor.fetchall()

        # 거래처
        with connection.cursor() as cursor:
            cursor.execute(" SELECT CUST_NBR, CUST_NME FROM MIS1TB003 WHERE CUST_GBN = '1' ")
            cboCust = cursor.fetchall()

        # 입출금구분
        with connection.cursor() as cursor:
            cursor.execute(" SELECT RESKEY, RESNAM FROM OSREFCP WHERE RECODE = 'OUA' AND RESKEY = '1' ORDER BY RESNAM ")
            cboGgn = cursor.fetchall()

        # 관리계정
        with connection.cursor() as cursor:
            cursor.execute(" SELECT MCODE, MCODENM FROM OSCODEM ")
            cboMCode = cursor.fetchall()

        # 회계게정
        with connection.cursor() as cursor:
            cursor.execute(" SELECT ACODE, ACODENM FROM OSCODEA ")
            cboACode = cursor.fetchall()

        # 결제방법
        with connection.cursor() as cursor:
            cursor.execute(" SELECT RESKEY, RESNAM FROM OSREFCP WHERE RECODE = 'OUB' ORDER BY RESNAM ")
            cboPay = cursor.fetchall()

        # 계좌번호
        with connection.cursor() as cursor:
            cursor.execute(" SELECT ACNUMBER FROM ACNUMBER ")
            cboAcnumber = cursor.fetchall()

        return JsonResponse({'modalform': modalform
                              , 'cboCust': cboCust, 'cboGgn': cboGgn, 'cboMCode': cboMCode, 'cboACode': cboACode
                              ,'cboPay': cboPay, "cboAcnumber": cboAcnumber})
    else:
        # with connection.cursor() as cursor:
        #     cursor.execute(" SELECT IFNULL(A.BAL_DD, ''), IFNULL(A.UP_CODE, ''), IFNULL(B.CUST_NME, '') "
        #                    "    , IFNULL(A.ITEM, ''), IFNULL(A.AMTS, 0), IFNULL(A.PASS_AMT, 0) "
        #                    "    FROM OSBILL A "
        #                    "    LEFT OUTER JOIN MIS1TB003 B "
        #                    "    ON A.UP_CODE = B.CUST_NBR "
        #                    "    WHERE A.AMTS >= A.PASS_AMT "
        #                    "    AND A.GUBUN = '1' "
        #                    "    AND YEAR(A.BAL_DD) = '" + str(year) + "' "
        #                    "    AND MONTH(A.BAL_DD) = '" + str(month) + "'"
        #                    )
        #     modalresult = cursor.fetchall()

        # 거래처
        with connection.cursor() as cursor:
            cursor.execute(" SELECT CUST_NBR, CUST_NME FROM MIS1TB003 WHERE CUST_GBN = '1' ")
            cboCust = cursor.fetchall()

        # 입출금구분
        with connection.cursor() as cursor:
            cursor.execute(" SELECT RESKEY, RESNAM FROM OSREFCP WHERE RECODE = 'OUA' AND RESKEY = '1' ORDER BY RESNAM ")
            cboGgn = cursor.fetchall()

        # 관리계정
        with connection.cursor() as cursor:
            cursor.execute(" SELECT MCODE, MCODENM FROM OSCODEM ")
            cboMCode = cursor.fetchall()

        # 회계게정
        with connection.cursor() as cursor:
            cursor.execute(" SELECT ACODE, ACODENM FROM OSCODEA ")
            cboACode = cursor.fetchall()

        # 결제방법
        with connection.cursor() as cursor:
            cursor.execute(" SELECT RESKEY, RESNAM FROM OSREFCP WHERE RECODE = 'OUB' ORDER BY RESNAM ")
            cboPay = cursor.fetchall()

        # 계좌번호
        with connection.cursor() as cursor:
            cursor.execute(" SELECT ACNUMBER FROM ACNUMBER ")
            cboAcnumber = cursor.fetchall()

        return JsonResponse({'cboCust': cboCust, 'cboGgn': cboGgn, 'cboMCode': cboMCode, 'cboACode': cboACode
                                , 'cboPay': cboPay, 'cboAcnumber': cboAcnumber})
