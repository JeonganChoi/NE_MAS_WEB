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
    strDate = request.POST.get('strDate').replace("-", "")
    endDate = request.POST.get('endDate').replace("-", "")
    # 미시행 '0'/ 시행 = 1
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


    if custCode != '' and actCode == '' and inputCardNum == '':
        with connection.cursor() as cursor:
            cursor.execute("  SELECT IFNULL(A.IODATE, ''), IFNULL(A.ACTITLE, ''), IFNULL(A.ACAMTS, 0) "
                           "        , IFNULL(A.CRE_USER, ''), IFNULL(C.EMP_NME, ''), IFNULL(A.ACSEQN, ''), IFNULL(A.ACIOGB, '')"
                           "        , IFNULL(A.MCODE, ''), IFNULL(D.MCODENM, ''), IFNULL(A.ACACNUMBER, ''),  IFNULL(A.FIN_OPT, '')"
                           "        , IFNULL(A.ACINFO, ''), IFNULL(E.ACBKCD, ''), IFNULL(F.RESNAM, ''), IFNULL(A.EXDATE, ''), IFNULL(A.ACGUBN, '')"
                           "        , IFNULL(A.FIN_AMTS, 0), IFNULL(A.ACDATE, ''), IFNULL(A.APPLYDT, '') "
                           "        , IFNULL(A.ACCUST, ''), IFNULL(B.CUST_NME, ''), IFNULL(A.ACUSE, ''), IFNULL(A.ACODE, ''), IFNULL(A.ACDESC, '') "
                           "        , IFNULL(H.CUST_ACNUM, ''), IFNULL(H.CUST_BKCD, '') "
                           " FROM SISACCTT A "
                           " LEFT OUTER JOIN PIS1TB001 C "
                           " ON A.CRE_USER = C.EMP_NBR "  
                           " LEFT OUTER JOIN OSCODEM D "
                           " ON A.MCODE = D.MCODE "
                           " LEFT OUTER JOIN MIS1TB003 B "
                           " ON A.ACCUST = B.CUST_NBR "
                           " LEFT OUTER JOIN MIS1TB003_D H "
                           " ON A.ACCUST = H.CUST_NBR AND A.ICUST = H.ICUST "
                           " LEFT OUTER JOIN ACNUMBER E "
                           " ON A.ACACNUMBER = E.ACNUMBER "
                           " LEFT OUTER JOIN OSREFCP F "
                           " ON E.ACBKCD = F.RESKEY "
                           " AND F.RECODE = 'BNK' "
                           " WHERE A.ACDATE >= '" + str(strDate) + "' AND A.ACDATE <= '" + str(endDate) + "' "
                           " AND A.FIN_OPT = 'N'  "                         
                           " AND A.MID_OPT = 'Y' "
                           " AND A.ICUST = '" + str(iCust) + "' "
                           " AND A.ACCUST = '" + str(custCode) + "' "
                           " OR B.CUST_NME like '%" + str(custCode) + "%' "
                           " OR A.ACUSE like '%" + str(custCode) + "%' "
                           " ORDER BY A.IODATE ASC ")
            mainresult = cursor.fetchall()

            return JsonResponse({"mainList": mainresult})

    if custCode != '' and actCode != '' and inputCardNum == '':
        with connection.cursor() as cursor:
            cursor.execute("  SELECT IFNULL(A.IODATE, ''), IFNULL(A.ACTITLE, ''), IFNULL(A.ACAMTS, 0) "
                           "        , IFNULL(A.CRE_USER, ''), IFNULL(C.EMP_NME, ''), IFNULL(A.ACSEQN, ''), IFNULL(A.ACIOGB, '')"
                           "        , IFNULL(A.MCODE, ''), IFNULL(D.MCODENM, ''), IFNULL(A.ACACNUMBER, ''),  IFNULL(A.FIN_OPT, '')"
                           "        , IFNULL(A.ACINFO, ''), IFNULL(E.ACBKCD, ''), IFNULL(F.RESNAM, ''), IFNULL(A.EXDATE, ''), IFNULL(A.ACGUBN, '')"
                           "        , IFNULL(A.FIN_AMTS, 0), IFNULL(A.ACDATE, ''), IFNULL(A.APPLYDT, '') "
                           "        , IFNULL(A.ACCUST, ''), IFNULL(B.CUST_NME, ''), IFNULL(A.ACUSE, ''), IFNULL(A.ACODE, ''), IFNULL(A.ACDESC, '')"
                           "        , IFNULL(H.CUST_ACNUM, ''), IFNULL(H.CUST_BKCD, '') "
                           " FROM SISACCTT A "
                           " LEFT OUTER JOIN PIS1TB001 C "
                           " ON A.CRE_USER = C.EMP_NBR "  
                           " LEFT OUTER JOIN OSCODEM D "
                           " ON A.MCODE = D.MCODE "
                           " LEFT OUTER JOIN MIS1TB003 B "
                           " ON A.ACCUST = B.CUST_NBR "
                           " LEFT OUTER JOIN MIS1TB003_D H "
                           " ON A.ACCUST = H.CUST_NBR AND A.ICUST = H.ICUST "
                           " LEFT OUTER JOIN ACNUMBER E "
                           " ON A.ACACNUMBER = E.ACNUMBER "
                           " LEFT OUTER JOIN OSREFCP F "
                           " ON E.ACBKCD = F.RESKEY "
                           " AND F.RECODE = 'BNK' "
                           " WHERE A.ACDATE >= '" + str(strDate) + "' AND A.ACDATE <= '" + str(endDate) + "' "
                           " AND A.FIN_OPT = 'N'  "                         
                           " AND A.MID_OPT = 'Y' "
                           " AND A.ICUST = '" + str(iCust) + "' "
                           " AND A.ACCUST = '" + str(custCode) + "' "
                           " AND A.ACACNUMBER = '" + str(actCode) + "' "
                           " OR B.CUST_NME like '%" + str(custCode) + "%' "
                           " OR A.ACUSE like '%" + str(custCode) + "%' "
                           " ORDER BY A.IODATE ASC ")
            mainresult = cursor.fetchall()

            return JsonResponse({"mainList": mainresult})

    if custCode != '' and actCode != '' and inputCardNum != '':
        with connection.cursor() as cursor:
            cursor.execute("  SELECT IFNULL(A.IODATE, ''), IFNULL(A.ACTITLE, ''), IFNULL(A.ACAMTS, 0) "
                           "        , IFNULL(A.CRE_USER, ''), IFNULL(C.EMP_NME, ''), IFNULL(A.ACSEQN, ''), IFNULL(A.ACIOGB, '')"
                           "        , IFNULL(A.MCODE, ''), IFNULL(D.MCODENM, ''), IFNULL(A.ACACNUMBER, ''),  IFNULL(A.FIN_OPT, '')"
                           "        , IFNULL(A.ACINFO, ''), IFNULL(E.ACBKCD, ''), IFNULL(F.RESNAM, ''), IFNULL(A.EXDATE, ''), IFNULL(A.ACGUBN, '')"
                           "        , IFNULL(A.FIN_AMTS, 0), IFNULL(A.ACDATE, ''), IFNULL(A.APPLYDT, '') "
                           "        , IFNULL(A.ACCUST, ''), IFNULL(B.CUST_NME, ''), IFNULL(A.ACUSE, ''), IFNULL(A.ACODE, ''), IFNULL(A.ACDESC, '') "
                           "        , IFNULL(H.CUST_ACNUM, ''), IFNULL(H.CUST_BKCD, '') "
                           " FROM SISACCTT A "
                           " LEFT OUTER JOIN PIS1TB001 C "
                           " ON A.CRE_USER = C.EMP_NBR "  
                           " LEFT OUTER JOIN OSCODEM D "
                           " ON A.MCODE = D.MCODE "
                           " LEFT OUTER JOIN MIS1TB003 B "
                           " ON A.ACCUST = B.CUST_NBR "
                           " LEFT OUTER JOIN MIS1TB003_D H "
                           " ON A.ACCUST = H.CUST_NBR AND A.ICUST = H.ICUST "
                           " LEFT OUTER JOIN ACNUMBER E "
                           " ON A.ACACNUMBER = E.ACNUMBER "
                           " LEFT OUTER JOIN OSREFCP F "
                           " ON E.ACBKCD = F.RESKEY "
                           " AND F.RECODE = 'BNK' "
                           " WHERE A.ACDATE >= '" + str(strDate) + "' AND A.ACDATE <= '" + str(endDate) + "' "
                           " AND A.FIN_OPT = 'N'  "                         
                           " AND A.MID_OPT = 'Y' "
                           " AND A.ICUST = '" + str(iCust) + "' "
                           " AND A.ACCUST = '" + str(custCode) + "' "
                           " AND A.ACCARD = '" + str(inputCardNum) + "' "
                           " AND A.ACACNUMBER = '" + str(actCode) + "' "
                           " OR B.CUST_NME like '%" + str(custCode) + "%' "
                           " OR A.ACUSE like '%" + str(custCode) + "%' "
                           " ORDER BY A.IODATE ASC ")
            mainresult = cursor.fetchall()

            return JsonResponse({"mainList": mainresult})

    if custCode != '' and actCode == '' and inputCardNum != '':
        with connection.cursor() as cursor:
            cursor.execute("  SELECT IFNULL(A.IODATE, ''), IFNULL(A.ACTITLE, ''), IFNULL(A.ACAMTS, 0) "
                           "        , IFNULL(A.CRE_USER, ''), IFNULL(C.EMP_NME, ''), IFNULL(A.ACSEQN, ''), IFNULL(A.ACIOGB, '')"
                           "        , IFNULL(A.MCODE, ''), IFNULL(D.MCODENM, ''), IFNULL(A.ACACNUMBER, ''),  IFNULL(A.FIN_OPT, '')"
                           "        , IFNULL(A.ACINFO, ''), IFNULL(E.ACBKCD, ''), IFNULL(F.RESNAM, ''), IFNULL(A.EXDATE, ''), IFNULL(A.ACGUBN, '')"
                           "        , IFNULL(A.FIN_AMTS, 0), IFNULL(A.ACDATE, ''), IFNULL(A.APPLYDT, '') "
                           "        , IFNULL(A.ACCUST, ''), IFNULL(B.CUST_NME, ''), IFNULL(A.ACUSE, ''), IFNULL(A.ACODE, ''), IFNULL(A.ACDESC, '') "
                           "        , IFNULL(H.CUST_ACNUM, ''), IFNULL(H.CUST_BKCD, '') "
                           " FROM SISACCTT A "
                           " LEFT OUTER JOIN PIS1TB001 C "
                           " ON A.CRE_USER = C.EMP_NBR "  
                           " LEFT OUTER JOIN OSCODEM D "
                           " ON A.MCODE = D.MCODE "
                           " LEFT OUTER JOIN MIS1TB003 B "
                           " ON A.ACCUST = B.CUST_NBR "
                           " LEFT OUTER JOIN MIS1TB003_D H "
                           " ON A.ACCUST = H.CUST_NBR AND A.ICUST = H.ICUST "
                           " LEFT OUTER JOIN ACNUMBER E "
                           " ON A.ACACNUMBER = E.ACNUMBER "
                           " LEFT OUTER JOIN OSREFCP F "
                           " ON E.ACBKCD = F.RESKEY "
                           " AND F.RECODE = 'BNK' "
                           " WHERE A.ACDATE >= '" + str(strDate) + "' AND A.ACDATE <= '" + str(endDate) + "' "
                           " AND A.FIN_OPT = 'N'  "                         
                           " AND A.MID_OPT = 'Y' "
                           " AND A.ICUST = '" + str(iCust) + "' "
                           " AND A.ACCUST = '" + str(custCode) + "' "
                           " AND A.ACCARD = '" + str(inputCardNum) + "' "
                           " OR B.CUST_NME like '%" + str(custCode) + "%' "
                           " OR A.ACUSE like '%" + str(custCode) + "%' "
                           " ORDER BY A.IODATE ASC ")
            mainresult = cursor.fetchall()

            return JsonResponse({"mainList": mainresult})

    if custCode == '' and actCode == '' and inputCardNum != '':
        with connection.cursor() as cursor:
            cursor.execute("  SELECT IFNULL(A.IODATE, ''), IFNULL(A.ACTITLE, ''), IFNULL(A.ACAMTS, 0) "
                           "        , IFNULL(A.CRE_USER, ''), IFNULL(C.EMP_NME, ''), IFNULL(A.ACSEQN, ''), IFNULL(A.ACIOGB, '')"
                           "        , IFNULL(A.MCODE, ''), IFNULL(D.MCODENM, ''), IFNULL(A.ACACNUMBER, ''),  IFNULL(A.FIN_OPT, '')"
                           "        , IFNULL(A.ACINFO, ''), IFNULL(E.ACBKCD, ''), IFNULL(F.RESNAM, ''), IFNULL(A.EXDATE, ''), IFNULL(A.ACGUBN, '')"
                           "        , IFNULL(A.FIN_AMTS, 0), IFNULL(A.ACDATE, ''), IFNULL(A.APPLYDT, '') "
                           "        , IFNULL(A.ACCUST, ''), IFNULL(B.CUST_NME, ''), IFNULL(A.ACUSE, ''), IFNULL(A.ACODE, ''), IFNULL(A.ACDESC, '') "
                           "        , IFNULL(H.CUST_ACNUM, ''), IFNULL(H.CUST_BKCD, '') "
                           " FROM SISACCTT A "
                           " LEFT OUTER JOIN PIS1TB001 C "
                           " ON A.CRE_USER = C.EMP_NBR "  
                           " LEFT OUTER JOIN OSCODEM D "
                           " ON A.MCODE = D.MCODE "
                           " LEFT OUTER JOIN MIS1TB003 B "
                           " ON A.ACCUST = B.CUST_NBR "
                           " LEFT OUTER JOIN MIS1TB003_D H "
                           " ON A.ACCUST = H.CUST_NBR AND A.ICUST = H.ICUST "
                           " LEFT OUTER JOIN ACNUMBER E "
                           " ON A.ACACNUMBER = E.ACNUMBER "
                           " LEFT OUTER JOIN OSREFCP F "
                           " ON E.ACBKCD = F.RESKEY "
                           " AND F.RECODE = 'BNK' "
                           " WHERE A.ACDATE >= '" + str(strDate) + "' AND A.ACDATE <= '" + str(endDate) + "' "
                           " AND A.FIN_OPT = 'N'  "                         
                           " AND A.MID_OPT = 'Y' "
                           " AND A.ICUST = '" + str(iCust) + "' "
                           " AND A.ACCARD = '" + str(inputCardNum) + "' "
                           " ORDER BY A.IODATE ASC ")
            mainresult = cursor.fetchall()

            return JsonResponse({"mainList": mainresult})

    if custCode == '' and actCode != '' and inputCardNum != '':
        with connection.cursor() as cursor:
            cursor.execute("  SELECT IFNULL(A.IODATE, ''), IFNULL(A.ACTITLE, ''), IFNULL(A.ACAMTS, 0) "
                           "        , IFNULL(A.CRE_USER, ''), IFNULL(C.EMP_NME, ''), IFNULL(A.ACSEQN, ''), IFNULL(A.ACIOGB, '')"
                           "        , IFNULL(A.MCODE, ''), IFNULL(D.MCODENM, ''), IFNULL(A.ACACNUMBER, ''),  IFNULL(A.FIN_OPT, '')"
                           "        , IFNULL(A.ACINFO, ''), IFNULL(E.ACBKCD, ''), IFNULL(F.RESNAM, ''), IFNULL(A.EXDATE, ''), IFNULL(A.ACGUBN, '')"
                           "        , IFNULL(A.FIN_AMTS, 0), IFNULL(A.ACDATE, ''), IFNULL(A.APPLYDT, '') "
                           "        , IFNULL(A.ACCUST, ''), IFNULL(B.CUST_NME, ''), IFNULL(A.ACUSE, ''), IFNULL(A.ACODE, ''), IFNULL(A.ACDESC, '') "
                           "        , IFNULL(H.CUST_ACNUM, ''), IFNULL(H.CUST_BKCD, '') "
                           " FROM SISACCTT A "
                           " LEFT OUTER JOIN PIS1TB001 C "
                           " ON A.CRE_USER = C.EMP_NBR "  
                           " LEFT OUTER JOIN OSCODEM D "
                           " ON A.MCODE = D.MCODE "
                           " LEFT OUTER JOIN MIS1TB003 B "
                           " ON A.ACCUST = B.CUST_NBR "
                           " LEFT OUTER JOIN MIS1TB003_D H "
                           " ON A.ACCUST = H.CUST_NBR AND A.ICUST = H.ICUST "
                           " LEFT OUTER JOIN ACNUMBER E "
                           " ON A.ACACNUMBER = E.ACNUMBER "
                           " LEFT OUTER JOIN OSREFCP F "
                           " ON E.ACBKCD = F.RESKEY "
                           " AND F.RECODE = 'BNK' "
                           " WHERE A.ACDATE >= '" + str(strDate) + "' AND A.ACDATE <= '" + str(endDate) + "' "
                           " AND A.FIN_OPT = 'N'  "                         
                           " AND A.MID_OPT = 'Y' "
                           " AND A.ICUST = '" + str(iCust) + "' "
                           " AND A.ACCARD = '" + str(inputCardNum) + "' "
                           " AND A.ACACNUMBER = '" + str(actCode) + "' "
                           " ORDER BY A.IODATE ASC ")
            mainresult = cursor.fetchall()

            return JsonResponse({"mainList": mainresult})

    if custCode == '' and actCode != '' and inputCardNum == '':
        with connection.cursor() as cursor:
            cursor.execute("  SELECT IFNULL(A.IODATE, ''), IFNULL(A.ACTITLE, ''), IFNULL(A.ACAMTS, 0) "
                           "        , IFNULL(A.CRE_USER, ''), IFNULL(C.EMP_NME, ''), IFNULL(A.ACSEQN, ''), IFNULL(A.ACIOGB, '')"
                           "        , IFNULL(A.MCODE, ''), IFNULL(D.MCODENM, ''), IFNULL(A.ACACNUMBER, ''),  IFNULL(A.FIN_OPT, '')"
                           "        , IFNULL(A.ACINFO, ''), IFNULL(E.ACBKCD, ''), IFNULL(F.RESNAM, ''), IFNULL(A.EXDATE, ''), IFNULL(A.ACGUBN, '')"
                           "        , IFNULL(A.FIN_AMTS, 0), IFNULL(A.ACDATE, ''), IFNULL(A.APPLYDT, '') "
                           "        , IFNULL(A.ACCUST, ''), IFNULL(B.CUST_NME, ''), IFNULL(A.ACUSE, ''), IFNULL(A.ACODE, ''), IFNULL(A.ACDESC, '') "
                           "        , IFNULL(H.CUST_ACNUM, ''), IFNULL(H.CUST_BKCD, '') "
                           " FROM SISACCTT A "
                           " LEFT OUTER JOIN PIS1TB001 C "
                           " ON A.CRE_USER = C.EMP_NBR "  
                           " LEFT OUTER JOIN OSCODEM D "
                           " ON A.MCODE = D.MCODE "
                           " LEFT OUTER JOIN MIS1TB003 B "
                           " ON A.ACCUST = B.CUST_NBR "
                           " LEFT OUTER JOIN MIS1TB003_D H "
                           " ON A.ACCUST = H.CUST_NBR AND A.ICUST = H.ICUST "
                           " LEFT OUTER JOIN ACNUMBER E "
                           " ON A.ACACNUMBER = E.ACNUMBER "
                           " LEFT OUTER JOIN OSREFCP F "
                           " ON E.ACBKCD = F.RESKEY "
                           " AND F.RECODE = 'BNK' "
                           " WHERE A.ACDATE >= '" + str(strDate) + "' AND A.ACDATE <= '" + str(endDate) + "' "
                           " AND A.FIN_OPT = 'N'  "                         
                           " AND A.MID_OPT = 'Y' "
                           " AND A.ICUST = '" + str(iCust) + "' "
                           " AND A.ACACNUMBER = '" + str(actCode) + "' "
                           " ORDER BY A.IODATE ASC ")
            mainresult = cursor.fetchall()

            return JsonResponse({"mainList": mainresult})

    if custCode == '' and actCode == '' and inputCardNum == '':
        with connection.cursor() as cursor:
            cursor.execute("  SELECT IFNULL(A.IODATE, ''), IFNULL(A.ACTITLE, ''), IFNULL(A.ACAMTS, 0) "
                           "        , IFNULL(A.CRE_USER, ''), IFNULL(C.EMP_NME, ''), IFNULL(A.ACSEQN, ''), IFNULL(A.ACIOGB, '')"
                           "        , IFNULL(A.MCODE, ''), IFNULL(D.MCODENM, ''), IFNULL(A.ACACNUMBER, ''),  IFNULL(A.FIN_OPT, '')"
                           "        , IFNULL(A.ACINFO, ''), IFNULL(E.ACBKCD, ''), IFNULL(F.RESNAM, ''), IFNULL(A.EXDATE, ''), IFNULL(A.ACGUBN, '')"
                           "        , IFNULL(A.FIN_AMTS, 0), IFNULL(A.ACDATE, ''), IFNULL(A.APPLYDT, '') "
                           "        , IFNULL(A.ACCUST, ''), IFNULL(B.CUST_NME, ''), IFNULL(A.ACUSE, ''), IFNULL(A.ACODE, ''), IFNULL(A.ACDESC, '') "
                           "        , IFNULL(H.CUST_ACNUM, ''), IFNULL(H.CUST_BKCD, '') "
                           " FROM SISACCTT A "
                           " LEFT OUTER JOIN PIS1TB001 C "
                           " ON A.CRE_USER = C.EMP_NBR "  
                           " LEFT OUTER JOIN OSCODEM D "
                           " ON A.MCODE = D.MCODE "
                           " LEFT OUTER JOIN MIS1TB003 B "
                           " ON A.ACCUST = B.CUST_NBR "
                           " LEFT OUTER JOIN MIS1TB003_D H "
                           " ON A.ACCUST = H.CUST_NBR AND A.ICUST = H.ICUST "
                           " LEFT OUTER JOIN ACNUMBER E "
                           " ON A.ACACNUMBER = E.ACNUMBER "
                           " LEFT OUTER JOIN OSREFCP F "
                           " ON E.ACBKCD = F.RESKEY "
                           " AND F.RECODE = 'BNK' "
                           " WHERE A.ACDATE >= '" + str(strDate) + "' AND A.ACDATE <= '" + str(endDate) + "' "
                           " AND A.FIN_OPT = 'N'  "                         
                           " AND A.MID_OPT = 'Y' "
                           " AND A.ICUST = '" + str(iCust) + "' "
                           " ORDER BY A.IODATE ASC ")
            mainresult = cursor.fetchall()

        return JsonResponse({"mainList": mainresult})

