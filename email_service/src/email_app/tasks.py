from datetime import datetime

from django_celery_beat.models import IntervalSchedule, PeriodicTask

from .models import Email, EmailEvent

schedule, created = IntervalSchedule.objects.get_or_create(
    every=1, period=IntervalSchedule.MINUTES
)

PeriodicTask.objects.create(
    interval=schedule,
    task="email_app.tasks.send_email",
)


def send_email():
    events = EmailEvent.objects.filter(event_type="created")
    for event in events:
        Email.objects.get(event.email).send_email()
    events.update(event_type="sent", timestamp=datetime.now())
