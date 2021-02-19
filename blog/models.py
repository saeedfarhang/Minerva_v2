from django.db import models
from django.conf import settings
from main.models import Category,Tag

class Blog(models.Model):
    category = models.ForeignKey(Category, related_name='blog_category', on_delete=models.PROTECT, default=2)
    tags = models.ManyToManyField(Tag, related_name='blog_tags')
    title=models.CharField(max_length=100)
    tumbbnail = models.ImageField(upload_to='blog_thumbnail/%Y/%m/%d',blank=True, null=True)
    body = models.TextField()
    is_published = models.BooleanField(default = True)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name='blog_author')
    date_added = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(null=True)


# add video link and course link and blog link to a blog object