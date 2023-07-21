from django.conf import settings
from django.db.models import F

from social.models import FundsObject, CustomUser


class FundsTransformationService:
    @staticmethod
    def is_two_degree(number):
        while number > 0 and number % 2 == 0:
            number //= 2
        if number == 1:
            return True
        return False

    @classmethod
    def execute(cls):
        current_user_count = CustomUser.objects.all().count()
        if cls.is_two_degree(current_user_count) and current_user_count >= settings.START_USERS_COUNT_TO_CONVERSION:
            points_to_funds = (current_user_count - 1) * settings.INVITE_REWARD
            CustomUser.objects.all().update(points=F("points") - settings.INVITE_REWARD)

            if not FundsObject.objects.all().exists():
                FundsObject.objects.create()
            funds = FundsObject.objects.all().first()
            funds.investment_fund += points_to_funds // 2
            funds.prize_fund += points_to_funds // 2
            funds.save()

            return True
        return False
