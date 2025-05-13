from django.shortcuts import render
from rest_framework import mixins
from rest_framework import generics
from . serializers import *
from core.models import *

from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters

from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from myproject.choices import EstadoOrden

from .pagination import CustomPagination
from .throttling import BurstRateThrottle, SustainedRateThrottle

from .permissions import IsAdminOrReadOnly, IsOwnerOrReadOnly


# Create your views here.
class ArticuloListCreateGeneric(mixins.ListModelMixin,mixins.CreateModelMixin,generics.GenericAPIView):
    """
    Lista todos los artículos o crea uno nuevo usando mixins.
    """
    queryset = Articulo.objects.all()

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return ArticuloCreateSerializer
        return ArticuloModelSerializer
    
    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)
    
    def perform_create(self, serializer):
        # Personalizar cómo se guarda el objeto
        articulo = serializer.save()
        # Podríamos hacer más cosas aquí, como logging

class ArticuloDetailGeneric(mixins.RetrieveModelMixin,mixins.UpdateModelMixin,mixins.DestroyModelMixin,generics.GenericAPIView):
    """
    Obtener, actualizar o eliminar un artículo usando mixins.
    """
    queryset = Articulo.objects.all()
    serializer_class = ArticuloSerializer

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)


# Ahora usando las vistas genéricas más simplificadas
class ArticuloListCreateSimple(generics.ListCreateAPIView):
    """
    Lista todos los artículos o crea uno nuevo.
    Versión simplificada con vistas genéricas.
    """
    queryset = Articulo.objects.all()
    pagination_class = CustomPagination

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return ArticuloCreateSerializer
        return ArticuloModelSerializer


class ArticuloDetailSimple(generics.RetrieveUpdateDestroyAPIView):
    """
    Obtener, actualizar o eliminar un artículo.
    Versión simplificada con vistas genéricas.
    """
    queryset = Articulo.objects.all()
    serializer_class = ArticuloSerializer



class ArticuloViewSet(viewsets.ModelViewSet):
    """
    Un viewset para ver y editar artículos.
    """
    queryset = Articulo.objects.all()

    def get_serializer_class(self):
        if self.action == 'create':
            return ArticuloCreateSerializer
        elif self.action == 'list':
            return ArticuloListSerializer
        return ArticuloSerializer

    @action(detail=True, methods=['get'])
    def precios(self, request, pk=None):
        """
        Endpoint personalizado para obtener precios de un artículo.
        GET /api/articulos/{id}/precios/
        """
        articulo = self.get_object()
        try:
            lista_precio = articulo.listaprecio
            serializer = ListaPrecioSerializer(lista_precio)
            return Response(serializer.data)
        except:
            return Response({"error": "No hay lista de precios"},status=status.HTTP_404_NOT_FOUND)

    @action(detail=False, methods=['get'])
    def bajo_stock(self, request):
        """
        Endpoint personalizado para obtener artículos con bajo stock.
        GET /api/articulos/bajo_stock/
        """
        articulos = Articulo.objects.filter(stock__lt=10)
        serializer = ArticuloListSerializer(articulos, many=True)
        return Response(serializer.data)
    

    filter_backends = [DjangoFilterBackend, filters.SearchFilter,filters.OrderingFilter]
    filterset_fields = ['grupo', 'linea', 'stock']
    search_fields = ['codigo_articulo', 'descripcion', 'codigo_barras']
    ordering_fields = ['codigo_articulo', 'descripcion', 'stock']
    throttle_classes = [SustainedRateThrottle] 
    permission_classes = [IsAdminOrReadOnly]


class OrdenViewSet(viewsets.ReadOnlyModelViewSet):
    """
    Un viewset para ver órdenes (solo lectura).
    """
    queryset = OrdenCompraCliente.objects.all()
    serializer_class = OrdenSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """
        Este viewset debe devolver solo las órdenes del usuario actual,
        a menos que sea staff.
        """
        user = self.request.user
        if user.is_staff:
            return OrdenCompraCliente.objects.all()
        
        # Para usuarios normales, mostrar solo sus propias órdenes
        # Suponiendo que el cliente está relacionado con el email del usuario
        return OrdenCompraCliente.objects.filter(cliente__correo_electronico=user.email)

    @action(detail=True, methods=['post'])
    def cancelar(self, request, pk=None):
        """
        Endpoint para cancelar una orden.
        POST /api/ordenes/{id}/cancelar/
        """

        orden = self.get_object()

        # Solo se pueden cancelar órdenes pendientes
        if orden.estado != EstadoOrden.PENDIENTE:
            return Response( {"error": "Solo se pueden cancelar órdenes pendientes."},status=status.HTTP_400_BAD_REQUEST)
        
        orden.estado = EstadoOrden.CANCELADA
        orden.save()
        serializer = self.get_serializer(orden)
        return Response(serializer.data)