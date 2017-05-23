"""myproject URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.8/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import include, url
from django.contrib import admin
from aparcamientos import views
from django.views.static import serve
from myproject import settings
from django.contrib.auth.views import login, logout

urlpatterns = [
    url(r'static/terrafirma/default\.css$', views.css),
    url(r'static/(?P<path>.*)$', serve, {'document_root':
        '/home/raul/sat/X-Serv-Practica-Aparcamientos/templates/'}),
    url(r'^about$', views.about, name="Información"),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^$', views.main, name="Pagina principal"),
    url(r'^aparcamientos$', views.parkings,
        name="Página con todos los aparcamientos"),
    url(r'^aparcamientos/(\d+)$', views.parking,
        name="Página de un aparcamiento"),
    url(r'^logout$', views.logout_view),
    url(r'^login$', views.login_view),
    url(r'^(.+)/xml', views.xml, name=""),
    url(r'^(.+)', views.user, name="Pagina personal del usuario"),
]
