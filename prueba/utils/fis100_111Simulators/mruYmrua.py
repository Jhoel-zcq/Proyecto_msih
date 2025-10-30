import matplotlib
matplotlib.use('Agg')

import matplotlib.pyplot as plt
from matplotlib.patches import FancyArrowPatch
from matplotlib.patches import Rectangle
from matplotlib.patches import Polygon
import random

import io , base64

import numpy as np
#funcion que convierte una figura de matplotlib a base64
def fig_to_base64(fig):
    buf = io.BytesIO()
    fig.savefig(buf, format='png', bbox_inches='tight')
    plt.close(fig)
    imagen_bytes = buf.getvalue()
    return base64.b64encode(imagen_bytes).decode('utf-8')


def cambiosPosicion(cambiosAceleracion, vi= 0, xi=0):
    i = 0
    velocidades = cambiosVelocidad(cambiosAceleracion, vi)["velocidades"]

    xf = xi

    tiempos = []
    posiciones = [xi]

    for intervalo in cambiosAceleracion:
        ti = float(intervalo.split("-")[0])
        tf = float(intervalo.split("-")[1])

        if ti not in tiempos: tiempos.append(ti)
        tiempos.append(tf)

        xf += (tf - ti) * velocidades[i]

        posiciones.append(xf)
        i += 1

    return {"tiempos": tiempos, "posiciones": posiciones}

def cambiosVelocidad(cambiosAceleracion, vi=0):
    i = 0
    vf = vi

    tiempos = []
    velocidades = [vf]

    for intervalo in cambiosAceleracion:
        i += 1
        ti = float(intervalo.split("-")[0])
        tf = float(intervalo.split("-")[1])

        if ti not in  tiempos: tiempos.append(ti)
        tiempos.append(tf)

        vf += (tf - ti) * cambiosAceleracion[intervalo]
        velocidades.append(vf)

        if(velocidades[i-1] > 0 and velocidades[i] < 0) or (velocidades[i-1] < 0 and velocidades[i] > 0):
            tiempos.insert(i, abs(velocidades[i-1]/cambiosAceleracion[intervalo]) + ti)
            velocidades.insert(i, 0)
            i+=1

    return {"tiempos": tiempos, "velocidades": velocidades}

def generarGraficosMRUA(cambiosAceleracion, xi=0, vi=0, mostrarDatos=[], unidadD="m", unidadT="s", testing=False, n=""):
    mrua = False
    genEstrob = True
    for intervalo in cambiosAceleracion:
        if cambiosAceleracion[intervalo] != 0: mrua = True
        if cambiosAceleracion[intervalo] < 0: genEstrob = False

    if genEstrob: estroboscopico(cambiosAceleracion, mostrarDatos, unidadT, testing, n)
    graficaAT(cambiosAceleracion, mostrarDatos, unidadD, unidadT, testing, n)
    graficaVT(cambiosAceleracion, vi, mostrarDatos, unidadD, unidadT, testing, n)
    if not mrua: grafDt = graficaDT(cambiosAceleracion, xi, vi, mostrarDatos, unidadD, unidadT, testing, n)
    
    graficos = {}
    
    graficos["aceleracion_tiempo"] = graficaAT(cambiosAceleracion, unidadD=unidadD, unidadT=unidadT)
    graficos["velocidad_tiempo"] = graficaVT(cambiosAceleracion, vi, unidadD=unidadD, unidadT=unidadT)
    graficos["distancia_tiempo"] = graficaDT(cambiosAceleracion, xi, vi, unidadD=unidadD, unidadT=unidadT)
    graficos["estroboscopico"] = estroboscopico(cambiosAceleracion)

    return graficos

