# Common HTTP constructs
from django.http import HttpResponse, HttpResponseBadRequest
import util
import json

class HttpBadRequestException(Exception):
	def __init__(self, reason_phrase):
		self.reason_phrase = reason_phrase
	def __str__(self):
		return repr(self.reason_phrase)


def get_json(json_str):
	if not util.is_json(json_str):
		raise HttpBadRequestException(
			reason_phrase=make_not_json_request_error()
			)
	
	return json.loads(json_str)

def check_keys(json_request_obj, req_attrs):
	has_keys, missing_key = util.check_dict_keys(json_request_obj, req_attrs)
	if not has_keys:
		raise HttpBadRequestException(
			reason_phrase=make_missing_attr_error(missing_key)
		)

def save_model_obj(new_model_obj):
	try:
		new_model_obj.clean_fields()
		new_model_obj.save()
	except Exception as e:
		raise HttpBadRequestException(
			reason_phrase=make_model_save_error(new_model_obj, str(e))
			)
	

def make_not_json_request_error():
	return "Request received is not a JSON request"

def make_missing_attr_error(missing_attr):
	return "JSON string is missing attribute: %s" %	missing_attr

def make_model_save_error(model, err_msg):
	return "Failed to save model %s: %s" % (str(model), err_msg)





