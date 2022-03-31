from django.test import TestCase
from django.urls import reverse

from explorebg.explore_auth.models import ExploreUser
from explorebg.questions.models import Question, Answer


class MyQuestionsListViewTest(TestCase):
    def setUp(self):
        test_user1 = ExploreUser.objects.create_user(email='test@mail.bg', password='123')
        test_user1.save()

        test_question = Question.objects.create(text='test_question', user=test_user1)
        answer1 = Answer.objects.create(text='answer1', correct=False, question=test_question)
        answer2 = Answer.objects.create(text='answer2', correct=False, question=test_question)
        answer3 = Answer.objects.create(text='answer3', correct=True, question=test_question)

    def test_redirect_if_not_logged_in(self):
        response = self.client.get(reverse('my questions'))
        self.assertRedirects(response, '/auth/login/?next=/questions/my-questions/')

    def test_logged_in_user_correct_template(self):
        login = self.client.login(email='test@mail.bg', password='123')
        response = self.client.get(reverse('my questions'))

        self.assertEqual(str(response.context['user']), 'test@mail.bg')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'my_questions.html')

    def test_logged_user_count_of_questions(self):
        test_user2 = ExploreUser.objects.create_user(email='test2@mail.bg', password='123')
        test_user2.save()

        test_question = Question.objects.create(text='test_question', user=test_user2)
        answer1 = Answer.objects.create(text='answer1', correct=False, question=test_question)
        answer2 = Answer.objects.create(text='answer2', correct=False, question=test_question)
        answer3 = Answer.objects.create(text='answer3', correct=True, question=test_question)

        login = self.client.login(email='test2@mail.bg', password='123')
        response = self.client.get(reverse('my questions'))

        self.assertEqual(len(Question.objects.filter(user=test_user2)), 1)

    def test_logged_user_do_not_have_questions(self):
        test_user2 = ExploreUser.objects.create_user(email='test2@mail.bg', password='123')
        test_user2.save()

        test_question = Question.objects.create(text='test_question', user=test_user2)
        answer1 = Answer.objects.create(text='answer1', correct=False, question=test_question)
        answer2 = Answer.objects.create(text='answer2', correct=False, question=test_question)
        answer3 = Answer.objects.create(text='answer3', correct=True, question=test_question)

        login = self.client.login(email='test2@mail.bg', password='123')
        response = self.client.get(reverse('my questions'))

        for q in Question.objects.filter(user=test_user2):
            q.delete()

        self.assertEqual(len(Question.objects.filter(user=test_user2)), 0)
