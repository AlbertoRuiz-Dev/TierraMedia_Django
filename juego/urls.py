from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, include
from rest_framework.routers import DefaultRouter


from juego import views
from juego.views import *


# Crea un router para tus views
router = DefaultRouter()
router.register(r'factions', FactionViewSet, basename='faction')
router.register(r'armors', ArmorViewSet, basename='armor')
router.register(r'weapons', WeaponViewSet, basename='weapon')
router.register(r'relationships', RelationshipViewSet, basename='relationship')
router.register(r'inventories', InventoryViewSet, basename='inventory')
router.register(r'characters', CharacterViewSet, basename='character')

app_name = 'juego'

urlpatterns = [
    path('', views.IndexView.as_view(), name='indexView'),
    path('api/', include(router.urls)),
    path('api/faction_member_count/', get_factions_member_count, name='faction_member_count'),
    path('character/', views.CharacterListView.as_view(), name='characterView'),
    path('character/<int:pk>/', views.CharacterDetailView.as_view(), name='characterDetailView'),
    path('character/<int:pk>/update/', views.CharacterUpdateView.as_view(), name='characterUpdateView'),
    path('character/<int:pk>/delete/', views.CharacterDeleteView.as_view(), name='characterDeleteView'),
    path('character/create/', views.CharacterCreateView.as_view(), name='characterCreateView'),
    path('equipment/', views.EquipmentView.as_view(), name='equipmentView'),
    path('faction/', views.FactionView.as_view(), name='factionView'),
    path('faction/list_faction/', views.FactionCharacterFormView.as_view(), name='factionCharacterFormView'),
    path('character/list_for_equipment/', views.EquipmentCharacterFormView.as_view(), name='equipmentCharacterFormView'),
    path('faction/create/', views.FactionCreateView.as_view(), name='factionCreateView'),
    path('faction/delete/<int:pk>', views.FactionDeleteView.as_view(), name='factionDeleteView'),
    path('faction/detail/<int:pk>', views.FactionDetailView.as_view(), name='factionDetailView'),
    path('faction/update/<int:pk>', views.FactionUpdateView.as_view(), name='factionUpdateView'),
    path('relation/', views.RelationCreateView.as_view(), name='relationCreateView'),
    path('battle/', views.BattleView.as_view(), name='battleView'),
    path('character/location/', views.LocationUpdateView.as_view(), name='locationUpdateView'),
    path('equipment/weapons/', views.WeaponListView.as_view(), name='weaponListView'),
    path('equipment/weapon/<int:pk>/', views.WeaponDetailView.as_view(), name='weaponDetailView'),
    path('equipment/weapons/<int:pk>/edit/', views.WeaponUpdateView.as_view(), name='weaponUpdateView'),
    path('equipment/weapons/<int:pk>/delete/', views.WeaponDeleteView.as_view(), name='weaponDeleteView'),
    path('equipment/create_weapon/', views.WeaponCreateView.as_view(), name='weaponCreateView'),
    path('equipment/armors/', views.ArmorListView.as_view(), name='armorListView'),
    path('equipment/armor/<int:pk>/', views.ArmorDetailView.as_view(), name='armorDetailView'),
    path('equipment/armor/<int:pk>/edit/', views.ArmorUpdateView.as_view(), name='armorUpdateView'),
    path('equipment/armor/<int:pk>/delete/', views.ArmorDeleteView.as_view(), name='armorDeleteView'),
    path('equipment/create_armor/', views.ArmorCreateView.as_view(), name='armorCreateView'),
    path('character/<int:pk>/inventory/add_items/', views.InventoryAddItemsView.as_view(), name='inventory_add_items'),
    path('character/<int:pk>/equip_weapon/', views.EquipWeaponView.as_view(), name='equip_weapon'),
    path('character/<int:pk>/equip_armor/', views.EquipArmorView.as_view(), name='equip_armor'),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

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