def permited_search(request):
    strDate = request.POST.get('strDate').replace("-", "")
    endDate = request.POST.get('endDate').replace("-", "")
    # 미시행 '0'/ 시행 = 1
    permitGbn = request.POST.get('permitGbn', '')
    custCode = request.POST.get('custCode', '')
    bankCode = request.POST.get('bankCode', '')
    actCode = request.POST.get('actCode', '')
    inputCard = request.POST.get('inputCard', '')
    inputCardNum = request.POST.get('inputCardNum', '')
    user = request.session.get('userId')
    iCust = request.session.get('USER_ICUST')
    # 시행
    if permitGbn == '1':
        if custCode != '' and bankCode == '' and inputCardNum == '':
            with connection.cursor() as cursor:
                cursor.execute(" SELECT IFNULL(A.ACDATE, ''), IFNULL(A.SEQ, ''), IFNULL(A.PMSEQN, ''), IFNULL(A.ACAMTS, 0) "
                               "      , IFNULL(A.IODATE, ''), IFNULL(A.ACSEQN, ''), IFNULL(A.ACIOGB, ''), IFNULL(A.FIN_AMTS, 0) AS FINAL "
                               "     , IFNULL(A.APPLYDT, ''), IFNULL(A.ACTITLE, ''), IFNULL(A.ACCUST, '') "
                               "     , IFNULL(G.CUST_NME, ''), IFNULL(A.ACUSE, ''), IFNULL(A.ACAMTS, 0) AS TOTAL "
                               "     , IFNULL(A.CRE_USER, ''), IFNULL(C.EMP_NME, ''), IFNULL(A.MCODE, ''), IFNULL(D.MCODENM, '') "
                               "     , IFNULL(A.ACODE, ''), IFNULL(H.RESNAM, ''), IFNULL(A.ACACNUMBER, ''), IFNULL(A.ACCUST_BNK, '') "
                               "     , IFNULL(A.ACCUST_ACT, ''), IFNULL(A.ACGUBN, ''), IFNULL(A.ACACNUMBER, ''), IFNULL(E.ACBKCD, '')"
                               "     , IFNULL(A.ACDESC, ''), IFNULL(A.ACCARD, ''), IFNULL(A.EXDATE, '') "
                               " FROM ACTSTMENT A "
                               " LEFT OUTER JOIN PIS1TB001 C  ON A.CRE_USER = C.EMP_NBR "
                               " LEFT OUTER JOIN OSCODEM D  ON A.MCODE = D.MCODE "
                               " LEFT OUTER JOIN MIS1TB003 G  ON A.ACCUST = G.CUST_NBR "
                               " LEFT OUTER JOIN OSREFCP H ON A.ACODE = H.RESKEY AND H.RECODE = 'ACD' "
                               " LEFT OUTER JOIN ACNUMBER E ON A.ACACNUMBER = E.ACNUMBER "
                               " WHERE A.ACDATE >= '" + str(strDate) + "' AND A.ACDATE <= '" + str(endDate) + "' "
                               " AND A.ICUST = '" + str(iCust) + "' "
                               " AND A.ACACNUMBER = '" + str(actCode) + "' "
                               " AND A.ACCARD = '" + str(inputCardNum) + "' "
                               " ORDER BY A.ACDATE ASC ")
                mainresult = cursor.fetchall()

                return JsonResponse({"mainList": mainresult})

        if custCode != '' and bankCode != '' and inputCardNum == '':
            with connection.cursor() as cursor:
                cursor.execute(" SELECT IFNULL(A.ACDATE, ''), IFNULL(A.SEQ, ''), IFNULL(A.PMSEQN, ''), IFNULL(A.ACAMTS, 0) "
                               "      , IFNULL(A.IODATE, ''), IFNULL(A.ACSEQN, ''), IFNULL(A.ACIOGB, ''), IFNULL(A.FIN_AMTS, 0) AS FINAL "
                               "     , IFNULL(A.APPLYDT, ''), IFNULL(A.ACTITLE, ''), IFNULL(A.ACCUST, '') "
                               "     , IFNULL(G.CUST_NME, ''), IFNULL(A.ACUSE, ''), IFNULL(A.ACAMTS, 0) AS TOTAL "
                               "     , IFNULL(A.CRE_USER, ''), IFNULL(C.EMP_NME, ''), IFNULL(A.MCODE, ''), IFNULL(D.MCODENM, '') "
                               "     , IFNULL(A.ACODE, ''), IFNULL(H.RESNAM, ''), IFNULL(A.ACACNUMBER, ''), IFNULL(A.ACCUST_BNK, '') "
                               "     , IFNULL(A.ACCUST_ACT, ''), IFNULL(A.ACGUBN, ''), IFNULL(A.ACACNUMBER, ''), IFNULL(E.ACBKCD, ''), IFNULL(A.ACDESC, ''), IFNULL(A.ACCARD, ''), IFNULL(A.EXDATE, '')  "
                               " FROM ACTSTMENT A "
                               " LEFT OUTER JOIN PIS1TB001 C  ON A.CRE_USER = C.EMP_NBR "
                               " LEFT OUTER JOIN OSCODEM D  ON A.MCODE = D.MCODE "
                               " LEFT OUTER JOIN MIS1TB003 G  ON A.ACCUST = G.CUST_NBR "
                               " LEFT OUTER JOIN OSREFCP H ON A.ACODE = H.RESKEY AND H.RECODE = 'ACD' "
                               " LEFT OUTER JOIN ACNUMBER E ON A.ACACNUMBER = E.ACNUMBER "
                               " WHERE A.ACDATE >= '" + str(strDate) + "' AND A.ACDATE <= '" + str(endDate) + "' "
                               " AND A.ICUST = '" + str(iCust) + "' "
                               " AND A.ACACNUMBER = '" + str(actCode) + "' "
                               " AND A.ACCARD = '" + str(inputCardNum) + "' "
                               " ORDER BY A.ACDATE ASC ")
                mainresult = cursor.fetchall()

                return JsonResponse({"mainList": mainresult})

        if custCode != '' and bankCode != '' and inputCardNum != '':
            with connection.cursor() as cursor:
                cursor.execute(" SELECT IFNULL(A.ACDATE, ''), IFNULL(A.SEQ, ''), IFNULL(A.PMSEQN, ''), IFNULL(A.ACAMTS, 0) "
                               "      , IFNULL(A.IODATE, ''), IFNULL(A.ACSEQN, ''), IFNULL(A.ACIOGB, ''), IFNULL(A.FIN_AMTS, 0) AS FINAL "
                               "     , IFNULL(A.APPLYDT, ''), IFNULL(A.ACTITLE, ''), IFNULL(A.ACCUST, '') "
                               "     , IFNULL(G.CUST_NME, ''), IFNULL(A.ACUSE, ''), IFNULL(A.ACAMTS, 0) AS TOTAL "
                               "     , IFNULL(A.CRE_USER, ''), IFNULL(C.EMP_NME, ''), IFNULL(A.MCODE, ''), IFNULL(D.MCODENM, '') "
                               "     , IFNULL(A.ACODE, ''), IFNULL(H.RESNAM, ''), IFNULL(A.ACACNUMBER, ''), IFNULL(A.ACCUST_BNK, '') "
                               "     , IFNULL(A.ACCUST_ACT, ''), IFNULL(A.ACGUBN, ''), IFNULL(A.ACACNUMBER, ''), IFNULL(E.ACBKCD, ''), IFNULL(A.ACDESC, ''), IFNULL(A.ACCARD, ''), IFNULL(A.EXDATE, '')  "
                               " FROM ACTSTMENT A "
                               " LEFT OUTER JOIN PIS1TB001 C  ON A.CRE_USER = C.EMP_NBR "
                               " LEFT OUTER JOIN OSCODEM D  ON A.MCODE = D.MCODE "
                               " LEFT OUTER JOIN MIS1TB003 G  ON A.ACCUST = G.CUST_NBR "
                               " LEFT OUTER JOIN OSREFCP H ON A.ACODE = H.RESKEY AND H.RECODE = 'ACD' "
                               " LEFT OUTER JOIN ACNUMBER E ON A.ACACNUMBER = E.ACNUMBER "
                               " WHERE A.ACDATE >= '" + str(strDate) + "' AND A.ACDATE <= '" + str(endDate) + "' "
                               " AND A.ICUST = '" + str(iCust) + "' "
                               " AND A.ACACNUMBER = '" + str(actCode) + "' "
                               " AND A.ACCARD = '" + str(inputCardNum) + "' "
                               " ORDER BY A.ACDATE ASC ")
                mainresult = cursor.fetchall()

                return JsonResponse({"mainList": mainresult})

        if custCode != '' and actCode == '' and inputCardNum != '':
            with connection.cursor() as cursor:
                cursor.execute(" SELECT IFNULL(A.ACDATE, ''), IFNULL(A.SEQ, ''), IFNULL(A.PMSEQN, ''), IFNULL(A.ACAMTS, 0) "
                               "      , IFNULL(A.IODATE, ''), IFNULL(A.ACSEQN, ''), IFNULL(A.ACIOGB, ''), IFNULL(A.FIN_AMTS, 0) AS FINAL "
                               "     , IFNULL(A.APPLYDT, ''), IFNULL(A.ACTITLE, ''), IFNULL(A.ACCUST, '') "
                               "     , IFNULL(G.CUST_NME, ''), IFNULL(A.ACUSE, ''), IFNULL(A.ACAMTS, 0) AS TOTAL "
                               "     , IFNULL(A.CRE_USER, ''), IFNULL(C.EMP_NME, ''), IFNULL(A.MCODE, ''), IFNULL(D.MCODENM, '') "
                               "     , IFNULL(A.ACODE, ''), IFNULL(H.RESNAM, ''), IFNULL(A.ACACNUMBER, ''), IFNULL(A.ACCUST_BNK, '') "
                               "     , IFNULL(A.ACCUST_ACT, ''), IFNULL(A.ACGUBN, ''), IFNULL(A.ACACNUMBER, ''), IFNULL(E.ACBKCD, ''), IFNULL(A.ACDESC, ''), IFNULL(A.ACCARD, ''), IFNULL(A.EXDATE, '')  "
                               " FROM ACTSTMENT A "
                               " LEFT OUTER JOIN PIS1TB001 C  ON A.CRE_USER = C.EMP_NBR "
                               " LEFT OUTER JOIN OSCODEM D  ON A.MCODE = D.MCODE "
                               " LEFT OUTER JOIN MIS1TB003 G  ON A.ACCUST = G.CUST_NBR "
                               " LEFT OUTER JOIN OSREFCP H ON A.ACODE = H.RESKEY AND H.RECODE = 'ACD' "
                               " LEFT OUTER JOIN ACNUMBER E ON A.ACACNUMBER = E.ACNUMBER "
                               " WHERE A.ACDATE >= '" + str(strDate) + "' AND A.ACDATE <= '" + str(endDate) + "' "
                               " AND A.ICUST = '" + str(iCust) + "' "
                               " AND A.ACACNUMBER = '" + str(actCode) + "' "
                               " AND A.ACCARD = '" + str(inputCardNum) + "' "
                               " ORDER BY A.ACDATE ASC ")
                mainresult = cursor.fetchall()

                return JsonResponse({"mainList": mainresult})

        if custCode == '' and actCode == '' and inputCardNum != '':
            with connection.cursor() as cursor:
                cursor.execute(" SELECT IFNULL(A.ACDATE, ''), IFNULL(A.SEQ, ''), IFNULL(A.PMSEQN, ''), IFNULL(A.ACAMTS, 0) "
                               "      , IFNULL(A.IODATE, ''), IFNULL(A.ACSEQN, ''), IFNULL(A.ACIOGB, ''), IFNULL(A.FIN_AMTS, 0) AS FINAL "
                               "     , IFNULL(A.APPLYDT, ''), IFNULL(A.ACTITLE, ''), IFNULL(A.ACCUST, '') "
                               "     , IFNULL(G.CUST_NME, ''), IFNULL(A.ACUSE, ''), IFNULL(A.ACAMTS, 0) AS TOTAL "
                               "     , IFNULL(A.CRE_USER, ''), IFNULL(C.EMP_NME, ''), IFNULL(A.MCODE, ''), IFNULL(D.MCODENM, '') "
                               "     , IFNULL(A.ACODE, ''), IFNULL(H.RESNAM, ''), IFNULL(A.ACACNUMBER, ''), IFNULL(A.ACCUST_BNK, '') "
                               "     , IFNULL(A.ACCUST_ACT, ''), IFNULL(A.ACGUBN, ''), IFNULL(A.ACACNUMBER, ''), IFNULL(E.ACBKCD, ''), IFNULL(A.ACDESC, ''), IFNULL(A.ACCARD, ''), IFNULL(A.EXDATE, '')  "
                               " FROM ACTSTMENT A "
                               " LEFT OUTER JOIN PIS1TB001 C  ON A.CRE_USER = C.EMP_NBR "
                               " LEFT OUTER JOIN OSCODEM D  ON A.MCODE = D.MCODE "
                               " LEFT OUTER JOIN MIS1TB003 G  ON A.ACCUST = G.CUST_NBR "
                               " LEFT OUTER JOIN OSREFCP H ON A.ACODE = H.RESKEY AND H.RECODE = 'ACD' "
                               " LEFT OUTER JOIN ACNUMBER E ON A.ACACNUMBER = E.ACNUMBER "
                               " WHERE A.ACDATE >= '" + str(strDate) + "' AND A.ACDATE <= '" + str(endDate) + "' "
                               " AND A.ICUST = '" + str(iCust) + "' "
                               " AND A.ACACNUMBER = '" + str(actCode) + "' "
                               " AND A.ACCARD = '" + str(inputCardNum) + "' "
                               " ORDER BY A.ACDATE ASC ")
                mainresult = cursor.fetchall()


                return JsonResponse({"mainList": mainresult})

        if custCode == '' and actCode != '' and inputCardNum != '':
            with connection.cursor() as cursor:
                cursor.execute(" SELECT IFNULL(A.ACDATE, ''), IFNULL(A.SEQ, ''), IFNULL(A.PMSEQN, ''), IFNULL(A.ACAMTS, 0) "
                               "      , IFNULL(A.IODATE, ''), IFNULL(A.ACSEQN, ''), IFNULL(A.ACIOGB, ''), IFNULL(A.FIN_AMTS, 0) AS FINAL "
                               "     , IFNULL(A.APPLYDT, ''), IFNULL(A.ACTITLE, ''), IFNULL(A.ACCUST, '') "
                               "     , IFNULL(G.CUST_NME, ''), IFNULL(A.ACUSE, ''), IFNULL(A.ACAMTS, 0) AS TOTAL "
                               "     , IFNULL(A.CRE_USER, ''), IFNULL(C.EMP_NME, ''), IFNULL(A.MCODE, ''), IFNULL(D.MCODENM, '') "
                               "     , IFNULL(A.ACODE, ''), IFNULL(H.RESNAM, ''), IFNULL(A.ACACNUMBER, ''), IFNULL(A.ACCUST_BNK, '') "
                               "     , IFNULL(A.ACCUST_ACT, ''), IFNULL(A.ACGUBN, ''), IFNULL(A.ACACNUMBER, ''), IFNULL(E.ACBKCD, ''), IFNULL(A.ACDESC, ''), IFNULL(A.ACCARD, ''), IFNULL(A.EXDATE, '')  "
                               " FROM ACTSTMENT A "
                               " LEFT OUTER JOIN PIS1TB001 C  ON A.CRE_USER = C.EMP_NBR "
                               " LEFT OUTER JOIN OSCODEM D  ON A.MCODE = D.MCODE "
                               " LEFT OUTER JOIN MIS1TB003 G  ON A.ACCUST = G.CUST_NBR "
                               " LEFT OUTER JOIN OSREFCP H ON A.ACODE = H.RESKEY AND H.RECODE = 'ACD' "
                               " LEFT OUTER JOIN ACNUMBER E ON A.ACACNUMBER = E.ACNUMBER "
                               " WHERE A.ACDATE >= '" + str(strDate) + "' AND A.ACDATE <= '" + str(endDate) + "' "
                               " AND A.ICUST = '" + str(iCust) + "' "
                               " AND A.ACACNUMBER = '" + str(actCode) + "' "
                               " AND A.ACCARD = '" + str(inputCardNum) + "' "
                               " ORDER BY A.ACDATE ASC ")
                mainresult = cursor.fetchall()

                return JsonResponse({"mainList": mainresult})

        if custCode == '' and actCode != '' and inputCardNum == '':
            with connection.cursor() as cursor:
                cursor.execute(" SELECT IFNULL(A.ACDATE, ''), IFNULL(A.SEQ, ''), IFNULL(A.PMSEQN, ''), IFNULL(A.ACAMTS, 0) "
                               "      , IFNULL(A.IODATE, ''), IFNULL(A.ACSEQN, ''), IFNULL(A.ACIOGB, ''), IFNULL(A.FIN_AMTS, 0) AS FINAL "
                               "     , IFNULL(A.APPLYDT, ''), IFNULL(A.ACTITLE, ''), IFNULL(A.ACCUST, '') "
                               "     , IFNULL(G.CUST_NME, ''), IFNULL(A.ACUSE, ''), IFNULL(A.ACAMTS, 0) AS TOTAL "
                               "     , IFNULL(A.CRE_USER, ''), IFNULL(C.EMP_NME, ''), IFNULL(A.MCODE, ''), IFNULL(D.MCODENM, '') "
                               "     , IFNULL(A.ACODE, ''), IFNULL(H.RESNAM, ''), IFNULL(A.ACACNUMBER, ''), IFNULL(A.ACCUST_BNK, '') "
                               "     , IFNULL(A.ACCUST_ACT, ''), IFNULL(A.ACGUBN, ''), IFNULL(A.ACACNUMBER, ''), IFNULL(E.ACBKCD, ''), IFNULL(A.ACDESC, ''), IFNULL(A.ACCARD, ''), IFNULL(A.EXDATE, '')  "
                               " FROM ACTSTMENT A "
                               " LEFT OUTER JOIN PIS1TB001 C  ON A.CRE_USER = C.EMP_NBR "
                               " LEFT OUTER JOIN OSCODEM D  ON A.MCODE = D.MCODE "
                               " LEFT OUTER JOIN MIS1TB003 G  ON A.ACCUST = G.CUST_NBR "
                               " LEFT OUTER JOIN OSREFCP H ON A.ACODE = H.RESKEY AND H.RECODE = 'ACD' "
                               " LEFT OUTER JOIN ACNUMBER E ON A.ACACNUMBER = E.ACNUMBER "
                               " WHERE A.ACDATE >= '" + str(strDate) + "' AND A.ACDATE <= '" + str(endDate) + "' "
                               " AND A.ICUST = '" + str(iCust) + "' "
                               " AND A.ACACNUMBER = '" + str(actCode) + "' "
                               " ORDER BY A.ACDATE ASC ")
                mainresult = cursor.fetchall()

                return JsonResponse({"mainList": mainresult})

        else:
            with connection.cursor() as cursor:
                cursor.execute(" SELECT IFNULL(A.ACDATE, ''), IFNULL(A.SEQ, ''), IFNULL(A.PMSEQN, ''), IFNULL(A.ACAMTS, 0) "
                               "      , IFNULL(A.IODATE, ''), IFNULL(A.ACSEQN, ''), IFNULL(A.ACIOGB, ''), IFNULL(A.FIN_AMTS, 0) AS FINAL "
                               "     , IFNULL(A.APPLYDT, ''), IFNULL(A.ACTITLE, ''), IFNULL(A.ACCUST, '') "
                               "     , IFNULL(G.CUST_NME, ''), IFNULL(A.ACUSE, ''), IFNULL(A.ACAMTS, 0) AS TOTAL "
                               "     , IFNULL(A.CRE_USER, ''), IFNULL(C.EMP_NME, ''), IFNULL(A.MCODE, ''), IFNULL(D.MCODENM, '') "
                               "     , IFNULL(A.ACODE, ''), IFNULL(H.RESNAM, ''), IFNULL(A.ACACNUMBER, ''), IFNULL(A.ACCUST_BNK, '') "
                               "     , IFNULL(A.ACCUST_ACT, ''), IFNULL(A.ACGUBN, ''), IFNULL(A.ACACNUMBER, ''), IFNULL(E.ACBKCD, ''), IFNULL(A.ACDESC, ''), IFNULL(A.ACCARD, ''), IFNULL(A.EXDATE, '')  "
                               " FROM ACTSTMENT A "
                               " LEFT OUTER JOIN PIS1TB001 C  ON A.CRE_USER = C.EMP_NBR "
                               " LEFT OUTER JOIN OSCODEM D  ON A.MCODE = D.MCODE "
                               " LEFT OUTER JOIN MIS1TB003 G  ON A.ACCUST = G.CUST_NBR "
                               " LEFT OUTER JOIN OSREFCP H ON A.ACODE = H.RESKEY AND H.RECODE = 'ACD' "
                               " LEFT OUTER JOIN ACNUMBER E ON A.ACACNUMBER = E.ACNUMBER "
                               " WHERE A.ACDATE >= '" + str(strDate) + "' AND A.ACDATE <= '" + str(endDate) + "' "
                               " AND A.ICUST = '" + str(iCust) + "' "
                               " ORDER BY A.ACDATE ASC ")
                mainresult = cursor.fetchall()

            return JsonResponse({"mainList": mainresult})


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
    acIogb = request.POST.get('acIogb')
    user = request.session.get('userId')
    iCust = request.session.get('USER_ICUST')

    with connection.cursor() as cursor:
        cursor.execute(" SELECT ACNUMBER, ACNUM_NAME FROM ACNUMBER WHERE ICUST = '" + str(iCust) + "' ORDER BY ACNUMBER ")
        cboActNum = cursor.fetchall()

    with connection.cursor() as cursor:
        cursor.execute(" SELECT A.ACBKCD, B.RESNAM FROM ACNUMBER A LEFT OUTER JOIN OSREFCP B ON A.ACBKCD = B.RESKEY AND B.RECODE = 'BNK'WHERE A.ICUST = '" + str(iCust) + "' GROUP BY A.ACBKCD, B.RESNAM ")
        cboBank = cursor.fetchall()

    if acIogb != '':
        # 출금
        if acIogb == '1':
            with connection.cursor() as cursor:
                cursor.execute(" SELECT MCODE, MCODENM FROM OSCODEM WHERE ICUST = '" + str(iCust) + "' AND MCODE LIKE '5%' ORDER BY MCODE ")
                cboMcode = cursor.fetchall()
        # 입금
        if acIogb == '2':
            with connection.cursor() as cursor:
                cursor.execute(" SELECT MCODE, MCODENM FROM OSCODEM WHERE ICUST = '" + str(iCust) + "' AND MCODE LIKE '4%' ORDER BY MCODE ")
                cboMcode = cursor.fetchall()

        return JsonResponse({'cboActNum': cboActNum, "cboBank": cboBank, "cboMcode": cboMcode})



