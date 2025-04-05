import logging
import uuid
import qrcode
from io import BytesIO
from django.db import models
from django.conf import settings
from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin,
)
import boto3
from django.utils.timezone import now
from django.contrib.auth import get_user_model


class CustomUserManager(BaseUserManager):
    def create_user(
        self, email, name, user_type="customer", password=None, **extra_fields
    ):
        if not email:
            raise ValueError("The Email field must be set")
        email = self.normalize_email(email)

        # Ensure extra fields contain necessary default values
        extra_fields.setdefault("is_staff", False)
        extra_fields.setdefault("is_superuser", False)

        user = self.model(email=email, name=name, user_type=user_type, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, name, password=None, **extra_fields):
        """Create and return a superuser with admin privileges"""

        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        return self.create_user(
            email, name, user_type="business", password=password, **extra_fields
        )


class CustomUser(AbstractBaseUser, PermissionsMixin):
    USER_TYPE_CHOICES = [
        ("customer", "Customer"),
        ("business", "Business"),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    email = models.EmailField(unique=True)
    name = models.CharField(max_length=100)
    user_type = models.CharField(
        max_length=10, choices=USER_TYPE_CHOICES, default="customer"
    )

    deleted = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    is_verified = models.BooleanField(default=False)

    is_onboarded = models.BooleanField(default=False)
    verification_code = models.CharField(max_length=6, blank=True, null=True)
    date_joined = models.DateTimeField(auto_now_add=True)

    objects = CustomUserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["name"]

    def __str__(self):
        return f"{self.name} ({self.user_type})"


class BusinessIdentifier(models.Model):
    """Model for business identifiers (e.g., Women-Owned, LGBTQ+)."""

    name = models.CharField(max_length=100, unique=True)

    slug = models.SlugField(max_length=100, unique=True)

    def __str__(self):
        return self.name


class BusinessProfile(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="business_profile",
    )

    official_name = models.CharField(max_length=255)
    street_address = models.CharField(max_length=255, blank=True, null=True)
    city = models.CharField(max_length=100, blank=True, null=True)
    state = models.CharField(max_length=100, blank=True, null=True)
    zip_code = models.CharField(max_length=20, blank=True, null=True)

    category = models.CharField(max_length=255, blank=True, null=True)
    flyerMessage = models.CharField(max_length=255, blank=True, null=True)
    flyerHeadline = models.CharField(max_length=255, blank=True, null=True)
    website = models.URLField(blank=True, null=True)
    phone = models.CharField(max_length=20, blank=True, null=True)
    logo = models.URLField(null=True, blank=True)
    identifiers = models.ManyToManyField(BusinessIdentifier, blank=True)
    is_claimed = models.BooleanField(default=False)
    claim_token = models.UUIDField(default=uuid.uuid4, unique=True, editable=False)

    qr_code_url = models.URLField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.official_name

    def generate_qr_code(self):
        logger = logging.getLogger(__name__)

        try:
            qr = qrcode.make(f"https://crossperks.com/business/{self.id}")
            buffer = BytesIO()
            qr.save(buffer, format="PNG")

            filename = f"business_qr_codes/qr_{self.id}.png"
            logger.debug(f"Attempting to upload QR Code: {filename}")

            s3 = boto3.client("s3")

            s3.put_object(
                Bucket=settings.AWS_STORAGE_BUCKET_NAME,
                Key=filename,
                Body=buffer.getvalue(),
                ContentType="image/png",
            )

            qr_url = f"https://{settings.AWS_STORAGE_BUCKET_NAME}.s3.amazonaws.com/{filename}"

            self.qr_code_url = qr_url
            self.save()

            logger.info(f"QR Code uploaded to S3: {self.qr_code_url}")

        except Exception as e:
            logger.error(f"Failed to upload QR Code: {str(e)}")


class CustomerProfile(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="customer_profile",
    )
    current_perk = models.ForeignKey(
        "Perk",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="current_perk",
    )
    previous_perks = models.ManyToManyField(
        "Perk", related_name="previous_perks", blank=True
    )

    preferred_identifiers = models.ManyToManyField("BusinessIdentifier", blank=True)

    def __str__(self):
        return f"Profile for {self.user.name}"


class Perk(models.Model):
    business = models.ForeignKey(
        "BusinessProfile", on_delete=models.CASCADE, related_name="perks"
    )
    title = models.CharField(max_length=255)
    description = models.CharField(max_length=255)
    total = models.IntegerField(default=0)
    remaining = models.IntegerField(default=0)
    redemptions = models.IntegerField(default=0)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    ended_at = models.DateTimeField(null=True, blank=True)

    def end_campaign(self):
        """Marks the campaign as ended"""
        self.is_active = False
        self.ended_at = now()
        self.save()

    def __str__(self):
        return f"{self.description} (From {self.business.official_name})"


class PasswordResetCode(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    code = models.CharField(max_length=6)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Reset code for {self.user.email}"
