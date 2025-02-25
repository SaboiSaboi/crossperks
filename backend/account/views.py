import random
from rest_framework import status, generics
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from django.core.mail import send_mail
from django.conf import settings
from .models import CustomUser
from .serializers import UserRegistrationSerializer


class SendVerificationCodeView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        print("minting code")
        email = request.data.get("email")
        name = request.data.get("name")
        user_type = request.data.get("user_type")

        if not email or not name:
            return Response(
                {"error": "Email and name are required"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        verification_code = str(random.randint(100000, 999999))

        user, created = CustomUser.objects.get_or_create(
            email=email,
            defaults={
                "name": name,
                "user_type": user_type,
                "verification_code": verification_code,
            },
        )

        if not created:
            user.verification_code = verification_code
            user.save()

        # Send verification email
        send_mail(
            "Your CrossPerks Verification Code",
            f"Your verification code is: {verification_code}",
            settings.DEFAULT_FROM_EMAIL,
            [email],
            fail_silently=False,
        )

        return Response(
            {"message": "Verification code sent."}, status=status.HTTP_200_OK
        )


class VerifyCodeView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        email = request.data.get("email")
        code = request.data.get("code")

        try:
            user = CustomUser.objects.get(email=email)
            if user.verification_code == code:
                user.is_verified = True
                user.verification_code = None
                user.save()
                return Response(
                    {"message": "Email verified successfully."},
                    status=status.HTTP_200_OK,
                )
            else:
                return Response(
                    {"error": "Invalid verification code."},
                    status=status.HTTP_400_BAD_REQUEST,
                )
        except CustomUser.DoesNotExist:
            return Response(
                {"error": "User not found."}, status=status.HTTP_404_NOT_FOUND
            )


class CompleteRegistrationView(generics.CreateAPIView):
    permission_classes = [AllowAny]

    serializer_class = UserRegistrationSerializer

    def post(self, request, *args, **kwargs):
        email = request.data.get("email")
        password = request.data.get("password")

        try:
            user = CustomUser.objects.get(email=email, is_verified=True)
            user.set_password(password)
            user.save()
            return Response(
                {"message": "Registration complete!"}, status=status.HTTP_200_OK
            )
        except CustomUser.DoesNotExist:
            return Response(
                {"error": "Email not verified or user not found."},
                status=status.HTTP_404_NOT_FOUND,
            )