def balanceChk(request):
    acNumber = request.POST.get('actNum')
    user = request.session.get('userId')
    iCust = request.session.get('USER_ICUST')

    with connection.cursor() as cursor:
        cursor.execute(" SELECT IFNULL(ACAMTS, 0) FROM ACBALANCE WHERE ACNUMBER = '" + str(acNumber) + "' AND ICUST = '" + str(iCust) + "' ")
        result = cursor.fetchall()
        total = int(result[0][0])

    # 출금
    with connection.cursor() as cursor:
        cursor.execute(" SELECT IFNULL(SUM(ACAMTS), 0) FROM SISACCTT WHERE ACIOGB = '1' AND ACACNUMBER = '" + str(acNumber) + "' AND ICUST = '" + str(iCust) + "' ")
        result2 = cursor.fetchall()
        outTotal = int(result2[0][0])

    # 입금
    with connection.cursor() as cursor:
        cursor.execute(" SELECT IFNULL(SUM(ACAMTS), 0) FROM SISACCTT WHERE ACIOGB = '2' AND ACACNUMBER = '" + str(acNumber) + "' AND ICUST = '" + iCust + "' ")
        result3 = cursor.fetchall()
        inTotal = int(result3[0][0])

        balance = (int(total) - int(outTotal)) + int(inTotal)
        print(balance)

        return JsonResponse({'balance': balance, 'acNumber': acNumber})




