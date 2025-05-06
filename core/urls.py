from django.urls import path 
from . import views

urlpatterns = [ 
    # URLs para Artículos 
    path('articulos/', views.articulos_list, name='articulos_list'), 
    path('articulos/nuevo/', views.articulo_create, name='articulo_create'), 
    path('articulos/<uuid:articulo_id>/', views.articulo_detail,name='articulo_detail'), 
    path('articulos/<uuid:articulo_id>/editar/', views.articulo_edit, name='articulo_edit'), 
    path('articulos/<uuid:articulo_id>/eliminar/', views.articulo_delete,name='articulo_delete'), 
    # API para operaciones AJAX 
    path('api/lineas-por-grupo/<uuid:grupo_id>/', views.get_lineas_por_grupo, name='get_lineas_por_grupo'), 

    # URLs para el Carrito de Compras 
    path('carrito/', views.cart_detail, name='cart_detail'), 
    path('carrito/agregar/<uuid:articulo_id>/', views.cart_add, name='cart_add'), 
    path('carrito/eliminar/<uuid:articulo_id>/', views.cart_remove, name='cart_remove'), 
    path('carrito/vaciar/', views.cart_clear, name='cart_clear'), 
    path('checkout/', views.checkout, name='checkout'), 
    path('orden/<uuid:pedido_id>/', views.order_detail, name='order_detail'), 
    # path('orden/cancelar/<uuid:pedido_id>/', views.cancel_order, name='cancel_order'), 
    # path('orden/pdf/<uuid:pedido_id>/', views.generate_pdf_order, name='generate_pdf_order'),

]