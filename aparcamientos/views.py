from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.models import User
from aparcamientos.models import Aparcamiento, PaginaUsuario, Comentarios
from aparcamientos.models import Elegidos
from bs4 import BeautifulSoup
import urllib
from django.template.loader import get_template
from django.template import Context, RequestContext
from django.contrib.auth import authenticate, login, logout
import datetime


def parser():
    web = 'http://datos.munimadrid.es/portal/site/egob/menuitem.ac61933d6ee3c'
    web += '31cae77ae7784f1a5a0/?vgnextoid=00149033f2201410VgnVCM100000171f5a'
    web += '0aRCRD&format=xml&file=0&filename=202584-0-aparcamientos-resident'
    web += 'es&mgmtid=e84276ac109d3410VgnVCM2000000c205a0aRCRD&preview=full'
    fil = urllib.request.urlopen(web)
    soup = BeautifulSoup(fil, 'html.parser')
    for contenido in soup.findAll('contenido'):
        record = Aparcamiento()
        for atributo in contenido.findAll('atributo'):
            if atributo.attrs["nombre"] == "ID-ENTIDAD":
                record.entidad = atributo.string
            if atributo.attrs["nombre"] == "NOMBRE":
                record.nombre = atributo.string
            if atributo.attrs["nombre"] == "CONTENT-URL":
                record.url = atributo.string
            if atributo.attrs["nombre"] == "DISTRITO":
                record.distrito = atributo.string
            if atributo.attrs["nombre"] == "BARRIO":
                record.barrio = atributo.string
            if atributo.attrs["nombre"] == "COORDENADA-X":
                record.coordX = atributo.string
            if atributo.attrs["nombre"] == "COORDENADA-Y":
                record.coordY = atributo.string
            if atributo.attrs["nombre"] == "LATITUD":
                record.latitud = atributo.string
            if atributo.attrs["nombre"] == "LONGITUD":
                record.longitud = atributo.string
            if atributo.attrs["nombre"] == "DESCRIPCION":
                record.descripcion = atributo.string
            if atributo.attrs["nombre"] == "TELEFONO":
                record.telefono = atributo.string
            if atributo.attrs["nombre"] == "EMAIL":
                record.email = atributo.string
            if atributo.attrs["nombre"] == "ACCESIBILIDAD":
                record.accesibilidad = atributo.string
            if atributo.attrs["nombre"] == "CLASE-VIAL":
                record.clasevial = atributo.string
            if atributo.attrs["nombre"] == "NOMBRE-VIA":
                record.nombrevia = atributo.string.replace("&", "&amp")
            if atributo.attrs["nombre"] == "TIPO-NUM":
                record.tiponum = atributo.string
            if atributo.attrs["nombre"] == "NUM":
                record.num = atributo.string
            if atributo.attrs["nombre"] == "LOCALIDAD":
                record.localidad = atributo.string
            if atributo.attrs["nombre"] == "PROVINCIA":
                record.provincia = atributo.string
            if atributo.attrs["nombre"] == "CODIGO-POSTAL":
                record.codigopostal = atributo.string
        direccion = (record.clasevial + " " + record.nombrevia + " " +
                     record.num + " " + record.localidad + " " +
                     record.provincia + " " + record.codigopostal)
        record.direccion = direccion
        record.save()


# Create your views here.


