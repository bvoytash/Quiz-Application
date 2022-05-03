from django.test import TestCase
from django.urls import reverse, reverse_lazy

from explorebg.explore_auth.models import ExploreUser
from explorebg.questions.models import Question, Answer


class StartQuizTest(TestCase):

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
        response = self.client.get(reverse('start quiz'))
        self.assertRedirects(response, '/auth/login/?next=/questions/start/')

    def test_logged_in_user_correct_template(self):
        login = self.client.login(email='test@mail.bg', password='123')
        response = self.client.get(reverse('start quiz'))

        self.assertEqual(str(response.context['user']), 'test@mail.bg')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'quiz/start_quiz.html')

    def test_count_of_questions_while_start_quiz(self):
        test_user2 = ExploreUser.objects.create_user(email='test2@mail.bg', password='123')
        test_user2.save()

        login = self.client.login(email='test2@mail.bg', password='123')
        response = self.client.post(reverse('start quiz'))
        self.assertTemplateUsed(response, 'quiz/play_quiz.html')
        self.assertEqual(len(response.context['questions']), 2)