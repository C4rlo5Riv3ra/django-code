from django.shortcuts import render, redirect, get_object_or_404 
from django.core.paginator import Paginator 
from django.contrib.auth.decorators import login_required 
from django.contrib import messages 
from django.http import JsonResponse 
import uuid 
from .models import *
from .forms import *
from django.views.decorators.http import require_POST 
from .cart import Cart 

@login_required 
def home(request): 
    """Vista para la página principal""" 
    # Obtener datos para los widgets 
    total_articulos = Articulo.objects.count() 
    total_usuarios = 0  # Obtener de tu modelo Usuario 
    bajo_stock = Articulo.objects.filter(stock__lt=10).count() 
    context = {
        'total_articulos': total_articulos, 
        'total_usuarios': total_usuarios, 
        'bajo_stock': bajo_stock, 
        'ventas_hoy': 0,  # En un caso real, calcularías las ventas del día 
    } 
    return render(request, 'core/index.html', context) 


@login_required 
def articulos_list(request): 
    """Vista para listar artículos""" 
    articulos_list = Articulo.objects.all() 
    # Filtros (podrías expandir esto) 
    q = request.GET.get('q') 
    if q: 
        articulos_list = articulos_list.filter(descripcion__icontains=q) 
    # Paginación 
    paginator = Paginator(articulos_list, 15)  # 15 artículos por página 
    page_number = request.GET.get('page') 
    articulos = paginator.get_page(page_number) 
    context = { 
        'articulos': articulos, 
    } 
    return render(request, 'core/articulos/list.html', context)


@login_required 
def articulo_detail(request, articulo_id): 
    """Vista para ver el detalle de un artículo""" 
    articulo = get_object_or_404(Articulo, articulo_id=articulo_id) 

    # Guardar en el historial de productos visitados
    if 'viewed_products' not in request.session: request.session['viewed_products'] = [] 

    # Convertir UUID a string para poder guardarlo en sesión 
    producto_actual = str(articulo.articulo_id) 
    viewed_products = request.session['viewed_products']

    # Eliminar si ya existe y añadir al principio 
    if producto_actual in viewed_products: 
        viewed_products.remove(producto_actual) 
    
    # Añadir al principio y mantener solo los últimos 5 
    viewed_products.insert(0, producto_actual) 
    request.session['viewed_products'] = viewed_products[:5] 
    request.session.modified = True

    # Obtener productos visitados recientemente 
    recent_products = [] 

    if viewed_products: 
        recent_uuids = [uuid.UUID(id_str) for id_str in viewed_products[1:6]]  # Excluir el actual 

    if recent_uuids: 
        recent_products = Articulo.objects.filter(articulo_id__in=recent_uuids) 

    context = { 
        'articulo': articulo, 
        'recent_products': recent_products,
    } 
    return render(request, 'core/articulos/detail.html', context) 


@login_required 
def articulo_create(request): 

    """Vista para crear un nuevo artículo""" 
    if request.method == 'POST': 
        form = ArticuloForm(request.POST) 
        precio_form = ListaPrecioForm(request.POST) 

        if form.is_valid() and precio_form.is_valid(): 
            # Generar ID para el artículo 
            articulo = form.save(commit=False) 
            articulo.articulo_id = uuid.uuid4()
            articulo.save()
            # Guardar precios 
            lista_precio = precio_form.save(commit=False) 
            lista_precio.articulo = articulo 
            lista_precio.save() 
            messages.success(request, 'Artículo creado correctamente.') 
            return redirect('articulo_detail', articulo_id=articulo.articulo_id) 
    else: 
        form = ArticuloForm() 
        precio_form = ListaPrecioForm() 

    context = { 
        'form': form, 
        'precio_form': precio_form, 
    } 

    return render(request, 'core/articulos/form.html', context) 

@login_required 
def articulo_edit(request, articulo_id): 
    """Vista para editar un artículo existente""" 
    articulo = get_object_or_404(Articulo, articulo_id=articulo_id) 
    lista_precio = get_object_or_404(ListaPrecio, articulo=articulo) 
    if request.method == 'POST': 
        form = ArticuloForm(request.POST, instance=articulo)
        precio_form = ListaPrecioForm(request.POST, instance=lista_precio) 
        if form.is_valid() and precio_form.is_valid(): 
            form.save() 
            precio_form.save() 
            messages.success(request, 'Artículo actualizado correctamente.') 
            return redirect('articulo_detail',articulo_id=articulo.articulo_id) 
    else: 
        form = ArticuloForm(instance=articulo) 
        precio_form = ListaPrecioForm(instance=lista_precio) 

    context = { 
        'form': form, 
        'precio_form': precio_form, 
    }

    return render(request, 'core/articulos/form.html', context) 


@login_required 
def articulo_delete(request, articulo_id): 
    """Vista para eliminar un artículo""" 
    articulo = get_object_or_404(Articulo, articulo_id=articulo_id) 

    if request.method == 'POST': 
        articulo.delete() 
        messages.success(request, 'Artículo eliminado correctamente.') 
        return redirect('articulos_list') 
    
    context = { 
    'articulo': articulo, 
    } 

    return render(request, 'core/articulos/delete.html', context)

