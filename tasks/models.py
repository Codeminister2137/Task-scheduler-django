from django.db import models


# Create your models here.
class Notification(models.Model):
    scheduled_for = models.DateTimeField()
    task_id = models.IntegerField()
