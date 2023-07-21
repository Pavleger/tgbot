from social.models import CustomUser
from social.services.bot_service import bot
from social.services.messages import ALREADY_REGISTER_IN_PROJECT_TEXT


class UserCreateService:
    @classmethod
    def execute(cls, raw_user, markup, inviter=None):
        if raw_user.username:
            username = raw_user.username
            telegram = raw_user.username
        else:
            username = raw_user.first_name
            telegram = None

        if CustomUser.objects.filter(username=username).exists():
            bot.send_message(raw_user.id, ALREADY_REGISTER_IN_PROJECT_TEXT, reply_markup=markup)
        else:
            try:
                user = CustomUser.objects.create_user(
                    username=username,
                    telegram=telegram,
                    chat_id=raw_user.id,
                    password=username,
                    first_name=raw_user.first_name if raw_user.first_name else "",
                    last_name=raw_user.last_name if raw_user.last_name else "",
                    inviter=inviter
                )
                if inviter:
                    inviter.add_invite_reward()

                return user
            except Exception:
                return
