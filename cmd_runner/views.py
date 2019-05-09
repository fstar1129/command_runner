from django.http import HttpResponse
from django.shortcuts import render
from .models import Script, Script_command, Queue, QParam
import json
from django.core import serializers
import datetime
import subprocess
import uuid
import html

def index(request):
    all_command = Script.objects.all()
    context = {
        'all_command': all_command
    }
    return render(request, 'index.html', context=context)

def change_script(request):
    if request.method == 'POST':
        command_id = request.POST.get('script_id')
        param = Script_command.objects.filter(script_id=command_id)
        data = serializers.serialize('json', list(param))
        return HttpResponse(json.dumps(data), content_type="application/json")

def run_script(request):
    if request.method == 'POST':
        command_id = request.POST.get('script')
        param = json.loads(request.POST.get('param[]'))
        currentDT = datetime.datetime.now()
        script = Script.objects.get(pk=command_id)
        u = uuid.uuid4()
        q = Queue(dateIn=currentDT, script_id=script, uuid=u.hex)
        q.save()
        k = 1
        command = script.command
        index = 0
        for i in param:
            p = Script_command.objects.get(pk=i['id'])
            qp = QParam(value=i['value'], param_id=p, queue_id=q)
            qp.save()
            command = command.replace("%"+str(index + 1), i['value'])
            index += 1
        try:
            MyOut = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
            stdout,stderr = MyOut.communicate()
        except:
            return HttpResponse(json.dumps("error"), content_type="application/json")
        result = str(stdout)[2:-1]
        mytext = result.replace('\\r\\n','<br />')
        q = Queue.objects.get(pk=q.id)
        q.result = mytext
        q.dateOut = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        q.save()

        return HttpResponse(json.dumps(u.hex), content_type="application/json")
def result(request, uuid):
    if request.method == "GET":
        q = Queue.objects.get(uuid=uuid)
        context = {
            'queue': q,
            'result': q.result
        }
        return render(request, 'result.html', context=context)
        
            
        


