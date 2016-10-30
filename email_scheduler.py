from apscheduler.schedulers.blocking import BlockingScheduler
import requests

sched = BlockingScheduler()

@sched.scheduled_job('interval', minutes=1)
def timed_job():
    url = "http://localhost:5000/emailApp/create"
    r=requests.post(url, data)

sched.start()