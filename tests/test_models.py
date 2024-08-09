from datetime import datetime

from django.test import TestCase

from tasks.models import Notification


class NotificationTest(TestCase):
    def create_notification(
        self,
        id: int = 1,
        scheduled_for: datetime = datetime(2024, 7, 24, 18, 30),
        task_id: int = 1,
    ):
        return Notification.objects.create(
            id=id, scheduled_for=scheduled_for, task_id=task_id
        )

    def test_notification_creation(self):
        # ACT
        example_notification = self.create_notification()
        # ASSERT
        self.assertTrue(isinstance(example_notification, Notification))
        self.assertEqual(example_notification.id, 1)
