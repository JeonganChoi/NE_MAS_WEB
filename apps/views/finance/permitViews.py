import datetime
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

# 임금대장
def permitViews(request):
    userId = request.session.get('userId')
    if userId == '' or userId is None:
        return redirect("/page-404/")
    else:
        return render(request, "finance/permit-reg.html")


def permitViews_search(request):
    perDate = request.POST.get('perDate')
    # 미시행 ''/ 시행 = 1
    permitGbn = request.POST.get('permitGbn','')
    custCode = request.POST.get('custCode','')
    bankCode = request.POST.get('bankCode','')
    actCode = request.POST.get('actCode','')
    inputCard = request.POST.get('inputCard','')
    inputCardNum = request.POST.get('inputCardNum','')
    # value = off
    offSet = request.POST.get('offSet','')
    user = request.session.get('userId')
    iCust = request.session.get('USER_ICUST')

    # if offSet and custCode:
    #     with connection.cursor() as cursor:
    #         cursor.execute("  SELECT IFNULL(A.IODATE, ''), IFNULL(A.ACTITLE, ''), IFNULL(A.ACAMTS, '') "
    #                        "        , IFNULL(B.EMP_NBR, ''), IFNULL(C.EMP_NME, ''), IFNULL(A.ACSEQN, ''), IFNULL(A.ACIOGB, '')"
    #                        "        , IFNULL(A.MCODE, ''), IFNULL(D.MCODENM, ''), IFNULL(A.ACACNUMBER, '') "
    #                        " FROM SISACCTT A "
    #                        " LEFT OUTER JOIN OSSIGN B "
    #                        " ON A.IODATE = B.ACDATE "
    #                        " AND A.ACSEQN = B.ACSEQN "
    #                        " AND A.ICUST = B.ICUST "
    #                        " AND A.FIN_OPT = 'N' "
    #                        " LEFT OUTER JOIN PIS1TB001 C "
    #                        " ON B.EMP_NBR = C.EMP_NBR "
    #                        " LEFT OUTER JOIN OSCODEM D "
    #                        " ON A.MCODE = D.MCODE "
    #                        " WHERE B.EMP_NBR = '" + user + "' "
    #                        " AND A.IODATE <= '" + perDate + "' "
    #                        " AND A.ACCUST = '" + custCode + "' "
    #                        " AND A.OFF_GBN = 'off'"
    #                        " AND A.ICUST = '" + iCust + "' "
    #                        " ORDER BY A.ACSEQN ASC ")
    #         mainresult = cursor.fetchall()
    #
    #     return JsonResponse({"mainList": mainresult})

    # elif custCode:
    #     with connection.cursor() as cursor:
    #         cursor.execute("  SELECT IFNULL(A.IODATE, ''), IFNULL(A.ACTITLE, ''), IFNULL(A.ACAMTS, '') "
    #                        "        , IFNULL(B.EMP_NBR, ''), IFNULL(C.EMP_NME, ''), IFNULL(A.ACSEQN, ''), IFNULL(A.ACIOGB, '')"
    #                        "        , IFNULL(A.MCODE, ''), IFNULL(D.MCODENM, ''), IFNULL(A.ACACNUMBER, '') "
    #                        " FROM SISACCTT A "
    #                        " LEFT OUTER JOIN OSSIGN B "
    #                        " ON A.IODATE = B.ACDATE "
    #                        " AND A.ACSEQN = B.ACSEQN "
    #                        " AND A.ICUST = B.ICUST "
    #                        " AND A.FIN_OPT = 'N' "
    #                        " LEFT OUTER JOIN PIS1TB001 C "
    #                        " ON B.EMP_NBR = C.EMP_NBR "
    #                        " LEFT OUTER JOIN OSCODEM D "
    #                        " ON A.MCODE = D.MCODE "
    #                        " WHERE B.EMP_NBR = '" + user + "' "
    #                        " AND A.IODATE <= '" + perDate + "' "
    #                        " AND A.ACCUST = '" + custCode + "' "
    #                        " AND A.ICUST = '" + iCust + "' "
    #                        " ORDER BY A.ACSEQN ASC ")
    #         mainresult = cursor.fetchall()
    #
    #     return JsonResponse({"mainList": mainresult})

    # 상계
    if offSet != '':
        if permitGbn == '':
            if actCode == '':
                with connection.cursor() as cursor:
                    cursor.execute("  SELECT IFNULL(A.IODATE, ''), IFNULL(A.ACTITLE, ''), IFNULL(A.ACAMTS, '') "
                                   "        , IFNULL(A.CRE_USER, ''), IFNULL(C.EMP_NME, ''), IFNULL(A.ACSEQN, ''), IFNULL(A.ACIOGB, '')"
                                   "        , IFNULL(A.MCODE, ''), IFNULL(D.MCODENM, ''), IFNULL(A.ACACNUMBER, ''), IFNULL(A.FIN_OPT, '')"
                                   "        , IFNULL(A.ACINFO, ''), IFNULL(E.ACBKCD, ''), IFNULL(F.RESNAM, ''), IFNULL(A.EXDATE, ''), IFNULL(A.ACGUBN, '') "
                                   " FROM SISACCTT A "
                                   " LEFT OUTER JOIN PIS1TB001 C "
                                   " ON A.CRE_USER = C.EMP_NBR "
                                   " LEFT OUTER JOIN OSCODEM D "
                                   " ON A.MCODE = D.MCODE "
                                   " LEFT OUTER JOIN ACNUMBER E "
                                   " ON A.ACACNUMBER = E.ACNUMBER "
                                   " LEFT OUTER JOIN OSREFCP F "
                                   " ON E.ACBKCD = F.RESKEY "
                                   " AND F.RECODE = 'BNK' "
                                   " WHERE A.FIN_OPT = 'N'  "
                                   # " AND A.IODATE <= '" + str(perDate) + "' "
                                   " AND A.OFF_GBN = 'off'"
                                   " AND A.ICUST = '" + str(iCust) + "' "
                                   " AND A.ACCUST like '%" + str(custCode) + "%' "
                                   " ORDER BY A.ACSEQN ASC ")
                    mainresult = cursor.fetchall()

                return JsonResponse({"mainList": mainresult})

            if actCode != '':
                with connection.cursor() as cursor:
                    cursor.execute("  SELECT IFNULL(A.IODATE, ''), IFNULL(A.ACTITLE, ''), IFNULL(A.ACAMTS, '') "
                                   "        , IFNULL(A.CRE_USER, ''), IFNULL(C.EMP_NME, ''), IFNULL(A.ACSEQN, ''), IFNULL(A.ACIOGB, '')"
                                   "        , IFNULL(A.MCODE, ''), IFNULL(D.MCODENM, ''), IFNULL(A.ACACNUMBER, ''), IFNULL(A.FIN_OPT, '')"
                                   "        , IFNULL(A.ACINFO, ''), IFNULL(E.ACBKCD, ''), IFNULL(F.RESNAM, ''), IFNULL(A.EXDATE, ''), IFNULL(A.ACGUBN, '') "
                                   " FROM SISACCTT A "
                                   " LEFT OUTER JOIN PIS1TB001 C "
                                   " ON A.CRE_USER = C.EMP_NBR "
                                   " LEFT OUTER JOIN OSCODEM D "
                                   " ON A.MCODE = D.MCODE "
                                   " LEFT OUTER JOIN ACNUMBER E "
                                   " ON A.ACACNUMBER = E.ACNUMBER "
                                   " LEFT OUTER JOIN OSREFCP F "
                                   " ON E.ACBKCD = F.RESKEY "
                                   " AND F.RECODE = 'BNK' "
                                   " WHERE A.FIN_OPT = 'N'  "
                                   # " AND A.IODATE <= '" + str(perDate) + "' "
                                   " AND A.OFF_GBN = 'off'"
                                   " AND A.ICUST = '" + str(iCust) + "' "
                                   " AND A.ACCUST like '%" + str(custCode) + "%' "
                                   " AND A.ACACNUMBER = '" + str(actCode) + "' "
                                   " ORDER BY A.ACSEQN ASC ")
                    mainresult = cursor.fetchall()

                return JsonResponse({"mainList": mainresult})

        if permitGbn != '':
            if actCode == '':
                with connection.cursor() as cursor:
                    cursor.execute("  SELECT IFNULL(A.IODATE, ''), IFNULL(A.ACTITLE, ''), IFNULL(A.ACAMTS, '') "
                                   "        , IFNULL(A.CRE_USER, ''), IFNULL(C.EMP_NME, ''), IFNULL(A.ACSEQN, ''), IFNULL(A.ACIOGB, '')"
                                   "        , IFNULL(A.MCODE, ''), IFNULL(D.MCODENM, ''), IFNULL(A.ACACNUMBER, ''), IFNULL(A.FIN_OPT, '')"
                                   "        , IFNULL(A.ACINFO, ''), IFNULL(E.ACBKCD, ''), IFNULL(F.RESNAM, ''), IFNULL(A.EXDATE, ''), IFNULL(A.ACGUBN, '') "
                                   " FROM SISACCTT A "
                                   " LEFT OUTER JOIN PIS1TB001 C "
                                   " ON A.CRE_USER = C.EMP_NBR "
                                   " LEFT OUTER JOIN OSCODEM D "
                                   " ON A.MCODE = D.MCODE "
                                   " LEFT OUTER JOIN ACNUMBER E "
                                   " ON A.ACACNUMBER = E.ACNUMBER "
                                   " LEFT OUTER JOIN OSREFCP F "
                                   " ON E.ACBKCD = F.RESKEY "
                                   " AND F.RECODE = 'BNK' "
                                   " WHERE A.FIN_OPT = 'Y'  "
                                   # " AND A.IODATE <= '" + str(perDate) + "' "
                                   " AND A.OFF_GBN = 'off'"
                                   " AND A.ICUST = '" + str(iCust) + "' "
                                   " AND A.ACCUST like '%" + str(custCode) + "%' "
                                   " ORDER BY A.ACSEQN ASC ")
                    mainresult = cursor.fetchall()
                # " AND NOT EXISTS (SELECT OPT FROM OSSIGN WHERE OPT = 'N') "

                return JsonResponse({"mainList": mainresult})
            if actCode != '':
                with connection.cursor() as cursor:
                    cursor.execute("  SELECT IFNULL(A.IODATE, ''), IFNULL(A.ACTITLE, ''), IFNULL(A.ACAMTS, '') "
                                   "        , IFNULL(A.CRE_USER, ''), IFNULL(C.EMP_NME, ''), IFNULL(A.ACSEQN, ''), IFNULL(A.ACIOGB, '')"
                                   "        , IFNULL(A.MCODE, ''), IFNULL(D.MCODENM, ''), IFNULL(A.ACACNUMBER, ''), IFNULL(A.FIN_OPT, '')"
                                   "        , IFNULL(A.ACINFO, ''), IFNULL(E.ACBKCD, ''), IFNULL(F.RESNAM, ''), IFNULL(A.EXDATE, ''), IFNULL(A.ACGUBN, '') "
                                   " FROM SISACCTT A "
                                   " LEFT OUTER JOIN PIS1TB001 C "
                                   " ON A.CRE_USER = C.EMP_NBR "
                                   " LEFT OUTER JOIN OSCODEM D "
                                   " ON A.MCODE = D.MCODE "
                                   " LEFT OUTER JOIN ACNUMBER E "
                                   " ON A.ACACNUMBER = E.ACNUMBER "
                                   " LEFT OUTER JOIN OSREFCP F "
                                   " ON E.ACBKCD = F.RESKEY "
                                   " AND F.RECODE = 'BNK' "
                                   " WHERE A.FIN_OPT = 'Y'  "
                                   # " AND A.IODATE <= '" + str(perDate) + "' "
                                   " AND A.OFF_GBN = 'off'"
                                   " AND A.ICUST = '" + str(iCust) + "' "
                                   " AND A.ACCUST like '%" + str(custCode) + "%' "
                                    " AND A.ACACNUMBER = '" + str(actCode) + "' "
                                   " ORDER BY A.ACSEQN ASC ")
                    mainresult = cursor.fetchall()
                # " AND NOT EXISTS (SELECT OPT FROM OSSIGN WHERE OPT = 'N') "

                return JsonResponse({"mainList": mainresult})

    else:
        if permitGbn == '':
            if actCode == '' and inputCardNum == '':
                with connection.cursor() as cursor:
                    cursor.execute("  SELECT IFNULL(A.IODATE, ''), IFNULL(A.ACTITLE, ''), IFNULL(A.ACAMTS, '') "
                                   "        , IFNULL(A.CRE_USER, ''), IFNULL(C.EMP_NME, ''), IFNULL(A.ACSEQN, ''), IFNULL(A.ACIOGB, '')"
                                   "        , IFNULL(A.MCODE, ''), IFNULL(D.MCODENM, ''), IFNULL(A.ACACNUMBER, ''),  IFNULL(A.FIN_OPT, '')"
                                   "        , IFNULL(A.ACINFO, ''), IFNULL(E.ACBKCD, ''), IFNULL(F.RESNAM, ''), IFNULL(A.EXDATE, ''), IFNULL(A.ACGUBN, '') "
                                   " FROM SISACCTT A "
                                   " LEFT OUTER JOIN PIS1TB001 C "
                                   " ON A.CRE_USER = C.EMP_NBR "
                                   " LEFT OUTER JOIN OSCODEM D "
                                   " ON A.MCODE = D.MCODE "
                                   " LEFT OUTER JOIN ACNUMBER E "
                                   " ON A.ACACNUMBER = E.ACNUMBER "
                                   " LEFT OUTER JOIN OSREFCP F "
                                   " ON E.ACBKCD = F.RESKEY "
                                   " AND F.RECODE = 'BNK' "
                                   " WHERE A.FIN_OPT = 'N'  "                         
                                   # " AND A.IODATE <= '" + str(perDate) + "' "
                                   " AND A.ICUST = '" + str(iCust) + "' "
                                   " AND A.ACCUST like '%" + str(custCode) + "%' "
                                   " ORDER BY A.ACSEQN ASC ")
                    mainresult = cursor.fetchall()
                # " AND NOT EXISTS (SELECT OPT FROM OSSIGN WHERE OPT = 'N') "

                with connection.cursor() as cursor:
                    cursor.execute(" SELECT CUST_NBR, CUST_NME FROM MIS1TB003 WHERE ICUST = '" + str(iCust) + "'")
                    cboCust = cursor.fetchall()

                with connection.cursor() as cursor:
                    cursor.execute(" SELECT ACNUMBER FROM ACNUMBER WHERE ICUST = '" + str(iCust) + "'")
                    cboAct = cursor.fetchall()

                with connection.cursor() as cursor:
                    cursor.execute(" SELECT A.ACBKCD, B.RESNAM FROM ACNUMBER A LEFT OUTER JOIN OSREFCP B ON A.ACBKCD = B.RESKEY AND B.RECODE = 'BNK'WHERE A.ICUST = '" + str(iCust) + "' GROUP BY A.ACBKCD, B.RESNAM ")
                    cboBank = cursor.fetchall()

                # 카드명
                with connection.cursor() as cursor:
                    cursor.execute(" SELECT A.CARDTYPE, B.RESNAM FROM ACCARD A LEFT OUTER JOIN OSREFCP B ON A.CARDTYPE = B.RESKEY AND B.RECODE = 'COC' WHERE A.ICUST = '" + str(iCust) + "' GROUP BY A.CARDTYPE, B.RESNAM ")
                    cboCard = cursor.fetchall()
                # 카드번호
                with connection.cursor() as cursor:
                    cursor.execute(" SELECT CARDNUM FROM ACCARD WHERE ICUST = '" + str(iCust) + "'")
                    cboCardNum = cursor.fetchall()

                return JsonResponse({"mainList": mainresult, "cboCust": cboCust, "cboAct": cboAct, "cboBank": cboBank, "cboCard": cboCard, "cboCardNum": cboCardNum})

            if actCode != '' and inputCardNum == '':
                with connection.cursor() as cursor:
                    cursor.execute("  SELECT IFNULL(A.IODATE, ''), IFNULL(A.ACTITLE, ''), IFNULL(A.ACAMTS, '') "
                                   "        , IFNULL(A.CRE_USER, ''), IFNULL(C.EMP_NME, ''), IFNULL(A.ACSEQN, ''), IFNULL(A.ACIOGB, '')"
                                   "        , IFNULL(A.MCODE, ''), IFNULL(D.MCODENM, ''), IFNULL(A.ACACNUMBER, ''),  IFNULL(A.FIN_OPT, '')"
                                   "        , IFNULL(A.ACINFO, ''), IFNULL(E.ACBKCD, ''), IFNULL(F.RESNAM, ''), IFNULL(A.EXDATE, ''), IFNULL(A.ACGUBN, '') "
                                   " FROM SISACCTT A "
                                   " LEFT OUTER JOIN PIS1TB001 C "
                                   " ON A.CRE_USER = C.EMP_NBR "
                                   " LEFT OUTER JOIN OSCODEM D "
                                   " ON A.MCODE = D.MCODE "
                                   " LEFT OUTER JOIN ACNUMBER E "
                                   " ON A.ACACNUMBER = E.ACNUMBER "
                                   " LEFT OUTER JOIN OSREFCP F "
                                   " ON E.ACBKCD = F.RESKEY "
                                   " AND F.RECODE = 'BNK' "
                                   " WHERE A.FIN_OPT = 'N'  "                         
                                   # " AND A.IODATE <= '" + str(perDate) + "' "
                                   " AND A.ICUST = '" + str(iCust) + "' "
                                   " AND A.ACCUST like '%" + str(custCode) + "%' "
                                   " AND A.ACACNUMBER = '" + str(actCode) + "' "
                                   " ORDER BY A.ACSEQN ASC ")
                    mainresult = cursor.fetchall()
                # " AND NOT EXISTS (SELECT OPT FROM OSSIGN WHERE OPT = 'N') "

                with connection.cursor() as cursor:
                    cursor.execute(" SELECT CUST_NBR, CUST_NME FROM MIS1TB003 WHERE ICUST = '" + str(iCust) + "'")
                    cboCust = cursor.fetchall()

                with connection.cursor() as cursor:
                    cursor.execute(" SELECT ACNUMBER FROM ACNUMBER WHERE ICUST = '" + str(iCust) + "'")
                    cboAct = cursor.fetchall()

                with connection.cursor() as cursor:
                    cursor.execute(" SELECT A.ACBKCD, B.RESNAM FROM ACNUMBER A LEFT OUTER JOIN OSREFCP B ON A.ACBKCD = B.RESKEY AND B.RECODE = 'BNK'WHERE A.ICUST = '" + str(iCust) + "' GROUP BY A.ACBKCD, B.RESNAM ")
                    cboBank = cursor.fetchall()

                # 카드명
                with connection.cursor() as cursor:
                    cursor.execute(" SELECT A.CARDTYPE, B.RESNAM FROM ACCARD A LEFT OUTER JOIN OSREFCP B ON A.CARDTYPE = B.RESKEY AND B.RECODE = 'COC' WHERE A.ICUST = '" + str(iCust) + "' GROUP BY A.CARDTYPE, B.RESNAM ")
                    cboCard = cursor.fetchall()
                # 카드번호
                with connection.cursor() as cursor:
                    cursor.execute(" SELECT CARDNUM FROM ACCARD WHERE ICUST = '" + str(iCust) + "'")
                    cboCardNum = cursor.fetchall()

                return JsonResponse({"mainList": mainresult, "cboCust": cboCust, "cboAct": cboAct, "cboBank": cboBank, "cboCard": cboCard, "cboCardNum": cboCardNum})

            if actCode == '' and inputCardNum != '':
                with connection.cursor() as cursor:
                    cursor.execute("  SELECT IFNULL(A.IODATE, ''), IFNULL(A.ACTITLE, ''), IFNULL(A.ACAMTS, '') "
                                   "        , IFNULL(A.CRE_USER, ''), IFNULL(C.EMP_NME, ''), IFNULL(A.ACSEQN, ''), IFNULL(A.ACIOGB, '')"
                                   "        , IFNULL(A.MCODE, ''), IFNULL(D.MCODENM, ''), IFNULL(A.ACACNUMBER, ''),  IFNULL(A.FIN_OPT, '')"
                                   "        , IFNULL(A.ACINFO, ''), IFNULL(E.ACBKCD, ''), IFNULL(F.RESNAM, ''), IFNULL(A.EXDATE, ''), IFNULL(A.ACGUBN, '') "
                                   " FROM SISACCTT A "
                                   " LEFT OUTER JOIN PIS1TB001 C "
                                   " ON A.CRE_USER = C.EMP_NBR "
                                   " LEFT OUTER JOIN OSCODEM D "
                                   " ON A.MCODE = D.MCODE "
                                   " LEFT OUTER JOIN ACNUMBER E "
                                   " ON A.ACACNUMBER = E.ACNUMBER "
                                   " LEFT OUTER JOIN OSREFCP F "
                                   " ON E.ACBKCD = F.RESKEY "
                                   " AND F.RECODE = 'BNK' "
                                   " WHERE A.FIN_OPT = 'N'  "                         
                                   # " AND A.IODATE <= '" + str(perDate) + "' "
                                   " AND A.ICUST = '" + str(iCust) + "' "
                                   " AND A.ACCUST like '%" + str(custCode) + "%' "
                                   " AND A.ACCARD = '" + str(inputCardNum) + "' "
                                   " ORDER BY A.ACSEQN ASC ")
                    mainresult = cursor.fetchall()
                # " AND NOT EXISTS (SELECT OPT FROM OSSIGN WHERE OPT = 'N') "

                with connection.cursor() as cursor:
                    cursor.execute(" SELECT CUST_NBR, CUST_NME FROM MIS1TB003 WHERE ICUST = '" + str(iCust) + "'")
                    cboCust = cursor.fetchall()

                with connection.cursor() as cursor:
                    cursor.execute(" SELECT ACNUMBER FROM ACNUMBER WHERE ICUST = '" + str(iCust) + "'")
                    cboAct = cursor.fetchall()

                with connection.cursor() as cursor:
                    cursor.execute(" SELECT A.ACBKCD, B.RESNAM FROM ACNUMBER A LEFT OUTER JOIN OSREFCP B ON A.ACBKCD = B.RESKEY AND B.RECODE = 'BNK'WHERE A.ICUST = '" + str(iCust) + "' GROUP BY A.ACBKCD, B.RESNAM ")
                    cboBank = cursor.fetchall()

                # 카드명
                with connection.cursor() as cursor:
                    cursor.execute(" SELECT A.CARDTYPE, B.RESNAM FROM ACCARD A LEFT OUTER JOIN OSREFCP B ON A.CARDTYPE = B.RESKEY AND B.RECODE = 'COC' WHERE A.ICUST = '" + str(iCust) + "' GROUP BY A.CARDTYPE, B.RESNAM ")
                    cboCard = cursor.fetchall()
                # 카드번호
                with connection.cursor() as cursor:
                    cursor.execute(" SELECT CARDNUM FROM ACCARD WHERE ICUST = '" + str(iCust) + "'")
                    cboCardNum = cursor.fetchall()

                return JsonResponse({"mainList": mainresult, "cboCust": cboCust, "cboAct": cboAct, "cboBank": cboBank, "cboCard": cboCard, "cboCardNum": cboCardNum})

            if actCode != '' and inputCardNum != '':
                with connection.cursor() as cursor:
                    cursor.execute("  SELECT IFNULL(A.IODATE, ''), IFNULL(A.ACTITLE, ''), IFNULL(A.ACAMTS, '') "
                                   "        , IFNULL(A.CRE_USER, ''), IFNULL(C.EMP_NME, ''), IFNULL(A.ACSEQN, ''), IFNULL(A.ACIOGB, '')"
                                   "        , IFNULL(A.MCODE, ''), IFNULL(D.MCODENM, ''), IFNULL(A.ACACNUMBER, ''),  IFNULL(A.FIN_OPT, '')"
                                   "        , IFNULL(A.ACINFO, ''), IFNULL(E.ACBKCD, ''), IFNULL(F.RESNAM, ''), IFNULL(A.EXDATE, ''), IFNULL(A.ACGUBN, '') "
                                   " FROM SISACCTT A "
                                   " LEFT OUTER JOIN PIS1TB001 C "
                                   " ON A.CRE_USER = C.EMP_NBR "
                                   " LEFT OUTER JOIN OSCODEM D "
                                   " ON A.MCODE = D.MCODE "
                                   " LEFT OUTER JOIN ACNUMBER E "
                                   " ON A.ACACNUMBER = E.ACNUMBER "
                                   " LEFT OUTER JOIN OSREFCP F "
                                   " ON E.ACBKCD = F.RESKEY "
                                   " AND F.RECODE = 'BNK' "
                                   " WHERE A.FIN_OPT = 'N'  "                         
                                   # " AND A.IODATE <= '" + str(perDate) + "' "
                                   " AND A.ICUST = '" + str(iCust) + "' "
                                   " AND A.ACCUST like '%" + str(custCode) + "%' "
                                   " AND A.ACCARD = '" + str(inputCardNum) + "' "
                                   " AND A.ACACNUMBER = '" + str(actCode) + "' "
                                   " ORDER BY A.ACSEQN ASC ")
                    mainresult = cursor.fetchall()
                # " AND NOT EXISTS (SELECT OPT FROM OSSIGN WHERE OPT = 'N') "

                with connection.cursor() as cursor:
                    cursor.execute(" SELECT CUST_NBR, CUST_NME FROM MIS1TB003 WHERE ICUST = '" + str(iCust) + "'")
                    cboCust = cursor.fetchall()

                with connection.cursor() as cursor:
                    cursor.execute(" SELECT ACNUMBER FROM ACNUMBER WHERE ICUST = '" + str(iCust) + "'")
                    cboAct = cursor.fetchall()

                with connection.cursor() as cursor:
                    cursor.execute(" SELECT A.ACBKCD, B.RESNAM FROM ACNUMBER A LEFT OUTER JOIN OSREFCP B ON A.ACBKCD = B.RESKEY AND B.RECODE = 'BNK'WHERE A.ICUST = '" + str(iCust) + "' GROUP BY A.ACBKCD, B.RESNAM ")
                    cboBank = cursor.fetchall()

                # 카드명
                with connection.cursor() as cursor:
                    cursor.execute(" SELECT A.CARDTYPE, B.RESNAM FROM ACCARD A LEFT OUTER JOIN OSREFCP B ON A.CARDTYPE = B.RESKEY AND B.RECODE = 'COC' WHERE A.ICUST = '" + str(iCust) + "' GROUP BY A.CARDTYPE, B.RESNAM ")
                    cboCard = cursor.fetchall()
                # 카드번호
                with connection.cursor() as cursor:
                    cursor.execute(" SELECT CARDNUM FROM ACCARD WHERE ICUST = '" + str(iCust) + "'")
                    cboCardNum = cursor.fetchall()

                return JsonResponse({"mainList": mainresult, "cboCust": cboCust, "cboAct": cboAct, "cboBank": cboBank, "cboCard": cboCard, "cboCardNum": cboCardNum})

        if permitGbn != '':
            if actCode == '' and inputCardNum == '':
                with connection.cursor() as cursor:
                    cursor.execute("  SELECT IFNULL(A.IODATE, ''), IFNULL(A.ACTITLE, ''), IFNULL(A.ACAMTS, '') "
                                   "        , IFNULL(A.CRE_USER, ''), IFNULL(C.EMP_NME, ''), IFNULL(A.ACSEQN, ''), IFNULL(A.ACIOGB, '')"
                                   "        , IFNULL(A.MCODE, ''), IFNULL(D.MCODENM, ''), IFNULL(A.ACACNUMBER, ''), IFNULL(A.FIN_OPT, '')"
                                   "        , IFNULL(A.ACINFO, ''), IFNULL(E.ACBKCD, ''), IFNULL(F.RESNAM, ''), IFNULL(A.EXDATE, ''), IFNULL(A.ACGUBN, '') "
                                   " FROM SISACCTT A "
                                   " LEFT OUTER JOIN PIS1TB001 C "
                                   " ON A.CRE_USER = C.EMP_NBR "
                                   " LEFT OUTER JOIN OSCODEM D "
                                   " ON A.MCODE = D.MCODE "
                                   " LEFT OUTER JOIN ACNUMBER E "
                                   " ON A.ACACNUMBER = E.ACNUMBER "
                                   " LEFT OUTER JOIN OSREFCP F "
                                   " ON E.ACBKCD = F.RESKEY "
                                   " AND F.RECODE = 'BNK' "
                                   " WHERE A.FIN_OPT = 'Y'  "    
                                   # " AND A.IODATE <= '" + str(perDate) + "' "
                                   " AND A.ICUST = '" + str(iCust) + "' "
                                   " AND A.ACCUST like '%" + str(custCode) + "%' "
                                   " ORDER BY A.ACSEQN ASC ")
                    mainresult = cursor.fetchall()
                # " AND NOT EXISTS (SELECT OPT FROM OSSIGN WHERE OPT = 'N') "

                with connection.cursor() as cursor:
                    cursor.execute(" SELECT CUST_NBR, CUST_NME FROM MIS1TB003 WHERE ICUST = '" + str(iCust) + "'")
                    cboCust = cursor.fetchall()

                with connection.cursor() as cursor:
                    cursor.execute(" SELECT ACNUMBER FROM ACNUMBER WHERE ICUST = '" + str(iCust) + "'")
                    cboAct = cursor.fetchall()

                with connection.cursor() as cursor:
                    cursor.execute(" SELECT A.ACBKCD, B.RESNAM FROM ACNUMBER A LEFT OUTER JOIN OSREFCP B ON A.ACBKCD = B.RESKEY AND B.RECODE = 'BNK'WHERE A.ICUST = '" + str(iCust) + "' GROUP BY A.ACBKCD, B.RESNAM ")
                    cboBank = cursor.fetchall()

                # 카드명
                with connection.cursor() as cursor:
                    cursor.execute(" SELECT A.CARDTYPE, B.RESNAM FROM ACCARD A LEFT OUTER JOIN OSREFCP B ON A.CARDTYPE = B.RESKEY AND B.RECODE = 'COC' WHERE A.ICUST = '" + str(iCust) + "' GROUP BY A.CARDTYPE, B.RESNAM ")
                    cboCard = cursor.fetchall()
                # 카드번호
                with connection.cursor() as cursor:
                    cursor.execute(" SELECT CARDNUM FROM ACCARD WHERE ICUST = '" + str(iCust) + "'")
                    cboCardNum = cursor.fetchall()

                return JsonResponse({"mainList": mainresult, "cboCust": cboCust, "cboAct": cboAct, "cboBank": cboBank, "cboCard": cboCard, "cboCardNum": cboCardNum})

            if actCode != '' and inputCardNum == '':
                with connection.cursor() as cursor:
                    cursor.execute("  SELECT IFNULL(A.IODATE, ''), IFNULL(A.ACTITLE, ''), IFNULL(A.ACAMTS, '') "
                                   "        , IFNULL(A.CRE_USER, ''), IFNULL(C.EMP_NME, ''), IFNULL(A.ACSEQN, ''), IFNULL(A.ACIOGB, '')"
                                   "        , IFNULL(A.MCODE, ''), IFNULL(D.MCODENM, ''), IFNULL(A.ACACNUMBER, ''), IFNULL(A.FIN_OPT, '')"
                                   "        , IFNULL(A.ACINFO, ''), IFNULL(E.ACBKCD, ''), IFNULL(F.RESNAM, ''), IFNULL(A.EXDATE, ''), IFNULL(A.ACGUBN, '') "
                                   " FROM SISACCTT A "
                                   " LEFT OUTER JOIN PIS1TB001 C "
                                   " ON A.CRE_USER = C.EMP_NBR "
                                   " LEFT OUTER JOIN OSCODEM D "
                                   " ON A.MCODE = D.MCODE "
                                   " LEFT OUTER JOIN ACNUMBER E "
                                   " ON A.ACACNUMBER = E.ACNUMBER "
                                   " LEFT OUTER JOIN OSREFCP F "
                                   " ON E.ACBKCD = F.RESKEY "
                                   " AND F.RECODE = 'BNK' "
                                   " WHERE A.FIN_OPT = 'Y'  "    
                                   # " AND A.IODATE <= '" + str(perDate) + "' "
                                   " AND A.ICUST = '" + str(iCust) + "' "
                                   " AND A.ACCUST like '%" + str(custCode) + "%' "
                                   " AND A.ACACNUMBER = '" + str(actCode) + "' "
                                   " ORDER BY A.ACSEQN ASC ")
                    mainresult = cursor.fetchall()
                # " AND NOT EXISTS (SELECT OPT FROM OSSIGN WHERE OPT = 'N') "

                with connection.cursor() as cursor:
                    cursor.execute(" SELECT CUST_NBR, CUST_NME FROM MIS1TB003 WHERE ICUST = '" + str(iCust) + "'")
                    cboCust = cursor.fetchall()

                with connection.cursor() as cursor:
                    cursor.execute(" SELECT ACNUMBER FROM ACNUMBER WHERE ICUST = '" + str(iCust) + "'")
                    cboAct = cursor.fetchall()

                with connection.cursor() as cursor:
                    cursor.execute(" SELECT A.ACBKCD, B.RESNAM FROM ACNUMBER A LEFT OUTER JOIN OSREFCP B ON A.ACBKCD = B.RESKEY AND B.RECODE = 'BNK'WHERE A.ICUST = '" + str(iCust) + "' GROUP BY A.ACBKCD, B.RESNAM ")
                    cboBank = cursor.fetchall()

                # 카드명
                with connection.cursor() as cursor:
                    cursor.execute(" SELECT A.CARDTYPE, B.RESNAM FROM ACCARD A LEFT OUTER JOIN OSREFCP B ON A.CARDTYPE = B.RESKEY AND B.RECODE = 'COC' WHERE A.ICUST = '" + str(iCust) + "' GROUP BY A.CARDTYPE, B.RESNAM ")
                    cboCard = cursor.fetchall()
                # 카드번호
                with connection.cursor() as cursor:
                    cursor.execute(" SELECT CARDNUM FROM ACCARD WHERE ICUST = '" + str(iCust) + "'")
                    cboCardNum = cursor.fetchall()

                return JsonResponse({"mainList": mainresult, "cboCust": cboCust, "cboAct": cboAct, "cboBank": cboBank, "cboCard": cboCard, "cboCardNum": cboCardNum})

            if actCode == '' and inputCardNum != '':
                with connection.cursor() as cursor:
                    cursor.execute("  SELECT IFNULL(A.IODATE, ''), IFNULL(A.ACTITLE, ''), IFNULL(A.ACAMTS, '') "
                                   "        , IFNULL(A.CRE_USER, ''), IFNULL(C.EMP_NME, ''), IFNULL(A.ACSEQN, ''), IFNULL(A.ACIOGB, '')"
                                   "        , IFNULL(A.MCODE, ''), IFNULL(D.MCODENM, ''), IFNULL(A.ACACNUMBER, ''), IFNULL(A.FIN_OPT, '')"
                                   "        , IFNULL(A.ACINFO, ''), IFNULL(E.ACBKCD, ''), IFNULL(F.RESNAM, ''), IFNULL(A.EXDATE, ''), IFNULL(A.ACGUBN, '') "
                                   " FROM SISACCTT A "
                                   " LEFT OUTER JOIN PIS1TB001 C "
                                   " ON A.CRE_USER = C.EMP_NBR "
                                   " LEFT OUTER JOIN OSCODEM D "
                                   " ON A.MCODE = D.MCODE "
                                   " LEFT OUTER JOIN ACNUMBER E "
                                   " ON A.ACACNUMBER = E.ACNUMBER "
                                   " LEFT OUTER JOIN OSREFCP F "
                                   " ON E.ACBKCD = F.RESKEY "
                                   " AND F.RECODE = 'BNK' "
                                   " WHERE A.FIN_OPT = 'Y'  "    
                                   # " AND A.IODATE <= '" + str(perDate) + "' "
                                   " AND A.ICUST = '" + str(iCust) + "' "
                                   " AND A.ACCUST like '%" + str(custCode) + "%' "
                                   " AND A.ACCARD = '" + str(inputCardNum) + "' "
                                   " ORDER BY A.ACSEQN ASC ")
                    mainresult = cursor.fetchall()
                # " AND NOT EXISTS (SELECT OPT FROM OSSIGN WHERE OPT = 'N') "

                with connection.cursor() as cursor:
                    cursor.execute(" SELECT CUST_NBR, CUST_NME FROM MIS1TB003 WHERE ICUST = '" + str(iCust) + "'")
                    cboCust = cursor.fetchall()

                with connection.cursor() as cursor:
                    cursor.execute(" SELECT ACNUMBER FROM ACNUMBER WHERE ICUST = '" + str(iCust) + "'")
                    cboAct = cursor.fetchall()

                with connection.cursor() as cursor:
                    cursor.execute(" SELECT A.ACBKCD, B.RESNAM FROM ACNUMBER A LEFT OUTER JOIN OSREFCP B ON A.ACBKCD = B.RESKEY AND B.RECODE = 'BNK'WHERE A.ICUST = '" + str(iCust) + "' GROUP BY A.ACBKCD, B.RESNAM ")
                    cboBank = cursor.fetchall()

                # 카드명
                with connection.cursor() as cursor:
                    cursor.execute(" SELECT A.CARDTYPE, B.RESNAM FROM ACCARD A LEFT OUTER JOIN OSREFCP B ON A.CARDTYPE = B.RESKEY AND B.RECODE = 'COC' WHERE A.ICUST = '" + str(iCust) + "' GROUP BY A.CARDTYPE, B.RESNAM ")
                    cboCard = cursor.fetchall()
                # 카드번호
                with connection.cursor() as cursor:
                    cursor.execute(" SELECT CARDNUM FROM ACCARD WHERE ICUST = '" + str(iCust) + "'")
                    cboCardNum = cursor.fetchall()

                return JsonResponse({"mainList": mainresult, "cboCust": cboCust, "cboAct": cboAct, "cboBank": cboBank, "cboCard": cboCard, "cboCardNum": cboCardNum})

            if actCode != '' and inputCardNum != '':
                with connection.cursor() as cursor:
                    cursor.execute("  SELECT IFNULL(A.IODATE, ''), IFNULL(A.ACTITLE, ''), IFNULL(A.ACAMTS, '') "
                                   "        , IFNULL(A.CRE_USER, ''), IFNULL(C.EMP_NME, ''), IFNULL(A.ACSEQN, ''), IFNULL(A.ACIOGB, '')"
                                   "        , IFNULL(A.MCODE, ''), IFNULL(D.MCODENM, ''), IFNULL(A.ACACNUMBER, ''), IFNULL(A.FIN_OPT, '')"
                                   "        , IFNULL(A.ACINFO, ''), IFNULL(E.ACBKCD, ''), IFNULL(F.RESNAM, ''), IFNULL(A.EXDATE, ''), IFNULL(A.ACGUBN, '') "
                                   " FROM SISACCTT A "
                                   " LEFT OUTER JOIN PIS1TB001 C "
                                   " ON A.CRE_USER = C.EMP_NBR "
                                   " LEFT OUTER JOIN OSCODEM D "
                                   " ON A.MCODE = D.MCODE "
                                   " LEFT OUTER JOIN ACNUMBER E "
                                   " ON A.ACACNUMBER = E.ACNUMBER "
                                   " LEFT OUTER JOIN OSREFCP F "
                                   " ON E.ACBKCD = F.RESKEY "
                                   " AND F.RECODE = 'BNK' "
                                   " WHERE A.FIN_OPT = 'Y'  "    
                                   # " AND A.IODATE <= '" + str(perDate) + "' "
                                   " AND A.ICUST = '" + str(iCust) + "' "
                                   " AND A.ACCUST like '%" + str(custCode) + "%' "
                                   " AND A.ACCARD = '" + str(inputCardNum) + "' "
                                   " AND A.ACACNUMBER = '" + str(actCode) + "' "
                                   " ORDER BY A.ACSEQN ASC ")
                    mainresult = cursor.fetchall()
                # " AND NOT EXISTS (SELECT OPT FROM OSSIGN WHERE OPT = 'N') "

                with connection.cursor() as cursor:
                    cursor.execute(" SELECT CUST_NBR, CUST_NME FROM MIS1TB003 WHERE ICUST = '" + str(iCust) + "'")
                    cboCust = cursor.fetchall()

                with connection.cursor() as cursor:
                    cursor.execute(" SELECT ACNUMBER FROM ACNUMBER WHERE ICUST = '" + str(iCust) + "'")
                    cboAct = cursor.fetchall()

                with connection.cursor() as cursor:
                    cursor.execute(" SELECT A.ACBKCD, B.RESNAM FROM ACNUMBER A LEFT OUTER JOIN OSREFCP B ON A.ACBKCD = B.RESKEY AND B.RECODE = 'BNK'WHERE A.ICUST = '" + str(iCust) + "' GROUP BY A.ACBKCD, B.RESNAM ")
                    cboBank = cursor.fetchall()

                # 카드명
                with connection.cursor() as cursor:
                    cursor.execute(" SELECT A.CARDTYPE, B.RESNAM FROM ACCARD A LEFT OUTER JOIN OSREFCP B ON A.CARDTYPE = B.RESKEY AND B.RECODE = 'COC' WHERE A.ICUST = '" + str(iCust) + "' GROUP BY A.CARDTYPE, B.RESNAM ")
                    cboCard = cursor.fetchall()
                # 카드번호
                with connection.cursor() as cursor:
                    cursor.execute(" SELECT CARDNUM FROM ACCARD WHERE ICUST = '" + str(iCust) + "'")
                    cboCardNum = cursor.fetchall()

                return JsonResponse({"mainList": mainresult, "cboCust": cboCust, "cboAct": cboAct, "cboBank": cboBank, "cboCard": cboCard, "cboCardNum": cboCardNum})


