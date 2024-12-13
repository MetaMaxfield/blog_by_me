from django.db.models.signals import post_delete, pre_save
from django.dispatch.dispatcher import receiver

from users.models import CustomUser


@receiver(post_delete, sender=CustomUser)
def customuser_image_file_delete(sender, instance, **kwargs):
    """Удаляет файл с изображением при удалении пользователя"""
    if instance.image:
        instance.image.delete(save=False)


@receiver(pre_save, sender=CustomUser)
def customuser_image_file_delete_when_replace(sender, instance, **kwargs):
    """Удаляет старый файл с изображением при изменении аватара пользователя"""
    if instance.id:
        old_instance = CustomUser.objects.get(id=instance.id)
        if old_instance.image and old_instance.image != instance.image:
            old_instance.image.delete(save=False)
