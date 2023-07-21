import uuid
import qrcode
from PIL import Image
from django.db import models
from django.conf import settings
from django.contrib.auth.models import AbstractUser, UserManager
from django.core.validators import MinLengthValidator, RegexValidator


telegram_validator = [
    MinLengthValidator(
        limit_value=5,
        message="Ник должен быть не менее 5 символов"
    ),
    RegexValidator(
        regex="^[a-zA-Z0-9_]*$",
        message="Телеграм должен содержать только латиницу, цифры и символ '_'",
        code="invalid_telegram"
    )
]


def _generate_qr_code_to_invite(_id):
    link = settings.SITE_URL + "social/invite/" + str(_id)
    qr_code_img = qrcode.make(link)
    qr_code_img.save(settings.MEDIA_ROOT + f"qr_codes/{str(_id)}.jpg")
    return


def _get_invite_qr(_id):
    return Image.open(settings.MEDIA_ROOT + f"qr_codes/{str(_id)}.jpg")


class CustomUser(AbstractUser):
    telegram = models.CharField(
        "Телеграм",
        max_length=50,
        unique=True,
        null=True,
        blank=True,
        validators=telegram_validator
    )
    chat_id = models.PositiveBigIntegerField("ID чата", null=True, blank=True)
    inviter = models.ForeignKey(
        "self",
        verbose_name="Пригласивший",
        related_name="invited",
        blank=True,
        null=True,
        on_delete=models.SET_NULL
    )
    invite_id = models.UUIDField(
        unique=True,
        null=True,
        editable=False,
    )
    points = models.IntegerField("Баллы", default=10500)
    objects = UserManager()

    @property
    def inviter_info(self):
        if self.inviter:
            return self.inviter.username
        return "-"

    @property
    def invited_count(self):
        return self.invited.all().count()

    @property
    def invite_link(self):
        return f"{settings.SITE_URL}social/invite/{str(self.invite_id)}"

    @property
    def invite_qr_code(self):
        return _get_invite_qr(self.invite_id)

    def save(self, *args, **kwargs):
        if not self.invite_id:
            self.create_invite()
        self.full_clean()
        return super(CustomUser, self).save(*args, **kwargs)

    def create_invite(self):
        invite_id = uuid.uuid4()
        self.invite_id = invite_id
        _generate_qr_code_to_invite(invite_id)

    def add_invite_reward(self):
        self.points += settings.INVITE_REWARD
        self.save()

    class Meta:
        verbose_name = "Пользователь"
        verbose_name_plural = "Пользователи"


class FundsObject(models.Model):
    investment_fund = models.IntegerField("Инвестиционный фонд", default=0)
    prize_fund = models.IntegerField("Призовой фонд", default=0)

    class Meta:
        verbose_name = "Объект фонда"
        verbose_name_plural = "Объекты фонда"
