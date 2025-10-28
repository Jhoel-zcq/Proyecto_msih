from django.contrib import admin

# Register your models here.
# blog/admin.py
from .models import Post , EjercicioTiempoDistancia , Ejercicios_vectores

admin.site.register(Post)

admin.site.register(EjercicioTiempoDistancia)
admin.site.register(Ejercicios_vectores)