from django.shortcuts import render, redirect
from django.views.generic import View


class CmdRunner(View):
  template_name = "index.html"

  def get(self, request, *args, **kwargs):
    return render(request, self.template_name, {})
  
  def post(self, request, *args, **kwargs):
    return redirect("")