from django.conf.urls.static import static
from django.urls import path

from explorebg import settings
from explorebg.design.views import AddDesignView, DesignListView, DeleteDesignView, EditDesignView, like_design

urlpatterns = [
    path('', DesignListView.as_view(), name='design list'),
    path('add/', AddDesignView.as_view(), name='add design'),
    path('delete/<int:pk>', DeleteDesignView.as_view(), name='delete design'),
    path('edit/<int:pk>', EditDesignView.as_view(), name='edit design'),
    path('like/<int:pk>', like_design, name='like design'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
