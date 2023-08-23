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


def empViews(request):

    return render(request, "base/base-emp.html")

def empViews_search(request):
    empCode = request.POST.get('empCode')
    empType = request.POST.get('empType')

    if empType == '0':
        with connection.cursor() as cursor:
            cursor.execute(
                            "SELECT "
                            "       A.EMP_NBR "
                            "     , IFNULL(A.EMP_GBN, '') "
                            "     , IFNULL(A.EMP_NME, '') "
                            "     , IFNULL(A.EMP_PASS, '') "
                            "     , IFNULL(A.EMP_IPSA, '') "
                            "     , IFNULL(A.EMP_TESA, '') "
                            "     , IFNULL(A.EMP_JO, '') "
                            "     , IFNULL(C.RESNAM, '') "
                            "     , IFNULL(A.EMP_DEPT, '') "
                            "     , IFNULL(B.RESNAM, '') "
                            "     , IFNULL(A.EMP_TEL, '') "
                            "     , IFNULL(A.EMP_PRC, '') "
                            "     , IFNULL(D.RESNAM, '') "
                            "     , IFNULL(A.EMP_PRC1, '') "
                            "     , IFNULL(E.RESNAM, '') "
                            "     , IFNULL(A.EMP_PRC2, '') "
                            "     , IFNULL(F.RESNAM, '') "
                            "     , IFNULL(A.EMP_PRC3, '') "
                            "     , IFNULL(G.RESNAM, '') "
                            "     , IFNULL(A.EMP_COM, '') "
                            "     , IFNULL(H.RESNAM, '') "
                            "   FROM pis1tb001 A "
                            "   LEFT OUTER JOIN osrefcp B "
                            "   ON B.RECODE = 'DPT' "
                            "   AND A.EMP_DEPT = B.RESKEY "
                            "   LEFT OUTER JOIN osrefcp C "
                            "   ON C.RECODE = 'JJO' "
                            "   AND A.EMP_JO = C.RESKEY "
                            "   LEFT OUTER JOIN osrefcp D "
                            "   ON D.RECODE = 'POP' "
                            "   AND A.EMP_PRC = D.RESKEY "
                            "   LEFT OUTER JOIN osrefcp E "
                            "   ON E.RECODE = 'POP' "
                            "   AND A.EMP_PRC1 = E.RESKEY "
                            "   LEFT OUTER JOIN osrefcp F "
                            "   ON F.RECODE = 'POP' "
                            "   AND A.EMP_PRC2 = F.RESKEY "
                            "   LEFT OUTER JOIN osrefcp G "
                            "   ON G.RECODE = 'POP' "
                            "   AND A.EMP_PRC3 = G.RESKEY "
                            "   LEFT OUTER JOIN osrefcp H "
                            "   ON H.RECODE = 'COM' "
                            "   AND A.EMP_COM = H.RESKEY "
                           )
            empresult = cursor.fetchall()

        return JsonResponse({"empList": empresult})

    if empCode != '' and empCode is not None:
        with connection.cursor() as cursor:
            cursor.execute(
                " SELECT "
                "       A.EMP_NBR "
                "     , IFNULL(A.EMP_GBN, '') "
                "     , IFNULL(A.EMP_NME, '') "
                "     , IFNULL(A.EMP_PASS, '') "
                "     , IFNULL(A.EMP_IPSA, '') "
                "     , IFNULL(A.EMP_TESA, '') "
                "     , IFNULL(A.EMP_JO, '') "
                "     , IFNULL(C.RESNAM, '') "
                "     , IFNULL(A.EMP_DEPT, '') "
                "     , IFNULL(B.RESNAM, '') "
                "     , IFNULL(A.EMP_TEL, '') "
                "     , IFNULL(A.EMP_PRC, '') "
                "     , IFNULL(D.RESNAM, '') "
                "     , IFNULL(A.EMP_PRC1, '') "
                "     , IFNULL(E.RESNAM, '') "
                "     , IFNULL(A.EMP_PRC2, '') "
                "     , IFNULL(F.RESNAM, '') "
                "     , IFNULL(A.EMP_PRC3, '') "
                "     , IFNULL(G.RESNAM, '') "
                "     , IFNULL(A.EMP_COM, '') "
                "     , IFNULL(H.RESNAM, '')"
                "   FROM pis1tb001 A "
                "   LEFT OUTER JOIN osrefcp B "
                "   ON B.RECODE = 'DPT' "
                "   AND A.EMP_DEPT = B.RESKEY "
                "   LEFT OUTER JOIN osrefcp C "
                "   ON C.RECODE = 'JJO' "
                "   AND A.EMP_JO = C.RESKEY "
                "   LEFT OUTER JOIN osrefcp D "
                "   ON D.RECODE = 'POP' "
                "   AND A.EMP_PRC = D.RESKEY "
                "   LEFT OUTER JOIN osrefcp E "
                "   ON E.RECODE = 'POP' "
                "   AND A.EMP_PRC1 = E.RESKEY "
                "   LEFT OUTER JOIN osrefcp F "
                "   ON F.RECODE = 'POP' "
                "   AND A.EMP_PRC2 = F.RESKEY "
                "   LEFT OUTER JOIN osrefcp G "
                "   ON G.RECODE = 'POP' "
                "   AND A.EMP_PRC3 = G.RESKEY "
                "   LEFT OUTER JOIN osrefcp H "
                "   ON H.RECODE = 'COM' "
                "   AND A.EMP_COM = H.RESKEY "
                "   WHERE A.EMP_NBR LIKE '%" + empCode + "%' "
                "   OR A.EMP_NME LIKE '%" + empCode + "%' "
                "   AND A.EMP_GBN LIKE '%" + empType + "%' "
            )
            empresult = cursor.fetchall()

        # 근무조 - 콤보박스
        with connection.cursor() as cursor:
            cursor.execute(" SELECT RESKEY, RESNAM FROM OSREFCP WHERE RECODE = 'JJO' ")
            jjoCombo = cursor.fetchall()

        # 부서 - 콤보박스
        with connection.cursor() as cursor:
            cursor.execute(" SELECT RESKEY, RESNAM FROM OSREFCP WHERE RECODE = 'DPT' ")
            dptCombo = cursor.fetchall()

        # 공정 - 콤보박스
        with connection.cursor() as cursor:
            cursor.execute(" SELECT RESKEY, RESNAM FROM OSREFCP WHERE RECODE = 'POP' ")
            bomCombo = cursor.fetchall()

        # 사업장 - 콤보박스
        with connection.cursor() as cursor:
            cursor.execute(" SELECT RESKEY, RESNAM FROM OSREFCP WHERE RECODE = 'COM' ")
            comCombo = cursor.fetchall()

        return JsonResponse({"jjoCombo": jjoCombo, "dptCombo": dptCombo, "bomCombo": bomCombo, "comCombo": comCombo
                                , "empList": empresult})

    else:
        with connection.cursor() as cursor:
            cursor.execute(
                            "SELECT "
                            "       A.EMP_NBR "
                            "     , IFNULL(A.EMP_GBN, '') "
                            "     , IFNULL(A.EMP_NME, '') "
                            "     , IFNULL(A.EMP_PASS, '') "
                            "     , IFNULL(A.EMP_IPSA, '') "
                            "     , IFNULL(A.EMP_TESA, '') "
                            "     , IFNULL(A.EMP_JO, '') "
                            "     , IFNULL(C.RESNAM, '') "
                            "     , IFNULL(A.EMP_DEPT, '') "
                            "     , IFNULL(B.RESNAM, '') "
                            "     , IFNULL(A.EMP_TEL, '') "
                            "     , IFNULL(A.EMP_PRC, '') "
                            "     , IFNULL(D.RESNAM, '') "
                            "     , IFNULL(A.EMP_PRC1, '') "
                            "     , IFNULL(E.RESNAM, '') "
                            "     , IFNULL(A.EMP_PRC2, '') "
                            "     , IFNULL(F.RESNAM, '') "
                            "     , IFNULL(A.EMP_PRC3, '') "
                            "     , IFNULL(G.RESNAM, '') "
                            "     , IFNULL(A.EMP_COM, '') "
                            "     , IFNULL(H.RESNAM, '')"
                            "   FROM pis1tb001 A "
                            "   LEFT OUTER JOIN osrefcp B "
                            "   ON B.RECODE = 'DPT' "
                            "   AND A.EMP_DEPT = B.RESKEY "
                            "   LEFT OUTER JOIN osrefcp C "
                            "   ON C.RECODE = 'JJO' "
                            "   AND A.EMP_JO = C.RESKEY "
                            "   LEFT OUTER JOIN osrefcp D "
                            "   ON D.RECODE = 'POP' "
                            "   AND A.EMP_PRC = D.RESKEY "
                            "   LEFT OUTER JOIN osrefcp E "
                            "   ON E.RECODE = 'POP' "
                            "   AND A.EMP_PRC1 = E.RESKEY "
                            "   LEFT OUTER JOIN osrefcp F "
                            "   ON F.RECODE = 'POP' "
                            "   AND A.EMP_PRC2 = F.RESKEY "
                            "   LEFT OUTER JOIN osrefcp G "
                            "   ON G.RECODE = 'POP' "
                            "   AND A.EMP_PRC3 = G.RESKEY "
                            "   LEFT OUTER JOIN osrefcp H "
                            "   ON H.RECODE = 'COM' "
                            "   AND A.EMP_COM = H.RESKEY "
                            "   WHERE A.EMP_GBN LIKE '%" + empType + "%' "
                           )
            empresult = cursor.fetchall()

        # 근무조 - 콤보박스
        with connection.cursor() as cursor:
            cursor.execute(" SELECT RESKEY, RESNAM FROM OSREFCP WHERE RECODE = 'JJO' ")
            jjoCombo = cursor.fetchall()

        # 부서 - 콤보박스
        with connection.cursor() as cursor:
            cursor.execute(" SELECT RESKEY, RESNAM FROM OSREFCP WHERE RECODE = 'DPT' ")
            dptCombo = cursor.fetchall()

        # 공정 - 콤보박스
        with connection.cursor() as cursor:
            cursor.execute(" SELECT RESKEY, RESNAM FROM OSREFCP WHERE RECODE = 'POP' ")
            bomCombo = cursor.fetchall()

        # 사업장 - 콤보박스
        with connection.cursor() as cursor:
            cursor.execute(" SELECT RESKEY, RESNAM FROM OSREFCP WHERE RECODE = 'COM' ")
            comCombo = cursor.fetchall()

        return JsonResponse({"jjoCombo": jjoCombo, "dptCombo": dptCombo, "bomCombo": bomCombo, "comCombo": comCombo
                                , "empList": empresult})


