from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator
from .models import Question, Choice, Vote
from django.db import IntegrityError
from django.contrib import messages
from django.utils import timezone
from django.urls import reverse

def has_user_already_voted(question, user_id):
	votes = len(Vote.objects.filter(question=question, user_id=user_id))
	return True if votes > 0 else False

@login_required
def index(request):
	latest_question_list = Question.objects.filter(pub_date__lte=timezone.now()).order_by('-pub_date')
	paginator = Paginator(latest_question_list, 3) 
	page_number = request.GET.get('page')
	page_obj = paginator.get_page(page_number)
	context = {
		'latest_question_list': latest_question_list,
		'page_obj': page_obj
	}
	return render(request, 'polls/index.html', context)

def detail(request, question_id):
	try:
		question = Question.objects.get(pk=question_id)
	except Question.DoesNotExist:
		raise Http404('Question does not exist!')
	return render(request, 'polls/detail.html', {'question': question})

def results(request, question_id):
	question = get_object_or_404(Question, pk=question_id)
	voted = has_user_already_voted(question, request.user.id)
	try:
		user_choice = str(Vote.objects.get(question=question, user_id=request.user.id).choice)
	except Vote.DoesNotExist:
		user_choice = None
	labels, data = [], []
	for choice in question.choice_set.all():
		labels.append(choice.choice_text)
		data.append(choice.votes)
	return render(request, 'polls/results.html', {
		'question': question,
		'labels': labels,
		'data': data,
		'user_choice': user_choice,
		'total': sum(data),
		'voted': voted,
	})

def vote(request, question_id):
	question = get_object_or_404(Question, pk=question_id)
	voted = has_user_already_voted(question, request.user.id)
	try:
		select_choice = question.choice_set.get(pk=request.POST['choice'])
		if voted:
			raise ValueError()
		vote = Vote(choice=select_choice, question=question, user_id=request.user.id)
		vote.save()
	except (KeyError, Choice.DoesNotExist):
		return render(request, 'polls/detail.html', {
			'question': question,
			'error_message': 'You did not select a choice.'
		})
	except ValueError:
		return render(request, 'polls/detail.html', {
			'question': question,
			'error_message': 'You already voted in this poll.'
		})
	else:
		select_choice.votes += 1
		select_choice.save()
		messages.success(request, f'You have chosen the option: {select_choice.choice_text}')
		return HttpResponseRedirect(reverse('pollster:results', args=(question_id,)))