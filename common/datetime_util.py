import datetime
import pytz
from django.utils import timezone

def sgt_now():
	return datetime.datetime.now(tz=pytz.timezone("Asia/Singapore"))