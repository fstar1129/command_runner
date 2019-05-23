from django.http import HttpResponse
from django.shortcuts import render
from .models import Script, Script_command, Queue, QParam
import json
from django.core import serializers
import datetime
import os
import uuid
import html
import time
from cmd_runner.tasks import run_script_task
import urllib
from django.shortcuts import render, redirect
from django.conf import settings
from django.contrib import messages

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

        ''' Begin reCAPTCHA validation '''
        recaptcha_response = request.POST.get('g-recaptcha-response')
        url = 'https://www.google.com/recaptcha/api/siteverify'
        values = {
            'secret': settings.GOOGLE_RECAPTCHA_SECRET_KEY,
            'response': recaptcha_response
        }
        data = urllib.parse.urlencode(values).encode()
        req =  urllib.request.Request(url, data=data)
        response = urllib.request.urlopen(req)
        result = json.loads(response.read().decode())
        ''' End reCAPTCHA validation '''

        if 1 == 1:
            command_id = request.POST.get('script')
            param = json.loads(request.POST.get('param[]'))
            u = uuid.uuid4()
            currentDT = datetime.datetime.now()
            script = Script.objects.get(pk=command_id)
            
            q = Queue(dateIn=currentDT, script_id=script, uuid=u.hex)
            q.save()
            run_script_task.delay(command_id, param, u.hex)

            return HttpResponse(json.dumps(u.hex), content_type="application/json")
        else:
            messages.error(request, 'Invalid reCAPTCHA. Please try again.')

        return redirect('index')
def result(request, uuid):
    if request.method == "GET":
        #try:
        q = Queue.objects.get(uuid=uuid)
        context = {
            'queue': q,
            'result': q.result
        }
        return render(request, 'result.html', context=context)
        # except Queue.DoesNotExist:
        #     q = Queue.objects.get(uuid=uuid)
        #     context = {
        #         'queue': 'x',
        #         'result': 'Running command on background ...'
        #     }
        #     return render(request, 'result.html', context=context)