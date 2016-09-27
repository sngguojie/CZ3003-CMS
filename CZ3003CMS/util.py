import json

def is_json(json_str):
	try:
		json_object = json.loads(myjson)
	except ValueError, e:
		return False
	return True