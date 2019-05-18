from .models import Queue
from scan.celery import app
import datetime
import os

@app.task
def run_script_task(qid, command):
    output = os.popen(command).read()

    res = str(output)[1:-1]
    mytext = res.replace('\n','<br />')
    q = Queue.objects.get(pk=qid)
    q.result = mytext
    q.dateOut = datetime.datetime.now()
    q.save()
    