def cboCardNum(request):
    cboCard = request.POST.get('cboCard')
    user = request.session.get('userId')
    iCust = request.session.get('USER_ICUST')

    # 카드번호
    with connection.cursor() as cursor:
        cursor.execute(" SELECT CARDNUM FROM ACCARD WHERE ICUST = '" + str(iCust) + "' AND CARDTYPE = '" + str(cboCard) + "'")
        cboCardNum = cursor.fetchall()

        return JsonResponse({'cboCardNum': cboCardNum})


def cboActNum_search(request):
    user = request.session.get('userId')
    iCust = request.session.get('USER_ICUST')

    with connection.cursor() as cursor:
        cursor.execute(" SELECT ACNUMBER, ACNUM_NAME FROM ACNUMBER WHERE ICUST = '" + str(iCust) + "' ORDER BY ACNUMBER ")
        cboActNum = cursor.fetchall()

    with connection.cursor() as cursor:
        cursor.execute(" SELECT A.ACBKCD, B.RESNAM FROM ACNUMBER A LEFT OUTER JOIN OSREFCP B ON A.ACBKCD = B.RESKEY AND B.RECODE = 'BNK'WHERE A.ICUST = '" + str(iCust) + "' GROUP BY A.ACBKCD, B.RESNAM ")
        cboBank = cursor.fetchall()

        return JsonResponse({'cboActNum': cboActNum, "cboBank": cboBank})



