from django.db import models
from django.contrib.auth import get_user_model
User = get_user_model()

class Category(models.Model):
    title = models.CharField(max_length=20)
    description = models.TextField()
    thumbnail = models.ImageField(upload_to='Categories_thumbnails/%Y/%m/%d', null=True, blank= True)
    def __str__(self):
        return self.title


class Tag(models.Model):
    title = models.CharField(max_length=20)
    def __str__(self):
        return self.title