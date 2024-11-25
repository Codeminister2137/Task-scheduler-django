import uuid

from django.db import models
from django.core.mail import send_mail

class BaseModel(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    class Meta:
        abstract = True

# Create your models here.
class Email(BaseModel):

    scheduled_for = models.DateTimeField()
    sender = models.EmailField()
    recipient = models.EmailField()
    subject = models.CharField(max_length=255)
    body = models.TextField()
    def __str__(self):
        return self.body
    def event_history(self):
        return self.events.order_by('-timestamp')
    def send_email(self):
        send_mail(subject=self.subject, message=self.body, from_email=self.sender, recipient_list=[self.recipient])

EVENT_TYPES = [
    ("created", "Created"), ("sent", "Sent"), ("rejected", "Rejected"), ("attendance_confirmed", "attendance_confirmed"),
]

class EmailEvent(BaseModel):
    email = models.ForeignKey(Email, on_delete=models.CASCADE, related_name="events")
    timestamp = models.DateTimeField(auto_now_add=True)
    event_type = models.CharField(max_length=20, choices=EVENT_TYPES)
    changes = models.JSONField(null=True, blank=True)

    def __str__(self):
        return f"{self.timestamp}: {self.event_type}"
