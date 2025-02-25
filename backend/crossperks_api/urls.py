from django.contrib import admin
from django.urls import include, path

from account.views import GetUserAPIView

urlpatterns = [
    path("admin/", admin.site.urls),
    path("account/", include("account.urls")),
]
