# mish/prueba/views.py

# BLOQUE 1: IMPORTACIONES 
from django.shortcuts import render, redirect
from django.http import HttpResponse
import random
from random import choice
import json
# Importaciones de modelos y formularios
from .models import Post, EjercicioTiempoDistancia , Ejercicios_vectores
from .forms import PostForm

# Importaciones de tus funciones de utilidades
from .utils.fis100.ejercicios_tiempo_y_distancia import desarrollo_id_3
from .utils.fis100_111Simulators.trianguloVectorial import generar_grafico_vectores , generar_grafico_vectores_iniciales
# BLOQUE 2: VISTAS PRINCIPALES DE LA PÁGINA
def index(request):
    return render(request, 'prueba/index.html')

def ejercitar(request):
    return render(request, "prueba/ejercitar.html")

def sandbox(request):
    return render(request, "prueba/sandbox.html")

def funcion_sandbox(request):
    return render(request, 'prueba/funcion_sandbox.html')

def funcion_ejercitar(request):
    return render(request,"prueba/funcion_ejercitar.html")

# BLOQUE 3: VISTAS DE EJERCICIOS DE FÍSICA 

def Tiempo_y_distancia(request):
    # esto va a solucionar un error del bucle: Si se pide "otro ejercicio", borramos el viejo y redirigimos.
    if request.method == 'POST' and request.POST.get('otro'):
        if 'ejercicio' in request.session:
            del request.session['ejercicio']
        return redirect('Tiempo_y_distancia')

    # Si no hay ejercicio en la sesión, creamos uno nuevo.
    if 'ejercicio' not in request.session:
        plantilla_ejercicio = choice(EjercicioTiempoDistancia.objects.all())
        
        # Lógica para tipo_id = 1 (Guitarra)
        if plantilla_ejercicio.tipo_id == 1:
            variables = json.loads(plantilla_ejercicio.variables_json)
            valor_variable = float(choice(variables['f']))
            valor_correcto = round(1000 / valor_variable, 4)
            enunciado_final = plantilla_ejercicio.enunciado_plantilla.format(f=valor_variable)
            desarrollo_final = plantilla_ejercicio.desarrollo_plantilla.format(f=valor_variable, valor_correcto=valor_correcto)
        
        # Lógica para tipo_id = 2 (Ondas)
        elif plantilla_ejercicio.tipo_id == 2:
            variables = json.loads(plantilla_ejercicio.variables_json)
            valor_variable = float(choice(variables['T']))
            valor_correcto = round(1000 / valor_variable , 4)
            enunciado_final = plantilla_ejercicio.enunciado_plantilla.format(T=valor_variable)
            desarrollo_final = plantilla_ejercicio.desarrollo_plantilla.format(T=valor_variable, valor_correcto=valor_correcto)

        # Lógica para tipo_id = 3 (Trapecistas)
        elif plantilla_ejercicio.tipo_id == 3:
            variables = json.loads(plantilla_ejercicio.variables_json)
            persona1 = choice(variables['persona1'])
            persona2 = choice(variables['persona2'])
            periodo1 = choice(variables['periodo1'])
            periodo2 = choice(variables['periodo2'])
            valor_correcto = round((periodo1 * periodo2) / abs(periodo2 - periodo1), 2)
            enunciado_final = plantilla_ejercicio.enunciado_plantilla.format(
                persona1=persona1, persona2=persona2, periodo1=periodo1, periodo2=periodo2
            )
            desarrollo_dict = desarrollo_id_3(periodo1, periodo2, persona1, persona2)
            desarrollo_final = desarrollo_dict.get("desarrollo", "Error al generar desarrollo.")#el .get es por si falla el desarrollo, si eso sucede se muestra "error al generar el desarrollo"

        # Guardamos el ejercicio completo en la sesión
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

    # Procesar la respuesta del usuario 
    ejercicio = request.session.get('ejercicio', {})
    mensaje = ""
    mostrar_pista = False
    mostrar_solucion = False

    if request.method == 'POST':
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
                    if request.session.get('intentos', 0) >= 1:
                        mostrar_pista = True
            except (ValueError, TypeError, AttributeError):
                mensaje = "Por favor, ingresa un número válido."

    # Enviar todo al template 
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

# Aquí van las otras vistas de FIS100
def Rapidez_de_cambio(request):
    return render(request,"prueba/fis100/Rapidez_de_cambio.html")

