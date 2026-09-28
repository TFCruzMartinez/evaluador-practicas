from django.db import models
from django.utils import timezone


class Registro(models.Model):
    semestre = models.IntegerField()
    horas_disponibles = models.IntegerField()
    resultado = models.CharField(max_length=200)
    fecha = models.DateTimeField(default=timezone.now)

    # Borrado lógico
    eliminado = models.BooleanField(default=False)
    fecha_eliminacion = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ["-fecha"]

    def __str__(self):
        return f"Semestre {self.semestre} - {self.resultado}"

    def soft_delete(self):
        self.eliminado = True
        self.fecha_eliminacion = timezone.now()
        self.save()