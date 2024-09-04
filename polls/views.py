from django.db.models import F
from django.http import HttpResponse, HttpResponseRedirect, Http404, JsonResponse
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.template import loader
from django.template.defaulttags import csrf_token
from django.views import generic
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_protect, requires_csrf_token, csrf_exempt, ensure_csrf_cookie
from django.middleware.csrf import get_token
import json

from .models import Choice, Question, EstimatedWaitTime

class IndexView(generic.ListView):
	template_name = "polls/index.html"
	context_object_name = "latest_wait_estimate"
	def get_queryset(self):
		"""Return the last five published questions."""
		return EstimatedWaitTime.objects.order_by("-pub_date")

class DetailView(generic.DetailView):
	model = EstimatedWaitTime
	template_name = "polls/detail.html"

class ResultsView(generic.DetailView):
	model = EstimatedWaitTime
	template_name = "polls/results.html"

def post(request):
	template_name = "polls/updateWaitTime/"
	context_object_name = "polls_post_estimate"
	try:
		responseDict = {"csrfmiddlewaretoken": request.META["CSRF_COOKIE"], "success": "false"}
		print(responseDict)
		if request.method == "POST":
			reqBody = json.loads(request.body)
			print("Body Data from POST req: ")
			print(reqBody)
			latest_eta_ref_value = get_object_or_404(EstimatedWaitTime, pk=1)
			calculated_time = latest_eta_ref_value #.set(pk=request.POST["waitEstimate"])
			calculated_time.waitingTime = reqBody['waitingTime']
			calculated_time.save()
			responseDict['waitingTime'] = calculated_time.waitingTime
			responseDict['success'] = "true"
			return JsonResponse(responseDict)
		else:
			print('csrf: ', request.META["CSRF_COOKIE"])
			# Extra request-side processing in the context of this else-conditional...
			latest_eta_ref_value = get_object_or_404(EstimatedWaitTime, pk=1)
			responseDict['waitingTime'] = latest_eta_ref_value.waitingTime
			return JsonResponse(responseDict)
	except (KeyError, Choice.DoesNotExist):
		# Redisplay question voting form
		return render(
			request,
			"polls/index.html",
			{
				"latest_eta_ref_value": latest_eta_ref_value,
				"error_message": "Error with Server configuration at this time - please try again later.",
			},
		)

def get_csrf_token(request):
    csrf_token = get_token(request)
    return JsonResponse({'csrf_token': csrf_token})
