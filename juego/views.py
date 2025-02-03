from django.http import HttpResponse
from django.shortcuts import render
from django.views import View
from django.views.generic import TemplateView


# Create your views here.

class IndexView(TemplateView):
    template_name = 'juego/index.html'
