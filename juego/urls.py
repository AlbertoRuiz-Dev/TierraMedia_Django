from django.urls import path

from juego import views

app_name = 'juego'

urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('personaje/', views.PersonajeView.as_view(), name='personaje'),
    path('equipamiento/', views.EquipamientoView.as_view(), name='equipamiento'),
    path('faccion/', views.FaccionView.as_view(), name='faccion'),
    path('batalla/', views.BatallaView.as_view(), name='batalla'),
    path('personaje/relaciones/', views.RelacionesView.as_view(), name='relaciones'),
]