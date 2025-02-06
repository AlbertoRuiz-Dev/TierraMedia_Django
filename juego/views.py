from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView, CreateView


# Create your views here.

class IndexView(LoginRequiredMixin, TemplateView):
    template_name = 'juego/index.html'

class PersonajeView(LoginRequiredMixin, TemplateView):
    template_name = 'juego/personaje.html'

class EquipamientoView(LoginRequiredMixin, TemplateView):
    template_name = 'juego/equipamiento.html'

class FaccionView(LoginRequiredMixin, TemplateView):
    template_name = 'juego/faccion.html'

class BatallaView(LoginRequiredMixin, TemplateView):
    template_name = 'juego/batalla.html'

class RelacionesView(LoginRequiredMixin, TemplateView):
    template_name = 'juego/relaciones.html'