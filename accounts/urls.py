from django.urls import path
from .import views
from rest_framework_simplejwt.views import TokenRefreshView
urlpatterns=[
    path('register/',views.RegisterView.as_view(),name='register'),
    path('login/',views.LoginView.as_view(),name='login'),
    path('profile/',views.ProfileView.as_view(),name='profile'),
    path('logout/',views.LogoutView.as_view(),name='logout'),
    path('token/refresh/',TokenRefreshView.as_view(),name='token_refresh'),

    path('verify-email/<uuid:token>/', views.VerifyEmailView.as_view()),
    path('resend-verification/', views.ResendVerificationView.as_view()),
    path('forgot-password/', views.ForgotPasswordView.as_view()),
    path('reset-password/<uuid:token>/', views.ResetPasswordView.as_view()),




]