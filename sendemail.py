from apscheduler.schedulers.blocking import BlockingScheduler

sched = BlockingScheduler()
count=0

@sched.scheduled_job('interval', minutes=1/60)
def timed_job():
    print('This job is run every one minutes.')
    global count, sched
    print "Count is %d !" % (count) 
    count=count+1
    if count==3:
       sched.shutdown()

sched.start()