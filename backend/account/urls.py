from django.urls import path
from .views import (
    BusinessDetailView,
    BusinessListView,
    BusinessOnboardingView,
    ClaimBusinessView,
    CreatePerkView,
    GetUserAPIView,
    LoginView,
    SendVerificationCodeView,
    UserPerkView,
    UserPerksView,
    VerifyCodeView,
    CompleteRegistrationView,
)

urlpatterns = [
    path("send-code/", SendVerificationCodeView.as_view(), name="send_code"),
    path("verify-code/", VerifyCodeView.as_view(), name="verify_code"),
    path(
        "complete-registration/",
        CompleteRegistrationView.as_view(),
        name="complete_registration",
    ),
    path("login/", LoginView.as_view(), name="login"),
    path("user/", GetUserAPIView.as_view(), name="get-user"),
    path("create-perk/", CreatePerkView.as_view(), name="create-perk"),
    path("businesses/", BusinessListView.as_view(), name="business-list"),
    path(
        "business/<uuid:claim_token>/",
        BusinessDetailView.as_view(),
        name="business-detail",
    ),
    path("past-perks/", UserPerksView.as_view(), name="get-past-perks"),
    path(
        "claim-business/",
        ClaimBusinessView.as_view(),
        name="business-detail",
    ),
    path("perk/", UserPerkView.as_view(), name="get-a-perk"),
    path("onboarding/", BusinessOnboardingView.as_view(), name="onboarding-user"),
]
