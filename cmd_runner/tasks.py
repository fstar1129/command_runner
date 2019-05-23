from .models import Queue, Script, Script_command, QParam
from scan.celery import app
import datetime
import os

@app.task
def run_script_task(command_id, param, uuid):
    #currentDT = datetime.datetime.now()
    script = Script.objects.get(pk=command_id)
    
    q = Queue.objects.get(uuid=uuid)
    # q.save()
    
    command = script.command
    index = 0
    for i in param:
        p = Script_command.objects.get(pk=i['id'])
        qp = QParam(value=i['value'], param_id=p, queue_id=q)
        qp.save()
        command = command.replace("%"+str(index + 1), i['value'])
        index += 1
    output = os.popen(command).read()

    res = str(output)[1:-1]
    mytext = res.replace('\n','<br />')
    q = Queue.objects.get(pk=q.id)
    q.result = mytext
    q.dateOut = datetime.datetime.now()
    q.save()
    