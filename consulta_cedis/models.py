from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

# Create your models here.
class Consulta(models.Model):
    created = models.DateTimeField(default=timezone.now)
    fecha_inicial = models.DateField(blank=True, null=True)
    fecha_final = models.DateField(blank=True, null=True)
    user = models.ForeignKey(User, on_delete=models.PROTECT, blank=True, null=True)
    tipo_consulta = (
        ("1", 'Consulta de UDIS'),
        ("2", 'Consulta de TIIE'),
    )
    tipo = models.CharField(max_length=1, choices=tipo_consulta, default="1")
        
    def __str__(self):
        return str(self.id)