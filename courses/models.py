from django.db import models
from django.conf import settings
from main.models import Category,Tag

class Course(models.Model):
    item_type = models.CharField(default='course', editable=False,max_length=50)
    master = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT)
    title = models.CharField(max_length=100)
    description = models.TextField()
    thumbnail = models.ImageField(upload_to='course_thumbnails/%Y/%m/%d', null=True, blank= True)
    price = models.IntegerField(null =True,blank=True)
    date_added = models.DateTimeField(auto_now_add=True)
    selected = models.BooleanField(default=False)
    published = models.BooleanField(default=False)
    updated_date = models.DateTimeField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE, default=1)
    tags = models.ManyToManyField(Tag, related_name='Course_tags', blank=True)


    def __str__(self):
        return self.title

class Lesson(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    master = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT)
    video = models.FileField(blank=True)
    title = models.CharField(max_length = 100)
    description = models.TextField()
    date_added = models.DateTimeField(auto_now_add=True)
    tags = models.ManyToManyField(Tag, related_name='lesson_tags', blank=True)

    def __str__(self):
        return self.title