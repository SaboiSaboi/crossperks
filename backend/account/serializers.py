from rest_framework import serializers
from .models import BusinessProfile, CustomUser, Perk


class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    user_type = serializers.ChoiceField(choices=CustomUser.USER_TYPE_CHOICES)

    class Meta:
        model = CustomUser
        fields = ["name", "email", "password", "user_type"]

    def create(self, validated_data):
        user = CustomUser.objects.create_user(
            name=validated_data["name"],
            email=validated_data["email"],
            password=validated_data["password"],
            user_type=validated_data["user_type"],
        )
        return user


class BusinessProfileSerializer(serializers.ModelSerializer):
    category = serializers.CharField(required=False, allow_blank=True)
    website = serializers.URLField(required=False, allow_blank=True)
    phone = serializers.CharField(required=False, allow_blank=True)
    identifiers = serializers.StringRelatedField(many=True)

    class Meta:
        model = BusinessProfile
        fields = [
            "official_name",
            "street_address",
            "city",
            "state",
            "zip_code",
            "category",
            "website",
            "phone",
            "logo",
            "identifiers",
        ]

        read_only_fields = ["is_claimed", "claim_token", "qr_code"]


class PerkSerializer(serializers.ModelSerializer):
    """Serializer for Perk model"""

    class Meta:
        model = Perk
        fields = [
            "id",
            "business",
            "title",
            "description",
            "total",
            "remaining",
            "redemptions",
            "is_active",
            "created_at",
            "ended_at",
        ]
        read_only_fields = ["id", "business", "created_at"]
