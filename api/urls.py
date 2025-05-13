from django.urls import path, include
from . import views
# pos_project/urls.py
from rest_framework.routers import DefaultRouter

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView,
)

from . import views_v2
app_name = 'api'

# Crear un router y registrar los viewsets
router = DefaultRouter()
router.register(r'articulos', views.ArticuloViewSet, basename='articulo')
router.register(r'ordenes', views.OrdenViewSet, basename='orden')

# Crear routers para cada versión
router_v1 = DefaultRouter()
router_v1.register(r'articulos', views.ArticuloViewSet, basename='articulo')
router_v1.register(r'ordenes', views.OrdenViewSet, basename='orden')
router_v2 = DefaultRouter()
router_v2.register(r'articulos', views_v2.ArticuloViewSetV2,
basename='articulo')
router_v2.register(r'ordenes', views_v2.OrdenViewSetV2, basename='orden')

urlpatterns = [

    path('', include(router.urls)),
    path('articulos/', views.articulo_list, name='articulo-list'),
    path('articulos/create/', views.articulo_create, name='articulo-create'),
    path('articulos/<uuid:pk>/', views.articulo_detail,name='articulo-detail'),
    path('articulos/func/', views.articulo_list, name='articulo-list-func'),
    path('articulos/func/create/', views.articulo_create,name='articulo-create-func'),
    path('articulos/func/<uuid:pk>/', views.articulo_detail,name='articulo-detail-func'),
    # Vistas basadas en clases
    path('articulos/class/', views.ArticuloListView.as_view(),name='articulo-list-class'),
    path('articulos/class/<uuid:pk>/', views.ArticuloDetailView.as_view(),name='articulo-detail-class'), 

    # Vistas con mixins
    path('articulos/mixins/', views.ArticuloListCreateGeneric.as_view(),name='articulo-list-mixins'),
    path('articulos/mixins/<uuid:pk>/', views.ArticuloDetailGeneric.as_view(),name='articulo-detail-mixins'),

    # Vistas genéricas simplificadas
    path('articulos/generic/', views.ArticuloListCreateSimple.as_view(),name='articulo-list-generic'),
    path('articulos/generic/<uuid:pk>/', views.ArticuloDetailSimple.as_view(),name='articulo-detail-generic'),

    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('token/verify/', TokenVerifyView.as_view(), name='token_verify'),

]


