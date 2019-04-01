from __future__ import unicode_literals
from django.db import models

# Create your models here.


class Rol(models.Model):
    nombre = models.CharField(max_length=20)
    descripcion = models.TextField(blank=True, null=True)

    def __unicode__(self):
        return '{}'.format(self.nombre)


class Usuario(models.Model):
    cod_usuario = models.AutoField(primary_key=True)

    full_name = models.CharField(max_length=100, blank=False, null=False)

    nick_name = models.CharField(
        max_length=12, unique=True, blank=False, null=False)

    correo = models.EmailField(unique=True, blank=False, null=False)

    password = models.CharField(max_length=20, blank=False, null=False)

    monto = models.DecimalField(
        max_digits=6, decimal_places=2, default=0, blank=True, null=False)

    rol = models.ForeignKey(Rol, null=False, blank=False,
                            on_delete=models.CASCADE)

    def __unicode__(self):
        return '{} ({})'.format(self.nick_name, self.correo_e)
