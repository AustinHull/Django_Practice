from django.db.models import F
from django.http import HttpResponse, HttpResponseRedirect
from django.http import Http404
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.template import loader

from .models import Choice, Question

def index(request):
	latest_question_list = Question.objects.order_by("-pub_date")[:5]
	template = loader.get_template("polls/index.html")
	context = {
		"latest_question_list": latest_question_list,
	}
	return HttpResponse(template.render(context, request))

def detail(request, question_id):
	question = get_object_or_404(Question, pk=question_id)
	return render(request, "polls/detail.html", {"question": question})

def results(request, question_id):
	waitTime = get_object_or_404(Question, pk=question_id)
	return render(request, "polls/results.html", {"question": waitTime})

def vote(request, question_id):
	latest_eta_ref_value = get_object_or_404(Question, pk=question_id)
	try:
		calculated_time = latest_eta_ref_value.choice_set.get(pk=request.POST["choice"])
	except (KeyError, Choice.DoesNotExist):
		# Redisplay question voting form
		return render(
			request,
			"polls/detail.html",
			{
				"latest_eta_ref_value": latest_eta_ref_value,
				"error_message": "You didn't select a choice.",
			},
		)
	else:
		calculated_time.votes = F("votes") + 1
		calculated_time.save()
		return HttpResponseRedirect(reverse("polls:results", args=(question_id,)))
