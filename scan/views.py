from django.shortcuts import render, redirect
from django.views.generic import View
from django.core.files.storage import FileSystemStorage

from PIL import Image
from pytesseract import image_to_string


class IMGView(View):
  template_name = "index.html"

  def get(self, request, *args, **kwargs):
    return render(request, self.template_name, {})
  
  def post(self, request, *args, **kwargs):
    if request.FILES:
      myimg = request.FILES['img']
      context = {}
      try:
        im = Image.open(myimg)
        text = image_to_string(im)
        if text == '':
          context['message'] = 'Sorry, This is an empty image :('
        else:
          fs = FileSystemStorage()
          filename = fs.save(myimg.name, myimg)
          uploaded_file_url = fs.url(filename)
          context['imgurl'] = uploaded_file_url
          context['alt'] = myimg.name
          context['content'] = text
      except:
        context['message'] = 'Sorry, This is not an image :('
      return render(request, self.template_name, context)
    else:
      return redirect('img')
