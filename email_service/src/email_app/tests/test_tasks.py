from unittest.mock import patch

from django.test import TestCase
from django.utils import timezone

from email_app.Enums import EventType
from email_app.models import Email, EmailEvent
from email_app.tasks import send_email


class SendEmailTaskTest(TestCase):
    def test_send_email_sends_created_events_and_marks_them_sent(self):
        email = Email.objects.create(
            scheduled_for=timezone.now(),
            sender="sender@example.com",
            recipient="recipient@example.com",
            subject="Reminder",
            body="Task reminder",
        )
        created_event = email.events.get()
        EmailEvent.objects.create(email=email, event_type=EventType.SENT)

        with patch.object(Email, "send_email") as send_email_mock:
            send_email()

        send_email_mock.assert_called_once_with()
        created_event.refresh_from_db()
        self.assertEqual(created_event.event_type, EventType.SENT)
        self.assertEqual(
            EmailEvent.objects.filter(event_type=EventType.SENT).count(),
            2,
        )
