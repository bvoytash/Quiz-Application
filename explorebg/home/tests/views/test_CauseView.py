from django.test import TestCase
from django.urls import reverse


class CauseViewTest(TestCase):

    def test_uses_correct_template(self):
        response = self.client.get(reverse('cause'))
        # Check we used correct template
        self.assertTemplateUsed(response, 'home/cause.html')