from django.contrib import admin
from .models import Course,Lesson

class CourseAdmin(admin.ModelAdmin):
    pass

admin.site.register(Course, CourseAdmin)

class LessonAdmin(admin.ModelAdmin):
    pass

admin.site.register(Lesson, LessonAdmin)