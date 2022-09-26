from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.test import TestCase
from django.urls import reverse

class RegisterViewTestCase(TestCase):
    def test_register_loads_properly(self):
        response = self.client.get('/accounts/register/')
        self.assertEqual(response.status_code, 200)

    def test_url_available_by_name(self):  
        response = self.client.get(reverse('accounts:register'))
        self.assertEqual(response.status_code, 200)

    def test_template_register_correct(self):  
        response = self.client.get(reverse('accounts:register'))
        self.assertTemplateUsed(response, 'accounts/register.html')

    def test_template_content(self):
        response = self.client.get(reverse('accounts:register'))
        self.assertContains(response, '<h1 class="ui header">Register</h1>')
        self.assertNotContains(response, 'Not on the page')

class LoginViewTestCase(TestCase):
    def test_login_loads_properly(self):
        response = self.client.get('/accounts/login/')
        self.assertEqual(response.status_code, 200)

    def test_url_available_by_name(self):  
        response = self.client.get(reverse('accounts:login'))
        self.assertEqual(response.status_code, 200)

    def test_template_login_correct(self):  
        response = self.client.get(reverse('accounts:login'))
        self.assertTemplateUsed(response, 'accounts/login.html')

    def test_template_content(self):
        response = self.client.get(reverse('accounts:login'))
        self.assertContains(response, '<h1 class="ui header">Login</h1>')
        self.assertNotContains(response, 'Not on the page')

class ProfileViewTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        user = User.objects.create_user(
            username='Test',
            first_name='Test',
            last_name='Test',
            email='test@test.com',
            password='test',
        )

    def test_profile_loads_properly(self):
        self.client.login(username='Test', password='test') 
        response = self.client.get('/accounts/profile/')
        self.assertEqual(response.status_code, 200)

    def test_url_available_by_name(self):  
        self.client.login(username='Test', password='test') 
        response = self.client.get(reverse('accounts:profile'))
        self.assertEqual(response.status_code, 200)

    def test_template_profile_correct(self):  
        self.client.login(username='Test', password='test') 
        response = self.client.get(reverse('accounts:profile'))
        self.assertTemplateUsed(response, 'accounts/profile.html')

    def test_template_content(self):
        self.client.login(username='Test', password='test') 
        response = self.client.get(reverse('accounts:profile'))
        self.assertContains(response, '<h1 class="ui header">Profile of')
        self.assertNotContains(response, 'Not on the page')

class LogoutViewTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        user = User.objects.create_user(
            username='Test',
            first_name='Test',
            last_name='Test',
            email='test@test.com',
            password='test',
        )

    def test_logout_loads_properly(self):
        self.client.login(username='Test', password='test') 
        response = self.client.get('/accounts/logout/')
        self.assertEqual(response.status_code, 302)

    def test_url_available_by_name(self):  
        self.client.login(username='Test', password='test') 
        response = self.client.get(reverse('accounts:logout'))
        self.assertEqual(response.status_code, 302)

class SignInTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        user = User.objects.create_user(
            username='Test',
            first_name='Test',
            last_name='Test',
            email='test@test.com',
            password='test',
        )

    def test_correct(self):
        user = authenticate(username='Test', password='test')
        self.assertTrue((user is not None) and user.is_authenticated)

    def test_wrong_username(self):
        user = authenticate(username='wrong', password='test')
        self.assertFalse(user is not None and user.is_authenticated)

    def test_wrong_password(self):
        user = authenticate(username='Test', password='wrong')
        self.assertFalse(user is not None and user.is_authenticated)

class UpdateUserTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        user = User.objects.create_user(
            username='Test',
            first_name='Test',
            last_name='Test',
            email='test@test.com',
            password='test',
        )

    def test_update_username(self):
        user = User.objects.get(id=1)
        user.username = 'Testing'
        user.save()
        self.assertEqual(user.username, 'Testing')

    def test_update_email(self):
        user = User.objects.get(id=1)
        user.email = 'test@testing.com'
        user.save()
        self.assertEqual(user.email, 'test@testing.com')