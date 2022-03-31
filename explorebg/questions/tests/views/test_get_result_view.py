from django.test import TestCase
from django.urls import reverse

from explorebg.explore_auth.models import ExploreUser
from explorebg.questions.models import Question, Answer


class GetResultTest(TestCase):

    def setUp(self):
        test_user1 = ExploreUser.objects.create_user(email='test@mail.bg', password='123')
        test_user1.save()

        test_question = Question.objects.create(text='test_question', user=test_user1)
        answer1 = Answer.objects.create(text='answer1', correct=False, question=test_question)
        answer2 = Answer.objects.create(text='answer2', correct=False, question=test_question)
        answer3 = Answer.objects.create(text='answer3', correct=True, question=test_question)

        test_question2 = Question.objects.create(text='test_question2', user=test_user1)
        answer1 = Answer.objects.create(text='answer1', correct=False, question=test_question2)
        answer2 = Answer.objects.create(text='answer2', correct=False, question=test_question2)
        answer3 = Answer.objects.create(text='answer3', correct=True, question=test_question2)

    def test_redirect_if_not_logged_in(self):
        response = self.client.get(reverse('get result'))
        self.assertRedirects(response, '/auth/login/?next=/questions/get-result/')

    def test_logged_in_user_get_result_correct_template_and_context(self):
        login = self.client.login(email='test@mail.bg', password='123')
        response = self.client.post(reverse('get result'))

        self.assertEqual(str(response.context['user']), 'test@mail.bg')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'finish_quiz.html')
        self.assertEqual(response.context['correct_answers'], 0)
