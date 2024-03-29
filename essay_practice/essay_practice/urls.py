from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.urls import include, path
from django.views.generic import TemplateView

from essayfeed.views import ReceivedEssaysView
from users.views import UserProfileView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', TemplateView.as_view(template_name='start.html'), name='start'),
    path('', include('essayfeed.urls')),
    path(
        'faq/',
        TemplateView.as_view(template_name='writing/manual.html'),
        name='about'
    ),
    path('profile/', UserProfileView.as_view(), name='profile'),
    path(
        'received-essays/',
        ReceivedEssaysView.as_view(), name='received_essays'),
    path('auth/', include('users.urls')),
    path('writing/', include('writing.urls')),
    path('auth/', include('django.contrib.auth.urls')),
    path('notifications/', include('core.urls'))
]


if settings.DEBUG:
    if settings.MEDIA_ROOT:
        urlpatterns += static(
            settings.MEDIA_URL,
            document_root=settings.MEDIA_ROOT
        )
    urlpatterns += staticfiles_urlpatterns()
