from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from datetime import datetime

from .models import EmailEvent, Email

@receiver(post_save, sender=Email)
def create_email_event(instance, **kwargs):

    EmailEvent.objects.create(email=instance)

@receiver(pre_save, sender=EmailEvent)
def track_email_event_changes(sender, instance, **kwargs):
    if instance.pk:
        old_instance= sender.objects.get(pk=instance.pk)
        changes = []
        current_timestamp = datetime.now().isoformat()
        if old_instance.email != instance.email:
            changes.append({
            "field": 'email',
            "old": old_instance.email,
            "new": instance.email,
            "timestamp": current_timestamp
            })
        if old_instance.event_type != instance.event_type:
            changes.append({
                "field": "event_type",
                "old": old_instance.event_type,
                "new": instance.event_type,
                "timestamp": current_timestamp,
            })
        if changes:
            if not isinstance(instance.changes, list):
                instance.changes = []
            instance.changes.extend(changes)
            instance.timestamp = current_timestamp
