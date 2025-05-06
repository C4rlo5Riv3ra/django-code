from django.db import models

class estadoEntidades(models.IntegerChoices):
    ACTIVO = 1, 'Activo'
    DE_BAJA = 2, 'De baja'

class EstadoOrden(models.IntegerChoices): 
    PENDIENTE = 1, "Pendiente" 
    PROCESANDO = 2, "Procesando" 
    COMPLETADA = 3, "Completada" 
    CANCELADA = 4, "Cancelada" 