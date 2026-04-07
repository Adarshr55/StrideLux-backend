# accounts/utils.py
from django.core.mail import send_mail
from django.conf import settings

def send_verification_email(user):
    link = f"{settings.FRONTEND_URL}/verify-email/{user.verification_token}"
    send_mail(
        subject="Verify your StrideLux account",
        message=f"Hi {user.username},\n\nVerify your email:\n{link}\n\n— StrideLux Team",
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[user.email],
        fail_silently=False,
    )

def send_password_reset_email(user):
    link = f"{settings.FRONTEND_URL}/reset-password/{user.reset_token}"
    send_mail(
        subject="Reset your StrideLux password",
        message=f"Hi {user.username},\n\nReset your password:\n{link}\n\nExpires in 15 minutes.\n\n— StrideLux Team",
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[user.email],
        fail_silently=False,
    )