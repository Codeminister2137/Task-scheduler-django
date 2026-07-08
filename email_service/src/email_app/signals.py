from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from django.utils import timezone

from .models import Email, EmailEvent


@receiver(post_save, sender=Email)
def create_email_event(instance, created, **kwargs):
    if not created:
        return
    EmailEvent.objects.create(email=instance)


@receiver(pre_save, sender=EmailEvent)
def track_email_event_changes(sender, instance, **kwargs):
    if instance._state.adding:
        return

    old_instance = sender.objects.get(pk=instance.pk)
    changes = []
    current_timestamp = timezone.now()
    if old_instance.email != instance.email:
        changes.append(
            {
                "field": "email",
                "old": str(old_instance.email_id),
                "new": str(instance.email_id),
                "timestamp": current_timestamp.isoformat(),
            }
        )
    if old_instance.event_type != instance.event_type:
        changes.append(
            {
                "field": "event_type",
                "old": old_instance.event_type,
                "new": instance.event_type,
                "timestamp": current_timestamp.isoformat(),
            }
        )
    if changes:
        if not isinstance(instance.changes, list):
            instance.changes = []
        instance.changes.extend(changes)
        instance.timestamp = current_timestamp
