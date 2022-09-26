from django.contrib.auth.models import User
from django.test import TestCase

class UserModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        user = User.objects.create(
            username='Test',
            first_name='Test',
            last_name='Test',
            email='test@test.com',
            password='test',
        )

    def test_username_label(self):
        user = User.objects.get(id=1)
        field_label = user._meta.get_field('username').verbose_name
        self.assertEqual(field_label, 'username')

    def test_first_name_label(self):
        user = User.objects.get(id=1)
        field_label = user._meta.get_field('first_name').verbose_name
        self.assertEqual(field_label, 'first name')

    def test_last_name_label(self):
        user = User.objects.get(id=1)
        field_label = user._meta.get_field('last_name').verbose_name
        self.assertEqual(field_label, 'last name')

    def test_email_label(self):
        user = User.objects.get(id=1)
        field_label = user._meta.get_field('email').verbose_name
        self.assertEqual(field_label, 'email address')

    def test_password_label(self):
        user = User.objects.get(id=1)
        field_label = user._meta.get_field('password').verbose_name
        self.assertEqual(field_label, 'password')

    def test_object_name_is_username(self):
        user = User.objects.get(id=1)
        expected_object_name = f'{user.username}'
        self.assertEqual(str(user), expected_object_name)