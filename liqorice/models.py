from uuid import uuid4
from django.db import models
from django.utils import timezone

def generateUUID():
    return str(uuid4())

# Create your models here.
class Comment(models.Model):
    id = models.CharField(default=generateUUID, max_length=36, primary_key=True, editable=False)
    author = models.CharField(max_length=200)
    post_date = models.DateTimeField(default=timezone.now)
    content = models.TextField()

    def __str__(self):
        return self.content
