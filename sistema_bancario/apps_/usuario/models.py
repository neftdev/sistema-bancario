from __future__ import unicode_literals
from django.db import models

# Create your models here.

class Rol(models.Model):
    nombre = models.CharField(max_length=20)
    descripcion = models.CharField(max_length=50)
    def __unicode__(self):
        return '{}'.format(self.nombre)

class Usuario(models.Model):
    cod_usuario = models.AutoField(primary_key=True)
    full_name = models.CharField(max_length=30, unique=True)
    nick_name = models.CharField(max_length=12, unique=True)
    correo = models.CharField(max_length=30, unique=True)
    password = models.CharField(max_length=8)
    monto = models.DecimalField(max_digits=5, decimal_places=2)
    rol = models.ForeignKey(Rol, null=False, blank=False, on_delete=models.CASCADE)
    def __unicode__(self):
        return '{}({})'.format(self.nick_name, self.correo)
