from django.test import TestCase
from django.urls import reverse, reverse_lazy

from explorebg.explore_auth.models import ExploreUser
from explorebg.questions.models import Question, Answer


class DeleteQuestionViewTest(TestCase):

    def setUp(self):
        test_user1 = ExploreUser.objects.create_user(email='test@mail.bg', password='123')
        test_user1.save()

        test_question = Question.objects.create(text='test_question', user=test_user1)
        answer1 = Answer.objects.create(text='answer1', correct=False, question=test_question)
        answer2 = Answer.objects.create(text='answer2', correct=False, question=test_question)
        answer3 = Answer.objects.create(text='answer3', correct=True, question=test_question)

    def test_redirect_if_not_logged_in(self):
        response = self.client.get(reverse('delete question', kwargs={'pk': 3}))
        self.assertRedirects(response, '/auth/login/?next=/questions/delete/3')

    def test_logged_in_user_correct_template(self):
        test_user2 = ExploreUser.objects.create_user(email='test2@mail.bg', password='123')
        test_user2.save()

        test_question = Question.objects.create(text='test_question', user=test_user2)
        answer1 = Answer.objects.create(text='answer1', correct=False, question=test_question)
        answer2 = Answer.objects.create(text='answer2', correct=False, question=test_question)
        answer3 = Answer.objects.create(text='answer3', correct=True, question=test_question)

        login = self.client.login(email='test2@mail.bg', password='123')
        response = self.client.get(reverse('delete question', kwargs={'pk': test_question.id}))

        self.assertEqual(str(response.context['user']), 'test2@mail.bg')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'questions/delete-question.html')

    def test_delete_question_successful_and_redirect_to_my_questions(self):
        test_user2 = ExploreUser.objects.create_user(email='test2@mail.bg', password='123')
        test_user2.save()

        test_question = Question.objects.create(text='test_question', user=test_user2)
        answer1 = Answer.objects.create(text='answer1', correct=False, question=test_question)
        answer2 = Answer.objects.create(text='answer2', correct=False, question=test_question)
        answer3 = Answer.objects.create(text='answer3', correct=True, question=test_question)

        login = self.client.login(email='test2@mail.bg', password='123')
        response = self.client.get(reverse('delete question', kwargs={'pk': test_question.id}))
        response = self.client.post(f'/questions/delete/{test_question.id}')
        self.assertRedirects(response, '/questions/my-questions/')

    def test_try_delete_question_which_dont_exist(self):
        test_user2 = ExploreUser.objects.create_user(email='test2@mail.bg', password='123')
        test_user2.save()

        login = self.client.login(email='test2@mail.bg', password='123')
        response = self.client.get(reverse('delete question', kwargs={'pk': 15}))

        self.assertEqual(str(response.context['user']), 'test2@mail.bg')
        self.assertEqual(response.status_code, 404)
        self.assertTemplateUsed(response, 'error_404.html')