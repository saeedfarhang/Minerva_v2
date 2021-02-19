from django.urls import path
from .views import ClipsApiView,ClipDetailApiView

urlpatterns = [
    path("", ClipsApiView.as_view(), name="clips"),
    path("<int:id>/<action>/", ClipDetailApiView.as_view(), name="clip_detail")
]
