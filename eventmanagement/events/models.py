from django.db import models
from eventusers.models import CustomUsers 

# Create your models here.

class Event(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    date = models.DateTimeField()
    location = models.CharField(max_length=200)
    owner = models.OneToOneField(CustomUsers, on_delete=models.CASCADE, related_name='event')
    attendees = models.ManyToManyField(CustomUsers, related_name='attending_events')

    def __str__(self):
        return self.title