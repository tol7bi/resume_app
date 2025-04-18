from django.core.mail import send_mail
from django.conf import settings
from rest_framework_simplejwt.tokens import AccessToken






def verification_email(user):
    token = str(AccessToken.for_user(user))
    verify_url = f"http://localhost:8000/api/users/verify-email/?token={token}"

    send_mail(
        subject="Verify your email",
        message=f"Click the link to verify your email: {verify_url}",
        from_email=settings.EMAIL_HOST_USER,
        recipient_list=[user.email])