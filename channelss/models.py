from django.db import models

from django.db import models

class ChatRoom(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.name
