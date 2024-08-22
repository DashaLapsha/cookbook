from django.urls import path, re_path, include
from dj_rest_auth.registration.views import VerifyEmailView, ConfirmEmailView, ResendEmailVerificationView
from dj_rest_auth.views import PasswordResetConfirmView, PasswordResetView
from .views import UserDetailsView, CustomLoginView, CustomLogoutView, CSRFTokenView, CustomRegisterView, CheckSessionView

urlpatterns = [
    path('session-check/', CheckSessionView.as_view(), name='check-session'),
    path('account-confirm-email/<str:key>/', ConfirmEmailView.as_view()),
    path('register/', CustomRegisterView.as_view(), name='register'),
    path('login/', CustomLoginView.as_view(), name='login'),
    path('logout/', CustomLogoutView.as_view(), name='logout'),

    path('verify-email/',
         VerifyEmailView.as_view(), name='rest_verify_email'),
    path('account-confirm-email/',
         VerifyEmailView.as_view(), name='account_email_verification_sent'),
    re_path(r'^account-confirm-email/(?P<key>[-:\w]+)/$',
         VerifyEmailView.as_view(), name='account_confirm_email'),
         path('resend-email/', ResendEmailVerificationView.as_view(), name="rest_resend_email"),
    path('<int:id>/', UserDetailsView.as_view(), name='user-details'),
    path('password-reset/', PasswordResetView.as_view()),
        path('password-reset-confirm/<uidb64>/<token>/',
         PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
         
    path('', include('dj_rest_auth.urls')), 
    path('csrf/', CSRFTokenView.as_view(), name='csrf_token'),
]