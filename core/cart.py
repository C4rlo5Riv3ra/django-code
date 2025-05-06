from decimal import Decimal 
from django.conf import settings 
from .models import Articulo

class Cart: 
    """ 
    Clase para gestionar el carrito de compras mediante sesiones 
    """
    def __init__(self, request): 
        """ 
        Inicializa el carrito 
        """ 
        self.session = request.session 
        cart = self.session.get('cart') 
        if not cart: 
            # Crear un carrito vacío si no existe 
            cart = self.session['cart'] = {} 
            self.cart = cart 
    def add(self, articulo, cantidad=1, update_cantidad=False): 
        """ 
        Añadir un producto al carrito o actualizar su cantidad 
        """ 
        articulo_id = str(articulo.articulo_id) 
        if articulo_id not in self.cart: 
            # Obtener el precio del artículo 
            try: 
                lista_precio = articulo.listaprecio 
                precio = float(lista_precio.precio_1) 
            except: 
                precio = 0 

        self.cart[articulo_id] = { 
            'cantidad': 0, 
            'precio': precio, 
            'descripcion': articulo.descripcion 
        } 
        if update_cantidad: 
            self.cart[articulo_id]['cantidad'] = cantidad 
        else: 
            self.cart[articulo_id]['cantidad'] += cantidad 
            self.save() 
    def save(self): 
        """ 
        Guardar los cambios en la sesión 
        """ 
        self.session.modified = True
        
    def remove(self, articulo): 
        """ 
        Eliminar un producto del carrito 
        """ 
        articulo_id = str(articulo.articulo_id) 
        if articulo_id in self.cart: 
            del self.cart[articulo_id] 
            self.save() 
    def __iter__(self): 
        """ 
        Iterar sobre los elementos en el carrito y obtener los artículos de la 
        base de datos 
        """ 
        articulo_ids = self.cart.keys() 
        articulos = Articulo.objects.filter(articulo_id__in=articulo_ids) 
        cart = self.cart.copy() 
        for articulo in articulos: 
            cart[str(articulo.articulo_id)]['articulo'] = articulo 

            for item in cart.values(): 
                item['precio'] = Decimal(item['precio']) 
                item['total_precio'] = item['precio'] * item['cantidad'] 
                yield item 

    def __len__(self): 
        """ 
        Contar todos los items en el carrito 
        """ 
        return sum(item['cantidad'] for item in self.cart.values()) 
    
    def get_total_price(self):
        """ 
        Calcular el costo total de los items 
        """ 
        return sum(Decimal(item['precio']) * item['cantidad'] for item in self.cart.values()) 
    
    def clear(self): 
        """ 
        Eliminar el carrito de la sesión 
        """ 
        del self.session['cart'] 
        self.save()