def balanceChk(request):
    acNumber = request.POST.get('acNum')
    user = request.session.get('userId')
    iCust = request.session.get('USER_ICUST')

    with connection.cursor() as cursor:
        cursor.execute(" SELECT IFNULL(ACAMTS, 0) FROM ACBALANCE WHERE ACNUMBER = '" + str(acNumber) + "' AND ICUST = '" + str(iCust) + "' ")
        result = cursor.fetchall()

        if result:
            total = result[0][0]
        else:
            total = 0
    # 출금
    with connection.cursor() as cursor:
        cursor.execute(" SELECT IFNULL(SUM(ACAMTS), 0) FROM SISACCTT WHERE ACIOGB = '1' AND ACACNUMBER = '" + str(acNumber) + "' AND ICUST = '" + str(iCust) + "' ")
        result2 = cursor.fetchall()
        outTotal = result2[0][0]
        if result:
            outTotal = result2[0][0]
        else:
            outTotal = 0
    # 입금
    with connection.cursor() as cursor:
        cursor.execute(" SELECT IFNULL(SUM(ACAMTS), 0) FROM SISACCTT WHERE ACIOGB = '2' AND ACACNUMBER = '" + acNumber + "' AND ICUST = '" + iCust + "' ")
        result3 = cursor.fetchall()
        inTotal = result3[0][0]
        if result:
            inTotal = result3[0][0]
        else:
            inTotal = 0

        balance = (total - outTotal) + inTotal
        print(balance)

        return JsonResponse({'balance': balance, 'acNumber': acNumber})

