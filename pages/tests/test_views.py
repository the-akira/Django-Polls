from django.test import TestCase
from django.urls import reverse

class ViewsTestCase(TestCase):
    def test_index_loads_properly(self):
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)

    def test_url_available_by_name(self):  
        response = self.client.get(reverse('index'))
        self.assertEqual(response.status_code, 200)

    def test_template_index_correct(self):  
        response = self.client.get(reverse('index'))
        self.assertTemplateUsed(response, 'pages/index.html')

    def test_template_content(self):
        response = self.client.get(reverse('index'))
        self.assertContains(response, '<div class="ui menu">')
        self.assertNotContains(response, 'Not on the page')