from django.contrib import admin
from django.urls import path, include

from main.views import page_404

urlpatterns = [
    path('admin-mode/', admin.site.urls),
    path('', include('main.urls')),
    path('', include('user.urls')),
    path('', include('user_ads.urls')),
    path('', include('mapping_app.urls')),
    path('', include('honeypot.urls')),
    path('404/', page_404, name='404'), # for debag mode test by enter www.site.com/404
]
handler404 = 'main.views.handler404'

from django.conf import settings
from django.conf.urls.static import static
from .settings import DEV_MODE
if DEV_MODE:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


from django.views.static import serve
from django.urls import re_path

urlpatterns += [
    re_path(r'^robots\.txt$', serve, {'document_root': settings.BASE_DIR, 'path': "/robots.txt"}),
]
