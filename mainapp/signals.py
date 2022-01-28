from .models import Dogs, ServicesInfo, User, AdditionalInformation
from django.db.models.signals import post_save
from django.dispatch import receiver


@receiver(post_save, sender=User)
def create_addictionalInformation_when_create_user (sender, instance, created, **kwargs):
    if created:
        AdditionalInformation.objects.create(userId=instance)
        if(instance.type == "2"):
            ServicesInfo.objects.create(userId=instance, type="WK")

