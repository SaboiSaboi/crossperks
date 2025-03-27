from rest_framework import serializers
from .models import BusinessIdentifier, BusinessProfile, CustomUser, CustomerProfile, Perk


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
    
    # ✅ Accept IDs when writing (update)
    identifiers = serializers.PrimaryKeyRelatedField(
        queryset=BusinessIdentifier.objects.all(), many=True, required=False
    )

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

    def to_representation(self, instance):
        """Customize output to return identifier names instead of IDs."""
        data = super().to_representation(instance)
        data["identifiers"] = [identifier.name for identifier in instance.identifiers.all()]
        return data

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

class CustomerProfileSerializer(serializers.ModelSerializer):
    preferred_identifiers = serializers.PrimaryKeyRelatedField(
        queryset=BusinessIdentifier.objects.all(), many=True, required=False
    )

    class Meta:
        model = CustomerProfile
        fields = ["preferred_identifiers"]

    def to_representation(self, instance):
        """Return identifier names instead of IDs."""
        data = super().to_representation(instance)
        data["preferred_identifiers"] = [identifier.name for identifier in instance.preferred_identifiers.all()]
        return data