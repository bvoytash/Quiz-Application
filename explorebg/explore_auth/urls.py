from django.urls import path

from explorebg.explore_auth.views import RegisterView, LoginUserView, LogoutView

urlpatterns = [
    path('register/', RegisterView.as_view(), name='sign up'),
    path('login/', LoginUserView.as_view(), name='sign in'),
    path('sign-out/', LogoutView.as_view(), name='sign out')
]