from django.urls import path,re_path
from apps.views.account.mainViews import *
from apps.views.base import baseCodeViews, empViews, custViews, accountViews, accountCodeViews, targetIndexViews

urlpatterns = [
    path('', redirectToMain, name="redirectToMain"),
    path('main/', index, name='home'),

#     기초정보
    # 계정코드관리
    path('base_accountCode/', accountCodeViews.accountCodeViews, name='base_accountCode'),
    # 참조코드관리
    path('base_code/', baseCodeViews.baseCodeViews, name='base_code'),
    # 직원정보관리
    path('base_emp/', empViews.empViews, name='base_emp'),
    path('base_emp_search/', empViews.empViews_search, name='base_emp_search'),
    path('base_emp_save/', empViews.empViews_save, name='base_emp_save'),
    path('base_emp_dlt/', empViews.empViews_dlt, name='base_emp_dlt'),
    # 거래처정보관리
    path('base_cust/', custViews.custViews, name='base_cust'),
    # 게좌관리
    path('base_account/', accountViews.accountViews, name='base_account'),
    path('base_account_search/', accountViews.accountViews_search, name='base_account_search'),
    path('base_account_save/', accountViews.accountViews_save, name='base_account_save'),
    path('base_account_dlt/', accountViews.accountViews_dlt, name='base_account_dlt'),
    # 지수관리
    path('base_targetIndex/', targetIndexViews.targetIndexViews, name='base_targetIndex'),
]