from rest_framework import generics
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import AccessToken
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import smart_bytes, smart_str
from django.core.mail import send_mail

from .serializers import RegisterSerializer
from .models import User
from .utils import verification_email

token_maker = PasswordResetTokenGenerator()


class RegisterView(generics.CreateAPIView):
    serializer_class = RegisterSerializer
    permission_classes = [AllowAny]
    queryset = User.objects.all()

    def perform_create(self, serializer):
        new_user = serializer.save()
        verification_email(new_user)
        return Response({'message': 'Check your email for the verification link.'}, status=201)


class VerifyEmailView(APIView):
    permission_classes = [AllowAny]

    def get(self, request):
        token = request.query_params.get('token')
        try:
            payload = AccessToken(token)
            user_id = payload.get('user_id')
            user = User.objects.get(pk=user_id)
            user.email_verified = True
            user.save()
            return Response({'message': 'Email verified successfully.'})
        except Exception:
            return Response({'error': 'Token is invalid or has expired.'}, status=400)


class RequestPasswordResetView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        email = request.data.get('email')
        try:
            user = User.objects.get(email=email)
            uid = urlsafe_base64_encode(smart_bytes(user.pk))
            token = token_maker.make_token(user)

            reset_link = f"http://localhost:8080/api/users/reset-password/?uid={uid}&token={token}"

            send_mail(
                subject='Password Reset Instructions',
                message=f'To reset your password, click the link below:\n{reset_link}',
                from_email='noreply@example.com',
                recipient_list=[email]
            )

            return Response({'message': 'Password reset link has been sent to your email.'})
        except User.DoesNotExist:
            return Response({'error': 'No user found with this email.'}, status=404)


class PasswordResetConfirmView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        uidb64 = request.query_params.get('uid')
        token = request.query_params.get('token')
        new_password = request.data.get('new_password')

        try:
            uid = smart_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=uid)

            if token_maker.check_token(user, token):
                user.set_password(new_password)
                user.save()
                return Response({'message': 'Password has been reset successfully.'})
            else:
                return Response({'error': 'Token is invalid or expired.'}, status=400)

        except Exception:
            return Response({'error': 'An error occurred during password reset.'}, status=400)
