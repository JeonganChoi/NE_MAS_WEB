import json
import os
from django.shortcuts import render, redirect
from django import template
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse, HttpResponseRedirect, FileResponse
from django.template import loader
from django.urls import reverse
from django.contrib import messages
from django.http import JsonResponse
from django.db import connection
from django.core.files.storage import FileSystemStorage
from urllib.parse import quote


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
                            "     , IFNULL(A.EMP_CLS, '')"
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

    if empType == '2':
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
                           "     , IFNULL(A.EMP_CLS, '')"
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
                           "   WHERE A.EMP_TESA != '' AND A.ICUST = '" + str(iCust) + "'"
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
                "     , IFNULL(A.EMP_CLS, '')"
                "     , IFNULL(A.EMP_FOLDER, '') "
                "     , IFNULL(A.EMP_LIMIT, '') "
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
            cursor.execute(" SELECT RESKEY, RESNAM FROM OSREFCP WHERE RECODE = 'JJO' AND ICUST = '" + str(iCust) + "' ")
            jjoCombo = cursor.fetchall()

        # 부서 - 콤보박스
        with connection.cursor() as cursor:
            cursor.execute(" SELECT RESKEY, RESNAM FROM OSREFCP WHERE RECODE = 'DPT' AND ICUST = '" + str(iCust) + "' ")
            dptCombo = cursor.fetchall()

        # 공정 - 콤보박스
        # with connection.cursor() as cursor:
        #     cursor.execute(" SELECT RESKEY, RESNAM FROM OSREFCP WHERE RECODE = 'POP' ")
        #     bomCombo = cursor.fetchall()

        # 사업장 - 콤보박스
        with connection.cursor() as cursor:
            cursor.execute(" SELECT RESKEY, RESNAM FROM OSREFCP WHERE RECODE = 'COM' AND ICUST = '" + str(iCust) + "' ")
            comCombo = cursor.fetchall()

        # 등급 - 콤보박스
        with connection.cursor() as cursor:
            cursor.execute(" SELECT RESKEY, RESNAM FROM OSREFCP WHERE RECODE = 'EOC' AND ICUST = '" + str(iCust) + "' ")
            comClass = cursor.fetchall()

        return JsonResponse({"jjoCombo": jjoCombo, "dptCombo": dptCombo, "comCombo": comCombo, "comClass": comClass
                                , "empList": empresult})

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
                           "     , IFNULL(A.EMP_CLS, '')"
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
            cursor.execute(" SELECT RESKEY, RESNAM FROM OSREFCP WHERE RECODE = 'JJO' AND ICUST = '" + str(iCust) + "' ORDER BY RESKEY ASC ")
            jjoCombo = cursor.fetchall()

        # 부서 - 콤보박스
        with connection.cursor() as cursor:
            cursor.execute(" SELECT RESKEY, RESNAM FROM OSREFCP WHERE RECODE = 'DPT' AND ICUST = '" + str(iCust) + "' ")
            dptCombo = cursor.fetchall()

        # 공정 - 콤보박스
        # with connection.cursor() as cursor:
        #     cursor.execute(" SELECT RESKEY, RESNAM FROM OSREFCP WHERE RECODE = 'POP' ")
        #     bomCombo = cursor.fetchall()

        # 사업장 - 콤보박스
        with connection.cursor() as cursor:
            cursor.execute(" SELECT RESKEY, RESNAM FROM OSREFCP WHERE RECODE = 'COM' AND ICUST = '" + str(iCust) + "' ")
            comCombo = cursor.fetchall()

        # 등급 - 콤보박스
        with connection.cursor() as cursor:
            cursor.execute(" SELECT RESKEY, RESNAM FROM OSREFCP WHERE RECODE = 'EOC' AND ICUST = '" + str(iCust) + "' ")
            comClass = cursor.fetchall()

        return JsonResponse({"jjoCombo": jjoCombo, "dptCombo": dptCombo, "comCombo": comCombo, "comClass": comClass, "empList": empresult})


