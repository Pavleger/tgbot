from django.core.management.base import BaseCommand
from social.services.telebot_service import TelebotStartService


class Command(BaseCommand):
    help = "Запуск социального бота"

    def handle(self, *args, **kwargs):
        tele_bot_service = TelebotStartService()
        tele_bot_service.execute()
