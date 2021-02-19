from django.db import models
from main.models import Category,Tag
from django.contrib.auth import get_user_model
User = get_user_model()

class Clip(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    clip = models.FileField(upload_to="clips/%Y/%m/%d", blank=True)
    title = models.CharField(max_length=100)
    description = models.TextField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='clip_category')
    tags = models.ManyToManyField(Tag, related_name='clip_tags')
    date_added = models.DateTimeField(auto_now_add=True)
    is_published = models.BooleanField(default = True)