#기존에 있는지 확인
def permitedChk(request):
    perDate = request.POST.get('perDate').replace("-", "")
    ioDate = request.POST.get('ioDate').replace("-", "")
    acIogb = request.POST.get('acIogb')
    acSeqn = request.POST.get('acSeqn')
    mCode = request.POST.get('mCode')
    acGubn = request.POST.get('acGubn')
    acAmts = request.POST.get('acAmts')
    user = request.session.get('userId')
    iCust = request.session.get('USER_ICUST')

    with connection.cursor() as cursor:
        cursor.execute(" SELECT COUNT(*) AS COUNTED FROM ACTSTMENT "
                       " WHERE ICUST = '" + str(iCust) + "' AND IODATE = '" + str(ioDate) + "' "
                       " AND ACIOGB = '" + str(acIogb) + "' AND ACSEQN = '" + str(acSeqn) + "' "
                       " AND MCODE = '" + str(mCode) + "' AND ACAMTS = '" + str(acAmts) + "'; ")
        result = cursor.fetchall()
        count = int(result[0][0])

        if count > 0:
            # with connection.cursor() as cursor:
            #     cursor.execute(" SELECT IFNULL(ACAMTS, 0) AS COUNTED FROM ACTSTMENT "
            #                    " WHERE ICUST = '" + str(iCust) + "' AND IODATE = '" + str(ioDate) + "' "
            #                    " AND ACIOGB = '" + str(acIogb) + "' AND ACSEQN = '" + str(acSeqn) + "' "
            #                    " AND MCODE = '" + str(mCode) + "'; ")
            #     result = cursor.fetchall()
            #     current = int(result[0][0])
            permit = 'y'
        else:
            permit = 'N'

        return JsonResponse({'permit': permit})






