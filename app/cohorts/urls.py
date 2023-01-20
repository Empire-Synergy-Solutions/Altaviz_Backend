from django.urls import path, include
#from cohorts import views
from cohorts.views.cohorts import ( cohort_list, 
                                    cohort_create, 
                                    cohort_detail, 
                                    cohort_member_add, 
                                    cohort_send_invitations,
                                    )
from cohorts.views.account import (
    ChangePasswordView,
    ConfirmEmailView,
    DeleteView,
    LoginView,
    LogoutView,
    PasswordResetTokenView,
    PasswordResetView,
    SettingsView,
    SignupView,
)
#app_name = "pinax_cohorts"

urlpatterns = [
    path("cohorts/", cohort_list, name="list"),
    path("create/", cohort_create, name="create"),
    path("cohort/<int:pk>/", cohort_detail, name="detail"),
    path("cohort/<int:pk>/add_member/", cohort_member_add, name="member_add"),
    path("cohort/<int:pk>/send_invitations/", cohort_send_invitations, name="send_invitations"),
    path("signup/", SignupView.as_view(), name="account_signup"),
    path("login/", LoginView.as_view(), name="account_login"),
    path("logout/", LogoutView.as_view(), name="account_logout"),
    path("confirm_email/<key>/", ConfirmEmailView.as_view(), name="account_confirm_email"),
    path("password/", ChangePasswordView.as_view(), name="account_password"),
    path("password/reset/", PasswordResetView.as_view(), name="account_password_reset"),
    path("password/reset/<uidb36>[0-9A-Za-z]<token>/", PasswordResetTokenView.as_view(), name="account_password_reset_token"),
    path("settings/", SettingsView.as_view(), name="account_settings"),
    path("delete/", DeleteView.as_view(), name="account_delete"),
]

