from pollster.models import Question
from django.utils import timezone
from django.test import TestCase
from django.urls import reverse
from http import HTTPStatus

class ChoiceFormTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        Question.objects.create(question_text='Test', pub_date=timezone.now())

    def test_post_choice(self):
        question = Question.objects.get(id=1)
        response = self.client.post(reverse('pollster:vote', args=(question.id,)), 
            data={'choice': question.question_text}
        )
        self.assertEqual(response.status_code, HTTPStatus.OK)

    def test_post_choice_double(self):
        question = Question.objects.get(id=1)
        response = self.client.post(reverse('pollster:vote', args=(question.id,)), 
            data={'choice': question.question_text}
        )
        self.assertEqual(response.status_code, HTTPStatus.OK)
        response = self.client.post(reverse('pollster:vote', args=(question.id,)), 
            data={'choice': question.question_text}
        )
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertContains(response, "You already voted in this poll.")

    def test_post_choice_empty(self):
        question = Question.objects.get(id=1)
        response = self.client.post(reverse('pollster:vote', args=(question.id,)), data={})
        self.assertContains(response, "You did not select a choice.")
        self.assertEqual(response.status_code, HTTPStatus.OK)