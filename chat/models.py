from django.db import models
from django.utils import timezone


class Room(models.Model):
    name = models.TextField()
    label = models.SlugField(unique=True)


class Message(models.Model):
    room = models.ForeignKey(Room)
    handle = models.TextField()
    message = models.TextField()
    timestamp = models.DateTimeField(default=timezone.now, db_index=True)

    @property
    def formatted_timestamp(self):
        return self.timestamp.strftime('%b %-d %-I:%M %p')

    def as_dict(self):
        return {
            'handle': self.handle,
            'message': self.message,
            'timestamp': self.formatted_timestamp,
        }
