from django.test import TestCase
from django.urls import reverse

from explorebg.explore_auth.models import ExploreUser


class CreateQuestionTest(TestCase):

    def setUp(self):
        test_user1 = ExploreUser.objects.create_user(email='test@mail.bg', password='123')
        test_user1.save()

    def test_get_redirect_with_no_loggen_user(self):
        response = self.client.get(reverse('create question'))
        self.assertRedirects(response, '/auth/login/?next=%2Fquestions%2Fcreate%2F')

    def test_get_correct_template_with_logged_user(self):
        login = self.client.login(email='test@mail.bg', password='123')
        response = self.client.get(reverse('create question'))
        self.assertEqual(str(response.context['user']), 'test@mail.bg')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'create_question.html')

    def test_try_to_create_question_with_some_blank_fields_form(self):
        login = self.client.login(email='test@mail.bg', password='123')
        response = self.client.get(reverse('create question'))

        response = self.client.post('/questions/create/', {})
        self.assertFormError(response, 'form', 'question_text', 'This field is required.')
        self.assertFormError(response, 'form', 'second_answer', 'This field is required.')
        self.assertFormError(response, 'form', 'first_answer', 'This field is required.')
        self.assertFormError(response, 'form', 'correct_answer', 'This field is required.')

    def test_create_question_success_and_redirect(self):
        login = self.client.login(email='test@mail.bg', password='123')
        response = self.client.get(reverse('create question'))
        response = self.client.post('/questions/create/', {
            'question_text': 'test_question',
            'first_answer': 'test_first_answer',
            'second_answer': 'test_second_answer',
            'correct_answer': 'test_correct_answer',
        })
        self.assertRedirects(response, '/questions/my-questions/')
