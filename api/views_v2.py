from rest_framework import viewsets, filters, status
from rest_framework.response import Response
from rest_framework.decorators import action
from django_filters.rest_framework import DjangoFilterBackend
from core.models import Articulo, OrdenCompraCliente,GrupoArticulo,LineaArticulo
from .serializers import ArticuloSerializer, ArticuloListSerializer,OrdenSerializer
from .permissions import IsAdminOrReadOnly
from .throttling import SustainedRateThrottle
from .pagination import CustomPagination
from myproject.choices import EstadoOrden

class ArticuloViewSetV2(viewsets.ModelViewSet):
    """
    API v2: Un viewset para ver y editar artículos.
    Cambios en V2:
    - Incluye información extendida de cada artículo
    - Paginación personalizada
    - Ordenamiento por defecto por código
    """
    queryset = Articulo.objects.all().order_by('codigo_articulo')
    filter_backends = [DjangoFilterBackend, filters.SearchFilter, filters.OrderingFilter]
    filterset_fields = ['grupo', 'linea', 'stock']
    search_fields = ['codigo_articulo', 'descripcion', 'codigo_barras']
    ordering_fields = ['codigo_articulo', 'descripcion', 'stock']
    throttle_classes = [SustainedRateThrottle]
    permission_classes = [IsAdminOrReadOnly]
    pagination_class = CustomPagination

    def get_serializer_class(self):
        if self.action == 'list':
            return ArticuloListSerializer
        return ArticuloSerializer
    
    @action(detail=True, methods=['get'])
    def precios(self, request, pk=None):
        """
        Endpoint personalizado para obtener precios de un artículo.
        GET /api/v2/articulos/{id}/precios/
        """
        articulo = self.get_object()
        try:
            lista_precio = articulo.listaprecio
            serializer = ListaPrecioSerializer(lista_precio)
            return Response(serializer.data)
        except:
            return Response({"error": "No hay lista de precios"},status=status.HTTP_404_NOT_FOUND)
    
    @action(detail=False, methods=['get'])
    def stats(self, request):
        """
        Endpoint nuevo en V2 que proporciona estadísticas sobre artículos.
        GET / /api/v2/articulos/stats/
        """
        total_articulos = Articulo.objects.count()
        bajo_stock = Articulo.objects.filter(stock__lt=10).count()

        # Artículos por grupo
        from django.db.models import Count
        grupos = GrupoArticulo.objects.annotate(
            articulos_count=Count('articulo')
        ).values('nombre_grupo', 'articulos_count')

        return Response({
            'total_articulos': total_articulos,
            'bajo_stock': bajo_stock,
            'distribucion_por_grupo': grupos
        })

class OrdenViewSetV2(viewsets.ReadOnlyModelViewSet):
    """
    API v2: Un viewset para ver órdenes (solo lectura).
    """
    queryset = OrdenCompraCliente.objects.all()
    serializer_class = OrdenSerializer
    pagination_class = CustomPagination

    def get_queryset(self):
        """
        Este viewset debe devolver solo las órdenes del usuario actual,
        a menos que sea staff.
        """
        user = self.request.user
        if user.is_staff:
            return OrdenCompraCliente.objects.all()
        # Para usuarios normales, mostrar solo sus propias órdenes
        return OrdenCompraCliente.objects.filter(cliente__correo_electronico=user.email)
    
    @action(detail=True, methods=['post'])
    def cancelar(self, request, pk=None):
        """
        Endpoint para cancelar una orden.
        POST /api/v2/ordenes/{id}/cancelar/
        """
        orden = self.get_object()
        # Solo se pueden cancelar órdenes pendientes
        if orden.estado != EstadoOrden.PENDIENTE:
            Response(
                {"error": "Solo se pueden cancelar órdenes pendientes."},status=status.HTTP_400_BAD_REQUEST
            )
        orden.estado = EstadoOrden.CANCELADA
        orden.save()
        serializer = self.get_serializer(orden)
        return Response(serializer.data)
    
    @action(detail=False, methods=['get'])
    def pendientes(self, request):
        """
        Endpoint nuevo en V2 que muestra solo órdenes pendientes.
        GET /api/v2/ordenes/pendientes/
        """
        ordenes = self.get_queryset().filter(estado=EstadoOrden.PENDIENTE)
        page = self.paginate_queryset(ordenes)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)
        serializer = self.get_serializer(ordenes, many=True)
        return Response(serializer.data)



