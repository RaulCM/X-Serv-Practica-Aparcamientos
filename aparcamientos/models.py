from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class Aparcamiento(models.Model):
    nombre = models.CharField(max_length=64, default="")
    url = models.URLField(max_length=300, default="")
    descripcion = models.TextField(default="")
    direccion = models.TextField(default="")
    barrio = models.CharField(max_length=200, default="")
    distrito = models.CharField(max_length=200, default="")
    coordX = models.CharField(max_length=200, default="")
    coordY = models.CharField(max_length=200, default="")
    latitud = models.CharField(max_length=200, default="")
    longitud = models.CharField(max_length=200, default="")
    telefono = models.CharField(max_length=200, default="")
    clasevial = models.CharField(max_length=200, default="")
    nombrevia = models.CharField(max_length=200, default="")
    tiponum = models.CharField(max_length=200, default="")
    num = models.CharField(max_length=200, default="")
    localidad = models.CharField(max_length=200, default="")
    provincia = models.CharField(max_length=200, default="")
    codigopostal = models.CharField(max_length=200, default="")
    email = models.URLField(max_length=200, default="")
    nComentarios = models.IntegerField(default=0)
    accesibilidad = models.IntegerField(default=0)
    entidad = models.CharField(max_length=200, default="")


class PaginaUsuario(models.Model):
    usuario = models.OneToOneField(User)
    titulo = models.CharField(max_length=200, default="")
    accesibilidad = models.IntegerField(default=0)
    color = models.CharField(max_length=200, default="")
    size = models.CharField(max_length=200, default="")


class Comentarios(models.Model):
    aparcamiento = models.ForeignKey(Aparcamiento)
    texto = models.TextField(max_length=300, default="")


class Elegidos(models.Model):
    aparcamiento = models.ForeignKey(Aparcamiento)
    usuario = models.ForeignKey(User)
    fecha = models.DateTimeField()
