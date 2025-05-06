from django.db import models
from myproject.choices import estadoEntidades
import uuid

# Create your models here.
class GrupoArticulo(models.Model):
    grupo_id = models.UUIDField(primary_key=True)
    codigo_grupo = models.CharField(max_length=10, null=False)
    nombre_grupo = models.CharField(max_length=150, null=False)
    estado =models.IntegerField(choices=estadoEntidades, default=estadoEntidades.ACTIVO)

    def __str__(self):
        return self.nombre_grupo

    class Meta:
        db_table = 'grupo_articulo'
        ordering = ['codigo_grupo']

class LineaArticulo(models.Model):
    linea_id = models.UUIDField(primary_key=True)
    codigo_linea = models.CharField(max_length=10, null=False)
    grupo = models.ForeignKey(GrupoArticulo, on_delete=models.RESTRICT, null=False, related_name='grupo_linea')
    nombre_linea = models.CharField(max_length=150, null=False)
    estado = models.IntegerField(choices=estadoEntidades, default=estadoEntidades.ACTIVO)

    def __str__(self):
        return self.nombre_linea

    class Meta:
        db_table = 'linea_articulo'
        ordering = ['codigo_linea']

class Articulo(models.Model):
    articulo_id = models.UUIDField(primary_key=True)
    codigo_articulo = models.CharField(max_length=25, null=False)
    codigo_barras = models.CharField(max_length=250, null=True)
    descripcion = models.CharField(max_length=500, null=False)
    presentacion = models.CharField(max_length=500, null=True)
    grupo = models.ForeignKey(GrupoArticulo, on_delete=models.RESTRICT, null=False, related_name='articulo_grupo')
    linea = models.ForeignKey(LineaArticulo, on_delete=models.RESTRICT, null=False, related_name='articulo_linea')
    stock = models.DecimalField(max_digits=10, decimal_places=2, null=False)
    
    class Meta:
        db_table = 'articulo'
        ordering = ['articulo_id']

class ListaPrecio(models.Model):
    articulo_id = models.ForeignKey(Articulo, on_delete=models.RESTRICT, null=False, related_name='lista_articulo')
    precio_1 = models.DecimalField(max_digits=10, decimal_places=2, null=False)
    precio_2 = models.DecimalField(max_digits=10, decimal_places=2, null=False)
    precio_3 = models.DecimalField(max_digits=10, decimal_places=2, null=False)
    precio_4 = models.DecimalField(max_digits=10, decimal_places=2, null=False)
    precio_compra = models.DecimalField(max_digits=10, decimal_places=2, null=False)
    precio_costo = models.DecimalField(max_digits=10, decimal_places=2, null=False)

    class Meta:
        db_table = 'lista_precio'
        ordering = ['articulo_id']