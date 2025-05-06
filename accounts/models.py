
from django.db import models 
from django.contrib.auth.models import AbstractUser 
#from easysales_api.helpers import photo_path_aws_instance 
#from easysales_api.constants import OPERADORES 
from django.contrib.auth.models import Group, Permission 

# Create your models here. 
class Perfil(models.Model): 
    perfil_id = models.IntegerField(primary_key=True) 
    perfil_nombre = models.CharField(max_length=100, null=False) 
    def __str__(self): 
        return '%d: %s' % (self.perfil_id, self.perfil_nombre) 
    class Meta: 
        db_table = 'perfiles'

class Usuario(AbstractUser): 
    username = models.CharField(max_length=25, blank = False, null = False, 
    unique = True,primary_key=True) 
    full_name = models.CharField(max_length=100, null=False,blank=False) 
    email = models.EmailField(null=False, unique=True)
    #avatar = models.ImageField(upload_to=photo_path_aws_instance, blank=True, null=True) 
    mobile = models.CharField(max_length=15) 
    perfil = models.ForeignKey(Perfil,null=False,on_delete=models.RESTRICT,related_name="perfiles_usuarios") 
    
    # unidades = models 
    # Override these two fields to fix the reverse accessor clashes 
    groups = models.ManyToManyField( 'auth.Group', verbose_name='groups', blank=True, 
        help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', 
        related_name='usuario_set', 
        related_query_name='usuario', 
    ) 

    user_permissions = models.ManyToManyField( 'auth.Permission', verbose_name='user permissions', blank=True, 
        help_text='Specific permissions for this user.', 
        related_name='usuario_set', 
        related_query_name='usuario', 
    ) 

    USERNAME_FIELD = 'username' 
    REQUIRED_FIELDS = ['full_name','perfil_id','email'] 

    class Meta: 
        db_table = "usuarios"   

    def __str__(self): 
        return self.full_name     

class DispositivoMovil(models.Model): 
    imei = models.CharField(max_length=20, unique=True, verbose_name="IMEI") 
    numero_celular = models.CharField(max_length=15, verbose_name="Número de celular") 
    # operador = models.CharField(max_length=10, choices=OPERADORES, verbose_name="Operador") 
    marca = models.CharField(max_length=50, null=True, blank=True) 
    modelo = models.CharField(max_length=50, null=True, blank=True) 
    sistema_operativo = models.CharField(max_length=50, null=True, blank=True)
    version_so = models.CharField(max_length=20, null=True, blank=True) 
    fecha_registro = models.DateTimeField(auto_now_add=True) 

    def __str__(self): 
        return f"{self.numero_celular} - {self.operador}" 
    
    class Meta: 
        db_table = "dispositivos"           
        verbose_name = "Dispositivo Móvil" 
        verbose_name_plural = "Dispositivos Móviles" 

class UbicacionDispositivo(models.Model): 
    dispositivo = models.ForeignKey('DispositivoMovil', 
    on_delete=models.CASCADE, related_name='ubicaciones') 
    latitud = models.DecimalField(max_digits=9, decimal_places=6) 
    longitud = models.DecimalField(max_digits=9, decimal_places=6) 
    precision = models.FloatField(null=True, blank=True, help_text="Precisión en metros") 
    altitud = models.FloatField(null=True, blank=True) 
    velocidad = models.FloatField(null=True, blank=True, help_text="Velocidad en m/s") 
    fecha_hora = models.DateTimeField(auto_now_add=True) 

    def __str__(self): 
        return f"Ubicación de {self.dispositivo.numero_celular} - {self.fecha_hora.strftime('%Y-%m-%d %H:%M:%S')}"
    
    class Meta: 
        db_table = "ubicacion_dispositivos"           
        verbose_name = "Ubicación de Dispositivo" 
        verbose_name_plural = "Ubicaciones de Dispositivos" 
        ordering = ['-fecha_hora']