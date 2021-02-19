from django.urls import path
from .views import TagsApiView, CategoriesApiView,CategoryDetailApiView,TagDetailApiView

app_name = 'main'

urlpatterns = [
    path('category/',CategoriesApiView.as_view(), name = 'categories'),
    path('category/<int:id>/<action>/',CategoryDetailApiView.as_view(), name = 'category_detail'),
    path('tags/',TagsApiView.as_view(), name = 'tags'),
    path('tags/<int:id>/',TagDetailApiView.as_view(), name = 'tag_detail'),
]
