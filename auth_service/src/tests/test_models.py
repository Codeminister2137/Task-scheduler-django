from django.test import TestCase
from django.contrib.auth import get_user_model


class UserModelTest(TestCase):
    def test_user_can_be_created_with_email(self):
        user = get_user_model().objects.create_user(
            username="scheduler-user",
            email="scheduler@example.com",
            password="strong-test-password",
        )

        self.assertEqual(user.username, "scheduler-user")
        self.assertEqual(user.email, "scheduler@example.com")
        self.assertTrue(user.check_password("strong-test-password"))
