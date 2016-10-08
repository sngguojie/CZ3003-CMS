from django.shortcuts import render
from django.http import HttpResponse, HttpResponseBadRequest, JsonResponse
from django.views.decorators.http import require_GET, require_POST
from django.views.decorators.csrf import csrf_exempt

from IncidentLog.models import IncidentLog
from models import Greeting

# Create your views here.
def index(request):
    # return HttpResponse('Hello from Python!')
    return render(request, 'index.html')


def db(request):

    greeting = Greeting()
    greeting.save()

    greetings = Greeting.objects.all()

    return render(request, 'db.html', {'greetings': greetings})
    
    
# Custom routes
# =============

@require_GET
@csrf_exempt
def list_logs_for_incident(request, incident_id):
	incident_logs = IncidentLog.objects.all().filter(incident_id=incident_id)
	
	expectedAttr = {
	    'DESCRIPTION' : "description",
	    'DATETIME' : "datetime",
	    'INCIDENT_ID' : 'incident_id'
	}

	json_results = []

	for log in incident_logs:
		log_json = {
			"id" : log.id,
			expectedAttr['INCIDENT_ID'] : log.incident_id,
			expectedAttr['DESCRIPTION'] : log.description,
			expectedAttr['DATETIME'] : log.datetime,
		}

		json_results.append(log_json)

	response = JsonResponse({
		"results" : json_results,
		"success" : True,
		})

	return response