def Vectores(request):
    if request.method == 'POST' and request.POST.get('otro'):
        if 'ejercicio_vector' in request.session:
            del request.session['ejercicio_vector']
            return redirect('Vectores')
    if 'ejercicio_vector' not in request.session:
        plantilla_ejercicio = choice(Ejercicios_vectores.objects.all())
        
        if plantilla_ejercicio.tipo_id == 1 :
            ax =random.choice([-10,10,-9,9,-8,8,-7,7,-6,6,-5,5,-4,4,-3,3,-2,2,-1,1,0])
            ay =random.choice([-1,-3,-5,-7,-9,-10,-2,-4,-6,-8,10,8,6,4,2,1,3,5,7,9,0])
            bx =random.choice([1,3,5,7,9,10,0,-1,-3,-5,-7,-8,-10,2,4,6,8,-2,-4,-6,-8])
            by =random.choice([10,8,6,4,2,1,0,3,5,7,9,-1,-3,-5,-7,-10,-9,-8,-6,-4,-2])
            n1 = random.choice([-1,-3,-5,1,3,5,-2,-4,4,2])
            n2 = random.choice([-5,-3,-1,5,3,1,-2,2,-4,4])
            an1x = ax * n1
            an1y = ay * n1 
            bn2x = bx * n2
            bn2y = by * n2 
            vector_an1 = (an1x,an1y)
            vector_bn2 = (bn2x,bn2y)
            vector_a = (ax,ay)
            vector_b = (bx,by)
            
            abx = an1x + bn2x
            aby = an1y + bn2y 
            vector_r_str= f"({abx},{aby})"
            enunciado = plantilla_ejercicio.enunciado_plantilla.format(vector_a=vector_a, vector_b=vector_b, n1 = n1, n2 = n2)
            desarrollo = plantilla_ejercicio.desarrollo_plantilla.format(ax = ax, ay = ay, bx = bx, by = by,n1 = n1, n2= n2 ,abx = abx, aby = aby )
            graficobase64 = generar_grafico_vectores_iniciales(vector_an1,vector_bn2)
            formula = '1 + 1 = 2'
            
            
            
            
            
        ejercicio_final = {
            'enunciado' : enunciado,
            'respuesta_correcta' : vector_r_str,
            'grafico_base64' : graficobase64,
            'formula' : formula,
            'desarrollo' : desarrollo,
            'vector_a' : vector_a,
            'vector_b' :vector_b,
        }
        request.session['ejercicio_vector'] = ejercicio_final
        request.session['intentos'] = 0
    
    
    
    contexto = request.session.get('ejercicio_vector', {})
    
    mensaje = contexto.get('mensaje', "") # Recupera mensajes previos si existen
    mostrar_pista = contexto.get('mostrar_pista', False)
    mostrar_solucion = contexto.get('mostrar_solucion', False)
    
    if request.method == "POST" and not request.POST.get('otro'):
        if request.POST.get('ver_solucion'):
            mostrar_solucion = True
        elif request.POST.get('respuesta'):
            try:
                respuesta_usuario = str(request.POST.get('respuesta'))
                if respuesta_usuario == contexto.get('respuesta_correcta'):
                    mensaje= "CORRECTO!"
                    mostrar_solucion = True
                    vector_a = contexto.get('vector_a')
                    vector_b = contexto.get('vector_b')
                    graficobase64 = generar_grafico_vectores(vector_a, vector_b)
                    contexto['grafico_base64'] = graficobase64
                    request.session['ejercicio_vector'] = contexto
                    #ejercicio_final['grafico_base64'] = graficobase64
                    #request.session['ejercicio_vector'] = ejercicio_final
                else:
                    mensaje = "incorrecto"
                    mostrar_pista= True
                    intentos = request.session.get('intentos', 0) + 1
                    request.session['intentos'] = intentos
                    if intentos >= 1:
                        mostrar_pista = True
            except Exception as x:
                mensaje = f"ingrese un valor valido, {x} no es un valor valido "
    
    
    contexto['mensaje']=mensaje
    contexto['mostrar_pista']=mostrar_pista
    contexto['mostrar_solucion']= mostrar_solucion
    
    
    
    return render(request,
        "prueba/fis100/Vectores.html",{
            "ejercicio": contexto,
            "mensaje": mensaje,
            "mostrar_pista": mostrar_pista,
            "mostrar_solucion": mostrar_solucion,
        }
    )
def Triangulo_vectorial(request):
    return render(request,"prueba/fis100/Triangulo_vectorial.html")

def Descripción_de_movimiento(request):
    return render(request,"prueba/fis100/Descripción_de_movimiento.html" )

def Fuerzas_y_leyes_de_Newton(request):
    return render(request,"prueba/fis100/Fuerzas_y_leyes_de_Newton.html")

# y las otras vistas de fis111
def Cinematica(request):
    return render(request,"prueba/fis111/Cinematica.html")

def Principios_de_Newton(request):
    return render(request,"prueba/fis111/Principios_de_Newton.html")

def Trabajo_y_energia(request):
    return render(request, "prueba/fis111/Trabajo_y_energia.html")


# BLOQUE 4: FUNCIONES ALEATORIAS 
def pagina_aleatoria_fis100(request):
    paginas = ['Tiempo_y_distancia', 'Medición', 'Rapidez_de_cambio', 'Vectores', 'Triangulo_vectorial', 'Descripción_de_movimiento', 'Fuerzas_y_leyes_de_Newton']
    return redirect(choice(paginas))

def pagina_aleatoria_fis111(request):
    paginas = ['Cinematica', 'Principios_de_Newton', 'Trabajo_y_energia']
    return redirect(choice(paginas))

#BLOQUE 5: VISTAS DEL BLOG 
def lista_posts(request):
    posts = Post.objects.all()
    return render(request, 'prueba/lista_posts.html', {'posts': posts})

def crear_post(request):
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('lista_posts')
    else:
        form = PostForm()
    return render(request, 'prueba/crear_post.html', {'form': form})