def permitViews_save(request):
    pmtArray = json.loads(request.POST.get('pmtArrList'))
    user = request.session.get('userId')
    iCust = request.session.get('USER_ICUST')
    offSet = request.POST.get('offSet')
    actNum = request.POST.get('actNum')
    actBank = request.POST.get('actBank')
    permitDate = request.POST.get('permitDate')
    permit = 'Y'

    # 저장하는 SEQ를 기준으로 PMSEQN 순번을 쌓음(여러개를 한번에 승인할때)
    with connection.cursor() as cursor:
        cursor.execute(" SELECT IFNULL (MAX(SEQ) + 1,1) AS COUNTED FROM ACTSTMENT A WHERE ACDATE = '" + str(permitDate).replace("-", "") + "' ")
        result3 = cursor.fetchall()
        seqKey = result3[0][0]

    pmtArrayLists = list(filter(len, pmtArray))
    for data in range(1, len(pmtArrayLists)):

        orgAmts = pmtArrayLists[data]["orgAmts"].replace(",", "")
        lastAmts = pmtArrayLists[data]["lastAmts"].replace(",", "")
        cntAmts = pmtArrayLists[data]["acAmts"].replace(",", "")

        if int(lastAmts) == 0:
            fin_amts = cntAmts
        if int(lastAmts) > 0:
            fin_amts = int(lastAmts) + int(cntAmts)
        # 최종금액이랑 전표금액이랑 같으면
        if fin_amts == orgAmts:
            fin_opt = 'Y'
        if cntAmts < orgAmts or fin_amts < orgAmts:
            fin_opt = 'N'


        with connection.cursor() as cursor:
            cursor.execute(" UPDATE SISACCTT SET "
                           "    ACDATE = '" + pmtArrayLists[data]["perDate"].replace("-", "") + "'"
                           "  , FIN_OPT = '" + str(fin_opt) + "' "
                           "  , FIN_AMTS = '" + str(fin_amts) + "' "
                           "  , ACGUNO_BK = '" + str(actBank) + "' "
                           "  , ACACNUMBER = '" + str(actNum) + "' "
                           "  , MCODE = '" + pmtArrayLists[data]["mCode"] + "' "
                           "     WHERE IODATE = '" + pmtArrayLists[data]["ioDate"].replace("-", "") + "' "
                           "     AND ACIOGB = '" + pmtArrayLists[data]["acIogb"] + "' "
                           "     AND ACSEQN = '" + pmtArrayLists[data]["acSeqn"] + "' "
                           "     AND ICUST = '" + str(iCust) + "' "
            )
            connection.commit()

        # acamts: 계속 쌓이는값, fin_amts:전표 금액
        # 금액이 얼마이던 시행으로 처리
        with connection.cursor() as cursor:
            cursor.execute(" INSERT INTO ACTSTMENT "
                           "   (    "
                           "      ACDATE "
                           "    , SEQ "
                           "    , PMSEQN "
                           "    , ACAMTS "
                           "    , ACODE "
                           "    , ACCUST "
                           "    , ACCUST_BNK "
                           "    , ACCUST_ACT "
                           "    , ACUSE "
                           "    , ACGUBN "
                           "    , ACGUNO_BK "
                           "    , ACACNUMBER "
                           "    , ACDESC "
                           "    , ACTITLE "
                           "    , CRE_USER "
                           "    , CRE_DT "
                           "    , ICUST "
                           "    , IODATE "
                           "    , ACSEQN "
                           "    , ACIOGB "
                           "    , MCODE "
                           "    , EXDATE "
                           "    , FIN_AMTS "
                           "    ) "
                           "    VALUES "
                           "    (   "
                           "    '" + str(pmtArrayLists[data]["perDate"].replace("-","")) + "' "
                           "    , '" + str(seqKey) + "' "
                           "    , (SELECT IFNULL (MAX(PMSEQN) + 1,1) AS COUNTED FROM ACTSTMENT A WHERE ACDATE = '" + str(pmtArrayLists[data]["perDate"].replace("-","")) + "'AND SEQ = '" + str(seqKey) + "' AND ICUST = '" + str(iCust) + "'  ) "
                           "    , '" + pmtArrayLists[data]["acAmts"].replace(",","") + "' "
                           "    , ( SELECT IFNULL(ACODE, '') AS ACODE FROM SISACCTT A WHERE ICUST = '" + str(iCust) + "' AND IODATE = '" + str(pmtArrayLists[data]["ioDate"].replace("-", "")) + "' AND ACIOGB = '" + str(pmtArrayLists[data]["acIogb"]) + "' AND ACSEQN = '" + str(pmtArrayLists[data]["acSeqn"]) + "'  ) "
                           "    , '" + str(pmtArrayLists[data]["acCust"]) + "'"
                           "    , ( SELECT IFNULL(CUST_BKCD, '') AS CUST_BNK FROM MIS1TB003_D A WHERE ICUST = '" + str(iCust) + "' AND CUST_NBR = '" + str(pmtArrayLists[data]["acCust"]) + "' ) "
                           "    , ( SELECT IFNULL(CUST_ACNUM, '') AS CUST_ACT FROM MIS1TB003_D A WHERE ICUST = '" + str(iCust) + "' AND CUST_NBR = '" + str(pmtArrayLists[data]["acCust"]) + "' ) "
                           "    , ( SELECT IFNULL(ACUSE, '') AS ACUSE FROM SISACCTT A WHERE ICUST = '" + str(iCust) + "' AND IODATE = '" + str(pmtArrayLists[data]["ioDate"].replace("-", "")) + "' AND ACIOGB = '" + str(pmtArrayLists[data]["acIogb"]) + "' AND ACSEQN = '" + str(pmtArrayLists[data]["acSeqn"]) + "'  ) "
                           "    , ( SELECT IFNULL(ACGUBN, '') AS ACGUBN FROM SISACCTT A WHERE ICUST = '" + str(iCust) + "' AND IODATE = '" + str(pmtArrayLists[data]["ioDate"].replace("-", "")) + "' AND ACIOGB = '" + str(pmtArrayLists[data]["acIogb"]) + "' AND ACSEQN = '" + str(pmtArrayLists[data]["acSeqn"]) + "'  ) "
                           "    , ( SELECT IFNULL(ACBKCD, '') AS ACBKCD FROM ACNUMBER A WHERE ICUST = '" + str(iCust) + "' AND ACNUMBER = '" + str(actNum) + "' ) "
                           "    , '" + str(actNum) + "' "
                           "    , ( SELECT IFNULL(ACDESC, '') AS ACDESC FROM SISACCTT A WHERE ICUST = '" + str(iCust) + "' AND IODATE = '" + str(pmtArrayLists[data]["ioDate"].replace("-", "")) + "' AND ACIOGB = '" + str(pmtArrayLists[data]["acIogb"]) + "' AND ACSEQN = '" + str(pmtArrayLists[data]["acSeqn"]) + "'  ) "
                           "    , ( SELECT IFNULL(ACTITLE, '') AS ACTITLE FROM SISACCTT A WHERE ICUST = '" + str(iCust) + "' AND IODATE = '" + str(pmtArrayLists[data]["ioDate"].replace("-", "")) + "' AND ACIOGB = '" + str(pmtArrayLists[data]["acIogb"]) + "' AND ACSEQN = '" + str(pmtArrayLists[data]["acSeqn"]) + "'  ) "
                           "    , '" + str(user) + "' "
                           "    , date_format(now(), '%Y%m%d') "
                           "    , '" + str(iCust) + "' "
                           "    , '" + str(pmtArrayLists[data]["ioDate"].replace("-", "")) + "'"
                           "    , '" + str(pmtArrayLists[data]["acSeqn"]) + "' "
                           "    , '" + str(pmtArrayLists[data]["acIogb"]) + "' "
                           "    , '" + pmtArrayLists[data]["mCode"] + "' "
                           "    , '" + str(pmtArrayLists[data]["exDate"].replace("-", "")) + "'"                           
                           "    , '" + str(orgAmts) + "' "
                           "    )   "
                           )
            connection.commit()

        return JsonResponse({'sucYn': "Y"})



