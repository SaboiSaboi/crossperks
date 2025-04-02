import random
from venv import logger
from rest_framework import status, generics
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from django.core.mail import send_mail
from django.conf import settings
from .models import (
    BusinessIdentifier,
    BusinessProfile,
    CustomUser,
    CustomerProfile,
    Perk,
)
from .serializers import (
    BusinessProfileSerializer,
    CustomerProfileSerializer,
    PerkSerializer,
)
from rest_framework.generics import ListAPIView
from knox.models import AuthToken
from django.contrib.auth import authenticate
from knox.auth import TokenAuthentication
from rest_framework.generics import CreateAPIView
from django.shortcuts import get_object_or_404


class SendVerificationCodeView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
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


class UpdateNameView(APIView):
    permission_classes = [IsAuthenticated]

    def put(self, request):
        user = request.user
        raw_name = request.data.get("name")

        if not raw_name:
            return Response(
                {"error": "Name is required."}, status=status.HTTP_400_BAD_REQUEST
            )

        normalized_name = " ".join(
            word.capitalize() for word in raw_name.strip().split()
        )

        user.name = normalized_name
        user.save()
        return Response(
            {"message": "Name updated successfully.", "name": normalized_name},
            status=status.HTTP_200_OK,
        )


class CompleteRegistrationView(generics.CreateAPIView):
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        email = request.data.get("email")
        password = request.data.get("password")

        try:
            user = CustomUser.objects.get(email=email, is_verified=True)

            if user.user_type == "customer":
                cus_name = request.data.get("name")
                if not cus_name:
                    return Response(
                        {"error": "Name is required for customers."},
                        status=status.HTTP_400_BAD_REQUEST,
                    )

                user.name = cus_name
                user.set_password(password)
                user.save()

                CustomerProfile.objects.get_or_create(user=user)

            elif user.user_type == "business":
                business_name = request.data.get("officialName")
                claim_token = request.data.get("claim_token")

                if not business_name or not claim_token:
                    return Response(
                        {"error": "Business name and claim token are required."},
                        status=status.HTTP_400_BAD_REQUEST,
                    )

                business = get_object_or_404(
                    BusinessProfile, claim_token=claim_token, is_claimed=False
                )

                user.name = business_name
                user.set_password(password)
                user.save()

                business.user = user
                business.is_claimed = True
                business.official_name = business_name
                business.generate_qr_code()
                business.save()

            else:
                return Response(
                    {"error": "Invalid user type."},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            _, token = AuthToken.objects.create(user)

            response_data = {
                "message": "Registration and login successful",
                "user": {
                    "email": user.email,
                    "name": user.name,
                    "user_type": user.user_type,
                },
                "auth_token": token,
            }

            return Response(response_data, status=status.HTTP_200_OK)

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


class BusinessListView(generics.ListAPIView):
    """
    Returns a list of unclaimed businesses.
    Only needed if you want an admin view of all unclaimed businesses.
    """

    queryset = BusinessProfile.objects.filter(is_claimed=False)
    serializer_class = BusinessProfileSerializer
    permission_classes = [AllowAny]


class BusinessDetailView(APIView):
    """
    Fetches a specific business's details using the claim token.
    """

    permission_classes = [AllowAny]

    def get(self, request, claim_token):

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

        user = CustomUser.objects.create_user(
            email=email, name=official_name, user_type="business", password=password
        )

        business.user = user
        business.official_name = official_name
        business.street_address = street_address
        business.city = city
        business.state = state
        business.zip_code = zip_code
        business.is_claimed = True

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
                "onboarded": user.is_onboarded,
            },
            "auth_token": token,
        }

        return Response(response_data, status=status.HTTP_200_OK)


