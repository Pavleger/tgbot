from django.shortcuts import render, Http404
from django.conf import settings

from social.models import CustomUser


def main_page_view(request, invite_id):
    users = CustomUser.objects.filter(invite_id=invite_id)
    if not users.exists():
        raise Http404

    return render(request, "social_bot/index.html", {"invite_id": invite_id, "BOT_NAME": settings.BOT_NAME})


def page_not_found(request, exception):
    return render(request, "404.html", {})
