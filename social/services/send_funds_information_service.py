from social.services.bot_service import bot
from social.services.messages import NO_FUNDS_TEXT, FUNDS_INFO_TEXT
from social.models import FundsObject


class SendFundsInformationService:
    @classmethod
    def execute(cls, user):
        if not FundsObject.objects.all().exists():
            bot.send_message(user.chat_id, NO_FUNDS_TEXT)
        else:
            fund = FundsObject.objects.all().first()
            bot.send_message(user.chat_id, FUNDS_INFO_TEXT.format(fund.investment_fund, fund.prize_fund))
