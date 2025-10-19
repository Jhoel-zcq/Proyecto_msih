#mish/prueba/views.py
from django.shortcuts import render , redirect
import random
from django.http import HttpResponse
from random import choice
from .forms import PostForm
#funciones de utlis
from .utils.ejercicios_tiempo_y_distancia import generar_ejercicios_tiempo_y_distancia
from .models import EjercicioTiempoDistancia # models
from .utils.ejercicios_tiempo_y_distancia import desarrollo_id_3

# Create your views here.

#paginas html
def index(request):
    return render(request,'prueba/index.html' )

def ejercitar(request):
    return render(request,"prueba/ejercitar.html")

def sandbox(request):
    return render(request, "prueba/sandbox.html")

def inicio(request):
    return render(request, 'prueba/index.html')

def funcion_sandbox(request): 
    return render(request, 'prueba/funcion_sandbox.html')

def funcion_ejercitar(request): 
    return render(request,"prueba/funcion_ejercitar.html")
#FUNCIONES
def pagina_aleatoria_fis100(request):
    paginas = ['Tiempo_y_distancia','Medición','Rapidez_de_cambio','Vectores','Triangulo_vectorial','Descripción_de_movimiento','Fuerzas_y_leyes_de_Newton']
    
    return redirect(choice(paginas))

def pagina_aleatoria_fis111(request):
    paginas=['Cinematica','Principios_de_Newton','Trabajo_y_energia']
    return redirect(choice(paginas))

# mish/prueba/views.py
from django.shortcuts import render
import random
import json # ¡Necesario para leer el formato JSON!
from .models import EjercicioTiempoDistancia

# ¡Importa tu función de desarrollo! Asegúrate de que la ruta sea correcta.
from .utils.ejercicios_tiempo_y_distancia import desarrollo_id_3 

