from django.contrib import admin
from django.urls import path, include, re_path
from django.conf import settings
from django.conf.urls.static import static
from frontend.views import index

urlpatterns = [
    path('', include('frontend.urls')),
    path('api/', include('main.urls')),
    path('api/accounts/', include('accounts.urls')),
    path('api/courses/', include('courses.urls')),
    path('api/blog/', include('blog.urls')),
    path('api/clips/', include('clips.urls')),
    path('admin/', admin.site.urls),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

urlpatterns += [re_path('.*/', index, name='index')]