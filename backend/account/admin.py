from django.contrib import admin

from account.models import BusinessIdentifier, BusinessProfile, CustomUser


@admin.register(BusinessIdentifier)
class BusinessIdentifierAdmin(admin.ModelAdmin):
    list_display = ("name",)  # Display the identifier name
    search_fields = ("name",)  # Add search functionality


@admin.register(BusinessProfile)
class BusinessProfileAdmin(admin.ModelAdmin):
    list_display = ("official_name", "city", "state", "is_claimed", "created_at")
    search_fields = ("official_name", "city", "state")
    list_filter = ("is_claimed",)


@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    list_display = ("email", "name", "user_type", "is_verified", "date_joined")
    search_fields = ("email", "name")
    list_filter = ("user_type", "is_verified")
