from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path("admin/", admin.site.urls),
    path("social/", include("social.urls")),
]

handler404 = "social.views.page_not_found"
