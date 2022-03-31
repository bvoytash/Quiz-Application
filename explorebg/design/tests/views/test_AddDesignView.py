from django.test import TestCase
from django.urls import reverse, reverse_lazy

from explorebg.design.models import Design
from explorebg.explore_auth.models import ExploreUser
from django.contrib.auth.models import Permission


class AddDesignTest(TestCase):
    def setUp(self):
        test_user1 = ExploreUser.objects.create_user(email='test@mail.bg', password='123')
        test_user1.save()

        test_user2 = ExploreUser.objects.create_superuser(email='test2@mail.bg', password='123')
        test_user2.save()

    def test_forbidden_if_logged_in_but_not_correct_permission(self):
        login = self.client.login(username='test@mail.bg', password='123')
        response = self.client.get(reverse('add design'))
        self.assertEqual(response.status_code, 403)

    def test_user_get_url_with_correct_permission(self):
        login = self.client.login(username='test2@mail.bg', password='123')
        response = self.client.get(reverse('add design'))
        self.assertEqual(response.status_code, 200)