def empViews_save(request):
    if 'btnSave' in request.POST:
        empNbr = request.POST.get('txtEmpNo')
        empNme = request.POST.get('txtEmpName')
        empPass = request.POST.get('txtEmpPw')
        empDept = request.POST.get('cboDpt')
        empGbn = '1'
        empJo = request.POST.get('cboGroup')
        empCom = request.POST.get('cboCom')
        empTel = request.POST.get('txtEmpTel')
        empIpsa = request.POST.get('txtEmployDate').replace('-', '')
        empTesa = request.POST.get('txtQuitDate').replace('-', '')
        inepno = '101'
        utepno = '101'
        # inepno = request.session['userid']
        # utepno = request.session['userid']

        if inepno is None or inepno == '':
            with connection.cursor() as cursor:
                cursor.execute("INSERT INTO PIS1TB001 "
                               "   ("
                               "     EMP_NBR "
                               ",    EMP_NME "
                               ",    EMP_PASS "
                               ",    EMP_DEPT "
                               ",    EMP_GBN "
                               ",    EMP_JO "
                               ",    EMP_COM "
                               ",    EMP_TEL "
                               ",    EMP_IPSA "
                               ",    EMP_TESA "
                               ",    CRE_DT "
                               ",    CRE_USER "
                               ") "
                               "    VALUES "
                               "    ("
                               "    '" + empNbr + "'"
                               ",   '" + str(empNme) + "'"
                               ",   '" + str(empPass) + "'"
                               ",   '" + str(empDept) + "'"
                               ",   '" + str(empGbn) + "'"
                               ",   '" + str(empJo) + "'"
                               ",   '" + str(empCom) + "'"
                               ",   '" + str(empTel) + "'"
                               ",   '" + str(empIpsa) + "'"
                               ",   '" + str(empTesa) + "'"
                               ",   date_format(now(), '%Y%m%d')"
                               ",   '" + str(inepno) + "'"
                               "    ) "
                               )

                connection.commit()

            return JsonResponse({'sucYn': "Y"})

        elif inepno:
            with connection.cursor() as cursor:
                cursor.execute("    UPDATE PIS1TB001 SET"
                               "     EMP_NME  = '" + str(empNme) + "' "
                               ",    EMP_PASS = '" + str(empPass) + "' "
                               ",    EMP_DEPT = '" + str(empDept) + "' "
                               ",    EMP_GBN  = '" + str(empGbn) + "' "
                               ",    EMP_JO  = '" + str(empJo) + "' "
                               ",    EMP_COM  = '" + str(empCom) + "' "
                               ",    EMP_TEL  = '" + str(empTel) + "' "
                               ",    EMP_IPSA = '" + str(empIpsa) + "' "
                               ",    EMP_TESA = '" + str(empTesa) + "'  "
                               ",    UPD_DT = date_format(now(), '%Y%m%d') "
                               ",    UPD_USER = '" + str(utepno) + "' "
                               "    WHERE EMP_NBR = '" + str(empNbr) + "' "
                               )
                connection.commit()

                return JsonResponse({'sucYn': "Y"})

        return render(request, 'base/base-emp.html')


def empViews_dlt(request):
    if request.method == "POST":
        dataList = json.loads(request.POST.get('arrList'))
        print(dataList)
        for emp in dataList:
            acc_split_list = emp.split(',')
            with connection.cursor() as cursor:
                cursor.execute(" DELETE FROM PIS1TB001 WHERE EMP_NBR = '" + acc_split_list[0] + "' ")
                connection.commit()

        return JsonResponse({'sucYn': "Y"})

    else:
        return render(request, 'base/base-emp.html')