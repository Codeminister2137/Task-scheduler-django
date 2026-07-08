from unittest.mock import patch

from django.test import TestCase
from django.utils import timezone

from email_app.Enums import EventType
from email_app.models import Email, EmailEvent


class EmailModelTest(TestCase):
    def setUp(self):
        self.example_email = Email.objects.create(
            scheduled_for=timezone.now(),
            sender="kubajaworski+test1@wp.pl",
            recipient="kuba2@wp.pl",
            subject="Testing email",
            body="Testing email",
        )

    def test_email_creation(self):
        self.assertEqual(self.example_email.subject, "Testing email")
        self.assertEqual(str(self.example_email), "Testing email")
        self.assertTrue(timezone.is_aware(self.example_email.scheduled_for))

    def test_creating_email_records_created_event(self):
        event = EmailEvent.objects.get(email=self.example_email)

        self.assertEqual(event.event_type, EventType.CREATED)
        self.assertIsNone(event.changes)

    def test_updating_email_does_not_create_duplicate_created_event(self):
        self.example_email.subject = "Updated subject"
        self.example_email.save()

        self.assertEqual(self.example_email.events.count(), 1)

    def test_event_history_returns_newest_events_first(self):
        first_event = self.example_email.events.get()
        second_event = EmailEvent.objects.create(
            email=self.example_email,
            event_type=EventType.SENT,
        )

        self.assertEqual(
            list(self.example_email.event_history()),
            [second_event, first_event],
        )

    @patch("email_app.models.send_mail")
    def test_send_email_uses_email_fields(self, send_mail_mock):
        self.example_email.send_email()

        send_mail_mock.assert_called_once_with(
            subject="Testing email",
            message="Testing email",
            from_email="kubajaworski+test1@wp.pl",
            recipient_list=["kuba2@wp.pl"],
        )

    def test_event_change_tracking_appends_changed_fields(self):
        event = self.example_email.events.get()

        event.event_type = EventType.SENT
        event.save()

        event.refresh_from_db()
        self.assertEqual(event.changes[0]["field"], "event_type")
        self.assertEqual(event.changes[0]["old"], EventType.CREATED)
        self.assertEqual(event.changes[0]["new"], EventType.SENT)

    def test_event_string_includes_timestamp_and_type(self):
        event = self.example_email.events.get()

        self.assertEqual(str(event), f"{event.timestamp}: {event.event_type}")

    def test_event_change_tracking_records_email_change(self):
        event = self.example_email.events.get()
        new_email = Email.objects.create(
            scheduled_for=timezone.now(),
            sender="another-sender@example.com",
            recipient="another-recipient@example.com",
            subject="Another email",
            body="Another body",
        )

        event.email = new_email
        event.save()

        event.refresh_from_db()
        self.assertEqual(event.changes[0]["field"], "email")
        self.assertEqual(event.changes[0]["old"], str(self.example_email.id))
        self.assertEqual(event.changes[0]["new"], str(new_email.id))