@csrf_exempt
def main(request):
    template = get_template("terrafirma/index.html")
    parkings = ""
    lista_aparcamientos = Aparcamiento.objects.all()
    if len(lista_aparcamientos) == 0:
        if request.method == 'GET':
            boton = "<form method = 'POST'><button type='submit' "
            boton += "name='Cargar' value=1>Cargar información de "
            boton += "aparcamientos</button><br>"
            c = RequestContext(request, {'boton': boton})
        elif request.method == 'POST':
            datos = request.body.decode('utf-8').split("=")[1]
            parser()
            return HttpResponseRedirect('/')
        else:
            template = get_template("terrafirma/error.html")
            c = RequestContext(request, {'error': "Method not allowed"})
            response = template.render(c)
            return HttpResponse(response, status=405)
    else:
        if request.method == 'GET':
            lista_aparcamientos = Aparcamiento.objects.all().order_by('-nComentarios')
            lista_aparcamientos = lista_aparcamientos.exclude(nComentarios=0)
            lista_aparcamientos = lista_aparcamientos[0:5]
            boton = "<form method = 'POST'><button type='submit' "
            boton += "name='Accesibilidad' value=1>"
            boton += "Mostrar aparcamientos accesibles</button>"
        elif request.method == 'POST':
            accesibilidad = request.body.decode('utf-8').split("=")[1]
            if int(accesibilidad) == 1:
                lista_aparcamientos = Aparcamiento.objects.all().order_by('-nComentarios')
                lista_aparcamientos = lista_aparcamientos.exclude(nComentarios=0)
                lista_aparcamientos = lista_aparcamientos.filter(accesibilidad=1)
                lista_aparcamientos = lista_aparcamientos[0:5]
                boton = "<form method = 'POST'><button type='submit' "
                boton += "name='Accesibilidad' value=0>Mostrar "
                boton += "todos los aparcamientos</button>"
            elif int(accesibilidad) == 0:
                lista_aparcamientos = Aparcamiento.objects.all().order_by('-nComentarios')
                lista_aparcamientos = lista_aparcamientos.exclude(nComentarios=0)
                lista_aparcamientos = lista_aparcamientos[0:5]
                boton = "<form method = 'POST'><button type='submit' "
                boton += "name='Accesibilidad' value=1>"
                boton += "Mostrar aparcamientos accesibles</button>"
        else:
            template = get_template("terrafirma/error.html")
            c = RequestContext(request, {'error': "Method not allowed"})
            response = template.render(c)
            return HttpResponse(response, status=405)
        lista_personales = ""
        lista_usuarios = User.objects.all()
        for user in lista_usuarios:
            try:
                titulo = PaginaUsuario.objects.get(usuario=user.id).titulo
                if titulo == "":
                    lista_personales += "<a href='/" + user.username + "'>Pagi"
                    lista_personales += "na de " + user.username + "</a><br>"
                else:
                    lista_personales += "<a href='/" + user.username + "'>"
                    lista_personales += titulo + "</a><br>"
            except PaginaUsuario.DoesNotExist:
                lista_personales += "<a href='/" + user.username + "'>Pagina "
                lista_personales += "de " + user.username + "</a><br>"
        c = RequestContext(request, {'Lateral': lista_personales, 'aparcamientos': lista_aparcamientos, 'boton': boton})
    response = template.render(c)
    return HttpResponse(response, status=200)


def formulariolista(request, resource):
    if str(request.user) == str(resource):
        formulario = "<form id='formTitulo' action='/" + str(resource)
        formulario += "' method='POST'>Introduce un nuevo titulo para "
        formulario += "tu lista personal: <br><input type='text' "
        formulario += "name='Titulo'><input type='submit'"
        formulario += " value='Enviar'></form>"
        formulario += "<form id='formTitulo' action='/" + str(resource)
        formulario += "' method='POST'>Introduce un nuevo color de fondo "
        formulario += "para tu lista personal: <br><input type='text' "
        formulario += "name='Color'><input type='submit'"
        formulario += " value='Enviar'></form>"
        formulario += "<form id='formTitulo' action='/" + str(resource)
        formulario += "' method='POST'>Introduce un nuevo tamaño de letra "
        formulario += "para tu lista personal: <br><input type='text' "
        formulario += "name='Size'><input type='submit'"
        formulario += " value='Enviar'></form>"
    else:
        formulario = ""
    return (formulario)


