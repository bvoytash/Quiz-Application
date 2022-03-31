from django.test import TestCase
from django.urls import reverse

from explorebg.explore_auth.models import ExploreUser
from explorebg.questions.models import Question, Answer


class EditAnswerViewTest(TestCase):

    def setUp(self):
        test_user1 = ExploreUser.objects.create_user(email='test@mail.bg', password='123')
        test_user1.save()

        test_question = Question.objects.create(text='test_question', user=test_user1)
        answer1 = Answer.objects.create(text='answer1', correct=False, question=test_question)
        answer2 = Answer.objects.create(text='answer2', correct=False, question=test_question)
        answer3 = Answer.objects.create(text='answer3', correct=True, question=test_question)

    def test_redirect_if_not_logged_in(self):
        response = self.client.get(reverse('edit answer', kwargs={'pk': 1}))
        self.assertRedirects(response, '/auth/login/?next=/questions/edit/answer/1')

    def test_logged_in_user_correct_template(self):
        test_user2 = ExploreUser.objects.create_user(email='test2@mail.bg', password='123')
        test_user2.save()

        test_question = Question.objects.create(text='test_question', user=test_user2)
        answer1 = Answer.objects.create(text='answer1', correct=False, question=test_question)
        answer2 = Answer.objects.create(text='answer2', correct=False, question=test_question)
        answer3 = Answer.objects.create(text='answer3', correct=True, question=test_question)

        login = self.client.login(email='test2@mail.bg', password='123')
        response = self.client.get(reverse('edit answer', kwargs={'pk': answer1.id}))

        self.assertEqual(str(response.context['user']), 'test2@mail.bg')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'edit_answer.html')

    def test_edit_successful_anwer_and_redirect_to_my_questions(self):
        test_user2 = ExploreUser.objects.create_user(email='test2@mail.bg', password='123')
        test_user2.save()

        test_question = Question.objects.create(text='test_question', user=test_user2)
        answer1 = Answer.objects.create(text='answer1', correct=False, question=test_question)
        answer2 = Answer.objects.create(text='answer2', correct=False, question=test_question)
        answer3 = Answer.objects.create(text='answer3', correct=True, question=test_question)

        login = self.client.login(email='test2@mail.bg', password='123')
        response = self.client.get(reverse('edit answer', kwargs={'pk': answer1.id}))
        response = self.client.post(f'/questions/edit/answer/{answer1.id}', {
            'text': 'answer1_edited',
        })
        self.assertRedirects(response, '/questions/my-questions/')

    def test_edit_answer_with_blank_field(self):
        test_user2 = ExploreUser.objects.create_user(email='test2@mail.bg', password='123')
        test_user2.save()

        test_question = Question.objects.create(text='test_question', user=test_user2)
        answer1 = Answer.objects.create(text='answer1', correct=False, question=test_question)
        answer2 = Answer.objects.create(text='answer2', correct=False, question=test_question)
        answer3 = Answer.objects.create(text='answer3', correct=True, question=test_question)

        login = self.client.login(email='test@mail.bg', password='123')
        response = self.client.get(reverse('edit answer', kwargs={'pk': answer1.id}))
        response = self.client.post('/questions/edit/1', {})
        self.assertFormError(response, 'form', 'text', 'This field is required.')

    def test_try_edit_answer_which_dont_exist(self):
        test_user2 = ExploreUser.objects.create_user(email='test2@mail.bg', password='123')
        test_user2.save()

        login = self.client.login(email='test2@mail.bg', password='123')
        response = self.client.get(reverse('edit answer', kwargs={'pk': 15}))

        self.assertEqual(str(response.context['user']), 'test2@mail.bg')
        self.assertEqual(response.status_code, 404)
        self.assertTemplateUsed(response, 'error_404.html')