def estroboscopico(cambiosAceleracion, mostrarDatos=[], unidadT="s", testing=False, n=""):
    fig, ax = plt.subplots()
    ax.spines.top.set(visible=False)
    ax.spines.left.set(visible=False)
    ax.spines.right.set(visible=False)
    ax.set_yticks([])
    ax.set_title("Gráfica Estroboscópico " + n)

    if "titulo" in mostrarDatos: ax.set_title("Gráfico estroboscópico " + n)

    tiempos = cambiosPosicion(cambiosAceleracion)["tiempos"]
    tiemposMapeados = np.linspace(tiempos[0], tiempos[-1], len(cambiosAceleracion)*4, endpoint=True).tolist()

    velocidadesMapeadas = []
    aceleracionesMapeadas = []
    aceleracionesMapeadasDict = {}

    i = 1
    
    while i < len(tiemposMapeados):
        for intervalo in cambiosAceleracion:

            t1 = float(intervalo.split("-")[0])
            t2 = float(intervalo.split("-")[1])

            if tiemposMapeados[i-1] >= t1 and tiemposMapeados[i-1] <= t2:
                aceleracionesMapeadasDict["{0}-{1}".format(tiemposMapeados[i-1], tiemposMapeados[i])] = cambiosAceleracion[intervalo]
                aceleracionesMapeadas.append(cambiosAceleracion[intervalo])
        i += 1

    velocidadesMapeadas = cambiosVelocidad(aceleracionesMapeadasDict)["velocidades"][:-1]

    j = 1
    sum=velocidadesMapeadas[0]
    while j < len(velocidadesMapeadas):
        sum +=velocidadesMapeadas[j-1]
        ax.add_patch(FancyArrowPatch((sum, 0.05), 
                                    (sum + velocidadesMapeadas[j], 0.05), 
                                    color="xkcd:cobalt blue",
                                    mutation_scale=10))
        ax.add_patch(FancyArrowPatch((sum, 0.1),
                                    (sum + aceleracionesMapeadas[j]*tiemposMapeados[1], 0.1),
                                    color="xkcd:scarlet",
                                    mutation_scale=10))
        j += 1

    ax.set(xlim=(velocidadesMapeadas[0], sum + velocidadesMapeadas[-1]),
        ylim=(-0.1, 0.5))
    fig.set_figheight(3)
    fig.set_figwidth(10)
    
    return fig_to_base64(fig)

def graficaDT(cambiosAceleracion, xi=0, vi=0, mostrarDatos=[], unidadD="m", unidadT="s", testing=False, n=""):
    fig, ax = plt.subplots()
    ax.set_ylabel(f"posición: x [{unidadD}]")
    ax.set_xlabel(f"tiempo: t [{unidadT}]")
    ax.spines.top.set(visible=False)
    ax.spines.right.set(visible=False)
    ax.spines.bottom.set(position=("data", 0))
    ax.set_title("Gráfica Distancia-Tiempo " + n)

    if "titutlo" in mostrarDatos: ax.set_title("Gráfico Distancia-Tiempo " + n)

    tiempos = cambiosPosicion(cambiosAceleracion, vi, xi)["tiempos"]
    posiciones = cambiosPosicion(cambiosAceleracion, vi, xi)["posiciones"]
    
    
    if "todo" in mostrarDatos or "ejes" in mostrarDatos or "x" in mostrarDatos: ax.set_xticks(tiempos)
    if "todo" in mostrarDatos or "ejes" in mostrarDatos or "y" in mostrarDatos or "posicion" in mostrarDatos: ax.set_yticks(posiciones)
    ax.plot(tiempos, posiciones)
    
    return fig_to_base64(fig)

def graficaVT(cambiosAceleracion, vi=0, mostrarDatos=[], unidadD="m", unidadT="s", testing=False, n=""):
    fig, ax = plt.subplots()
    ax.set_ylabel(f"velocidad: v [{unidadD}/{unidadT}]")
    ax.set_xlabel(f"tiempo: t [{unidadT}]")
    ax.spines.top.set(visible=False)
    ax.spines.right.set(visible=False)
    ax.spines.bottom.set(position=("data", 0))


    if "titulo" in mostrarDatos: ax.set_title("Gráfico Velocidad-Tiempo " + n)


    tiempos = cambiosVelocidad(cambiosAceleracion, vi)["tiempos"]
    velocidades = cambiosVelocidad(cambiosAceleracion, vi)["velocidades"]
    i = 1
    while i < len(tiempos) and "area" in mostrarDatos:
        if not (velocidades[i-1] == 0 and velocidades[i] == 0):
            ax.annotate(r"$\Delta x_{0}$".format(i), 
                        xy=(0,0), 
                        xycoords="data", 
                        xytext=(tiempos[i-1] + (tiempos[i]-tiempos[i-1])/2, 0),
                        size=14,
                        horizontalalignment="center",
                        verticalalignment="bottom")
            ax.add_patch(Polygon(((tiempos[i-1], velocidades[i-1]),
                                (tiempos[i-1], 0),
                                (tiempos[i], 0),
                                (tiempos[i], velocidades[i])), 
                                color="whitesmoke"))
            ax.vlines(tiempos[i-1], 0, velocidades[i-1], colors="gainsboro", ls="--")
            ax.vlines(tiempos[i], 0, velocidades[i], colors="gainsboro", ls="--")
        i+=1

    if "todo" in mostrarDatos or "ejes" in mostrarDatos or "x" in mostrarDatos: ax.set_xticks(tiempos)
    if "todo" in mostrarDatos or "ejes" in mostrarDatos or "y" in mostrarDatos or "velocidad" in mostrarDatos: ax.set_yticks(velocidades)
    ax.plot(tiempos, velocidades, color="xkcd:cobalt blue")
    
    return fig_to_base64(fig)


