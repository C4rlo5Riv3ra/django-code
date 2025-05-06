from django.urls import path 
from . import views

urlpatterns = [ 
    # URLs para Artículos 
    path('articulos/', views.articulos_list, name='articulos_list'), 
    path('articulos/nuevo/', views.articulo_create, name='articulo_create'), 
    path('articulos/<uuid:articulo_id>/', views.articulo_detail,name='articulo_detail'), 
    path('articulos/<uuid:articulo_id>/editar/', views.articulo_edit, 
    name='articulo_edit'), 
    path('articulos/<uuid:articulo_id>/eliminar/', views.articulo_delete,name='articulo_delete'), 
    # API para operaciones AJAX 
    path('api/lineas-por-grupo/<uuid:grupo_id>/', views.get_lineas_por_grupo, name='get_lineas_por_grupo'), 
]