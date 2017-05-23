from django.contrib import admin
from aparcamientos.models import Aparcamiento, PaginaUsuario, Comentarios
from aparcamientos.models import Elegidos


# Register your models here.

admin.site.register(Aparcamiento)
admin.site.register(PaginaUsuario)
admin.site.register(Comentarios)
admin.site.register(Elegidos)
