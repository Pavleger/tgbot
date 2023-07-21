from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand
from django.conf import settings

from social.models import FundsObject


class Command(BaseCommand):
    help = "Инициализация проекта, создание фондов и супер юзера"

    def handle(self, *args, **kwargs):
        User = get_user_model()
        if not User.objects.filter(username=settings.ADMIN_USERNAME).exists():
            User.objects.create_superuser(
                username=settings.ADMIN_USERNAME,
                password=settings.ADMIN_PASSWORD,
                email=f"{settings.ADMIN_USERNAME}@mail.ru"
            )

        if not FundsObject.objects.all().exists():
            FundsObject.objects.create()
