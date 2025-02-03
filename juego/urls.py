from django.urls import path

from juego import views

urlpatterns = [
    path('', views.index, name='index'),
]