from __future__ import unicode_literals
from django.db import models

# Create your models here.
class Usuario(models.Model):
    rol = models.ForeignKey(Rol, null=False, blank=False, on_delete=models.CASCADE)
    nombre = models.CharField(max_length=10, unique=True)
    telefono = models.CharField(max_length=15, unique=True)
    dir = models.CharField(max_length=40)
    correo_e = models.CharField(max_length=20, unique=True)
    foto = models.FileField(upload_to='Images/%Y_%m_%d')
    password = models.CharField(max_length=30)
    fecha_reg = models.DateField(auto_now=False, auto_now_add=False)
    def __unicode__(self):
        return '{}({})'.format(self.nombre, self.correo_e)