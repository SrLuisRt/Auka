from django.db import models
from django.utils import timezone

class NewsItem(models.Model):
    titulo = models.CharField(max_length=100)
    contenido = models.TextField()
    creado_en = models.DateTimeField(auto_now_add=True)
    actualizado_en = models.DateTimeField(auto_now=True)
    publicado = models.BooleanField(default=True)
    fecha_expiracion = models.DateField(null=True, blank=True, verbose_name="Fecha de expiración")

    class Meta:
        verbose_name = 'Noticia'
        verbose_name_plural = 'Noticias'
        ordering = ['-creado_en']

    def __str__(self):
        return self.titulo
    
    @property
    def dias_restantes(self):
        """Devuelve el número de días que faltan para expirar.
           Si no tiene fecha, devuelve None."""
        if self.fecha_expiracion:
            hoy = timezone.now().date()
            delta = self.fecha_expiracion - hoy
            return delta.days
        return None