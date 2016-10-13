# helpers.py

from django.contrib.auth.models import Group

def to_groups(groups_str):
	"""
		Input:
		groups_str: String
		Output:
		success: Boolean
		groups: list of Group
	"""
	groups = []

	if groups_str == '':
		return True, groups

	try:
		group_names = groups_str.split(', ')
		for group_name in group_names:
			get_group = Group.objects.filter(name=group_name)
			has_grp = len(get_group) >= 1
			if not has_grp:
				continue
			cur_group = get_group[0]
			groups.append(cur_group)
	except Exception as e:
		return False, e

	return True, groups

def to_groups_str(groups):
	"""
		Input:
		groups: list of Group
		Output:
		success: Boolean
		groups_str: String 
	"""
	groups_str = ''
	if len(groups) == 0:
		return True, groups_str

	try:
		for group in groups:
			groups_str += group.name + ', '
		groups_str = groups_str[:-2]
	except Exception as e:
		return False, e

	return True, groups_str
