from social.services.bot_service import bot
from social.services.messages import ACCOUNT_INFORMATION_TEXT


class SendAccountInformationService:
    @classmethod
    def execute(cls, user):
        bot.send_message(
            user.chat_id,
            ACCOUNT_INFORMATION_TEXT.format(
                user.points,
                user.inviter_info,
                user.invited_count
            )
        )
