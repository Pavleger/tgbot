from django.core.exceptions import ValidationError
from django.db.models.signals import pre_save, post_save
from django.dispatch import receiver

from social.models import FundsObject, CustomUser
from social.services.funds_transformation_service import FundsTransformationService


@receiver(pre_save, sender=FundsObject)
def check_instance_exists(sender, instance, **kwargs):
    if not instance.pk and FundsObject.objects.all().exists():
        raise ValidationError("Не может быть два объекта с фондами")


@receiver(post_save, sender=CustomUser)
def check_funds_transformation(sender, instance, created, **kwargs):
    if created:
        transformation = FundsTransformationService.execute()
        if transformation:
            instance.save()
