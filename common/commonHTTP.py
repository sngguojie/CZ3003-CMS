# Common HTTP functions
from django.http import HttpResponse, HttpResponseBadRequest
import json

def makeNotJsonResponse(reason_phrase="Data is not a JSON string"):
	return HttpResponseBadRequest(reason=reason_phrase)

def makeMissingAttrResponse(missing_attr):
	return HttpResponseBadRequest(reason="JSON string is missing attribute: %s" %
		missing_attr)

def makeModelSaveError(model, err_msg):
	return HttpResponseBadRequest(reason="Failed to save model %s: %s" % (str(model), err_msg))






