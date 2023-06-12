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


def depositRegViews(request):

    return render(request, "finance/deposit-reg.html")

def depositRegViews_search(request):
    date = request.POST.get('date')
    year = request.POST.get('inputYear')
    month = request.POST.get('inputMonth')

    if date != '' and date is not None:
        with connection.cursor() as cursor:
            # 거래처구분/명/행/결제방법명/결제방법코드/입출금구분/계정/금액/순번/날짜/계좌번호
            cursor.execute(" SELECT IFNULL(A.ACSEQN,''), IFNULL(A.ACCUST, ''), IFNULL(B.CUST_NME, '') "
                           "    , IFNULL(A.ACRECN,''), IFNULL(A.ACGUBN,''), IFNULL(C.RESNAM,'') "
                           "    , IFNULL(A.ACIOGB,''), IFNULL(E.RESNAM, ''), IFNULL(A.ACCODE,''), IFNULL(D.RESNAM, '') "
                           "    , IFNULL(A.ACAMTS, 0), IFNULL(A.ACDATE,''), IFNULL(A.ACACNUMBER,'')"
                           "    FROM SISACCTT A "
                           "    LEFT OUTER JOIN MIS1TB003 B "
                           "    ON A.ACCUST = B.CUST_NBR "
                           "    LEFT OUTER JOIN OSREFCP C "
                           "    ON A.ACGUBN = C.RESKEY "
                           "    AND C.RECODE = 'OUB' "
                           "    LEFT OUTER JOIN OSREFCP D "
                           "    ON A.ACCODE = D.RESKEY "
                           "    AND D.RECODE = 'BNK' "
                           "    LEFT OUTER JOIN OSREFCP E "
                           "    ON A.ACIOGB = E.RESKEY "
                           "    AND E.RECODE = 'OUA' "
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


def depositRegViews_save(request):
    if 'btnSave' in request.POST:
        acDate = request.POST.get("txtDepRegDate")      # 등록일자
        acSeqn = request.POST.get("txtDepSeq")           # 순번
        acRecn = '1' # 행
        acCust = request.POST.get("cboDepCust")     # 거래처
        acIogb = request.POST.get("cboDepGbn")    # 구분(입금)
        acCode = request.POST.get("cboDepCode")  # 계정과목
        acAmts = request.POST.get("txtDepPrice")      # 금액
        acAcnumber = request.POST.get("cboDepActNum")     # 계좌번호
        acGubn = request.POST.get("cboDepMethod")     # 결제방법
        acDesc = request.POST.get("txtDepRemark")     # 비고
        acIuser = request.session['userid']
        acIdate = acDate.replace('-', '')
        acUuser = request.session['userid']

        if acSeqn == '' and acSeqn is None:
            with connection.cursor() as cursor:
                cursor.execute("INSERT INTO SISACCTT "
                               "   (    "
                               "     ACDATE "
                               ",    ACSEQN "
                               ",    ACCUST "
                               ",    ACGUBN "
                               ",    ACCODE "
                               ",    ACAMTS "
                               ",    ACACNUMBER "
                               ",    ACRECN "
                               ",    ACDESC "
                               ",    IUSER "
                               ",    IDATE "
                               "    ) "
                               "    VALUES "
                               "    (   "
                               "    '" + str(acDate).replace('-', '') + "'"
                               ",   (SELECT IFNULL (MAX(ACSEQN) + 1,1) AS COUNTED FROM SISACCTT A WHERE ACDATE = '" + acDate + "' AND ACIOGB = '" + acIogb + "')"
                               ",   '" + str(acCust) + "'"
                               ",   '" + str(acGubn) + "'"
                               ",   '" + str(acCode) + "'"
                               ",   '" + str(acAmts) + "'"
                               ",   '" + str(acAcnumber) + "'"
                               ",   '" + str(acRecn) + "'"
                               ",   '" + str(acDesc) + "'"
                               ",   '" + str(acIuser) + "'"
                               ",   '" + str(acIdate) + "'"
                               "    )   "
                               )
                connection.commit()

            messages.success(request, '저장 되었습니다.')
            return render(request, 'finance/deposit-reg.html')

        elif acSeqn:
            with connection.cursor() as cursor:
                cursor.execute(" UPDATE SISACCTT SET "
                               "     ACCUST = '" + str(acCust) + "' "
                               ",    ACGUBN = '" + str(acGubn) + "' "
                               ",    ACCODE = '" + str(acCode) + "' "
                               ",    ACAMTS = '" + str(acAmts) + "' "
                               ",    ACACNUMBER = '" + str(acAcnumber) + "' "
                               ",    ACRECN = '" + str(acRecn) + "' "
                               ",    ACDESC = '" + str(acDesc) + "' "
                               ",    UUSER = '" + str(acUuser) + "' "
                               ",    UDATE = date_format(now(), '%Y%m%d') "
                               "     WHERE ACDATE = '" + str(acDate) + "' "
                               "     AND ACSEQN = '" + str(acSeqn) + "' "
                               "     AND ACIOGB = '" + str(acIogb) + "' "
                               )
                connection.commit()

            messages.success(request, '수정 되었습니다.')
            return render(request, 'finance/deposit-reg.html')


    else:
        messages.warning(request, '입력 하신 정보를 확인 해주세요.')
        return redirect('/deposit_reg')



def depositRegViews_dlt(request):
    if request.method == "POST":
        dataList = json.loads(request.POST.get('arrList'))
        print(dataList)
        for dep in dataList:
            acc_split_list = dep.split(',')
            with connection.cursor() as cursor:
                cursor.execute(" DELETE FROM SISACCTT WHERE ACDATE = '" + acc_split_list[0] + "' "
                               "                        AND ACSEQN = '" + acc_split_list[1] + "' "
                               "                        AND ACRECN = '" + acc_split_list[2] + "' "
                               "                        AND ACIOGB = '" + acc_split_list[3] + "' "
                               "                        AND ACCUST = '" + acc_split_list[4] + "' ")
                connection.commit()

        return JsonResponse({'sucYn': "Y"})

    else:
        return render(request, 'finance/deposit-reg.html')




# 모달 조회
def depositRegOutList_search(request):
    year = request.POST.get('inputYear')
    month = request.POST.get('inputMonth')
    upCode = request.POST.get('custCode')
    seq = request.POST.get('seq')
    date = request.POST.get('date')

    if seq != '' and seq is not None:
        with connection.cursor() as cursor:
            cursor.execute(" SELECT IFNULL(A.BAL_DD, ''), IFNULL(A.UP_CODE, ''), IFNULL(B.CUST_NME, '') "
                           "    , IFNULL(A.ITEM, ''), IFNULL(A.AMTS, 0), IFNULL(A.PASS_AMT, 0) "
                           "    FROM OSBILL A "
                           "    LEFT OUTER JOIN MIS1TB003 B "
                           "    ON A.UP_CODE = B.CUST_NBR "
                           "    WHERE A.AMTS >= A.PASS_AMT "
                           "    AND A.GUBUN = '2' "
                           "    AND A.BAL_DD = '" + date + "' "
                           "    AND A.UPCODE = '" + str(upCode) + "'")
            modalresult = cursor.fetchall()

            with connection.cursor() as cursor:
                cursor.execute(" SELECT IFNULL(A.BAL_DD, ''), IFNULL(A.UP_CODE, ''), IFNULL(B.CUST_NME, '') "
                               "    , IFNULL(A.ITEM, ''), IFNULL(A.AMTS, 0), IFNULL(A.PASS_AMT, 0) "
                               "    FROM OSBILL A "
                               "    LEFT OUTER JOIN MIS1TB003 B "
                               "    ON A.UP_CODE = B.CUST_NBR "
                               "    WHERE A.AMTS >= A.PASS_AMT "
                               "    AND A.GUBUN = '2' "
                               "    AND A.UPCODE = '" + str(upCode) + "'"
                               "    AND A.ACDATE = '" + str(date) + "'"
                               "    AND A.ACSEQN = '" + str(seq) + "'")
                modalform = cursor.fetchall()

            cursor.execute(" SELECT CUST_NBR, CUST_NME FROM MIS1TB003 WHERE CUST_GBN = '2' ")
            cboCust = cursor.fetchall()
        return JsonResponse({'modalList': modalresult, 'modalform': modalform, 'cboCust': cboCust})

    else:
        with connection.cursor() as cursor:
            cursor.execute(" SELECT IFNULL(A.BAL_DD, ''), IFNULL(A.UP_CODE, ''), IFNULL(B.CUST_NME, '') "
                           "    , IFNULL(A.ITEM, ''), IFNULL(A.AMTS, 0), IFNULL(A.PASS_AMT, 0) "
                           "    FROM OSBILL A "
                           "    LEFT OUTER JOIN MIS1TB003 B "
                           "    ON A.UP_CODE = B.CUST_NBR "
                           "    WHERE A.AMTS >= A.PASS_AMT "
                           "    AND A.GUBUN = '2' "
                           "    AND YEAR(A.BAL_DD ) = '" + str(year) + "' "
                           "    AND MONTH(A.BAL_DD) = '" + str(month) + "' "
                           "    AND A.UP_CODE LIKE '%" + str(upCode) + "%' ")
            modalresult = cursor.fetchall()

            cursor.execute(" SELECT CUST_NBR, CUST_NME FROM MIS1TB003 WHERE CUST_GBN = '2' ")
            cboCust = cursor.fetchall()

            print(cboCust)

        return JsonResponse({'modalList': modalresult, 'cboCust': cboCust})