from django.urls import path

from juego import views

urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
]