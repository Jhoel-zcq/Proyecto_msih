# blog/urls.py
from django.urls import path
from . import views
from django.contrib import admin
from django.urls import include

urlpatterns = [
    path('', views.index, name='index'),
    path('ejercitar/',views.ejercitar, name="ejercitar"),
    path('sandbox/', views.sandbox, name="sandbox"),
    path('index/',views.index, name= " index"),
    path('admin/', admin.site.urls),
    path('posts/', views.lista_posts, name='lista_posts'), # conectar la app blogconecta con la pagina index
    path('funcion_sandbox/',views.funcion_sandbox, name= "funcion_sandbox"),
    path('funcion_ejercitar/',views.funcion_ejercitar, name="funcion_ejercitar"),
]

# miweb/urls.pys
