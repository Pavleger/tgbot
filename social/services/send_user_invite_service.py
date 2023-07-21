from social.services.bot_service import bot
from social.services.messages import INVITE_MESSAGE_TEXT


class SendUserInviteService:
    @classmethod
    def execute(cls, user):
        bot.send_photo(user.chat_id, user.invite_qr_code)
        bot.send_message(user.chat_id, INVITE_MESSAGE_TEXT.format(user.invite_link))
