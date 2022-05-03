from django.test import TestCase
from django.urls import reverse


class HomePageViewTest(TestCase):

    def test_uses_correct_template(self):
        response = self.client.get(reverse('home'))
        # Check we used correct template
        self.assertTemplateUsed(response, 'home/home.html')