from __future__ import unicode_literals
from django.db import models

# Create your models here.
class Debito(models.Model):
    cuenta = models.ForeignKey(Usuario, null=False, blank=False, on_delete=models.CASCADE)
    monto = models.DecimalField(max_digits=6, decimal_places=2, default=0, blank=True, null=False)
    descripcion = models.TextField(blank=True, null=True)
    fecha_reg = models.DateField(auto_now=False, auto_now_add=False)
    def __unicode__(self):
        return '{}'.format(self.cuenta, self.descripcion, self.fecha_reg)
