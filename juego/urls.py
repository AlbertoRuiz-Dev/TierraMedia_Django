from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, include
from rest_framework.routers import DefaultRouter


from juego import views
from juego.views import *

# Importar DefaultRouter para crear rutas automáticas para los ViewSets
router = DefaultRouter()

# Registrar las rutas de la API para diferentes modelos usando ViewSets
router.register(r'factions', FactionViewSet, basename='faction')  # Ruta para Faction
router.register(r'armors', ArmorViewSet, basename='armor')  # Ruta para Armor
router.register(r'weapons', WeaponViewSet, basename='weapon')  # Ruta para Weapon
router.register(r'relationships', RelationshipViewSet, basename='relationship')  # Ruta para Relationship
router.register(r'inventories', InventoryViewSet, basename='inventory')  # Ruta para Inventory
router.register(r'characters-info', CharacterViewSet, basename='character_info')  # Ruta para ver la info de los Characters
router.register(r'characters-modidy', CharacterModifyViewSet, basename='character_modify')  # Ruta para modificar, eliminar y crear Characters


# Definir el nombre de la aplicación para los nombres de las rutas
app_name = 'juego'

# Definir las rutas de URL para la aplicación
urlpatterns = [
    # Ruta para la vista principal del índice
    path('', views.IndexView.as_view(), name='indexView'),

    # Incluir las rutas definidas por el router (API)
    path('api/', include(router.urls)),

    # Ruta para obtener el conteo de miembros por facción
    path('api/faction_member_count/', get_factions_member_count, name='get_factions_member_count'),

    path('character/', views.CharacterListView.as_view(), name='characterView'),  # Vista de lista de personajes
    path('character/<int:pk>/', views.CharacterDetailView.as_view(), name='characterDetailView'), # Vista de detalle de personaje
    path('character/<int:pk>/update/', views.CharacterUpdateView.as_view(), name='characterUpdateView'), # Vista para actualizar personaje
    path('character/<int:pk>/delete/', views.CharacterDeleteView.as_view(), name='characterDeleteView'), # Vista para eliminar personaje
    path('character/create/', views.CharacterCreateView.as_view(), name='characterCreateView'), # Vista para crear un nuevo personaje

    path('equipment/', views.EquipmentView.as_view(), name='equipmentView'), # Vista para ver el equipo

    path('faction/', views.FactionView.as_view(), name='factionView'),  # Vista para ver la lista de facciones
    path('faction/list_faction/', views.FactionCharacterFormView.as_view(), name='factionCharacterFormView'), # Vista de formulario de facción
    path('faction/create/', views.FactionCreateView.as_view(), name='factionCreateView'), # Vista para crear una nueva facción
    path('faction/delete/<int:pk>', views.FactionDeleteView.as_view(), name='factionDeleteView'), # Vista para eliminar una facción
    path('faction/detail/<int:pk>', views.FactionDetailView.as_view(), name='factionDetailView'), # Vista para ver los detalles de una facción
    path('faction/update/<int:pk>', views.FactionUpdateView.as_view(), name='factionUpdateView'), # Vista para actualizar una facción

     # Vista para crear una relación entre personajes
    path('character/relationship/', views.RelationCreateView.as_view(), name='relationCreateView'),
    path('character/relationship_list/', views.RelationshipListView.as_view(), name= 'relationshipListView'),
    path('character/relationship_delete/<int:pk>/', views.RelationshipDeleteView.as_view(), name="relationshipDeleteView"),
    path('character/relationship_update/<int:pk>/', views.RelationshipUpdateView.as_view(), name="relationshipUpdateView"),

    path('battle/', views.BattleView.as_view(), name='battleView'), # Vista para batallas entre personajes
    path('battle/attack/', views.AttackView.as_view(), name='attackView'),

    path('equipment/weapons/', views.WeaponListView.as_view(), name='weaponListView'), # Vista de lista de armas
    path('equipment/weapon/<int:pk>/', views.WeaponDetailView.as_view(), name='weaponDetailView'), # Vista de detalle de arma
    path('equipment/weapons/<int:pk>/edit/', views.WeaponUpdateView.as_view(), name='weaponUpdateView'), # Vista para editar arma
    path('equipment/weapons/<int:pk>/delete/', views.WeaponDeleteView.as_view(), name='weaponDeleteView'), # Vista para eliminar arma
    path('equipment/create_weapon/', views.WeaponCreateView.as_view(), name='weaponCreateView'), # Vista para crear un arma nueva

    # FALTA IMPLEMENTAR!!!!
    path('equipment/list_character_for_equipment/', views.EquipmentCharacterFormView.as_view(), name='equipmentCharacterFormView'), # Vista para listar personajes segun un equipamiento

    path('equipment/armors/', views.ArmorListView.as_view(), name='armorListView'), # Vista de lista de armaduras
    path('equipment/armor/<int:pk>/', views.ArmorDetailView.as_view(), name='armorDetailView'), # Vista de detalle de armadura
    path('equipment/armor/<int:pk>/edit/', views.ArmorUpdateView.as_view(), name='armorUpdateView'), # Vista para editar armadura
    path('equipment/armor/<int:pk>/delete/', views.ArmorDeleteView.as_view(), name='armorDeleteView'), # Vista para eliminar armadura
    path('equipment/create_armor/', views.ArmorCreateView.as_view(), name='armorCreateView'), # Vista para crear una armadura nueva

    path('character/<int:pk>/inventory/add_items/', views.InventoryAddItemsView.as_view(), name='inventory_add_items'), # Vista para agregar items al inventario de un personaje

    # Rutas para equipar armas y armaduras a un personaje
    path('character/<int:pk>/equip_weapon/', views.EquipWeaponView.as_view(), name='equip_weapon'),
    path('character/<int:pk>/equip_armor/', views.EquipArmorView.as_view(), name='equip_armor'),


    path('accounts/register/', views.RegisterView.as_view(), name='register'), # Vista para registro de usuarios
]

# Si el modo DEBUG está habilitado, agregar las rutas para servir archivos estáticos y medios
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
