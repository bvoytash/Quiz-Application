from django.urls import path
from django.contrib.auth import views as auth_views
from explorebg.explore_auth.views import RegisterView, LoginUserView, LogoutView

urlpatterns = [
    path('register/', RegisterView.as_view(), name='sign up'),
    path('login/', LoginUserView.as_view(), name='sign in'),
    path('sign-out/', LogoutView.as_view(), name='sign out'),

    path('reset_password/', auth_views.PasswordResetView.as_view(template_name='auth/password-reset.html'), name='reset_password'),
    path('reset_password_sent/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset_password/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset_password_complete/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),

]