def graficaAT(cambiosAceleracion, mostrarDatos=[], unidadD="m", unidadT="s", testing=False, n=""):
    i = 0
    fig, ax = plt.subplots()
    ax.set_ylabel(r"aceleración: a [{0}/${1}^2$]".format(unidadD, unidadT))
    ax.set_xlabel(f"tiempo: t [{unidadT}]")
    ax.spines.top.set(visible=False)
    ax.spines.right.set(visible=False)
    ax.spines.bottom.set(position=("data", 0))
    ax.set_title("Gráfica Aceleración-Tiempo " + n)

    if "titulo" in mostrarDatos: ax.set_title("Gráfico Aceleración-Tiempo " + n)

    for intervalo in cambiosAceleracion:
        if cambiosAceleracion[intervalo] != 0: i += 1
        ti = float(intervalo.split("-")[0])
        tf = float(intervalo.split("-")[1])
        ax.hlines(cambiosAceleracion[intervalo], ti, tf, color="xkcd:scarlet")
        if "todo" in mostrarDatos or "area" in mostrarDatos and cambiosAceleracion[intervalo] != 0:
            ax.annotate(r"$\Delta v_{0}$".format(i), 
                        xy=(0,0), 
                        xycoords="data", 
                        xytext=(ti + (tf-ti)/2, cambiosAceleracion[intervalo]/2),
                        size=14,
                        horizontalalignment="center",
                        verticalalignment="center")
            ax.add_patch(Rectangle((ti, 0), tf-ti, cambiosAceleracion[intervalo], color="whitesmoke"))
            ax.vlines(ti, 0, cambiosAceleracion[intervalo], colors="gainsboro", ls="--")
            ax.vlines(tf, 0, cambiosAceleracion[intervalo], colors="gainsboro", ls="--")


    if "todo" in mostrarDatos or "ejes" in mostrarDatos or "x" in mostrarDatos: ax.set_xticks(cambiosPosicion(cambiosAceleracion)["tiempos"])
    if "todo" in mostrarDatos or "ejes" in mostrarDatos or "y" in mostrarDatos or "aceleracion" in mostrarDatos: ax.set_yticks(list(cambiosAceleracion.values()))

    """if not testing: fig.savefig("mruaAT{0}.png".format(n))
    else: plt.show()"""
    return fig_to_base64(fig)

def generarParametros(unidadD="", unidadT="", testing=False, mostrarDatos=[], soloAccPositiva=False):

    intervalos = {}
    random.seed()
    nIntervalos = random.randint(1, 4)
    
    if random.randint(1, 5) == 1: tiempos = [random.randint(0, 15)]
    else: tiempos= [0]

    aceleraciones = [random.randint(-1,3) - 0.5 * random.randint(0,1)]

    i = 1
    while i <= nIntervalos:
        tiempos.append(tiempos[i-1] + random.randint(1, 6))
        aceleraciones.append(random.randint(0,3) - 0.5 * random.randint(0,1))
        while aceleraciones[i] == aceleraciones[i-1]: 
            if aceleraciones[i-1] == 0: aceleraciones[i] = random.randint(-1,3) - 0.5 * random.randint(0,1)
            else: aceleraciones[i] = 0
        i += 1

    i = 1
    while i <= nIntervalos:
        intervalos["{0}-{1}".format(tiempos[i-1], tiempos[i])] = aceleraciones[i-1]
        i += 1
    
    if random.randint(0,3) == 1: xi = random.randint(0,15)
    else: xi = 0

    if random.randint(0,5) == 1: vi = random.randint(0,7)
    else: vi = 0
    
    if unidadD == "": unidadD = {0: "cm", 1: "m", 2: "km"}[random.randint(0,2)]
    if unidadT == "": unidadT = {0: "s", 1: "min", 2: "h"}[random.randint(0,2)]


    if testing:
        generarGraficosMRUA(intervalos, xi, vi, mostrarDatos, unidadD, unidadT, testing=True)
        generarGraficosMRUA(intervalos, xi, vi, mostrarDatos, unidadD, unidadT, testing=True, n="Solucion")

    return {"intervalos": intervalos, "xi": xi, "vi": vi, "unidadD": unidadD, "unidadT": unidadT}

