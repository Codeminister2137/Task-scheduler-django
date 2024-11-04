from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import EmailEvent, Email

@receiver(post_save, sender=Email)
def create_email_event(sender, instance, created, **kwargs):

    EmailEvent.objects.create(email=instance, event_type="created")