def empViews_save(request):
    empNbr = request.POST.get('txtEmpNo')
    empNme = request.POST.get('txtEmpName')
    empPass = request.POST.get('txtEmpPw')
    empDept = request.POST.get('cboDpt')
    empGbn = request.POST.get('cboGroup')
    empCom = request.POST.get('cboCom')
    empTel = request.POST.get('txtEmpTel')
    limit = request.POST.get('txtLimit').replace(',', '')
    empIpsa = request.POST.get('txtEmployDate').replace('-', '')
    empTesa = request.POST.get('txtQuitDate').replace('-', '')
    # usage = request.POST.get('usage')
    empClass = request.POST.get('cboClass')

    charge = request.POST.get('chkPermit')
    user = request.session.get('userId')
    iCust = request.session.get('USER_ICUST')

    fileOverwriteYn = request.POST.get("fileOverwriteYn")

    uploaded_file = request.FILES.get('file')
    if uploaded_file is None:
        uploaded_file = ''

    if uploaded_file:
        # 원하는 경로 설정, FileResponse
        # desired_path = "D:/NE_FTP/MAS_FILES/중요문건"
        # desired_path = "D:\\NE_FTP\\MAS_FILES\\"
        # desired_path = "D:\\NE_FTP\\MAS_FILES\\UploadFiles\\"
        # desired_path = "D:/NE_FTP/MAS_FILES/UploadFiles/"
        desired_path = "/Users/thenaeunsys/Documents/ImportFile/"

        # 해당 디렉토리가 없으면 생성
        if not os.path.exists(desired_path):
            os.makedirs(desired_path)

        destination = os.path.join(desired_path, uploaded_file.name)

        # 해당 경로에 동일한 이름의 파일이 있다면
        if os.path.exists(destination):
            if fileOverwriteYn == 'Y':
                os.remove(destination)
            else:
                return JsonResponse({'sucYn': 'N', 'message': "same file name exists"})

        with open(destination, 'wb+') as destination_file:
            for chunk in uploaded_file.chunks():
                destination_file.write(chunk)

        uploaded_file = destination

    with connection.cursor() as cursor:
        cursor.execute("SELECT EMP_NBR FROM PIS1TB001 WHERE EMP_NBR = '" + str(empNbr) + "' AND ICUST = '" + str(iCust) + "' ")
        result = cursor.fetchall()

    if result:
        emp = result[0][0]
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
                           ",    EMP_CLS = '" + str(empClass) + "'  "
                           ",    EMP_LIMIT = '" + str(limit) + "'  "
                           ",    EMP_CHARGE = '" + str(charge) + "'  "
                           ",    EMP_FOLDER = '" + str(uploaded_file) + "'  "
                           ",    UPD_DT = date_format(now(), '%Y%m%d') "
                           ",    UPD_USER = '" + str(user) + "' "
                           "    WHERE EMP_NBR = '" + str(emp) + "' "
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
                           ",    EMP_LIMIT "
                           ",    EMP_CLS "
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
                           ",   '" + str(limit) + "' "
                           ",   '" + str(empClass) + "' "
                           ",   '" + str(charge) + "' "
                           ",   '" + str(uploaded_file) + "' "
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



# 파일 불러오기
def download_file_emp(request):
    empCode = request.GET.get('empCode')
    empClass = request.GET.get('empClass')
    iCust = request.session.get("USER_ICUST")

    with connection.cursor() as cursor:
        cursor.execute(
                    "    SELECT EMP_FOLDER"
                    "     FROM PIS1TB001 "
                    "     WHERE EMP_NBR = '" + str(empCode) + "' "
                    "     AND EMP_CLS = '" + str(empClass) + "' "
                    "     AND ICUST = '" + str(iCust) + "' "
                       )
        result = cursor.fetchall()

    #     file_path = result[0][0]
    #
    # if file_path:
    if result:
        file_path = result[0][0]
        # 한글 파일명 처리를 위한 인코딩
        filename = quote(os.path.basename(file_path).encode('utf-8'))

        response = FileResponse(open(file_path, 'rb'))
        response['Content-Disposition'] = 'attachment; filename*=UTF-8\'\'%s' % filename
        return response
    else:
        return render(request, "finance/back.html")