def aparcamientoselegidos(request, resource):
    usuario = User.objects.get(username=resource)
    elegidos = Elegidos.objects.filter(usuario=usuario)
    opcion = request.body.decode('utf-8').split("=")[0]
    anterior = ""
    siguiente = ""
    if opcion == 'next':
        n = request.body.decode('utf-8').split("=")[1]
        m = int(n)+5
        anterior = "<form action='/" + resource + "' method='POST'><button"
        anterior += " type='submit' name='previous' value='" + n + "'"
        anterior += " class='btn-link'>Anterior</button></form>"
        if len(elegidos) >= m:
            siguiente = "<form action='/" + resource + "' method='POST'><button"
            siguiente += " type='submit' name='next' value='" + str(m) + "'"
            siguiente += " class='btn-link'>Siguiente</button></form>"
        else:
            siguiente = ""
        elegidos = elegidos[int(n):m]
    elif opcion == 'previous':
        m = request.body.decode('utf-8').split("=")[1]
        n = int(m)-5
        if n == 0:
            anterior = ""
        else:
            anterior = "<form action='/" + resource + "' method='POST'><button"
            anterior += " type='submit' name='previous' value='" + str(n) + "'"
            anterior += " class='btn-link'>Anterior</button></form>"
        siguiente = "<form action='/" + resource + "' method='POST'><button"
        siguiente += " type='submit' name='next' value='" + m + "'"
        siguiente += " class='btn-link'>Siguiente</button></form>"
        elegidos = elegidos[n:int(m)]
    else:
        if len(elegidos) > 5:
            elegidos = elegidos[0:5]
            anterior = ""
            siguiente = "<form action='/" + resource + "' method='POST'><button"
            siguiente += " type='submit' name='next' value='5'"
            siguiente += " class='btn-link'>Siguiente</button></form>"
    return(elegidos, siguiente, anterior)


@csrf_exempt
def user(request, resource):
    formulario = ""
    template = get_template("terrafirma/user.html")
    if request.method == 'GET':
        try:
            usuario = User.objects.get(username=resource)
            lista_personal = PaginaUsuario.objects.get(usuario=usuario)
            if lista_personal.titulo == "":
                titulo = "Página de " + usuario.username
            else:
                titulo = lista_personal.titulo
            formulario = formulariolista(request, resource)
        except User.DoesNotExist:
            template = get_template("terrafirma/error.html")
            c = RequestContext(request, {'error': "Usuario no existente"})
            response = template.render(c)
            return HttpResponse(response, status=404)
        except PaginaUsuario.DoesNotExist:
            pagina_personal = PaginaUsuario(usuario=usuario)
            pagina_personal.save()
            formulario = formulariolista(request, resource)
            response = "La lista esta vacia<br>" + formulario
            return HttpResponseRedirect('/' + resource)
    elif request.method == 'POST':
        opcion = request.body.decode('utf-8').split("=")[0]
        formulario = formulariolista(request, resource)
        if opcion == 'Titulo':
            if str(request.user) == str(resource):
                titulo = request.body.decode('utf-8').split("=")[1].replace("+", " ")
                usuario = User.objects.get(username=resource)
                pagina_personal = PaginaUsuario.objects.get(usuario=usuario)
                pagina_personal.titulo = titulo
                pagina_personal.save()
        elif opcion == 'Color':
            color = request.body.decode('utf-8').split("=")[1]
            usuario = User.objects.get(username=resource)
            pagina_personal = PaginaUsuario.objects.get(usuario=usuario)
            pagina_personal.color = color
            pagina_personal.save()
        elif opcion == 'Size':
            size = request.body.decode('utf-8').split("=")[1]
            usuario = User.objects.get(username=resource)
            pagina_personal = PaginaUsuario.objects.get(usuario=usuario)
            pagina_personal.size = size
            pagina_personal.save()
        elif opcion == 'next':
            (elegidos, siguiente, anterior) = aparcamientoselegidos(request, resource)
        elif opcion == 'previous':
            (elegidos, siguiente, anterior) = aparcamientoselegidos(request, resource)
    else:
        template = get_template("terrafirma/error.html")
        c = RequestContext(request, {'error': "Method not allowed"})
        response = template.render(c)
        return HttpResponse(response, status=405)
    (elegidos, siguiente, anterior) = aparcamientoselegidos(request, resource)
    c = RequestContext(request, {'elegidos': elegidos, 'formulario': formulario, 'siguiente': siguiente, 'anterior': anterior, 'usuario': resource})
    response = template.render(c)
    return HttpResponse(response, status=200)


