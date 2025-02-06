from django.urls import path

from juego import views

app_name = 'juego'

urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('personaje/', views.PersonajeView.as_view(), name='personaje'),
    path('equipamiento/', views.EquipamientoView.as_view(), name='equipamiento'),
    path('faccion/', views.FaccionView.as_view(), name='faccion'),
    path('batalla/', views.BatallaView.as_view(), name='batalla'),
    path('personaje/listar_personajes/', views.CharacterListView.as_view(), name='characterListView'),
    path('faccion/listar_personajes/', views.FactionCharacterFormView.as_view(), name='factionPlayersListView'),
    path('personaje/listar_por_equipamiento/', views.EquipmentCharacterFormView.as_view(), name='InventoryPlayersListView'),
    path('relation/', views.RelationCreateView.as_view(), name='relationCreateView'),
    path('character_create/', views.CharacterCreateView.as_view(), name='playerCreateView'),
    path('character/weapon/', views.WeaponCreateView.as_view(), name='weaponCreateView'),
    path('battle/', views.BattleView.as_view(), name='battleCreateView'),
    path('character/location/', views.LocationUpdateView.as_view(), name='locationUpdateView'),
    path('character/inventory/', views.InventoryUpdateView.as_view(), name='inventoryUpdateView'),
]

"""

    Pagina principal donde se muestra un menu con las difrentes funciones
    Pagina para el login/logout
    Pagina para mostrar los personajes de una faccion
    Pagina para mostrar los personajes segun un equipamiento
    Pagina para las batallas

    Opcion Personaje:
        Pagina para crear el personaje
        Pagina para crear las relaciones
        Pagina para mostrar todos los personajes
        Pagina para modificar inventario
        Pagina para modificar equipamiento
        Pagina para cambiar la localizacion
        Pagina para crear las armas

"""