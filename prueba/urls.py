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
    path('posts/', views.lista_posts, name='lista_posts'), # conectar la app blogconecta con la pagina index
    path('funcion_sandbox/',views.funcion_sandbox, name= "funcion_sandbox"),
    path('funcion_ejercitar/',views.funcion_ejercitar, name="funcion_ejercitar"),
    #fis100
    path('Tiempo_y_distancia/',views.Tiempo_y_distancia, name='Tiempo_y_distancia'),
    path('Medición/',views.Medición,name="Medición"),
    path('Rapidez_de_cambio/', views.Rapidez_de_cambio, name="Rapidez_de_cambio"),
    path('Vectores/', views.Vectores, name="Vectores"),
    path('Triangulo_vectorial/', views.Triangulo_vectorial, name='Triangulo_vectorial'),
    path('Descripción_de_movimiento/',views.Descripción_de_movimiento, name='Descripción_de_movimiento'),
    path('Fuerzas_y_leyes_de_Newton/', views.Fuerzas_y_leyes_de_Newton, name='Fuerzas_y_leyes_de_Newton'),
    #def aleatoria
    path('pagina_aleatoria_fis100/', views.pagina_aleatoria_fis100, name='pagina_aleatoria_fis100'),
    path('pagina_aleatoria_fis111/', views.pagina_aleatoria_fis111, name='pagina_aleatoria_fis111'),
    #fis111
    path('Cinematica/', views.Cinematica, name='Cinematica'),
    path('Principios_de_Newton/',views.Principios_de_Newton,name='Principios_de_Newton'),
    path('Trabajo_y_energia/',views.Trabajo_y_energia, name='Trabajo_y_energia'),
    #templates del sandbox
    path('Rapidez_de_cambio_sandbox/', views.rapidez_de_cambio_sandbox,name="Rapidez_de_cambio_sandbox" ),
    path('Vectores_sandbox', views.vectores_sandbox, name="Vectores_sandbox"),
    path('Triangulo_vectorial_sandbox/', views.triangulo_vectorial_sandbox, name="triangulo_vectorial_sandbox"),
    path('descripcion_de_movimiento_sandbox', views.descripcion_de_movimiento_sandbox, name="descripcion_de_movimiento_sandbox"),
]

# miweb/urls.pys
