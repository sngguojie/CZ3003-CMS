# initialize_db.py

from django.contrib.auth.models import Group, User

from login.constants import GRP_NAMES, USERS
from login.helpers import to_groups
from Agency.constants import AGENCIES

from CMSStatus.models import CMSStatus
from Agency.models import Agency

# Initialize group names
for GRP_NAME in GRP_NAMES:
	has_grp = len(Group.objects.filter(name=GRP_NAME)) >= 1
	if not has_grp:
		Group.objects.create(name=GRP_NAME)

# Initialize users
for user in USERS:
	get_user = User.objects.filter(username=user['username'])
	if not (len(get_user) == 0):
		continue
	cur_user = User.objects.create_user(username=user['username'], email=user['email'], password=user['password'])
	groups_str = user['groups']
	success, groups = to_groups(groups_str)
	if not success:
		logger.debug(groups)
		continue
	for group in groups:
		cur_user.groups.add(group)
		cur_user.save()

# Initialize CMSStatus
if len(CMSStatus.objects.all()) == 0:
	CMSStatus.objects.create()

# Initialize Agency
if len(Agency.objects.all()) == 0:
	for agency in AGENCIES:
		Agency.objects.create(name=agency['name'],description=agency['description'],sms_contact_no=agency['sms_contact_no'])