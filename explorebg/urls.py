from django.contrib import admin
from django.urls import path, include

from explorebg.home import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('explorebg.home.urls')),
    path('questions/', include('explorebg.questions.urls')),
    path('auth/', include('explorebg.explore_auth.urls')),
    path('design/', include('explorebg.design.urls')),
] + static(settings.STATIC_URL, document_root=settings.STATICFILES_DIRS[0])

handler404 = views.handler404
handler500 = views.handler500