def Tiempo_y_distancia(request):
    # --- BLOQUE 1: GENERAR UN NUEVO EJERCICIO ---
    # Esto se ejecuta si el usuario pide "otro ejercicio" o si es la primera vez que entra.
    if request.method == 'GET' or request.POST.get('otro'):
        plantilla_ejercicio = random.choice(EjercicioTiempoDistancia.objects.all())
        
        # Lógica para ejercicios SIMPLES (como el de la guitarra, tipo_id = 1)
        if plantilla_ejercicio.tipo_id == 1:
            variables = json.loads(plantilla_ejercicio.variables_json)
            valor_variable = float(random.choice(variables['f']))
            
            valor_correcto = round((1 / valor_variable)*1000, 4)
            enunciado_final = plantilla_ejercicio.enunciado_plantilla.format(f=valor_variable)
            desarrollo_final = plantilla_ejercicio.desarrollo_plantilla.format(f=valor_variable, valor_correcto=valor_correcto)
        elif plantilla_ejercicio.tipo_id == 2:
            variables = json.loads(plantilla_ejercicio.variables_json)
            valor_variable = float(random.choice(variables['T']))
            
            valor_correcto = round(1/(valor_variable/1000),4)
            enunciado_final = plantilla_ejercicio.enunciado_plantilla.format(T=valor_variable)
            desarrollo_final = plantilla_ejercicio.desarrollo_plantilla.format(T=valor_variable,valor_correcto=valor_correcto)
        # Lógica para ejercicios COMPLEJOS (como los trapecistas, tipo_id = 3)
        elif plantilla_ejercicio.tipo_id == 3:
            variables = json.loads(plantilla_ejercicio.variables_json)
            persona1 = random.choice(variables['persona1'])
            persona2 = random.choice(variables['persona2'])
            periodo1 = random.choice(variables['periodo1'])
            periodo2 = random.choice(variables['periodo2'])

            valor_correcto = round((periodo1 * periodo2) / abs(periodo2 - periodo1), 2)
            enunciado_final = plantilla_ejercicio.enunciado_plantilla.format(
                persona1=persona1, persona2=persona2, periodo1=periodo1, periodo2=periodo2
            )
            
            desarrollo_dict = desarrollo_id_3(periodo1, periodo2, persona1, persona2)
            desarrollo_final = desarrollo_dict.get("desarrollo", "Error al generar desarrollo.")
        # ... (aquí añadirías más 'elif' para otros tipos de ejercicios) ...
        
        # Guardamos el ejercicio completo en la sesión del usuario
        ejercicio_final = {
            "enunciado": enunciado_final,
            "formula": plantilla_ejercicio.formula_texto,
            "valor_correcto": valor_correcto,
            "desarrollo": desarrollo_final,
            "unidades": {"resultado": plantilla_ejercicio.unidad_resultado},
            "imagen": plantilla_ejercicio.imagen.url if plantilla_ejercicio.imagen else None
        }
        request.session['ejercicio'] = ejercicio_final
        request.session['intentos'] = 0

    # --- BLOQUE 2: PROCESAR LA RESPUESTA DEL USUARIO ---
    ejercicio = request.session.get('ejercicio', {}) # Usamos .get para evitar errores si la sesión está vacía
    mensaje = ""
    mostrar_pista = False
    mostrar_solucion = False

    # Esto solo se ejecuta cuando el usuario envía una respuesta (y no pide "otro")
    if request.method == 'POST' and not request.POST.get('otro'):
        if request.POST.get('ver_solucion'):
            mostrar_solucion = True
        else:
            try:
                respuesta_usuario = float(request.POST.get('respuesta'))
                if abs(respuesta_usuario - ejercicio.get('valor_correcto', float('inf'))) < 0.01:
                    mensaje = "¡CORRECTO!"
                    mostrar_solucion = True
                else:
                    mensaje = "Incorrecto."
                    request.session['intentos'] += 1
                    if request.session['intentos'] >= 1:
                        mostrar_pista = True
            except (ValueError, TypeError, AttributeError):
                mensaje = "Por favor, ingresa un número válido."

    # --- BLOQUE 3: ENVIAR todo AL TEMPLATE ---
    contexto = {
        'ejercicio': ejercicio,
        'mensaje': mensaje,
        'mostrar_pista': mostrar_pista,
        'mostrar_solucion': mostrar_solucion,
        'ejercicio_imagen': bool(ejercicio.get("imagen")),
    }
    return render(request, "prueba/fis100/Tiempo_y_distancia.html", contexto)


def Medición(request):
    return render(request, "prueba/fis100/Medición.html")

def Rapidez_de_cambio(request):
    return render(request,"prueba/fis100/Rapidez_de_cambio.html")

def Vectores(request):
    return render(request,"prueba/fis100/Vectores.html")

def Triangulo_vectorial(request):
    return render(request,"prueba/fis100/Triangulo_vectorial.html")

def Descripción_de_movimiento(request):
    return render(request,"prueba/fis100/Descripción_de_movimiento.html" )

def Fuerzas_y_leyes_de_Newton(request):
    return render(request,"prueba/fis100/Fuerzas_y_leyes_de_Newton.html")

#FIS111
def Cinematica(request):
    return render(request,"prueba/fis111/Cinematica.html")

def Principios_de_Newton(request):
    return render(request,"prueba/fis111/Principios_de_Newton.html")

def Trabajo_y_energia(request):
    return render(request, "prueba/fis111/Trabajo_y_energia.html")

# blog/views.py
from .models import Post

def lista_posts(request):#es el inicio
    posts = Post.objects.all()  
    return render(request, 'prueba/lista_posts.html', {'posts': posts})

# vista para crear un post


def crear_post(request):
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():  # Valida datos automáticamente
            form.save()      # Guarda en la base de datos
            return redirect('lista_posts')
    else:
        form = PostForm()
    return render(request, 'prueba/crear_post.html', {'form': form})
