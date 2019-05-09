from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('change_script/', views.change_script),
    path('run_script/', views.run_script),
    path('result/<uuid>', views.result)
]