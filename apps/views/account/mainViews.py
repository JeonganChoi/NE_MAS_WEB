from django.shortcuts import render, redirect
from django import template
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse, HttpResponse, HttpResponseRedirect
from django.template import loader
from django.db import connection
from django.urls import reverse


def loginView(request):
    if request.method == 'GET':
        return render(request, "account/login.html")

    elif request.method == 'POST':
        userId = request.POST.get('userId')
        userPw = request.POST.get('userPw')
        msg = None

        with connection.cursor() as cursor:
            cursor.execute("SELECT IFNULL(EMP_NBR, ''), IFNULL(EMP_NME, ''), IFNULL(EMP_DEPT, ''), IFNULL(EMP_GBN, '') "
                           "        , IFNULL(ICUST, ''), IFNULL(EMP_CHARGE, ''), IFNULL(EMP_TESA, ''), IFNULL(EMP_CLS, '') "
                           "    FROM pis1tb001 "
                           "    WHERE EMP_NBR = '" + str(userId) + "' AND EMP_PASS = '" + str(userPw) + "' ")
            result = cursor.fetchall()

            if len(result) == 0:
                # if len(result) == 0:
                msg = '아이디 또는 비밀번호가 일치 하지 않습니다.'
                # return render(request, "account/login.html", {'login': "N", "msg": msg})
                return JsonResponse({'login': "N", "msg": msg})
            else:
                if result[0][6] != '':
                    tesa = result[0][6]
                    msg = '사용 불가능한 아이디입니다.'
                    # return render(request, "account/login.html", {'login': "N", "msg": msg})
                    return JsonResponse({'login': "N", "msg": msg})
                else:
                    USER_NM = result[0][1]
                    USER_GBN = result[0][7]
                    USER_ICUST = result[0][4]
                    if result[0][5] != '':
                        USER_CHARGE = result[0][5]
                    else:
                        USER_CHARGE = '0'
                    request.session['userId'] = userId
                    request.session['USER_NM'] = USER_NM
                    request.session['USER_GBN'] = USER_GBN
                    request.session['USER_ICUST'] = USER_ICUST
                    request.session['USER_CHARGE'] = USER_CHARGE

                    with connection.cursor() as cursor:
                        cursor.execute("INSERT INTO LOG_RECODE "
                                       "(LOG_SEQ"
                                       ", USER_ID"
                                       ", USER_NM"
                                       ", LOGIN_DT"
                                       ", ICUST"
                                       ") "
                                       "VALUES"
                                       "("
                                       "(SELECT IFNULL(MAX(LOG_SEQ) + 1, 1) AS LOG_SEQ FROM LOG_RECODE A) "
                                       ", '" + userId + "'"
                                       ", '" + USER_NM + "'"
                                       ", NOW() "
                                       ", '" + USER_ICUST + "'"
                                       ")"
                                       )
                        connection.commit()

                # return render(request, "home/index.html")
                return JsonResponse({'login': "Y"})

            # return render(request, "home/index.html", {})




def logoutViews(request):

    if request.method == "POST":

        request.session.clear()

        return JsonResponse({'logout': "Y"})



def signupView(request):

    return render(request, "account/signup.html")

def index(request):
    userId = request.session.get('userId')
    if userId == '' or userId is None:
        return redirect("/page-404/")
    else:
        return render(request, "home/index.html")


def page404(request):

    return render(request, "account/page-404.html")

def redirectToMain(request):

    return redirect("home")

# def redirectToLogin(request):
#
#     return redirect("login")
#
# def login(request):
#
#     return render(request, "account/login.html")