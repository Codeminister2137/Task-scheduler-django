from django.test import TestCase
from datetime import datetime
from email_service.src.email_app.tasks import send_email
from email_service.src.email_app.models import Email, EmailEvent
from email_service.src.email_app.Enums import EventType


# Create your tests here.

class TestEmail(TestCase):

    def setUp(self):
        self.example_email = Email.objects.create(scheduled_for=datetime.now().isoformat(),
                                             sender="kubajaworski+test1@wp.pl", recipient='kuba2@wp.pl',
                                             subject='Testing email', content='Testing email')
    def tearDown(self):
        self.example_email.delete()

    def test_creating_email(self):
        assert self.example_email.subject == "Testing email"

    def test_creating_event(self):
        assert EmailEvent.objects.filter(email=self.example_email).exists()

    def test_sending_emails(self):
        self.example_email.send_email()
        assert EmailEvent.objects.filter(event_type=EventType.SENT).exists()


