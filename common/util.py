# Utility functions across apps

import json

def is_json(json_str):
	try:
		json_object = json.loads(json_str)
	except ValueError, e:
		return False
	return True

def check_keys(dictionary, keys):
	"""Check that dictionary contains all the keys, returns missing key""" 
	for key in keys:
		if key not in dictionary.keys():
			return False, key

	return True, None