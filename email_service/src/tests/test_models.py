from django.test import TestCase
from django.utils import timezone

from ..email_app.models import email


class EmailTest(TestCase):
    def setUp(self):
        test_tz_time = timezone.now()
        Email.objects.create(id=1, scheduled_for=test_tz_time, task_id=1)

    def test_notification_creation(self):
        # ACT
        example_notification = Notification.objects.get(id=1)
        # ASSERT
        self.assertTrue(isinstance(example_notification, Notification))
        self.assertEqual(example_notification.id, 1)
        self.assertTrue(timezone.is_aware(example_notification.scheduled_for))
