from django.contrib import admin
from django.urls import path, include

from explorebg.home import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('explorebg.home.urls')),
    path('questions/', include('explorebg.questions.urls')),
    path('auth/', include('explorebg.explore_auth.urls')),
    path('design/', include('explorebg.design.urls')),
]

handler404 = views.handler404
handler500 = views.handler500
