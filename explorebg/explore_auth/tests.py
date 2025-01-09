from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model

UserModel = get_user_model()  # Custom user model

class RegisterViewTests(TestCase):
    def test_register_view_valid_post_creates_user(self):
        response = self.client.post(reverse('sign up'), {
            'email': 'test@example.com',
            'password1': 'ComplexPass123',
            'password2': 'ComplexPass123',
        })
        self.assertEqual(response.status_code, 302)  # Should redirect to 'home'
        self.assertTrue(UserModel.objects.filter(email='test@example.com').exists())

    def test_register_view_invalid_post(self):
        # Password mismatch
        response = self.client.post(reverse('sign up'), {
            'email': 'test@example.com',
            'password1': 'ComplexPass123',
            'password2': 'DifferentPass123',
        })
        self.assertEqual(response.status_code, 200)  # Should re-render the registration page
        self.assertFalse(UserModel.objects.filter(email='test@example.com').exists())


class LoginUserViewTests(TestCase):
    def setUp(self):
        self.user = UserModel.objects.create_user(
            email='test@example.com',
            password='ComplexPass123',
        )

    def test_login_view_renders_correct_template(self):
        response = self.client.get(reverse('sign in'))  # Replace 'sign in' with the actual URL name
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'auth/sign_in.html')

    def test_login_view_valid_credentials(self):
        # Get the CSRF token
        response = self.client.get(reverse('sign in'))
        csrf_token = response.cookies['csrftoken'].value

        # Post the login form with the CSRF token
        response = self.client.post(reverse('sign in'), {
            'username': 'test@example.com',  # Use 'username' as the field name
            'password': 'ComplexPass123',
            'csrfmiddlewaretoken': csrf_token,
        })
        self.assertEqual(response.status_code, 302)  # Should redirect to 'home'
        self.assertRedirects(response, reverse('home'))

    def test_login_view_invalid_credentials(self):
        # Get the CSRF token
        response = self.client.get(reverse('sign in'))
        csrf_token = response.cookies['csrftoken'].value

        # Post the login form with invalid credentials and the CSRF token
        response = self.client.post(reverse('sign in'), {
            'username': 'test@example.com',  # Use 'username' as the field name
            'password': 'WrongPass123',
            'csrfmiddlewaretoken': csrf_token,
        })
        if response.context:
            print(response.context['form'].errors)  # Debugging: Print form errors
        else:
            print("No context returned in response.")
        self.assertEqual(response.status_code, 200)  # Should re-render the login page
        self.assertIn('form', response.context)
        self.assertTrue(response.context['form'].errors)

class LogoutViewTests(TestCase):
    def setUp(self):
        self.user = UserModel.objects.create_user(
            email='test@example.com',
            password='ComplexPass123',
        )
        self.client.login(email='test@example.com', password='ComplexPass123')

    def test_logout_view_logs_out_user(self):
        response = self.client.get(reverse('sign out'))  # Replace 'sign out' with the actual URL name for LogoutView
        self.assertEqual(response.status_code, 302)  # Should redirect to 'home'
        self.assertNotIn('_auth_user_id', self.client.session)