class GetUserAPIView(APIView):
    """Fetches the logged-in user's details along with profile info."""

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

        response_data = {
            "user": {
                "id": user.id,
                "name": user.name,
                "email": user.email,
                "user_type": role,
                "is_onboarded": user.is_onboarded,
            },
            "auth_token": token,
        }

        if role == "business":
            business = getattr(user, "business_profile", None)
            if business:
                response_data["business_profile"] = {
                    "official_name": business.official_name,
                    "street_address": business.street_address,
                    "city": business.city,
                    "state": business.state,
                    "zip_code": business.zip_code,
                    "is_claimed": business.is_claimed,
                    "created_at": business.created_at,
                    "qr_code": business.qr_code_url,
                    "website": business.website,
                    "category": business.category,
                    "flyerMessage": business.flyerMessage,
                    "flyerHeadline": business.flyerHeadline,
                    "phone": business.phone,
                    "identifiers": [
                        identifier.name for identifier in business.identifiers.all()
                    ],
                }
        elif role == "customer":
            customer = getattr(user, "customer_profile", None)
            if customer:
                response_data["customer_profile"] = {
                    "current_perk": (
                        PerkSerializer(customer.current_perk).data
                        if customer.current_perk
                        else None
                    ),
                    "previous_perks": PerkSerializer(
                        customer.previous_perks.all(), many=True
                    ).data,
                    "preferred_identifiers": [
                        identifier.name
                        for identifier in customer.preferred_identifiers.all()
                    ],
                }

        return Response(response_data, status=status.HTTP_200_OK)


class CreatePerkView(CreateAPIView):
    """Allows a business to create a perk."""

    permission_classes = [IsAuthenticated]
    serializer_class = PerkSerializer

    def perform_create(self, serializer):
        user = self.request.user
        if user.user_type != "business":
            return Response(
                {"error": "Only businesses can create perks."},
                status=status.HTTP_403_FORBIDDEN,
            )

        business = user.business_profile
        serializer.save(business=business)


class CustomerOnboardingView(APIView):
    permission_classes = [IsAuthenticated]

    def put(self, request, *args, **kwargs):
        """Allow customers to set preferred identifiers."""
        customer_profile = CustomerProfile.objects.get_or_create(user=request.user)
        serializer = CustomerProfileSerializer(
            customer_profile, data=request.data, partial=True
        )

        if serializer.is_valid():
            serializer.save()
            request.user.is_onboarded = True
            request.user.save()
            return Response(serializer.data, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class BusinessOnboardingView(generics.UpdateAPIView):

    serializer_class = BusinessProfileSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return get_object_or_404(BusinessProfile, user=self.request.user)

    def update(self, request, *args, **kwargs):
        business_profile = self.get_object()
        serializer = self.serializer_class(
            business_profile, data=request.data, partial=True
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()

        user = request.user
        user.is_onboarded = True
        user.save()

        return Response(serializer.data, status=status.HTTP_200_OK)


class UserPerkView(generics.RetrieveAPIView):
    serializer_class = PerkSerializer
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        user = request.user
        perk = get_object_or_404(Perk, business__user=user, is_active=True)
        serializer = self.get_serializer(perk)
        return Response({"perk": serializer.data})


class UserPerksView(generics.ListAPIView):
    serializer_class = PerkSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return Perk.objects.filter(business__user=user, is_active=False)


class EndCampaignView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, campaign_id):
        perk = get_object_or_404(
            Perk, id=campaign_id, business__user=request.user, is_active=True
        )

        perk.end_campaign()

        return Response(
            {
                "message": "Campaign ended successfully",
                "ended_at": perk.ended_at.strftime("%Y-%m-%d %H:%M:%S"),
            },
            status=status.HTTP_200_OK,
        )


class BusinessProfileListView(ListAPIView):
    queryset = BusinessProfile.objects.all()
    serializer_class = BusinessProfileSerializer
    permission_classes = [AllowAny]

    # def list(self, request, *args, **kwargs):
    #     try:
    #         queryset = self.get_queryset()
    #         serializer = self.get_serializer(queryset, many=True)
    #         return Response(serializer.data, status=status.HTTP_200_OK)
    #     except Exception as e:
    #         logger.error(f"Error fetching businesses: {str(e)}", exc_info=True)
    #         return Response(
    #             {"error": "Internal Server Error", "details": str(e)},
    #             status=status.HTTP_500_INTERNAL_SERVER_ERROR,
    #         )


class BusinessIdentifierListView(APIView):
    permission_classes = [AllowAny]  # Allow public access

    def get(self, request):
        identifiers = BusinessIdentifier.objects.all().values("id", "name")
        return Response(identifiers)
