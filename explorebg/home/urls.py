from django.urls import path

from explorebg.home.views import HomePageView, CauseView


urlpatterns = [
    path('', HomePageView.as_view(), name='home'),
    path('cause/', CauseView.as_view(), name='cause'),
]
