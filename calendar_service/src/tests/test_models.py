# from email_service.src.email_app.models import Email
#
#
#
# class EmailTest(TestCase):
#     def setUp(self):
#         test_tz_time = timezone.now()
#         Email.objects.create(id=1, created_at=test_tz_time - timedelta(hours=1), scheduled_for=test_tz_time, sender='<EMAIL>', recipient='<EMAIL>', subject='Test Email', body='Test Email' )
#
#     def test_email_creation(self):
#         # ACT
#         example_email = Email.objects.get(id=1)
#         # ASSERT
#         self.assertTrue(isinstance(example_email, Email))
#         self.assertEqual(example_email.id, 1)
#         self.assertTrue(timezone.is_aware(example_email.scheduled_for))