@csrf_exempt
def parkings(request):
    response = ""
    parkings = ""
    if request.method == 'GET':
        lista_aparcamientos = Aparcamiento.objects.all()
        for a in lista_aparcamientos:
            parkings += "<a href='/aparcamientos/" + str(a.id)
            parkings += "'>" + a.nombre + "</a><br>"
        distritos = lista_aparcamientos.order_by().values_list('distrito', flat=True).distinct()
        formulario = "<form method='POST'>Filtrado por distrito: "
        formulario += "<select name='Distrito'>"
        for element in distritos:
            formulario += "<option value='" + element + "'>"
            formulario += element + "</option>"
        formulario += "</select><input type='submit' value='Enviar'></form>"
        response = formulario + parkings
    elif request.method == 'POST':
        distrito = request.body.decode('utf-8').split("=")[1]
        lista_aparcamientos = Aparcamiento.objects.all().filter(distrito=distrito)
        parkings += "Aparcamientos del distrito \"" + distrito + "\":<br>"
        for a in lista_aparcamientos:
            parkings += "<a href='/aparcamientos/" + str(a.id)
            parkings += "'>" + a.nombre + "</a><br>"
        distritos = Aparcamiento.objects.order_by().values_list('distrito', flat=True).distinct()
        formulario = "<form method='POST'>Filtrado por distrito: "
        formulario += "<select name='Distrito'>"
        for element in distritos:
            formulario += "<option value='" + element + "'>"
            formulario += element + "</option>"
        formulario += "</select><input type='submit' value='Enviar'></form>"
    else:
        template = get_template("terrafirma/error.html")
        c = RequestContext(request, {'error': "Method not allowed"})
        response = template.render(c)
        return HttpResponse(response, status=405)
    template = get_template("terrafirma/aparcamientos.html")
    c = RequestContext(request, {'Parkings': formulario + parkings})
    response = template.render(c)
    return HttpResponse(response, status=200)


@csrf_exempt
def parking(request, resource):
    response = ""
    template = get_template("terrafirma/aparcamiento.html")
    if request.method == 'GET':
        aparcamiento = Aparcamiento.objects.get(id=resource)
        comentarios = Comentarios.objects.all().filter(aparcamiento=aparcamiento)
    elif request.method == 'POST':
        opcion = request.body.decode('utf-8').split("=")[0]
        if opcion == 'Add':
            aparcamiento = Aparcamiento.objects.get(id=resource)
            elegido = Elegidos()
            elegido.aparcamiento = aparcamiento
            usuario = User.objects.get(username=request.user)
            elegido.usuario = usuario
            today = datetime.date.today()
            elegido.fecha = today
            elegidos = Elegidos.objects.filter(usuario=usuario)
            encontrado = False
            for a in elegidos:
                if a.aparcamiento == aparcamiento:
                    encontrado = True
            if encontrado is False:
                elegido.save()
            comentarios = Comentarios.objects.all().filter(aparcamiento=aparcamiento)
        elif opcion == 'Comentario':
            aparcamiento = Aparcamiento.objects.get(id=resource)
            comentario = Comentarios()
            comentario.aparcamiento = aparcamiento
            comentario.texto = request.body.decode('utf-8').split("=")[1].replace("+", " ")
            comentario.save()
            aparcamiento.nComentarios = aparcamiento.nComentarios + 1
            aparcamiento.save()
            comentarios = Comentarios.objects.all().filter(aparcamiento=aparcamiento)
    else:
        template = get_template("terrafirma/error.html")
        c = RequestContext(request, {'error': "Method not allowed"})
        response = template.render(c)
        return HttpResponse(response, status=405)
    c = RequestContext(request, {'aparcamiento': aparcamiento,
                       'comentarios': comentarios})
    response = template.render(c)
    return HttpResponse(response, status=200)


def xml(request, resource):
    try:
        usuario = User.objects.get(username=resource)
    except User.DoesNotExist:
        template = get_template('error.html')
        return HttpResponse(plantilla.render(), status=404)
    template = get_template('xml/canales_usuario.xml')
    elegidos = Elegidos.objects.filter(usuario=usuario)
    c = RequestContext(request, {'usuario': usuario, 'elegidos': elegidos})
    response = template.render(c)
    return HttpResponse(response, status=200, content_type="text/xml")


