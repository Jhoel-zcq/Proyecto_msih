from django.contrib import admin

# Register your models here.
# blog/admin.py
from .models import Post , EjercicioTiempoDistancia

admin.site.register(Post)

admin.site.register(EjercicioTiempoDistancia)