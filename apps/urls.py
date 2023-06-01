from django.urls import path,re_path
from apps.views.account.mainViews import *
from apps.views.base import baseCodeViews, empViews, custViews, accountViews, accountCodeViews, targetIndexViews
from apps.views.finance import purchaseViews, depositViews, custBalanceViews, actBalanceViews, cashBalanceViews
from apps.views.currentstate import receivepayViews

urlpatterns = [
    path('', redirectToMain, name="redirectToMain"),
    path('main/', index, name='home'),

#     기초정보
    # 계정코드관리
    path('base_accountCode/', accountCodeViews.accountCodeViews, name='base_accountCode'),
    # 참조코드관리
    path('base_code/', baseCodeViews.baseCodeViews, name='base_code'),
    path('base_code_search/', baseCodeViews.baseCodeViews_search, name='base_code_search'),
    path('base_code_save/', baseCodeViews.baseCodeViews_save, name='base_code_save'),
    path('base_code_dlt/', baseCodeViews.baseCodeViews_dlt, name='base_code_dlt'),
    # 직원정보관리
    path('base_emp/', empViews.empViews, name='base_emp'),
    path('base_emp_search/', empViews.empViews_search, name='base_emp_search'),
    path('base_emp_save/', empViews.empViews_save, name='base_emp_save'),
    path('base_emp_dlt/', empViews.empViews_dlt, name='base_emp_dlt'),
    # 거래처정보관리
    path('base_cust/', custViews.custViews, name='base_cust'),
    path('base_cust_search/', custViews.custViews_search, name='base_cust_search'),
    path('base_cust_save/', custViews.custViews_save, name='base_cust_save'),
    path('base_cust_dlt/', custViews.custViews_dlt, name='base_cust_dlt'),
    # 게좌관리
    path('base_account/', accountViews.accountViews, name='base_account'),
    path('base_account_search/', accountViews.accountViews_search, name='base_account_search'),
    path('base_account_save/', accountViews.accountViews_save, name='base_account_save'),
    path('base_account_dlt/', accountViews.accountViews_dlt, name='base_account_dlt'),
    # 지수관리
    path('base_targetIndex/', targetIndexViews.targetIndexViews, name='base_targetIndex'),
    path('base_target_search/', targetIndexViews.targetIndexSearchViews, name='base_target_search'),
    path('base_target_save/', targetIndexViews.targetIndexSaveViews, name='base_target_save'),
    # 계좌잔액등록
    path('actBalance_reg/', actBalanceViews.actBalRegViews, name='actBalance_reg'),
    path('actBalance_reg_search/', actBalanceViews.actBalRegViews_search, name='actBalance_reg_search'),
    path('actBalance_reg_save/', actBalanceViews.actBalRegViews_save, name='actBalance_reg_save'),
    path('actBalance_reg_dlt/', actBalanceViews.actBalRegViews_dlt, name='actBalance_reg_dlt'),
    # 거래처시산잔액등록
    path('custBalance_reg/', custBalanceViews.custBalRegViews, name='custBalance_reg'),
    path('custBalance_reg_search/', custBalanceViews.custBalRegViews_search, name='custBalance_reg_search'),
    path('custBalance_reg_save/', custBalanceViews.custBalRegViews_save, name='custBalance_reg_save'),
    path('custBalance_reg_dlt/', custBalanceViews.custBalRegViews_dlt, name='custBalance_reg_dlt'),
    # 현금시재등록
    path('cashBalance_reg/', cashBalanceViews.cashBalRegViews, name='cashBalance_reg'),
    path('cashBalance_bank/', cashBalanceViews.cashBalRegBankViews, name='cashBalance_bank'),
    path('cashBalance_search', cashBalanceViews.cashBalRegSearchViews, name='cashBalacne_search'),
    path('cashBalance_search_scnd', cashBalanceViews.cashBalRegSearchScndViews, name='cashBalance_search_scnd'),
    path('cashBalance_acnum_search', cashBalanceViews.cashBalRegCboSearchViews, name='cashBalance_acnum_search'),
    path('cashBalance_acname_search', cashBalanceViews.cashBalRegAcNmSearchViews, name='cashBalance_acname_search'),
    path('cashBalacne_save', cashBalanceViews.cashBalRegSaveViews, name='cashBalacne_save'),

#     매입/매출 관리
    path('purchase_reg/', purchaseViews.purchaseRegViews, name='purchase_reg'),
    path('purchase_reg_search/', purchaseViews.purchaseRegViews, name='purchase_reg_search'),


#     입금/출금 관리
    path('deposit_reg/', depositViews.depositRegViews, name='deposit_reg'),

#     자금관리 현황
    path('receive_pay/', receivepayViews.receivepaySheetViews, name='receive_pay'),

]