def permitViews_dlt(request):
    pmtArray = json.loads(request.POST.get('pmtArrList'))
    iCust = request.session.get('USER_ICUST')
    permit = 'N'
    final = 0

    pmtArrayLists = list(filter(len, pmtArray))
    for data in range(0, len(pmtArrayLists)):
        with connection.cursor() as cursor:
            cursor.execute(" DELETE FROM ACTSTMENT WHERE ACDATE = '" + str(pmtArrayLists[data]["perDate"].replace("-", "")) + "'"
                           "                      AND SEQ = '" + str(pmtArrayLists[data]["seq"]) + "' "
                           "                      AND PMSEQN = '" + str(pmtArrayLists[data]["pmSeqn"]) + "'"
                           "                      AND ICUST = '" + str(iCust) + "'")
            connection.commit()

        if pmtArrayLists[data]["orgAmts"] != '':
            orgAmts = pmtArrayLists[data]["orgAmts"].replace(",", "")
        if pmtArrayLists[data]["orgAmts"] == '':
            orgAmts = 0

        if pmtArrayLists[data]["lastAmts"] != '':
            lastAmts = pmtArrayLists[data]["lastAmts"].replace(",", "")
        if pmtArrayLists[data]["lastAmts"] == '':
            lastAmts = 0
        if pmtArrayLists[data]["acAmts"] != '':
            acAmts = pmtArrayLists[data]["acAmts"].replace(",", "")
        if pmtArrayLists[data]["acAmts"] == '':
            acAmts = 0

        if int(lastAmts) > 0:
            final = int(orgAmts) - int(lastAmts)
        if int(lastAmts) == 0:
            final = int(orgAmts) - int(acAmts)

        with connection.cursor() as cursor:
            cursor.execute(" UPDATE SISACCTT SET "
                           "    ACDATE = '" + pmtArrayLists[data]["exDate"] + "'"
                           "  , FIN_OPT = 'N' "
                           "  , FIN_AMTS = '" + str(final) + "' "
                           "     WHERE IODATE = '" + pmtArrayLists[data]["ioDate"].replace("-", "") + "' "
                           "     AND ACIOGB = '" + pmtArrayLists[data]["acIogb"] + "' "
                           "     AND ACSEQN = '" + pmtArrayLists[data]["acSeqn"] + "' "
                           "     AND ICUST = '" + str(iCust) + "' ")
            connection.commit()


        # with connection.cursor() as cursor:
        #     cursor.execute(" DELETE FROM SISACCTT WHERE ACSEQN = '" + pmtArrayLists[data]["acSeqn"] + "'"
        #                    "                      AND ACIOGB = '" + pmtArrayLists[data]["acIogb"] + "' "
        #                    "                      AND IODATE = '" + pmtArrayLists[data]["ioDate"].replace("-", "") + "'"
        #                    "                      AND MCODE = '" + pmtArrayLists[data]["mCode"] + "' "
        #                    "                      AND ICUST = '" + str(iCust) + "'")
        #     connection.commit()

        # with connection.cursor() as cursor:
        #     cursor.execute(" SELECT COUNT(SEQ) FROM OSSIGN WHERE ACSEQN = '" + pmtArrayLists[data]["acSeqn"] + "' AND ACIOGB = '" + pmtArrayLists[data]["acIogb"] + "' "
        #                    "                                AND ACDATE = '" + pmtArrayLists[data]["ioDate"].replace("-", "") + "'  AND ICUST = '" + str(iCust) + "' ")
        #     result = cursor.fetchall()
        #     count = int(result[0][0])
        #
        # if count > 0:
        #     with connection.cursor() as cursor:
        #         cursor.execute(" DELETE FROM OSSIGN WHERE ACSEQN = '" + pmtArrayLists[data]["acSeqn"] + "'"
        #                        "                      AND ACIOGB = '" + pmtArrayLists[data]["acIogb"] + "' "
        #                        "                      AND ACDATE = '" + pmtArrayLists[data]["ioDate"].replace("-", "") + "'"
        #                        "                      AND ICUST = '" + str(iCust) + "'")
        #         connection.commit()

    return JsonResponse({'sucYn': "Y"})




    #     with connection.cursor() as cursor:
    #         cursor.execute(" UPDATE SISACCTT SET "
    #                        "    ACDATE = '" + pmtArrayLists[data]["perDate"].replace("-", "") + "'"
    #                        "  , FIN_OPT = '" + str(permit) + "' "
    #                        "  , FIN_AMTS = '" + str(acAmts) + "' "
    #                        "  , ACAMTS = '" + str(acAmts) + "' "
    #                        "  , ACACNUMBER = '" + str(actNum) + "' "
    #                        "  , ACINFO = '" + str(custBank) + "," + str(custAct) + "' "
    #                        "  , ACCUST_BNK = '" + str(custBank) + "' "
    #                        "  , ACCUST_ACT = '" + str(custAct) + "' "
    #                        "  , MCODE = '" + pmtArrayLists[data]["mCode"] + "' "
    #                        "     WHERE IODATE = '" + pmtArrayLists[data]["ioDate"].replace("-", "") + "' "
    #                        "     AND ACIOGB = '" + pmtArrayLists[data]["acIogb"] + "' "
    #                        "     AND ACSEQN = '" + pmtArrayLists[data]["acSeqn"] + "' "
    #                        "     AND ICUST = '" + str(iCust) + "' "
    #         )
    #         connection.commit()
    #
    # return JsonResponse({'sucYn': "Y"})


    # 상계 ###########################################################################################################
    # if offSet == '2':
    #     balance = 0
    #     acUse = ""
    #     custCode = ""
    #     custBank = ""
    #     custAct = ""
    #
    #     with connection.cursor() as cursor:
    #         cursor.execute(" SELECT IFNULL (MAX(PMSEQN) + 1,1) AS COUNTED FROM ACTSTMENT A WHERE ACDATE = '" + str(permitDate).reaplace("-", "") + "' ")
    #         result3 = cursor.fetchall()
    #         pmSeqn = result3[0][0]
    #
    #
    #     pmtArrayLists = list(filter(len, pmtArray))
    #     for data in range(0, len(pmtArrayLists)):
    #
    #         with connection.cursor() as cursor:
    #             cursor.execute(" SELECT B.CUST_BKCD, B.CUST_ACNUM, A.ACDESC FROM SISACCTT A "
    #                            " LEFT OUTER JOIN MIS1TB003_D B "
    #                            " ON A.ACCUST = B.CUST_NBR "
    #                            " WHERE A.IODATE = '" + pmtArrayLists[data]["perDate"].replace("-", "") + "' AND A.ACIOGB = '" + pmtArrayLists[data]["acIogb"] + "' "
    #                            " AND A.ACSEQN = '" + pmtArrayLists[data]["acSeqn"] + "' AND A.ICUST = '" + str(iCust) + "' ")
    #
    #             result = cursor.fetchall()
    #             check = int(result[0][0])
    #
    #             if check > 0:
    #                 custBank = result[0][0]
    #                 custAct = result[0][1]
    #                 acDesc = result[0][2]
    #
    #         if pmtArrayLists[data]["acIogb"]:
    #             with connection.cursor() as cursor:
    #                 cursor.execute(" UPDATE SISACCTT SET "
    #                                "    ACDATE = '" + pmtArrayLists[data]["perDate"].replace("-", "") + "'"
    #                                "  , FIN_OPT = '" + str(permit) + "' "
    #                                "  , FIN_AMTS = '" + pmtArrayLists[data]["acAmts"].replace(",", "") + "' "
    #                                "  , MCODE = '" + pmtArrayLists[data]["mCode"] + "' "
    #                                "  , OFF_GBN = '" + str(offSet) + "' "
    #                                "  , OFF_DATE = '" + pmtArrayLists[data]["perDate"].replace("-", "") + "' "
    #                                "     WHERE IODATE = '" + pmtArrayLists[data]["ioDate"].replace("-", "") + "' "
    #                                "     AND ACIOGB = '" + pmtArrayLists[data]["acIogb"] + "' "
    #                                "     AND ACSEQN = '" + pmtArrayLists[data]["acSeqn"] + "' "
    #                                "     AND ICUST = '" + str(iCust) + "' "
    #                 )
    #                 connection.commit()
    #
    #         if pmtArrayLists[data]["acIogb"] == '1':
    #             balance -= pmtArrayLists[data]["acAmts"]
    #         if pmtArrayLists[data]["acIogb"] == '2':
    #             balance += pmtArrayLists[data]["acAmts"]
    #
    #         if balance < 0:
    #             finalacIogb = '2'
    #             finalTitle = '상계 매입'
    #         if balance >= 0:
    #             finalacIogb = '1'
    #             finalTitle = '상계 매출'
    #
    #         # mCode, aCode 계정코드를 어떻게 저장하면 되는지 물어보
    #
    #         # 입금 or 출금 전표 저장
    #         now = datetime.date
    #         with connection.cursor() as cursor:
    #             cursor.execute("INSERT INTO ACTSTMENT "
    #                            "   (    "
    #                            "     ACDATE "
    #                            ",    PMSEQN "
    #                            ",    ACSEQN "
    #                            ",    SEQ "
    #                            ",    ACIOGB "
    #                            ",    ACTITLE "
    #                            ",    ACAMTS "
    #                            ",    ACACNUMBER "
    #                            ",    ICUST "
    #                            ",    OFF_GBN "
    #                            ",    ACINFO "
    #                            ",    ACCUST_BNK "
    #                            ",    ACCUST_ACT "
    #                            "    ) "
    #                            "    VALUES "
    #                            "    (   "
    #                            "    '" + str(permitDate).reaplace("-", "") + "' "
    #                            ",   '" + str(pmSeqn) + "' "
    #                            ",   '" + pmtArrayLists[data]["acSeqn"] + "' "
    #                            ",   (SELECT IFNULL (MAX(SEQ) + 1,1) AS COUNTED FROM ACTSTMENT A WHERE ACDATE = '" + pmtArrayLists[data]["perDate"].replace("-", "") + "' AND ACIOGB = '" + str(finalacIogb) + "' AND ACSEQN = '" + pmtArrayLists[data]["acSeqn"] + "' AND ICUST = '" + str(iCust) + "' ) "
    #                            ",   '" + str(finalacIogb) + "'"
    #                            ",   '" + str(finalTitle) + "'"
    #                            ",   '" + pmtArrayLists[data]["acAmts"] + "'"
    #                            ",   '" + str(actNum) + "'"
    #                            ",   '" + str(iCust) + "'"
    #                            ",   '" + str(offSet) + "' "
    #                            ",   '" + str(custBank) + "," + str(custAct) + "' "
    #                            ",   '" + str(custBank) + "' "
    #                            ",   '" + str(custAct) + "' "
    #                            "    )   "
    #                            )
    #             connection.commit()
    #
    #     return JsonResponse({'sucYn': "Y"})


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
    # if offSet != '':
    #     if permitGbn == '':
    #         if actCode == '':
    #             with connection.cursor() as cursor:
    #                 cursor.execute(" SELECT IFNULL(A.IODATE, ''), IFNULL(A.ACTITLE, ''), IFNULL(A.ACAMTS, 0) "
    #                                "        , IFNULL(A.CRE_USER, ''), IFNULL(C.EMP_NME, ''), IFNULL(A.ACSEQN, ''), IFNULL(A.ACIOGB, '')"
    #                                "        , IFNULL(A.MCODE, ''), IFNULL(D.MCODENM, ''), IFNULL(A.ACACNUMBER, ''), IFNULL(A.FIN_OPT, '')"
    #                                "        , IFNULL(A.ACINFO, ''), IFNULL(E.ACBKCD, ''), IFNULL(F.RESNAM, ''), IFNULL(A.EXDATE, ''), IFNULL(A.ACGUBN, '')"
    #                                "        , IFNULL(A.FIN_AMTS, 0), IFNULL(A.ACDATE, ''), IFNULL(A.APPLYDT, '') "
    #                                " FROM SISACCTT A "
    #                                " LEFT OUTER JOIN PIS1TB001 C "
    #                                " ON A.CRE_USER = C.EMP_NBR "
    #                                " LEFT OUTER JOIN OSCODEM D "
    #                                " ON A.MCODE = D.MCODE "
    #                                " LEFT OUTER JOIN ACNUMBER E "
    #                                " ON A.ACACNUMBER = E.ACNUMBER "
    #                                " LEFT OUTER JOIN OSREFCP F "
    #                                " ON E.ACBKCD = F.RESKEY "
    #                                " AND F.RECODE = 'BNK' "
    #                                " WHERE A.FIN_OPT = 'N'  "
    #                                " AND A.MID_OPT = 'Y' "
    #                                " AND A.OFF_GBN = 'off' "
    #                                " AND A.ICUST = '" + str(iCust) + "' "
    #                                " AND A.ACCUST like '%" + str(custCode) + "%' "
    #                                " ORDER BY A.IODATE ASC ")
    #                 mainresult = cursor.fetchall()
    #
    #             return JsonResponse({"mainList": mainresult})
    #
    #         if actCode != '':
    #             with connection.cursor() as cursor:
    #                 cursor.execute("  SELECT IFNULL(A.IODATE, ''), IFNULL(A.ACTITLE, ''), IFNULL(A.ACAMTS, 0) "
    #                                "        , IFNULL(A.CRE_USER, ''), IFNULL(C.EMP_NME, ''), IFNULL(A.ACSEQN, ''), IFNULL(A.ACIOGB, '')"
    #                                "        , IFNULL(A.MCODE, ''), IFNULL(D.MCODENM, ''), IFNULL(A.ACACNUMBER, ''), IFNULL(A.FIN_OPT, '')"
    #                                "        , IFNULL(A.ACINFO, ''), IFNULL(E.ACBKCD, ''), IFNULL(F.RESNAM, ''), IFNULL(A.EXDATE, ''), IFNULL(A.ACGUBN, '')"
    #                                "        , IFNULL(A.FIN_AMTS, 0), IFNULL(A.ACDATE, ''), IFNULL(A.APPLYDT, '') "
    #                                " FROM SISACCTT A "
    #                                " LEFT OUTER JOIN PIS1TB001 C "
    #                                " ON A.CRE_USER = C.EMP_NBR "
    #                                " LEFT OUTER JOIN OSCODEM D "
    #                                " ON A.MCODE = D.MCODE "
    #                                " LEFT OUTER JOIN ACNUMBER E "
    #                                " ON A.ACACNUMBER = E.ACNUMBER "
    #                                " LEFT OUTER JOIN OSREFCP F "
    #                                " ON E.ACBKCD = F.RESKEY "
    #                                " AND F.RECODE = 'BNK' "
    #                                " WHERE A.FIN_OPT = 'N'  "
    #                                " AND A.MID_OPT = 'Y' "
    #                                " AND A.OFF_GBN = 'off'"
    #                                " AND A.ICUST = '" + str(iCust) + "' "
    #                                " AND A.ACCUST like '%" + str(custCode) + "%' "
    #                                " AND A.ACACNUMBER = '" + str(actCode) + "' "
    #                                " ORDER BY A.IODATE ASC ")
    #                 mainresult = cursor.fetchall()
    #
    #             return JsonResponse({"mainList": mainresult})
    #
    #     if permitGbn != '':
    #         if actCode == '':
    #             with connection.cursor() as cursor:
    #                 cursor.execute("  SELECT IFNULL(A.IODATE, ''), IFNULL(A.ACTITLE, ''), IFNULL(A.ACAMTS, 0) "
    #                                "        , IFNULL(A.CRE_USER, ''), IFNULL(C.EMP_NME, ''), IFNULL(A.ACSEQN, ''), IFNULL(A.ACIOGB, '')"
    #                                "        , IFNULL(A.MCODE, ''), IFNULL(D.MCODENM, ''), IFNULL(A.ACACNUMBER, ''), IFNULL(A.FIN_OPT, '')"
    #                                "        , IFNULL(A.ACINFO, ''), IFNULL(E.ACBKCD, ''), IFNULL(F.RESNAM, ''), IFNULL(A.EXDATE, ''), IFNULL(A.ACGUBN, '')"
    #                                "        , IFNULL(A.FIN_AMTS, 0), IFNULL(A.ACDATE, ''), IFNULL(A.APPLYDT, '') "
    #                                " FROM SISACCTT A "
    #                                " LEFT OUTER JOIN PIS1TB001 C "
    #                                " ON A.CRE_USER = C.EMP_NBR "
    #                                " LEFT OUTER JOIN OSCODEM D "
    #                                " ON A.MCODE = D.MCODE "
    #                                " LEFT OUTER JOIN ACNUMBER E "
    #                                " ON A.ACACNUMBER = E.ACNUMBER "
    #                                " LEFT OUTER JOIN OSREFCP F "
    #                                " ON E.ACBKCD = F.RESKEY "
    #                                " AND F.RECODE = 'BNK' "
    #                                " WHERE A.FIN_OPT = 'Y'  "
    #                                " AND A.MID_OPT = 'Y' "
    #                                " AND A.OFF_GBN = 'off'"
    #                                " AND A.ICUST = '" + str(iCust) + "' "
    #                                " AND A.ACCUST like '%" + str(custCode) + "%' "
    #                                " ORDER BY A.IODATE ASC ")
    #                 mainresult = cursor.fetchall()
    #             # " AND NOT EXISTS (SELECT OPT FROM OSSIGN WHERE OPT = 'N') "
    #
    #             return JsonResponse({"mainList": mainresult})
    #         if actCode != '':
    #             with connection.cursor() as cursor:
    #                 cursor.execute("  SELECT IFNULL(A.IODATE, ''), IFNULL(A.ACTITLE, ''), IFNULL(A.ACAMTS, 0) "
    #                                "        , IFNULL(A.CRE_USER, ''), IFNULL(C.EMP_NME, ''), IFNULL(A.ACSEQN, ''), IFNULL(A.ACIOGB, '')"
    #                                "        , IFNULL(A.MCODE, ''), IFNULL(D.MCODENM, ''), IFNULL(A.ACACNUMBER, ''), IFNULL(A.FIN_OPT, '')"
    #                                "        , IFNULL(A.ACINFO, ''), IFNULL(E.ACBKCD, ''), IFNULL(F.RESNAM, ''), IFNULL(A.EXDATE, ''), IFNULL(A.ACGUBN, '')"
    #                                "        , IFNULL(A.FIN_AMTS, 0), IFNULL(A.ACDATE, ''), IFNULL(A.APPLYDT, '') "
    #                                " FROM SISACCTT A "
    #                                " LEFT OUTER JOIN PIS1TB001 C "
    #                                " ON A.CRE_USER = C.EMP_NBR "
    #                                " LEFT OUTER JOIN OSCODEM D "
    #                                " ON A.MCODE = D.MCODE "
    #                                " LEFT OUTER JOIN ACNUMBER E "
    #                                " ON A.ACACNUMBER = E.ACNUMBER "
    #                                " LEFT OUTER JOIN OSREFCP F "
    #                                " ON E.ACBKCD = F.RESKEY "
    #                                " AND F.RECODE = 'BNK' "
    #                                " WHERE A.FIN_OPT = 'Y'  "
    #                                " AND A.MID_OPT = 'Y' "
    #                                " AND A.OFF_GBN = 'off'"
    #                                " AND A.ICUST = '" + str(iCust) + "' "
    #                                " AND A.ACCUST like '%" + str(custCode) + "%' "
    #                                 " AND A.ACACNUMBER = '" + str(actCode) + "' "
    #                                " ORDER BY A.IODATE ASC ")
    #                 mainresult = cursor.fetchall()
    #             # " AND NOT EXISTS (SELECT OPT FROM OSSIGN WHERE OPT = 'N') "
    #
    #             return JsonResponse({"mainList": mainresult})

