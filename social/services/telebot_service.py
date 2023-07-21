import telebot

from social.models import CustomUser
from social.services.bot_service import bot
from social.services.user_create_service import UserCreateService
from social.services.send_user_invite_service import SendUserInviteService
from social.services.send_account_information_service import SendAccountInformationService
from social.services.send_funds_information_service import SendFundsInformationService
from social.services.messages import *


CONTENT_TYPES = ["text", "audio", "document", "photo", "sticker", "video", "video_note", "voice", "location", "contact",
                 "new_chat_members", "left_chat_member", "new_chat_title", "new_chat_photo", "delete_chat_photo",
                 "group_chat_created", "supergroup_chat_created", "channel_chat_created", "migrate_to_chat_id",
                 "migrate_from_chat_id", "pinned_message"]


class TelebotStartService:
    def _run(self):
        @bot.message_handler(commands=["start", ])
        def _send_welcome(message):
            invite_id = message.text[7:]
            markup = self._get_main_keyboard()
            if invite_id:
                users = CustomUser.objects.filter(invite_id=invite_id)
                user = None
                if users.exists():
                    user = UserCreateService.execute(message.from_user, markup, users.first())
                else:
                    bot.send_message(message.chat.id, WRONG_INVITE_TEXT)
            else:
                user = UserCreateService.execute(message.from_user, markup)

            if user:
                bot.send_message(message.chat.id, PROJECT_WELCOME_TEXT, reply_markup=markup)

        @bot.message_handler(content_types=CONTENT_TYPES)
        def button_handler(message):
            user = CustomUser.objects.get(chat_id=message.chat.id, is_active=True)
            markup = self._get_main_keyboard()
            if message.text == MY_INVITE_BTN_TEXT:
                SendUserInviteService.execute(user)
            elif message.text == ACCOUNT_INFORMATION_BTN_TEXT:
                SendAccountInformationService.execute(user)
            elif message.text == FUNDS_INFORMATION_BTN_TEXT:
                SendFundsInformationService.execute(user)

    @staticmethod
    def _get_main_keyboard():
        markup_main = telebot.types.ReplyKeyboardMarkup(True, one_time_keyboard=False)
        invite_btn = telebot.types.KeyboardButton(MY_INVITE_BTN_TEXT)
        info_btn = telebot.types.KeyboardButton(ACCOUNT_INFORMATION_BTN_TEXT)
        funds_info_btn = telebot.types.KeyboardButton(FUNDS_INFORMATION_BTN_TEXT)
        markup_main.add(invite_btn, info_btn, funds_info_btn)
        return markup_main

    def execute(self):
        self._run()

        bot.infinity_polling(timeout=100, long_polling_timeout=100)
