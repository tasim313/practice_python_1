from django.urls import path
from .views import *

urlpatterns = [

    path("customer_payment_info_add/", CustomerBillingInfoAdd.as_view(), name="customer_payment_info_add"),  # Naznin --- User Payment Info url

    path("provider_payment_info_add/", ProviderBillingInfoAdd.as_view(), name="provider_payment_info_add"),  # Naznin --- User Payment Info url

    path("customer_payment_info/<user_id>", CustomerPaymentInfoView.as_view(), name="customer_payment_info"),  # Naznin --- User Payment Info url

    path("provider_payment_info/<user_id>", ProviderPaymentInfoView.as_view(), name="provider_payment_info"),  # Naznin --- User Payment Info url

    path("customer_bank_info/", CustomerBankInfoAdd.as_view(), name="customer_bank_info"),  # Naznin --- User Payment Info url

    path("provider_bank_info/", ProviderBankInfoAdd.as_view(), name="provider_bank_info"),  # Naznin --- User Payment Info url

    path("customer_bank_info/<user_id>", CustomerBankInfoCRUD.as_view(), name="customer_bank_info"),  # Naznin --- User Payment Info url

    path("provider_bank_info/<user_id>", ProviderBankInfoCRUD.as_view(), name="provider_bank_info"),  # Naznin --- User Payment Info url

    path("customer_credit_card_info/", CustomerCreditCardInfoAdd.as_view(), name="customer_credit_card_info"),  # Naznin --- User Payment Info url

    path("provider_credit_card_info/", ProviderCreditCardInfoAdd.as_view(), name="provider_credit_card_info"),  # Naznin --- User Payment Info url

    path("customer_credit_card_info/<user_id>", CustomerCreditCardInfoCRUD.as_view(), name="customer_credit_card_info"),  # Naznin --- User Payment Info url

    path("provider_credit_card_info/<user_id>", ProviderCreditCardInfoCRUD.as_view(), name="provider_credit_card_info"),  # Naznin --- User Payment Info url

    path("get_bill_history/", GetBillHistoryListView.as_view(), name="get_bill_history"),  # Naznin --- User Payment Info url

    path("create_user_bill/", CreateBillApiView.as_view(), name="create_user_bill"),  # Naznin --- User Payment Info url

]