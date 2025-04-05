from django.urls import path
from .views import (
    BusinessDetailView,
    BusinessIdentifierListView,
    BusinessOnboardingView,
    BusinessProfileListView,
    ClaimBusinessView,
    CreatePerkView,
    CustomerOnboardingView,
    DeleteAccountView,
    EndCampaignView,
    GetUserAPIView,
    LoginView,
    ResetPasswordAPIView,
    SendResetCodeAPIView,
    SendVerificationCodeView,
    UpdateFlyerView,
    UpdateNameView,
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
    path(
        "customer-onboarding/", CustomerOnboardingView.as_view(), name="customer-user"
    ),
    path(
        "perks/<int:campaign_id>/end/", EndCampaignView.as_view(), name="end_campaign"
    ),
    path("businesses/", BusinessProfileListView.as_view(), name="business-list"),
    path("identifiers/", BusinessIdentifierListView.as_view(), name="identifier-list"),
    path("update-name/", UpdateNameView.as_view(), name="update-name"),
    path("update-flyer/", UpdateFlyerView.as_view(), name="update-name"),
    path("send-reset-code/", SendResetCodeAPIView.as_view(), name="send-reset-code"),
    path("delete-account/", DeleteAccountView.as_view(), name="delete-account"),
    path("reset-password/", ResetPasswordAPIView.as_view(), name="reset-password"),
]
