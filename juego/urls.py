from django.urls import path

from juego import views

urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('chararcter/characters', views.ListView.as_view(), name='playerListView'),
    path('faction', views.FactionCharacterListView.as_view(), name='factionPlayersListView'),
    path('character/equipment', views.EquipmentCharacterListView.as_view(), name='equipmentPlayersListView'),
    path('relation', views.RelationCreateView.as_view(), name='relationCreateView'),
    path('character_create', views.CharacterCreateView.as_view(), name='playerCreateView'),
    path('character/weapon', views.WeaponCreateView.as_view(), name='weaponCreateView'),
    path('battle', views.BattleView.as_view(), name='battleCreateView'),
    path('character/location', views.LocationUpdateView.as_view(), name='locationUpdateView'),
    path('character/inventory', views.InventoryUpdateView.as_view(), name='inventoryUpdateView'),
    path('character/equipment_update', views.EquipmentUpdateView.as_view(), name='equipmentUpdateView'),
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