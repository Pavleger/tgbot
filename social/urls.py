from django.urls import path
from social.views import main_page_view


urlpatterns = [
    path("invite/<str:invite_id>/", main_page_view, name="user-invite"),
]