# Vistas para obtener información por AJAX 
@login_required 
def get_lineas_por_grupo(request, grupo_id): 
    """API para obtener líneas de artículo según el grupo seleccionado""" 
    lineas = LineaArticulo.objects.filter(grupo_id=grupo_id, estado=1) 
    data = [{'id': str(linea.linea_id), 'nombre': linea.nombre_linea} for linea in lineas] 
    return JsonResponse(data, safe=False) 

@require_POST 
def cart_add(request, articulo_id): 
    """ 
    Añadir artículo al carrito 
    """ 
    cart = Cart(request) 
    articulo = get_object_or_404(Articulo, articulo_id=articulo_id) 
    cantidad = int(request.POST.get('cantidad', 1)) 
    update = request.POST.get('update') 
    cart.add(articulo=articulo, cantidad=cantidad, update_cantidad=update) 

    messages.success(request, f'"{articulo.descripcion}" añadido al carrito.') 
    return redirect('cart_detail')


def cart_remove(request, articulo_id): 
    """ 
    Eliminar artículo del carrito 
    """ 
    cart = Cart(request) 
    articulo = get_object_or_404(Articulo, articulo_id=articulo_id) 
    cart.remove(articulo) 
    messages.info(request, f'"{articulo.descripcion}" eliminado del carrito.') 
    return redirect('cart_detail') 

def cart_detail(request): 
    """ 
    Ver detalle del carrito 
    """ 
    cart = Cart(request) 
    return render(request, 'core/cart/detail.html', {'cart': cart}) 

def cart_clear(request): 
    """ 
    Vaciar el carrito 
    """ 
    cart = Cart(request) 
    cart.clear() 

    messages.info(request, 'Carrito vaciado correctamente.') 
    return redirect('cart_detail')

@login_required 
def checkout(request): 
    """ 
    Finalizar compra 
    """ 
    cart = Cart(request)
    if len(cart) == 0: 
        messages.warning(request, 'Tu carrito está vacío') 
        return redirect('cart_detail') 
    
    # Obtener o crear cliente para el usuario 
    try: 
        cliente = Cliente.objects.get(correo_electronico=request.user.email)

    except Cliente.DoesNotExist: 
        # Obtener tipo de identificación predeterminado (puedes ajustar según tus datos) 
        try:  
            tipo_id = TipoIdentificacion.objects.first() 
            canal = CanalCliente.objects.first() 

            # Crear cliente con datos básicos del usuario 
            cliente = Cliente.objects.create( 
                cliente_id=uuid.uuid4(), 
                tipo_identificacion=tipo_id, 
                nro_documento=request.user.username[:11],
                nombres=request.user.full_name, 
                correo_electronico=request.user.email, 
                canal=canal, 
                estado=estadoEntidades.ACTIVO 
            ) 
        except: 
            messages.error(request, 'Error al procesar el cliente. Contacte al administrador.') 
            return redirect('cart_detail')
        # Obtener vendedor predeterminado para la orden 
    try: 
        vendedor = Vendedor.objects.first() 
    except: 
        messages.error(request, 'No hay vendedores disponibles. Contacte al administrador.') 
        return redirect('cart_detail') 
    if request.method == 'POST': 
        # Crear la orden 
        try: 
            orden = OrdenCompraCliente.objects.create( 
                pedido_id=uuid.uuid4(), 
                cliente=cliente, 
                vendedor=vendedor, 
                estado=EstadoOrden.PENDIENTE, 
                notas=request.POST.get('notas', ''), 
                creado_por=request.user 
            ) 
            # Crear los items de la orden 
            for item in cart: 
                articulo = item['articulo'] 
                ItemOrdenCompraCliente.objects.create( 
                    item_id=uuid.uuid4(), 
                    pedido=orden, 
                    nro_item=1,  # Puedes implementar una secuencia 
                    articulo=articulo, 
                    cantidad=item['cantidad'], 
                    precio_unitario=item['precio'], 
                    creado_por=request.user 
                ) 
            # Limpiar el carrito 
            cart.clear()
            messages.success(request, f'¡Orden creada exitosamente! Tu número de orden es: {orden.nro_pedido}')
            return redirect('order_detail', pedido_id=orden.pedido_id) 
        
        except Exception as e: 
            messages.error(request, f'Error al procesar la orden: {str(e)}') 
            return redirect('cart_detail')
    
    return render(request, 'core/cart/checkout.html', { 'cart': cart, 'cliente': cliente })


@login_required 
def order_detail(request, pedido_id): 
    """ 
    Ver detalle de una orden 
    """ 
    orden = get_object_or_404(OrdenCompraCliente, pedido_id=pedido_id) 
    # Verificar que la orden pertenece al usuario actual 
    if orden.cliente.correo_electronico != request.user.email and not request.user.is_staff: 
        messages.error(request, 'No tienes permiso para ver esta orden.') 
        return redirect('home') 
    return render(request, 'core/cart/order_detail.html', {'orden': orden}) 
