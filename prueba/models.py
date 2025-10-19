from django.db import models

# Create your models here.


class Post(models.Model):
    titulo = models.CharField(max_length=100)
    contenido = models.TextField()
    fecha = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.titulo


class EjercicioTiempoDistancia(models.Model):
    tipo_id = models.IntegerField(unique=True)
    enunciado_plantilla = models.TextField()
    desarrollo_plantilla = models.TextField(
        help_text="Para desarrollos simples con .format(). Para los complejos, dejar un placeholder."
    )
    
    # ¡ASEGÚRATE DE QUE ESTA LÍNEA ESTÉ EXACTAMENTE ASÍ!
    variables_json = models.TextField(
        help_text='Un JSON con claves para cada variable y listas de sus posibles valores.'
    )

    unidad_resultado = models.CharField(max_length=20)
    formula_texto = models.CharField(max_length=200)
    imagen = models.ImageField(upload_to='img/', null=True, blank=True)

    def __str__(self):
        return self.enunciado_plantilla[:50] + "..."