from django.contrib.auth import login, logout
from django.contrib.auth.views import LoginView, PasswordResetView
from django.shortcuts import redirect
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import CreateView

from explorebg.explore_auth.forms import SignUpForm, SignInForm


class RegisterView(CreateView):
    form_class = SignUpForm
    template_name = 'auth/sign_up.html'
    success_url = reverse_lazy('home')

    def form_valid(self, form):
        result = super().form_valid(form)
        login(self.request, self.object)
        return result


class LoginUserView(LoginView):
    template_name = 'auth/sign_in.html'
    authentication_form = SignInForm
    success_url = reverse_lazy('home')

    def form_invalid(self, form):
        print("Form is invalid")
        print(form.errors)
        return super().form_invalid(form)


class LogoutView(View):
    def get(self, request):
        logout(request)
        return redirect('home')
