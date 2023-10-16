from django.urls import path,re_path
from apps.views.account import mainViews
from apps.views.base import baseCodeViews, empViews, custViews, accountViews, accountCodeViews, targetIndexViews, baseChargeViews, cardViews
from apps.views.finance import purchaseViews, salesViews, depositViews, withdrawalViews, custBalanceViews, actBalanceViews\
    , cashBalanceViews, financeSearchViews, depreciationViews, payrollViews, paymentViews, approvalViews, permitViews
from apps.views.currentstate import receivepayViews, yearlyMonthlyAnalysisViews, yearlyMonthlyAccountAnalysisViews\
    , monthlyCircleFundsViews, monthlyCountViews, monthlyProfitLossViews, breakdownBalanceViews, receiptPaymentViews

urlpatterns = [
    # path('', redirectToMain, name="redirectToMain"),
    # path('main/', index, name='home'),
    # path('', redirectToLogin, name="redirectToLogin"),
    # path('login/', login, name='login'),

    # 로그인/로그아웃 관리
    path('', mainViews.loginView, name="login"),
    path('logout/', mainViews.logoutViews, name="logout"),
    path('main/', mainViews.index, name="index"),
    path('signup/', mainViews.signupView, name="signup"),
    path('page-404/', mainViews.page404, name="page-404"),


#     기초정보
    # 계정코드관리
    path('base_accountCode/', accountCodeViews.accountCodeViews, name='base_accountCode'),
    path('base_accountCode_search/', accountCodeViews.accountCodeViews_search, name='base_accountCode_search'),
    path('base_chk_code/', accountCodeViews.chkCodeViews_search, name='base_chk_code'),
    path('base_accountCode_saveM/', accountCodeViews.accountCodeViews_saveM, name='base_accountCode_saveM'),
    path('base_accountCode_dltM/', accountCodeViews.accountCodeViews_dltM, name='base_accountCode_dltM'),
    # 계정코드관리
    path('base_charge/', baseChargeViews.baseChargeViews, name='base_charge'),
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
    # 카드관리
    path('base_card/', cardViews.cardViews, name='base_card'),
    path('base_card_search/', cardViews.cardViews_search, name='base_card_search'),
    path('base_card_save/', cardViews.cardViews_save, name='base_card_save'),
    path('base_card_dlt/', cardViews.cardViews_dlt, name='base_card_dlt'),
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

    #  매입 관리
    path('purchase_reg/', purchaseViews.purchaseRegViews, name='purchase_reg'),
    path('purchase_reg_search/', purchaseViews.purchaseRegViews_search, name='purchase_reg_search'),
    path('purchase_reg_save/', purchaseViews.purchaseRegViews_save, name='purchase_reg_save'),
    path('purchase_reg_dlt/', purchaseViews.purchaseRegViews_dlt, name='purchase_reg_dlt'),
    #  매출관리
    path('sales_reg/', salesViews.salesRegViews, name='sales_reg'),
    path('sales_reg_search/', salesViews.salesRegViews_search, name='sales_reg_search'),
    path('sales_reg_save/', salesViews.salesRegViews_save, name='sales_reg_save'),
    path('sales_reg_dlt/', salesViews.salesRegViews_search, name='sales_reg_dlt'),
    # 매입 내역서
    path('purchases_report/', financeSearchViews.purTransSearchViews, name='purchases_report'),
    path('purchases_report_search/', financeSearchViews.purTransSearchViews_search, name='purchases_report_search'),
    # 매출 내역서
    path('sales_report/', financeSearchViews.saleTransSearchViews, name='sales_report'),
    path('sales_report_search/', financeSearchViews.saleTransSearchViews_search, name='sales_report_search'),

    # 결재등록
    path('approval_reg/', approvalViews.approvalViews, name='approval_reg'),
    path('approval_reg_search/', approvalViews.approvalViews_search, name='approval_reg_search'),
    path('approval_sub_search/', approvalViews.approvalSubViews_search, name='approval_sub_search'),
    path('approval_reg_save/', approvalViews.approvalViews_save, name='approval_reg_save'),

    # 실행등록
    path('permit_reg/', permitViews.permitViews, name='permit_reg'),
    path('permit_reg_search/', permitViews.permitViews_search, name='permit_reg_search'),
    path('permit_reg_save/', permitViews.permitViews_save, name='permit_reg_save'),
    path('permit_cbo_search/', permitViews.cboActNum_search, name='permit_cbo_search'),

    # 입금관리
    path('deposit_reg/', depositViews.depositRegViews, name='deposit_reg'),
    path('deposit_reg_search/', depositViews.depositRegViews_search, name='deposit_reg_search'),
    path('deposit_reg_save/', depositViews.depositRegViews_save, name='deposit_reg_save'),
    path('deposit_reg_dlt/', depositViews.depositRegViews_dlt, name='deposit_reg_dlt'),
    path('deposit_reg_out/', depositViews.depositRegOutList_search, name='deposit_reg_out'),

    # 출금관리
    path('with_reg/', withdrawalViews.withRegViews, name='with_reg'),
    path('with_reg_search/', withdrawalViews.withRegViews_search, name='with_reg_search'),
    path('with_reg_save/', withdrawalViews.withRegViews_save, name='with_reg_save'),
    path('with_reg_dlt/', withdrawalViews.withRegViews_dlt, name='with_reg_dlt'),
    path('with_reg_out/', withdrawalViews.withRegOutList_search, name='with_reg_out'),

    # 출금관리-수불장
    path('with_reg_sheet/', paymentViews.withRegNewViews, name='with_reg_sheet'),
    path('receivePay_search/', paymentViews.receivePay_search, name='receivePay_search'),
    path('payment_search/', paymentViews.paymentViews_search, name='payment_search'),
    path('payment_save/', paymentViews.paymentViews_save, name='payment_save'),
    path('offSet_save/', paymentViews.offSetViews_save, name='offSet_save'),
    path('payment_dlt/', paymentViews.paymentViews_dlt, name='payment_dlt'),
    path('apvLine_modal/', paymentViews.apvLine_modal_search, name='apvLine_modal'),
    path('checkLimit/', paymentViews.checkLimit_search, name='checkLimit'),
    path('cboAct/', paymentViews.cboActNum_search, name='cboAct'),

    # 감가상각비명세서
    path('depreciation_reg/', depreciationViews.depreciationViews, name='depreciation_reg'),
    path('dpt_search/', depreciationViews.dptViews_search, name='dpt_search'),
    path('dpt_save/', depreciationViews.dptViews_save, name='dpt_save'),
    # 임금대장
    path('payroll_reg/', payrollViews.payrollViews, name='payroll_reg'),
    path('payroll_search/', payrollViews.payrollViews_search, name='payroll_search'),
    path('payroll_save/', payrollViews.payrollViews_save, name='payroll_save'),

    # 거래처원장
    path('custLedger_report/', financeSearchViews.custLedgerViews, name='custLedger_report'),
    path('custLedger_report_search/', financeSearchViews.custLedgerViews_search, name='custLedger_report_search'),


    #  자금 분석
    path('yearly_monthly_sales/', yearlyMonthlyAnalysisViews.yearlyMontlySales, name='yearly_monthly_sales'),
    path('ym_sales_search/', yearlyMonthlyAnalysisViews.yearlyMontlySales_search, name='ym_sales_search'),
    path('yearly_monthly_purs/', yearlyMonthlyAnalysisViews.yearlyMontlyPurs, name='yearly_monthly_purs'),
    path('ym_purchases_search/', yearlyMonthlyAnalysisViews.yearlyMontlyPurs_search, name='ym_purchases_search'),
    path('yearly_monthly_account/', yearlyMonthlyAccountAnalysisViews.yearlyMontlyAccount, name='yearly_monthly_account'),
    path('ym_account_cbo/', yearlyMonthlyAccountAnalysisViews.yearlyMontlyAccount_cbo, name='ym_account_cbo'),
    path('ym_account_search/', yearlyMonthlyAccountAnalysisViews.yearlyMontlyAccount_search,
         name='ym_account_search'),

    #  자금 현황
    # 내역별 잔액
    path('receipts_payments/', receiptPaymentViews.receiptPaymentViews, name='receipts_payments'),
    path('receipts_payments_search/', receiptPaymentViews.receiptPaymentViews_search, name='receipts_payments_search'),

    # 은행 내역서
    path('receive_pay/', receivepayViews.receivepaySheetViews, name='receive_pay'),
    path('receive_pay_search/', receivepayViews.receivepaySheetViews_search, name='receive_pay_search'),
    # 계정별 내역서
    path('receive_pay_code/', receivepayViews.receivepayCodeSheetViews, name='receive_pay_code'),
    path('receive_pay_code_search/', receivepayViews.receivepayCodeSheetViews_search, name='receive_pay_code_search'),

    # 월별 자금 유동 현황
    path('monthly_circle_funds/', monthlyCircleFundsViews.montlyCircleFundsViews, name='monthly_circle_funds'),
    path('monthly_circle_funds_search/', monthlyCircleFundsViews.montlyCircleFundsViews_search, name='monthly_circle_funds_search'),

    # 월별 자금 유동 현황
    path('monthly_count/', monthlyCountViews.montlyCountViews, name='monthly_count'),
    path('monthly_count_search/', monthlyCountViews.montlyCountViews_search, name='monthly_count_search'),

    # 손익 계산서
    path('monthly_profit_loss/', monthlyProfitLossViews.montlyProfitLossViews, name='monthly_profit_loss'),
    path('monthly_profit_loss_search/', monthlyProfitLossViews.montlyProfitLossViews_search, name='monthly_profit_loss_search'),

    # 내역별 잔액
    path('breakdown_balance/', breakdownBalanceViews.breakdownBalanceViews, name='breakdown_balance'),
    path('breakdown_balance_search/', breakdownBalanceViews.breakdownBalanceViews_search, name='breakdown_balance_search'),
]