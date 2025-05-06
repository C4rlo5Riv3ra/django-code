from django.db import models
from myproject.choices import estadoEntidades, EstadoOrden
from django.contrib.auth.hashers import make_password
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

class CanalCliente(models.Model):
    canal_id = models.UUIDField(primary_key=True)
    nombre_canal = models.CharField(max_length=100, null=False)

    class Meta:
        db_table = 'canal_cliente'
        ordering = ['canal_id']

class TipoIdentificacion(models.Model):
    tipo_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    codigo = models.CharField(max_length=5, null=False, unique=True)
    descripcion = models.CharField(max_length=100, null=False)
    estado = models.IntegerField(choices=estadoEntidades, default=estadoEntidades.ACTIVO)

    def __str__(self):
        return self.descripcion

    class Meta:
        db_table = "tipo_identificacion"
        ordering = ["tipo_id"]

class Cliente(models.Model):
    cliente_id = models.UUIDField(primary_key=True)
    nro_identificacion =  models.CharField(max_length=12, null=False)
    tipo_id = models.ForeignKey(TipoIdentificacion, on_delete=models.RESTRICT, null=False, related_name='clientes', db_column='tipo_id')
    nombres = models.CharField(max_length=150, null=False)
    direccion = models.CharField(max_length=150, null=False)
    correo_electronico = models.CharField(max_length=255, null=False)
    nro_movil = models.CharField(max_length=15, null=False)
    estado = models.IntegerField(choices=estadoEntidades, default=estadoEntidades.ACTIVO)
    canal_id = models.ForeignKey(CanalCliente, on_delete=models.RESTRICT, null=False, related_name='cliente_canal', db_column='canal_id')

    class Meta:
        db_table = 'cliente'
        ordering = ['cliente_id']


class Pedido(models.Model):
    pedido_id = models.UUIDField(primary_key=True)
    nro_pedido = models.IntegerField(null=False)
    cliente_id = models.ForeignKey(Cliente, on_delete=models.RESTRICT, null=False, related_name='cliente_pedido', db_column='cliente_id')
    importe = models.DecimalField(max_digits=12, decimal_places=2, null=False)
    estado = models.IntegerField(choices=estadoEntidades, default=estadoEntidades.ACTIVO)

    class Meta:
        db_table = 'pedido'
        ordering = ['pedido_id']


class Usuario(models.Model):
    usuario_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    nombre_usuario = models.CharField(max_length=150, null=False)
    correo = models.EmailField(max_length=255, unique=True, null=False)
    contrasena = models.CharField(max_length=128, null=False)  # Reemplazable con hashed password si se usa Django auth
    estado = models.IntegerField(choices=estadoEntidades, default=estadoEntidades.ACTIVO)
    fecha_creacion = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        # Hash de la contraseña solo si no está hasheada
        if not self.password.startswith('pbkdf2_'):
            self.password = make_password(self.contrasena)
        super().save(*args, **kwargs)

    class Meta:
        db_table = "usuario"
        ordering = ["usuario_id"]


class Vendedor(models.Model):
    vendedor_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    tipo_id = models.ForeignKey(TipoIdentificacion, on_delete=models.RESTRICT, null=False, related_name='vendedores', db_column='tipo_id')
    nombres = models.CharField(max_length=150, null=False)
    apellidos = models.CharField(max_length=150, null=False)
    correo = models.EmailField(max_length=255, unique=True, null=False)
    telefono = models.CharField(max_length=20, null=True)
    estado = models.IntegerField(choices=estadoEntidades, default=estadoEntidades.ACTIVO)
    fecha_creacion = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.nombres} {self.apellidos}"

    class Meta:
        db_table = "vendedor"
        ordering = ["vendedor_id"]


class ItemPedido(models.Model):
    item_id = models.UUIDField(primary_key=True)
    pedido_id = models.ForeignKey(Pedido, on_delete=models.RESTRICT, null=False, related_name='itemp_pedido',db_column='pedido_id')
    articulo_id = models.ForeignKey(Articulo, on_delete=models.RESTRICT, null=False, related_name='itemp_articulo', db_column='articulo_id')
    cantidad = models.IntegerField(null=False)
    precio_unitario = models.DecimalField(max_digits=12, decimal_places=2, null=False)
    total = models.DecimalField(max_digits=12, decimal_places=2, null=False)
    estado = models.IntegerField(choices=estadoEntidades, default=estadoEntidades.ACTIVO)

    class Meta:
        db_table = 'item_pedido'
        ordering = ['item_id']

class OrdenCompraCliente(models.Model):
    pedido_id = models.UUIDField(primary_key=True, default=uuid.uuid4,editable=False)
    nro_pedido = models.UUIDField(default=uuid.uuid4, unique=True, editable=False)
    fecha_pedido = models.DateField(auto_now_add=True, null=False)
    cliente = models.ForeignKey(Cliente, on_delete=models.RESTRICT,null=False)
    vendedor = models.ForeignKey(Vendedor, on_delete=models.RESTRICT,null=False)
    importe = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    estado = models.IntegerField(choices=EstadoOrden,default=EstadoOrden.PENDIENTE)
    notas = models.TextField(blank=True, null=True)
    creado_por = models.ForeignKey(Usuario, on_delete=models.RESTRICT,null=False)
    fecha_creacion = models.DateTimeField(auto_now_add=True, null=False)

    def actualizar_total(self):
        """Actualiza el total de la orden basado en los items"""
        total = sum(item.total_item for item in self.items_orden_compra.all())
        self.importe = total
        self.save()

    def __str__(self):
        return f"Orden #{self.nro_pedido} - {self.cliente}"

    class Meta:
        db_table = "ordenes_compra_cliente"
        ordering = ["-fecha_creacion"]


class ItemOrdenCompraCliente(models.Model):
    item_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    pedido = models.ForeignKey(OrdenCompraCliente, on_delete=models.CASCADE, null=False, related_name='items_orden_compra')
    nro_item = models.PositiveIntegerField(default=1, null=False)
    articulo = models.ForeignKey(Articulo, on_delete=models.RESTRICT, null=False, related_name='articulo_item_orden_compra')
    cantidad = models.PositiveIntegerField(null=False, default=1)
    precio_unitario = models.DecimalField(max_digits=12, decimal_places=2, null=False, default=0)
    total_item = models.DecimalField(max_digits=12, decimal_places=2, null=False, default=0)
    estado = models.IntegerField(choices=estadoEntidades, default=estadoEntidades.ACTIVO)
    creado_por = models.ForeignKey(Usuario, on_delete=models.RESTRICT, null=False)
    fecha_creacion = models.DateTimeField(auto_now_add=True, null=False)

    def save(self, *args, **kwargs):
        # Si no se ha establecido el precio unitario, tomarlo del artículo
        if self.precio_unitario == 0:
            try:
                lista_precio = self.articulo.listaprecio
                self.precio_unitario = lista_precio.precio_1
            except Exception:
                pass  # Podrías registrar esto para auditoría

        # Calcular el total del ítem
        self.total_item = self.cantidad * self.precio_unitario

        super().save(*args, **kwargs)

        # Actualizar el total de la orden
        self.pedido.actualizar_total()

    def __str__(self):
        return f"{self.cantidad} x {self.articulo.descripcion}"

    class Meta:
        db_table = "items_ordenes_compra_cliente"
