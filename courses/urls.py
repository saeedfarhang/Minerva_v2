from django.urls import path
from .views import CourseApiView,CourseDetailApiView,LessonsApiView,LessonDetailApiView

urlpatterns = [
    path("", CourseApiView.as_view(), name="courses"),
    path("<course_id>/lessons/", LessonsApiView.as_view(), name='lessons'),
    path("<int:course_id>/lesson/<int:lesson_id>/<action>/", LessonDetailApiView.as_view(), name='lesson_detail'),
    path("<int:id>/<action>/", CourseDetailApiView.as_view(), name="course_detail"),
]
