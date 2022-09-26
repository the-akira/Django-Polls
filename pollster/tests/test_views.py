from django.contrib.auth.models import User
from pollster.models import Question
from django.utils import timezone
from django.test import TestCase
from django.urls import reverse
import datetime

class ViewsTestCase(TestCase):
    @classmethod
    def setUpTestData(cls):
        Question.objects.create(question_text='Test', pub_date=timezone.now())
        number_of_questions = 15

        for question_id in range(number_of_questions):
            Question.objects.create(
                question_text=f'Test {question_id}',
                pub_date=timezone.now(),
            )
        user = User.objects.create_user(
            username='Test',
            first_name='Test',
            last_name='Test',
            email='test@test.com',
            password='test',
        )

    def test_template_detail_correct(self):  
        question = Question.objects.get(id=1)
        response = self.client.get(reverse('pollster:detail', args=(question.id,)))
        self.assertTemplateUsed(response, 'polls/detail.html')

    def test_template_results_correct(self):  
        question = Question.objects.get(id=1)
        response = self.client.get(reverse('pollster:results', args=(question.id,)))
        self.assertTemplateUsed(response, 'polls/results.html')

    def test_template_vote_correct(self):  
        question = Question.objects.get(id=1)
        response = self.client.get(reverse('pollster:vote', args=(question.id,)))
        self.assertTemplateUsed(response, 'polls/detail.html')

    def test_template_vote_correct_post(self):  
        question = Question.objects.get(id=1)
        data = {'choice': question.question_text}
        response = self.client.post(reverse('pollster:vote', args=(question.id,)), data)
        self.assertEqual(response.status_code, 200) 
        self.assertTemplateUsed(response, 'polls/detail.html')

    def test_details_loads_properly(self):
        question = Question.objects.get(id=1)
        response = self.client.get(f'/polls/{question.id}/')
        self.assertEqual(response.status_code, 200)

    def test_results_loads_properly(self):
        question = Question.objects.get(id=1)
        response = self.client.get(f'/polls/{question.id}/results/')
        self.assertEqual(response.status_code, 200)

    def test_template_content_results(self):
        question = Question.objects.get(id=1)
        response = self.client.get(reverse('pollster:results', args=(question.id,)))
        self.assertContains(response, "<p>You haven't voted yet in this poll</p>")
        self.assertNotContains(response, 'Not on the page')

    def test_list_all_questions(self):
        self.client.login(username='Test', password='test') 
        response = self.client.get(reverse('pollster:index'))
        self.assertEqual(response.status_code, 200)
        self.assertTrue(len(response.context['latest_question_list']) == 16)

    def test_total_pages_is_six(self):
        self.client.login(username='Test', password='test') 
        response = self.client.get(reverse('pollster:index'))
        self.assertEqual(response.status_code, 200)
        pages = response.context['page_obj'].paginator.num_pages
        self.assertEqual(pages, 6)

def create_question(question_text, days):
    time = timezone.now() + datetime.timedelta(days=days)
    return Question.objects.create(question_text=question_text, pub_date=time)

class QuestionIndexViewTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        user = User.objects.create_user(
            username='Test',
            first_name='Test',
            last_name='Test',
            email='test@test.com',
            password='test',
        )

    def test_no_questions(self):
        self.client.login(username='Test', password='test') 
        response = self.client.get(reverse('pollster:index'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "No polls available")
        self.assertQuerysetEqual(response.context['latest_question_list'], [])

    def test_past_question(self):
        question = create_question(question_text="Past question.", days=-30)
        self.client.login(username='Test', password='test')
        response = self.client.get(reverse('pollster:index'))
        self.assertQuerysetEqual(
            response.context['latest_question_list'],
            [question],
        )

    def test_future_question(self):
        create_question(question_text="Future question.", days=30)
        self.client.login(username='Test', password='test')
        response = self.client.get(reverse('pollster:index'))
        self.assertContains(response, "No polls available")
        self.assertQuerysetEqual(response.context['latest_question_list'], [])

    def test_future_question_and_past_question(self):
        question = create_question(question_text="Past question.", days=-30)
        create_question(question_text="Future question.", days=30)
        self.client.login(username='Test', password='test')
        response = self.client.get(reverse('pollster:index'))
        self.assertQuerysetEqual(
            response.context['latest_question_list'],
            [question],
        )

    def test_two_past_questions(self):
        question1 = create_question(question_text="Past question 1.", days=-30)
        question2 = create_question(question_text="Past question 2.", days=-5)
        self.client.login(username='Test', password='test')
        response = self.client.get(reverse('pollster:index'))
        self.assertQuerysetEqual(
            response.context['latest_question_list'],
            [question2, question1],
        )

    def test_template_index_correct(self): 
        self.client.login(username='Test', password='test') 
        response = self.client.get(reverse('pollster:index'))
        self.assertTemplateUsed(response, 'polls/index.html')

    def test_index_loads_properly(self):
        self.client.login(username='Test', password='test') 
        response = self.client.get('/')
        self.assertEqual(response.status_code, 200)

    def test_template_content_index(self):
        self.client.login(username='Test', password='test') 
        response = self.client.get(reverse('pollster:index'))
        self.assertContains(response, "<h1>Questions</h1>")
        self.assertNotContains(response, 'Not on the page')

    def test_redirect_if_not_logged_in(self):
        response = self.client.get(reverse('pollster:index'))
        self.assertRedirects(response, '/accounts/login/?next=/polls/')

    def test_logged_in_uses_correct_template(self):
        self.client.login(username='Test', password='test') 
        response = self.client.get(reverse('pollster:index'))
        self.assertEqual(str(response.context['user']), 'Test')
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'polls/index.html')