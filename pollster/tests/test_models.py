from pollster.models import Question, Choice, Vote
from django.contrib.auth.models import User
from django.test import TestCase
from django.utils import timezone
import datetime

class QuestionModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        Question.objects.create(question_text='Test', pub_date=timezone.now())

    def test_question_text_label(self):
        question = Question.objects.get(id=1)
        field_label = question._meta.get_field('question_text').verbose_name
        self.assertEqual(field_label, 'question text')

    def test_pub_date_label(self):
        question = Question.objects.get(id=1)
        field_label = question._meta.get_field('pub_date').verbose_name
        self.assertEqual(field_label, 'date published')

    def test_question_text_length(self):
        question = Question.objects.get(id=1)
        max_length = question._meta.get_field('question_text').max_length
        self.assertEqual(max_length, 200)

    def test_object_name_is_question_text(self):
        question = Question.objects.get(id=1)
        expected_object_name = f'{question.question_text}'
        self.assertEqual(str(question), expected_object_name)

    def test_question_was_published_recently(self):
        question = Question.objects.get(id=1)
        now = timezone.now()
        return now - datetime.timedelta(days=1) <= question.pub_date <= now

    def test_was_published_recently_with_old_question(self):
        time = timezone.now() - datetime.timedelta(days=1, seconds=1)
        old_question = Question(pub_date=time)
        self.assertIs(old_question.was_published_recently(), False)

    def test_was_published_recently_with_recent_question(self):
        time = timezone.now() - datetime.timedelta(hours=23, minutes=59, seconds=59)
        recent_question = Question(pub_date=time)
        self.assertIs(recent_question.was_published_recently(), True)

class ChoiceModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        question = Question.objects.create(question_text='Test', pub_date=timezone.now())
        Choice.objects.create(question=question, choice_text='Test', votes=0)

    def test_choice_text_label(self):
        choice = Choice.objects.get(id=1)
        field_label = choice._meta.get_field('choice_text').verbose_name
        self.assertEqual(field_label, 'choice text')

    def test_votes_label(self):
        choice = Choice.objects.get(id=1)
        field_label = choice._meta.get_field('votes').verbose_name
        self.assertEqual(field_label, 'votes')

    def test_question_label(self):
        choice = Choice.objects.get(id=1)
        field_label = choice._meta.get_field('question').verbose_name
        self.assertEqual(field_label, 'question')

    def test_choice_text_length(self):
        choice = Choice.objects.get(id=1)
        max_length = choice._meta.get_field('choice_text').max_length
        self.assertEqual(max_length, 200)

class VoteModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        question = Question.objects.create(question_text='Test', pub_date=timezone.now())
        choice = Choice.objects.create(question=question, choice_text='Test', votes=0)
        user = User.objects.create(
            username='Test',
            first_name='Test',
            last_name='Test',
            email='test@test.com',
            password='test',
        )
        Vote.objects.create(question=question, choice=choice, user=user)

    def test_question_label(self):
        vote = Vote.objects.get(id=1)
        field_label = vote._meta.get_field('question').verbose_name
        self.assertEqual(field_label, 'question')

    def test_choice_label(self):
        vote = Vote.objects.get(id=1)
        field_label = vote._meta.get_field('choice').verbose_name
        self.assertEqual(field_label, 'choice')

    def test_user_label(self):
        vote = Vote.objects.get(id=1)
        field_label = vote._meta.get_field('user').verbose_name
        self.assertEqual(field_label, 'user')