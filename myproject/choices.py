from django.db import models

class estadoEntidades(models.IntegerChoices):
    ACTIVO = 1, 'Activo'
    DE_BAJA = 2, 'De baja'
