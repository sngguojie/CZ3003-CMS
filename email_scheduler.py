from apscheduler.schedulers.blocking import BlockingScheduler
import requests
import logging

sched = BlockingScheduler()
logging.basicConfig()

@sched.scheduled_job('interval', minutes=1)
def timed_job():
    url = "http://localhost:5000/emailApp/create/"
    r=requests.post(url,json={"start": "start"})

sched.start()