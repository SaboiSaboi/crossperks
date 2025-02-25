import random
from rest_framework import status, generics
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from django.core.mail import send_mail
from django.conf import settings
from .models import CustomUser
from .serializers import UserRegistrationSerializer
from knox.models import AuthToken
from django.contrib.auth import authenticate


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


class LoginView(APIView):
    authentication_classes = []
    permission_classes = [AllowAny]

    def post(self, request):
        email = request.data.get("email")
        password = request.data.get("password")

        if not email or not password:
            return Response({"error": "Email and password are required."}, status=400)

        user = authenticate(request, username=email, password=password)
        if user is None:
            return Response({"error": "Invalid email or password."}, status=400)

        _, token = AuthToken.objects.create(user)

        response_data = {
            "message": "Login successful",
            "user": {
                "id": user.id,
                "email": user.email,
                "name": user.name,
                "user_type": user.user_type,
            },
            "auth_token": token,
        }

        return Response(response_data, status=status.HTTP_200_OK)


from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from knox.auth import TokenAuthentication


class GetUserAPIView(APIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        auth_header = request.META.get("HTTP_AUTHORIZATION")
        token = (
            auth_header.split(" ")[1]
            if auth_header and auth_header.startswith("Token ")
            else None
        )

        user = request.user

        role = user.user_type if hasattr(user, "user_type") else "Unknown"
        company = getattr(user, "company", None)

        response_data = {
            "message": "User data retrieved successfully",
            "user": {
                "id": user.id,
                "name": user.name,
                "email": user.email,
                "user_type": role,
            },
            "auth_token": token,
        }

        if company:
            response_data["company"] = {
                "id": company.id,
                "name": company.name,
                "admin_id": getattr(company.admin, "id", None),
                "created_at": company.created_at,
            }
        else:
            response_data["company"] = None

        return Response(response_data, status=status.HTTP_200_OK)
