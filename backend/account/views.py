import random
from rest_framework import status, generics
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from django.core.mail import send_mail
from django.conf import settings
from .models import BusinessProfile, CustomUser
from .serializers import BusinessProfileSerializer, UserRegistrationSerializer
from knox.models import AuthToken
from django.contrib.auth import authenticate

from django.shortcuts import get_object_or_404


class SendVerificationCodeView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        print("minting code")
        email = request.data.get("email")
        user_type = request.data.get("user_type")

        if not email:
            return Response(
                {"error": "Email is required"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        verification_code = str(random.randint(100000, 999999))

        user, created = CustomUser.objects.get_or_create(
            email=email,
            defaults={
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
            if user.user_type == "customer":
                cus_name = request.data.get("name")
                user.name = cus_name
                user.set_password(password)
                user.save()
                return Response(
                    {"message": "Registration complete!"}, status=status.HTTP_200_OK
                )
            if user.user_type == "business":
                businessName = request.data.get("officialName")
                user.name = businessName
                user.set_password(password)
                claim_token = request.data.get("claim_token")
                business = get_object_or_404(
                    BusinessProfile, claim_token=claim_token, is_claimed=False
                )
                business.user = user
                business.is_claimed = True
                business.save()
                user.save()

                return Response(
                    {"message": "Business claimed successfully! You can now log in."},
                    status=status.HTTP_200_OK,
                )

        except CustomUser.DoesNotExist:
            return Response(
                {"error": "Email not verified or user not found."},
                status=status.HTTP_404_NOT_FOUND,
            )


class PreloadBusinessView(APIView):
    """Admin API to pre-load businesses into the system"""

    def post(self, request):
        data = request.data
        business = BusinessProfile.objects.create(
            official_name=data["official_name"],
            street_address=data["street_address"],
            city=data["city"],
            state=data["state"],
            zip_code=data["zip_code"],
        )
        return Response(
            {
                "message": "Business added successfully!",
                "claim_token": business.claim_token,
            },
            status=status.HTTP_201_CREATED,
        )


class SendClaimEmailView(APIView):
    """Sends a claim invitation email to a business owner"""

    def post(self, request):
        claim_token = request.data.get("claim_token")
        business = get_object_or_404(
            BusinessProfile, claim_token=claim_token, is_claimed=False
        )
        email = request.data.get("email")

        claim_url = f"https://crossperks.com/claim-business/{business.claim_token}"
        send_mail(
            subject="Claim Your Business on CrossPerks",
            message=f"Hi, claim your business {business.official_name} on CrossPerks by clicking here: {claim_url}",
            from_email="noreply@crossperks.com",
            recipient_list=[email],
        )

        return Response(
            {"message": "Claim email sent successfully!"}, status=status.HTTP_200_OK
        )


class ClaimBusinessView(APIView):
    """Allows a business owner to claim a business"""

    def post(self, request):
        claim_token = request.data.get("claim_token")
        email = request.data.get("email")
        password = request.data.get("password")

        business = get_object_or_404(
            BusinessProfile, claim_token=claim_token, is_claimed=False
        )

        # Create user
        user = CustomUser.objects.create_user(
            email=email,
            name=business.official_name,
            user_type="business",
            password=password,
        )
        business.user = user
        business.is_claimed = True
        business.save()

        return Response(
            {"message": "Business claimed successfully! You can now log in."},
            status=status.HTTP_200_OK,
        )


### **1️⃣ API: List All Unclaimed Businesses (Optional)**
class BusinessListView(generics.ListAPIView):
    """
    Returns a list of unclaimed businesses.
    Only needed if you want an admin view of all unclaimed businesses.
    """

    queryset = BusinessProfile.objects.filter(is_claimed=False)
    serializer_class = BusinessProfileSerializer
    permission_classes = [AllowAny]  # Change this if only admins should access it


### **2️⃣ API: Fetch Business Details by Claim Token**
class BusinessDetailView(APIView):
    """
    Fetches a specific business's details using the claim token.
    """

    permission_classes = [AllowAny]  # Anyone with a claim link should access this

    def get(self, request, claim_token):

        print("in func", request)
        business = get_object_or_404(BusinessProfile, claim_token=claim_token)

        if business.is_claimed == True:
            no_data = {"is_claimed": True}
            return Response(no_data)
        else:
            data = {
                "official_name": business.official_name,
                "street_address": business.street_address,
                "city": business.city,
                "state": business.state,
                "zip_code": business.zip_code,
                "is_claimed": business.is_claimed,
            }

            return Response(data)


class ClaimBusinessView(APIView):
    permission_classes = [AllowAny]
    """Allows a business owner to claim a business, set details, and generate a QR code."""

    def post(self, request):
        claim_token = request.data.get("claim_token")
        email = request.data.get("email")
        password = request.data.get("password")
        official_name = request.data.get("official_name")
        street_address = request.data.get("street_address")
        city = request.data.get("city")
        state = request.data.get("state")
        zip_code = request.data.get("zip_code")

        business = get_object_or_404(
            BusinessProfile, claim_token=claim_token, is_claimed=False
        )

        # Create business owner account
        user = CustomUser.objects.create_user(
            email=email, name=official_name, user_type="business", password=password
        )

        # Update business profile with details
        business.user = user
        business.official_name = official_name
        business.street_address = street_address
        business.city = city
        business.state = state
        business.zip_code = zip_code
        business.is_claimed = True

        # Generate QR Code
        business.generate_qr_code()
        business.save()

        return Response(
            {
                "message": "Business successfully claimed!",
                "qr_code_url": business.qr_code.url,
            },
            status=status.HTTP_200_OK,
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
