from django.conf import settings
from django.conf.urls.static import static
from django.urls import path

from juego import views

app_name = 'juego'

urlpatterns = [
    path('', views.IndexView.as_view(), name='indexView'),
    path('character/', views.CharacterView.as_view(), name='characterView'),
    path('equipment/', views.EquipmentView.as_view(), name='equipmentView'),
    path('faction/', views.FactionView.as_view(), name='factionView'),
    path('character/list_character/', views.CharacterListView.as_view(), name='characterListView'),
    path('faction/list_faction/', views.FactionCharacterFormView.as_view(), name='factionCharacterFormView'),
    path('character/list_for_equipment/', views.EquipmentCharacterFormView.as_view(), name='equipmentCharacterFormView'),
    path('faction/create/', views.FactionCreateView.as_view(), name='factionCreateView'),
    path('faction/delete/<pk>', views.FactionDeleteView.as_view(), name='factionDeleteView'),
    path('relation/', views.RelationCreateView.as_view(), name='relationCreateView'),
    path('character_create/', views.CharacterCreateView.as_view(), name='characterCreateView'),
    path('equipment/create_weapon/', views.WeaponCreateView.as_view(), name='weaponCreateView'),
    path('battle/', views.BattleView.as_view(), name='battleView'),
    path('character/location/', views.LocationUpdateView.as_view(), name='locationUpdateView'),
    path('character/inventory/', views.InventoryUpdateView.as_view(), name='inventoryUpdateView'),
    path('equipment/weapons/', views.WeaponListView.as_view(), name='weaponListView'),
    path('equipment/weapon/<int:pk>/', views.WeaponDetailView.as_view(), name='weaponDetailView'),
    path('equipment/weapons/<int:pk>/edit/', views.WeaponUpdateView.as_view(), name='weaponUpdateView'),
    path('equipment/weapons/<int:pk>/delete/', views.WeaponDeleteView.as_view(), name='weaponDeleteView'),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

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