# with connection.cursor() as cursor:
#     cursor.execute(" SELECT COUNT(*) AS COUNTED FROM ACTSTMENT "
#                    " WHERE ICUST = '" + str(iCust) + "' AND IODATE = '" + str(pmtArrayLists[data]["ioDate"].replace("-", "")) + "' "
#                    " AND ACIOGB = '" + str(pmtArrayLists[data]["acIogb"]) + "' AND ACSEQN = '" + str(pmtArrayLists[data]["acSeqn"]) + "' ")
#
#     result = cursor.fetchall()
#     count = int(result[0][0])
#
#     # 입/출금 전표건으로 시행된 건이 있으면
#     if count > 0:
#         with connection.cursor() as cursor:
#             cursor.execute(" SELECT SUM(IFNULL(FIN_AMTS, 0)) FROM SISACCTT "
#                            " WHERE ICUST = '" + str(iCust) + "' AND IODATE = '" + str(pmtArrayLists[data]["ioDate"].replace("-", "")) + "' "
#                            " AND ACIOGB = '" + str(pmtArrayLists[data]["acIogb"]) + "' AND ACSEQN = '" + str(pmtArrayLists[data]["acSeqn"]) + "' ")
#
#             result2 = cursor.fetchall()
#             fin_amts = int(result2[0][0])
#
#             fin_amts = int(fin_amts) + int(pmtArrayLists[data]["acAmts"].replace(",",""))
#
#     # 입/출금 전표건으로 시행된 건이 없으면
#     else:
#         fin_amts = pmtArrayLists[data]["acAmts"].replace(",","")
#         print(fin_amts)



