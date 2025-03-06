import logging
import uuid
import qrcode
from io import BytesIO
from django.db import models
from django.core.files.base import ContentFile
from django.conf import settings
from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin,
)


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

        # Ensure superuser has admin privileges
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

    email = models.EmailField(unique=True)
    name = models.CharField(max_length=100)
    user_type = models.CharField(
        max_length=10, choices=USER_TYPE_CHOICES, default="customer"
    )

    # 🔥 ADD THESE TWO FIELDS TO FIX THE ERROR
    is_staff = models.BooleanField(default=False)  # Required for Django admin
    is_superuser = models.BooleanField(default=False)  # Required for superusers

    is_verified = models.BooleanField(default=False)
    verification_code = models.CharField(max_length=6, blank=True, null=True)
    date_joined = models.DateTimeField(auto_now_add=True)

    objects = CustomUserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["name"]

    def __str__(self):
        return f"{self.name} ({self.user_type})"


class BusinessProfile(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="business_profile",
    )

    # Business Details (Entered when business claims)
    official_name = models.CharField(max_length=255)
    street_address = models.CharField(max_length=255, blank=True, null=True)
    city = models.CharField(max_length=100, blank=True, null=True)
    state = models.CharField(max_length=100, blank=True, null=True)
    zip_code = models.CharField(max_length=20, blank=True, null=True)

    # Claiming System
    is_claimed = models.BooleanField(default=False)
    claim_token = models.UUIDField(default=uuid.uuid4, unique=True, editable=False)

    # QR Code
    qr_code = models.ImageField(upload_to="", blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.official_name

    def generate_qr_code(self):
        logger = logging.getLogger(__name__)
        """Generates and saves a QR code for the business in S3"""

        try:
            qr = qrcode.make(f"https://crossperks.com/business/{self.id}")
            buffer = BytesIO()
            qr.save(buffer, format="PNG")

            filename = f"business_qr_codes/qr_{self.id}.png"

            logger.debug(f"🚀 Attempting to upload QR Code: {filename}")

            # Save QR Code to S3
            self.qr_code.save(filename, ContentFile(buffer.getvalue()), save=True)

            logger.info(f"✅ QR Code uploaded to S3: {self.qr_code.url}")
            print(f"✅ QR Code uploaded to S3: {self.qr_code.url}")

        except Exception as e:
            logger.error(f"❌ Failed to upload QR Code: {str(e)}")
            print(f"❌ Failed to upload QR Code: {str(e)}")
