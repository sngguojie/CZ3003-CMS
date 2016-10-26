from apscheduler.schedulers.blocking import BlockingScheduler
import requests

sched = BlockingScheduler()
count=0

@sched.scheduled_job('interval', minutes=1)
def timed_job():
    print('This job is run every one minutes.')
    global count, sched
    print "Count is %d !" % (count) 
    count=count+1
    url = "http://localhost:5000/emailApp/create"
    r=requests.post(url, data)

sched.start()