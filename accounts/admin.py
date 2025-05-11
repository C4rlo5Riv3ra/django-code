from django.contrib import admin
from .models import Perfil, Usuario, DispositivoMovil, UbicacionDispositivo

# Register your models here.
admin.site.register(Perfil)
admin.site.register(Usuario)
admin.site.register(DispositivoMovil)
admin.site.register(UbicacionDispositivo)
