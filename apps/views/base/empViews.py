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
from django.core.files.storage import FileSystemStorage


def empViews(request):

    return render(request, "base/base-emp.html")

def empViews_search(request):
    empCode = request.POST.get('empCode')
    empType = request.POST.get('empType')
    iCust = request.session.get('USER_ICUST')

    if empType == '0':
        with connection.cursor() as cursor:
            cursor.execute(" SELECT "
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
                            "     , IFNULL(A.EMP_COM, '') "
                            "     , IFNULL(H.RESNAM, '') "
                            "     , IFNULL(A.ICUST, '')"
                            "   FROM pis1tb001 A "
                            "   LEFT OUTER JOIN osrefcp B "
                            "   ON B.RECODE = 'DPT' "
                            "   AND A.EMP_DEPT = B.RESKEY "
                            "   LEFT OUTER JOIN osrefcp C "
                            "   ON C.RECODE = 'JJO' "
                            "   AND A.EMP_JO = C.RESKEY "
                            "   LEFT OUTER JOIN osrefcp H "
                            "   ON H.RECODE = 'COM' "
                            "   AND A.EMP_COM = H.RESKEY "
                            "   WHERE A.ICUST = '" + str(iCust) + "' "
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
                "     , IFNULL(A.EMP_COM, '') "
                "     , IFNULL(H.RESNAM, '') "
                "     , IFNULL(A.ICUST, '') "
                "     , IFNULL(A.EMP_FOLDER, '') "
                "   FROM pis1tb001 A "
                "   LEFT OUTER JOIN osrefcp B "
                "   ON B.RECODE = 'DPT' "
                "   AND A.EMP_DEPT = B.RESKEY "
                "   LEFT OUTER JOIN osrefcp C "
                "   ON C.RECODE = 'JJO' "
                "   AND A.EMP_JO = C.RESKEY "
                "   LEFT OUTER JOIN osrefcp H "
                "   ON H.RECODE = 'COM' "
                "   AND A.EMP_COM = H.RESKEY "
                "   WHERE A.EMP_NBR LIKE '%" + empCode + "%' "
                "   OR A.EMP_NME LIKE '%" + empCode + "%' "
                "   AND A.EMP_GBN LIKE '%" + empType + "%' "
                "   AND A.ICUST = '" + str(iCust) + "' "
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
        # with connection.cursor() as cursor:
        #     cursor.execute(" SELECT RESKEY, RESNAM FROM OSREFCP WHERE RECODE = 'POP' ")
        #     bomCombo = cursor.fetchall()

        # 사업장 - 콤보박스
        with connection.cursor() as cursor:
            cursor.execute(" SELECT RESKEY, RESNAM FROM OSREFCP WHERE RECODE = 'COM' ")
            comCombo = cursor.fetchall()

        return JsonResponse({"jjoCombo": jjoCombo, "dptCombo": dptCombo, "comCombo": comCombo, "empList": empresult})

    else:
        with connection.cursor() as cursor:
            cursor.execute(" SELECT "
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
                           "     , IFNULL(A.EMP_COM, '') "
                           "     , IFNULL(H.RESNAM, '')"
                           "     , IFNULL(A.ICUST, '')"
                           "   FROM pis1tb001 A "
                           "   LEFT OUTER JOIN osrefcp B "
                           "   ON B.RECODE = 'DPT' "
                           "   AND A.EMP_DEPT = B.RESKEY "
                           "   LEFT OUTER JOIN osrefcp C "
                           "   ON C.RECODE = 'JJO' "
                           "   AND A.EMP_JO = C.RESKEY "
                           "   LEFT OUTER JOIN osrefcp H "
                           "   ON H.RECODE = 'COM' "
                           "   AND A.EMP_COM = H.RESKEY "
                           "   WHERE A.EMP_TESA IS NULL or A.EMP_TESA = '' AND A.ICUST = '" + str(iCust) + "'"
                           )
            empresult = cursor.fetchall()

        # 근무조 - 콤보박스
        with connection.cursor() as cursor:
            cursor.execute(" SELECT RESKEY, RESNAM FROM OSREFCP WHERE RECODE = 'JJO' ORDER BY RESKEY ASC ")
            jjoCombo = cursor.fetchall()

        # 부서 - 콤보박스
        with connection.cursor() as cursor:
            cursor.execute(" SELECT RESKEY, RESNAM FROM OSREFCP WHERE RECODE = 'DPT' ")
            dptCombo = cursor.fetchall()

        # 공정 - 콤보박스
        # with connection.cursor() as cursor:
        #     cursor.execute(" SELECT RESKEY, RESNAM FROM OSREFCP WHERE RECODE = 'POP' ")
        #     bomCombo = cursor.fetchall()

        # 사업장 - 콤보박스
        with connection.cursor() as cursor:
            cursor.execute(" SELECT RESKEY, RESNAM FROM OSREFCP WHERE RECODE = 'COM' ")
            comCombo = cursor.fetchall()

        return JsonResponse({"jjoCombo": jjoCombo, "dptCombo": dptCombo, "comCombo": comCombo, "empList": empresult})


def empViews_save(request):
    empNbr = request.POST.get('txtEmpNo')
    empNme = request.POST.get('txtEmpName')
    empPass = request.POST.get('txtEmpPw')
    empDept = request.POST.get('cboDpt')
    empGbn = request.POST.get('cboGroup')
    empCom = request.POST.get('cboCom')
    empTel = request.POST.get('txtEmpTel')
    limit = request.POST.get('limit')
    empIpsa = request.POST.get('txtEmployDate').replace('-', '')
    empTesa = request.POST.get('txtQuitDate').replace('-', '')
    usage = request.POST.get('usage')

    charge = request.POST.get('chkPermit')
    user = request.session.get('userId')
    iCust = request.session.get('USER_ICUST')


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
        cursor.execute("SELECT EMP_NBR FROM PIS1TB001 WHERE EMP_NBR = '" + str(empNbr) + "' AND ICUST = '" + str(iCust) + "' ")
        result = cursor.fetchall()

    if result:
        with connection.cursor() as cursor:
            cursor.execute("    UPDATE PIS1TB001 SET"
                           "     EMP_NME  = '" + str(empNme) + "' "
                           ",    EMP_PASS = '" + str(empPass) + "' "
                           ",    EMP_DEPT = '" + str(empDept) + "' "
                           ",    EMP_GBN  = '" + str(empGbn) + "' "
                           ",    EMP_COM  = '" + str(empCom) + "' "
                           ",    EMP_TEL  = '" + str(empTel) + "' "
                           ",    EMP_IPSA = '" + str(empIpsa) + "' "
                           ",    EMP_TESA = '" + str(empTesa) + "'  "
                           ",    EMP_USE = '" + str(usage) + "'  "
                           ",    EMP_CHARGE = '" + str(charge) + "'  "
                           ",    EMP_FOLDER = '" + str(Rfilenameloc) + "'  "
                           ",    UPD_DT = date_format(now(), '%Y%m%d') "
                           ",    UPD_USER = '" + str(user) + "' "
                           "    WHERE EMP_NBR = '" + str(empNbr) + "' "
                           "      AND ICUST = '" + str(iCust) + "' "
                           )
            connection.commit()

            return JsonResponse({'sucYn': "Y"})

    else:
        with connection.cursor() as cursor:
            cursor.execute("INSERT INTO PIS1TB001 "
                           "   ("
                           "     EMP_NBR "
                           ",    EMP_NME "
                           ",    EMP_PASS "
                           ",    EMP_DEPT "
                           ",    EMP_GBN "
                           ",    EMP_COM "
                           ",    EMP_TEL "
                           ",    EMP_IPSA "
                           ",    EMP_TESA "
                           ",    EMP_USE "
                           ",    EMP_CHARGE "
                           ",    EMP_FOLDER "
                           ",    CRE_DT "
                           ",    CRE_USER "
                           ",    ICUST "
                           ") "
                           "    VALUES "
                           "    ("
                           "    '" + empNbr + "' "
                           ",   '" + str(empNme) + "' "
                           ",   '" + str(empPass) + "' "
                           ",   '" + str(empDept) + "' "
                           ",   '" + str(empGbn) + "' "
                           ",   '" + str(empCom) + "' "
                           ",   '" + str(empTel) + "' "
                           ",   '" + str(empIpsa) + "' "
                           ",   '" + str(empTesa) + "' "
                           ",   '" + str(usage) + "' "
                           ",   '" + str(charge) + "' "
                           ",   '" + str(Rfilenameloc) + "' "
                           ",   date_format(now(), '%Y%m%d') "
                           ",   '" + str(user) + "' "
                           ",   '" + str(iCust) + "' "
                           "    ) "
                           )

            connection.commit()

        return JsonResponse({'sucYn': "Y"})

    return render(request, 'base/base-emp.html')


def empViews_dlt(request):
    iCust = request.session.get('USER_ICUST')

    if request.method == "POST":
        dataList = json.loads(request.POST.get('arrList'))
        print(dataList)
        for emp in dataList:
            acc_split_list = emp.split(',')
            with connection.cursor() as cursor:
                cursor.execute(" DELETE FROM PIS1TB001 WHERE EMP_NBR = '" + acc_split_list[0] + "' AND ICUST = '" + str(iCust) + "' ")
                connection.commit()

        return JsonResponse({'sucYn': "Y"})

    else:
        return render(request, 'base/base-emp.html')