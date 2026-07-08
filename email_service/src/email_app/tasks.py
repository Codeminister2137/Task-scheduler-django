from celery import shared_task
from django.utils import timezone

from .Enums import EventType
from .models import EmailEvent


@shared_task
def send_email():
    events = EmailEvent.objects.select_related("email").filter(
        event_type=EventType.CREATED
    )

    for event in events:
        event.email.send_email()

    events.update(event_type=EventType.SENT, timestamp=timezone.now())