def permitViews_save(request):
    pmtArray = json.loads(request.POST.get('pmtArrList'))
    iCust = request.session.get('USER_ICUST')
    offSet = request.POST.get('offSet')
    actNum = request.POST.get('actNum')
    perDate = request.POST.get('perDate')
    permit = 'Y'

    if offSet != '' and offSet is not None:
        balance = 0
        custBank = ""
        custAct = ""
        pmtArrayLists = list(filter(len, pmtArray))
        for data in range(1, len(pmtArrayLists)):

            with connection.cursor() as cursor:
                cursor.execute(" SELECT B.CUST_BKCD, B.CUST_ACNUM FROM SISACCTT A "
                               " LEFT OUTER JOIN MIS1TB003_D B "
                               " ON A.ACCUST = B.CUST_NBR "
                               " WHERE A.IODATE = '" + pmtArrayLists[data]["perDate"].replace("-", "") + "' AND A.ACIOGB = '" + pmtArrayLists[data]["acIogb"] + "' "
                               " AND A.ACSEQN = '" + pmtArrayLists[data]["acSeqn"] + "' AND A.ICUST = '" + str(iCust) + "' ")

                result = cursor.fetchall()

                if (len(result) != 0):
                    custBank = result[0][0]
                    custAct = result[0][1]

            if pmtArrayLists[data]["acIogb"]:
                with connection.cursor() as cursor:
                    cursor.execute(" UPDATE SISACCTT SET "
                                   "    ACDATE = '" + pmtArrayLists[data]["perDate"].replace("-", "") + "'"
                                   "  , FIN_OPT = '" + str(permit) + "' "
                                   "  , FIN_AMTS = '" + pmtArrayLists[data]["acAmts"] + "' "
                                   "  , OFF_GBN = '" + str(permit) + "' "
                                   "  , OFF_DATE = '" + pmtArrayLists[data]["perDate"].replace("-", "") + "' "
                                   "  , ACINFO = '" + str(custBank) + "," + str(custAct) + "' "
                                   "  , ACCUST_BNK = '" + str(custBank) + "' "
                                   "  , ACCUST_ACT = '" + str(custAct) + "' "
                                   "     WHERE IODATE = '" + pmtArrayLists[data]["ioDate"].replace("-", "") + "' "
                                   "     AND ACIOGB = '" + pmtArrayLists[data]["acIogb"] + "' "
                                   "     AND ACSEQN = '" + pmtArrayLists[data]["acSeqn"] + "' "
                                   "     AND ICUST = '" + str(iCust) + "' "
                    )
                    connection.commit()

                if pmtArrayLists[data]["acIogb"] == '1':
                    balance -= pmtArrayLists[data]["acAmts"]
                if pmtArrayLists[data]["acIogb"] == '2':
                    balance += pmtArrayLists[data]["acAmts"]

        if balance < 0:
            finalacIogb = '2'
            finalTitle = '상계 매입'
        if balance >= 0:
            finalacIogb = '1'
            finalTitle = '상계 매출'

        # mCode, aCode 계정코드를 어떻게 저장하면 되는지 물어보

        # 입금 or 출금 전표 저장
        now = datetime.date
        with connection.cursor() as cursor:
            cursor.execute("INSERT INTO SISACCTT "
                           "   (    "
                           "     IODATE "
                           ",    ACSEQN "
                           ",    ACIOGB "
                           ",    ACTITLE "
                           ",    ACAMTS "
                           ",    ACACNUMBER "
                           ",    ICUST "
                           ",    EXDATE "
                           ",    ACDATE "
                           ",    FIN_OPT "
                           ",    FIN_AMTS "
                           ",    OFF_GBN "
                           ",    OFF_AMTS "
                           ",    OFF_DATE "
                           ",    ACINFO "
                           ",    ACCUST_BNK "
                           ",    ACCUST_ACT "
                           "    ) "
                           "    VALUES "
                           "    (   "
                           "    '" + str(perDate).replace("-", "") + "' "
                           ",   (SELECT IFNULL (MAX(ACSEQN) + 1,1) AS COUNTED FROM SISACCTT A WHERE IODATE = '" + str(perDate).replace("-", "") + "' AND ACIOGB = '" + str(finalacIogb) + "') "
                           ",   '" + str(finalacIogb) + "'"
                           ",   '" + str(finalTitle) + "'"
                           ",   '" + str(balance) + "'"
                           ",   '" + str(actNum) + "'"
                           ",   '" + str(iCust) + "'"
                           ",   '" + str(perDate).replace("-", "") + "' "
                           ",   '" + str(perDate).replace("-", "") + "' "
                           ",   '" + str(permit) + "' "
                           ",   '" + str(balance) + "' "
                           ",   '" + str(permit) + "' "
                           ",   '" + str(balance) + "' "
                           ",   '" + str(perDate).replace("-", "") + "' "
                           ",   '" + str(custBank) + "," + str(custAct) + "' "
                           ",   '" + str(custBank) + "' "
                           ",   '" + str(custAct) + "' "
                           "    )   "
                           )
            connection.commit()

        return JsonResponse({'sucYn': "Y"})

    else:
        pmtArrayLists = list(filter(len, pmtArray))
        for data in range(1, len(pmtArrayLists)):
            custBank = ""
            custAct = ""
            if pmtArrayLists[data]["acIogb"]:
                amts = pmtArrayLists[data]["acAmts"]
                acAmts = amts.replace(",", "")
                print(acAmts)

            if pmtArrayLists[data]["acGubn"] == '2':
                with connection.cursor() as cursor:
                    cursor.execute(" SELECT B.CUST_BKCD, B.CUST_ACNUM FROM SISACCTT A "
                                   " LEFT OUTER JOIN MIS1TB003_D B "
                                   " ON A.ACCUST = B.CUST_NBR "
                                   " WHERE A.IODATE = '" + pmtArrayLists[data]["perDate"].replace("-", "") + "' AND A.ACIOGB = '" + pmtArrayLists[data]["acIogb"] + "' "
                                   " AND A.ACSEQN = '" + pmtArrayLists[data]["acSeqn"] + "' AND A.ICUST = '" + str(iCust) + "' ")

                    result = cursor.fetchall()

                    if (len(result) != 0):
                        custBank = result[0][0]
                        custAct = result[0][1]

            with connection.cursor() as cursor:
                cursor.execute(" UPDATE SISACCTT SET "
                               "    ACDATE = '" + pmtArrayLists[data]["perDate"].replace("-", "") + "'"
                               "  , FIN_OPT = '" + str(permit) + "' "
                               "  , FIN_AMTS = '" + str(acAmts) + "' "
                               "  , ACACNUMBER = '" + str(actNum) + "' "
                               "  , ACINFO = '" + str(custBank) + "," + str(custAct) + "' "
                               "  , ACCUST_BNK = '" + str(custBank) + "' "
                               "  , ACCUST_ACT = '" + str(custAct) + "' "
                               "     WHERE IODATE = '" + pmtArrayLists[data]["ioDate"].replace("-", "") + "' "
                               "     AND ACIOGB = '" + pmtArrayLists[data]["acIogb"] + "' "
                               "     AND ACSEQN = '" + pmtArrayLists[data]["acSeqn"] + "' "
                               "     AND ICUST = '" + str(iCust) + "' "
                )
                connection.commit()

        return JsonResponse({'sucYn': "Y"})