def xmlmain(request):
    template = get_template('xml/canales_main.xml')
    lista_aparcamientos = Aparcamiento.objects.all().order_by('-nComentarios')
    lista_aparcamientos = lista_aparcamientos.exclude(nComentarios=0)
    lista_aparcamientos = lista_aparcamientos.filter(accesibilidad=0)
    lista_aparcamientos = lista_aparcamientos[0:5]
    c = RequestContext(request, {'aparcamientos': lista_aparcamientos})
    response = template.render(c)
    return HttpResponse(response, status=200, content_type="text/xml")


def json(request):
    template = get_template('json/canales_main.json')
    lista_aparcamientos = Aparcamiento.objects.all().order_by('-nComentarios')
    lista_aparcamientos = lista_aparcamientos.exclude(nComentarios=0)
    lista_aparcamientos = lista_aparcamientos.filter(accesibilidad=0)
    lista_aparcamientos = lista_aparcamientos[0:5]
    c = RequestContext(request, {'aparcamientos': lista_aparcamientos})
    response = template.render(c)
    return HttpResponse(response, status=200, content_type="text/json")


def jsonusuario(request, resource):
    try:
        usuario = User.objects.get(username=resource)
    except User.DoesNotExist:
        template = get_template('error.html')
        return HttpResponse(plantilla.render(), status=404)
    template = get_template('json/canales_usuario.json')
    elegidos = Elegidos.objects.filter(usuario=usuario)
    c = RequestContext(request, {'usuario': usuario, 'elegidos': elegidos})
    response = template.render(c)
    return HttpResponse(response, status=200, content_type="text/json")


def rss(request):
    template = get_template('rss/canales_comentarios.rss')
    comentarios = Comentarios.objects.all()
    c = RequestContext(request, {'comentarios': comentarios})
    response = template.render(c)
    return HttpResponse(response, status=200, content_type="text/rss")



@csrf_exempt
def login_view(request):
    username = request.POST['username']
    password = request.POST['password']
    user = authenticate(username=username, password=password)
    if user is not None:
        login(request, user)
        return HttpResponseRedirect('/')
    else:
        return HttpResponseRedirect('/')


@csrf_exempt
def logout_view(request):
    if request.method == 'POST':
        logout(request)
    return HttpResponseRedirect('/')


@csrf_exempt
def registro(request):
    if request.method == 'GET':
        formulario = "Introduzca los datos del usuario a registrar:<br>"
        formulario += "<form class='register' method='POST' action='/registro'>"
        formulario += "<table><tr><td><label for='username'>Usuario:"
        formulario += " </label></td><td><input name='username'></td></tr><tr>"
        formulario += "<td><label for='password'>Contraseña: </label></td>"
        formulario += "<td><input name='password' type='password'></td></tr>"
        formulario += "</table><input class='boton' type='submit' "
        formulario += "value='Registrar'></form>"
    elif request.method == 'POST':
        formulario = ""
        username = request.POST['username']
        password = request.POST['password']
        usuario = User.objects.create_user(username = username, password = password)
        usuario.save()
        return HttpResponseRedirect('/')
    else:
        template = get_template("terrafirma/error.html")
        c = RequestContext(request, {'error': "Method not allowed"})
        response = template.render(c)
        return HttpResponse(response, status=405)
    template = get_template("terrafirma/registro.html")
    c = RequestContext(request, {'formulario': formulario})
    response = template.render(c)
    return HttpResponse(response, status=200)

def about(request):
    template = get_template('terrafirma/about.html')
    c = RequestContext(request)
    response = template.render(c)
    return HttpResponse(response, status=200)


def css(request):
    if request.user.is_authenticated():
        usuario = User.objects.get(username=request.user.username)
        pagina_personal = PaginaUsuario.objects.get(usuario=usuario)
        color = pagina_personal.color
        size = pagina_personal.size + "px"
        template = get_template("terrafirma/default.css")
        c = Context({'size': size, 'color': color})
        response = template.render(c)
        return HttpResponse(response, content_type="text/css")
    else:
        template = get_template("terrafirma/default.css")
        color = '#8C8C73'
        size = '11px'
        c = Context({'size': size, 'color': color})
        response = template.render()
        return HttpResponse(response, content_type="text/css")
