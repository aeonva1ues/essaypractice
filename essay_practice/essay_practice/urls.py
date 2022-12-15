from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.urls import include, path


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('essayfeed.urls')),
    path('auth/', include('users.urls')),
    path('writing/', include('writing.urls')),
    path('auth/', include('django.contrib.auth.urls')),
]


if settings.DEBUG:
    if settings.MEDIA_ROOT:
        urlpatterns += static(
            settings.MEDIA_URL,
            document_root=settings.MEDIA_ROOT
        )
    urlpatterns += staticfiles_urlpatterns()
