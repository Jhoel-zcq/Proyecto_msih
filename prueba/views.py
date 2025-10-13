#mish/prueba/views.py
from django.shortcuts import render , redirect
import random
from django.http import HttpResponse
from random import choice
from .forms import PostForm
#funciones de utlis
from .utils.ejercicios_tiempo_y_distancia import generar_ejercicios_tiempo_y_distancia

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

#FIS100
def Tiempo_y_distancia(request):
    if 'ejercicio' not in request.session:
        ejercicio=generar_ejercicios_tiempo_y_distancia()
        request.session['ejercicio'] = ejercicio
        request.session['intentos'] = 0
    else :
        ejercicio = request.session['ejercicio']
    
    mensaje = ""
    mostrar_pista=False
    mostrar_solucion = False
    if request.method == 'POST':
        respuesta_usuario = request.POST.get('respuesta')
        ver_solucion = request.POST.get('ver_solucion')
        otro = request.POST.get('otro')
        if otro:
            ejercicio= generar_ejercicios_tiempo_y_distancia()
            request.session['ejercicio'] = ejercicio
            request.session['intentos'] = 0
            return render(request,'prueba/fis100/Tiempo_y_distancia.html',{'ejercicio':ejercicio})
        
        if ver_solucion:
            mostrar_solucion = True
        else:
            try:
                valor_usuario = float(respuesta_usuario)
                valor_correcto = ejercicio['valor_correcto']
                diferencia = abs(valor_usuario - valor_correcto)
                
                if diferencia < 0.01:
                    mensaje = "¡CORECTO!"
                    mostrar_solucion = True
                else: 
                    mensaje = "incorrecto"
                    request.session['intentos'] +=1
                    if request.session['intentos'] >=1:
                        mostrar_pista = True
            except ValueError:
                mensaje = "por favor, ingresa un número válido."
    contexto = {
        'ejercicio':ejercicio,
        'mensaje' : mensaje,
        'mostrar_pista':mostrar_pista,
        'mostrar_solucion' : mostrar_solucion,
    }
    return render(request,"prueba/fis100/Tiempo_y_distancia.html", contexto)

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
