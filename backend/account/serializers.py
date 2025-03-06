from rest_framework import serializers
from .models import BusinessProfile, CustomUser


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
    class Meta:
        model = BusinessProfile
        fields = [
            "official_name",
            "street_address",
            "city",
            "state",
            "zip_code",
            "is_claimed",
            "claim_token",
        ]
