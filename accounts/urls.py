from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView,TokenRefreshView
from .views import SignupView, UserView

urlpatterns = [
    path('token/', TokenObtainPairView.as_view(), name='access_token'),
    path('token/refresh/', TokenRefreshView.as_view(), name='refresh_token'),
    path('signup/', SignupView.as_view(), name='signup'),
    path('', UserView.as_view(), name='user')
]
