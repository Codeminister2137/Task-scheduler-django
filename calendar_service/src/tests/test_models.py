from django.test import TestCase
from django.utils import timezone

from calendar_app.models import Notification


class NotificationModelTest(TestCase):
    def test_notification_creation_preserves_schedule_and_task(self):
        scheduled_for = timezone.now()

        notification = Notification.objects.create(
            scheduled_for=scheduled_for,
            task_id=42,
        )

        self.assertIsNotNone(notification.id)
        self.assertEqual(notification.scheduled_for, scheduled_for)
        self.assertEqual(notification.task_id, 42)
        self.assertTrue(timezone.is_aware(notification.scheduled_for))
