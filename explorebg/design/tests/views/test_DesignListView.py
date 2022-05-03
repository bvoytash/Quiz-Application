from django.test import TestCase
from django.urls import reverse

from explorebg.design.models import Design
from explorebg.explore_auth.models import ExploreUser


class DesignListViewTest(TestCase):

    def setUp(self):
        test_user1 = ExploreUser.objects.create_superuser(email='test@mail.bg', password='123')
        test_user1.save()

        test_design = Design.objects.create(name='test_question')

    def test_redirect_if_not_logged_in(self):
        response = self.client.get(reverse('design list'))
        self.assertRedirects(response, '/auth/login/?next=/design/')

    def test_logged_in_user_correct_template(self):
        login = self.client.login(email='test@mail.bg', password='123')
        response = self.client.get(reverse('design list'))

        self.assertEqual(str(response.context['user']), 'test@mail.bg')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'design/design_list.html')

    def test_logged_user_count_of_designs(self):
        login = self.client.login(email='test@mail.bg', password='123')
        response = self.client.get(reverse('design list'))
        self.assertEqual(len(Design.objects.all()), 1)

    def test_logged_user_do_not_have_questions(self):
        login = self.client.login(username='test@mail.bg', password='123')
        response = self.client.get(reverse('design list'))
        for design in Design.objects.all():
            design.delete()

        self.assertEqual(len(Design.objects.all()), 0)