def ejercicioTipo1MRUA():
    """
    Modo de uso: Para este tipo de ejercicio se genera 1 estroboscópico <mruaEj1Estrob.png>,
    para este estroboscopico se generan 3 alternativas de gráficas de aceleracion-tiempo
    <mruaEj1AT1>, <muraEj1AT2>, <muraEj1AT3>, una de estas gráficas corresponde a la del
    estroboscopico mostrado, las demás son incorrectas.
    Luego de escoger el gráfico de aceleración correcto se presentará la misma dimámica ahora
    para gráficos de velocidad-tiempo. <mruaEj1VT1.png>, <mruaEj1VT2.png>, <mruaEj1VT3.png>
    El correcto para ambas es siempre el primero, por lo que el orden de las imagenes debe
    ser alterado aleatoriamente al momento de mostrarlas, NO al momento de generarlas.
    
    Una manera detectar cuál es el archivo correcto (esto sería útil al momento de programar
    la respuesta correcta) es verificar si el último carácter del nombre del archivo luego de
    hacer split por "." es "o".

    Me refiero a hacer esto:
    ej:
    s1 = "mruaAT0.png"
    s2 = "mruaATCorrecto.png"


    if s1.split(".")[0][-1] == "o"   ----->   FALSE
    if s2.split(".")[0][-1] == "o"   ----->   TRUE

    """

    correcto = generarParametros()

    generarGraficosMRUA(correcto["intervalos"], 
                        correcto["xi"], 
                        correcto["vi"],
                        [], 
                        correcto["unidadD"], 
                        correcto["unidadT"], 
                        False, 
                        "Correcto")
    """
    Se genera los 3 gráficos del caso correcto: estroboscopicoCorrecto.png, graficaATCorrecto.png,
    graficaVTCorrecto.png
    """

    incorrectos = []

    i = 0
    while i < 4:
        incorrectos.append(generarParametros())
        if i % 2 == 0: graficaAT(incorrectos[i]["intervalos"],
                                ["todo"],
                                correcto["unidadD"], 
                                correcto["unidadT"], 
                                i)
        else: graficaVT(incorrectos[i]["intervalos"],
                        incorrectos[i]["vi"],
                        ["todo"],
                        correcto["unidadD"], 
                        correcto["unidadT"],  
                        i)
        i += 1

def ejercicioTipo2MRUA():
    """
    Este tipo de ejercicios consiste en una modalidad donde dado un gráfico
    el alumno debe poder extraer información de este. Por ejemplo, dado un gráfico
    de aceleración tiempo, el estudiante tiene que poder calcular los cambios de
    velocidad a lo largo del intervalo dado.
    """
    return "test"

def ejercicioTipo2Variedad1MRUA():
    """
    Dado un gráfico de aceleración-tiempo, encontrar la velocidad en cada punto solicitado.
    """
    caso = {"intervalos": {"0-5": 1, "5-10": 0}, "unidadD":"m", "unidadT": "s"}

    graficaAT(caso["intervalos"],
            ["titulo"],
            caso["unidadD"],
            caso["unidadT"],
            testing=True)

    tiempos = cambiosVelocidad(caso)["tiempos"]
    velocidades = cambiosVelocidad(caso)["velocidades"]
    
    aceleracion = caso["intervalos"].values()
    print(aceleracion)

    return "test"


testing1 = {"0-5": 1, "5-7": 0, "7-10": 2}
testing2 = {"0-10": 0}
testing3 = {"0-5": 1, "5-10": 0}

tests = [testing1, testing2, testing3]


#generarGraficosMRUA(testing1, mostrarDatos=True)

ejercicioTipo2Variedad1MRUA()

