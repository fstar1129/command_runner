from django.db import models


class Script(models.Model):
    name = models.CharField(max_length=30)
    command = models.CharField(max_length=30)
    example = models.CharField(max_length=100)

class Script_command(models.Model):
    script_id = models.ForeignKey(Script, on_delete=models.CASCADE)
    name = models.CharField(max_length=30)
    format = models.CharField(max_length=200)

class Queue(models.Model):
    script_id = models.ForeignKey(Script, on_delete=models.CASCADE)
    result = models.TextField()
    dateIn = models.DateField()
    dateOut = models.DateField()

class QParam(models.Model):
    queue_id = models.ForeignKey(Queue, on_delete=models.CASCADE)
    param_id = models.ForeignKey(Script_command, on_delete=models.CASCADE)
    value = models.CharField(max_length=30)