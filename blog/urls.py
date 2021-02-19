from django.urls import path
from .views import BlogApiView,BlogDetailApiView
urlpatterns = [
    path('',BlogApiView.as_view(),name="blogs"),
    path("<int:id>/<action>/", BlogDetailApiView.as_view(), name="blog_detail"),
]
