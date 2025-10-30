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

def generarGraficosMRUA(cambiosAceleracion, xi=0, vi=0, mostrarDatos=False, unidadD="m", unidadT="s", testing=False, n=""):
    #estroboscopico(cambiosAceleracion, xi, vi, mostrarDatos, unidadD, unidadT)
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

def estroboscopico(cambiosAceleracion, mostrarDatos=False, unidadT="s", testing=False, n=""):
    fig, ax = plt.subplots()
    ax.spines.top.set(visible=False)
    ax.spines.left.set(visible=False)
    ax.spines.right.set(visible=False)
    ax.set_yticks([])
    ax.set_title("Gráfica Estroboscópico " + n)

    tiempos = cambiosPosicion(cambiosAceleracion)["tiempos"]
    aceleracones = cambiosAceleracion.values()
    tiemposMapeados = np.linspace(tiempos[0], tiempos[-1], len(cambiosAceleracion)*4, endpoint=True).tolist()

    posicionesMapeadas = []
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

def graficaDT(cambiosAceleracion, xi=0, vi=0, mostrarDatos=False, unidadD="m", unidadT="s", testing=False, n=""):
    fig, ax = plt.subplots()
    ax.set_ylabel(f"posición: x [{unidadD}]")
    ax.set_xlabel(f"tiempo: t [{unidadT}]")
    ax.spines.top.set(visible=False)
    ax.spines.right.set(visible=False)
    ax.spines.bottom.set(position=("data", 0))
    ax.set_title("Gráfica Distancia-Tiempo " + n)

    tiempos = cambiosPosicion(cambiosAceleracion, vi, xi)["tiempos"]
    posiciones = cambiosPosicion(cambiosAceleracion, vi, xi)["posiciones"]
    
    if mostrarDatos:
        ax.set_xticks(tiempos)
        ax.set_yticks(posiciones)
    ax.plot(tiempos, posiciones)
    
    return fig_to_base64(fig)

def graficaVT(cambiosAceleracion, vi=0, mostrarDatos=False, unidadD="m", unidadT="s", testing=False, n=""):
    fig, ax = plt.subplots()
    ax.set_ylabel(f"velocidad: v [{unidadD}/{unidadT}]")
    ax.set_xlabel(f"tiempo: t [{unidadT}]")
    ax.spines.top.set(visible=False)
    ax.spines.right.set(visible=False)
    ax.spines.bottom.set(position=("data", 0))
    ax.set_title("Gráfica Velocidad-Tiempo " + n)
    tiempos = cambiosVelocidad(cambiosAceleracion, vi)["tiempos"]
    velocidades = cambiosVelocidad(cambiosAceleracion, vi)["velocidades"]
    i = 1
    while i < len(tiempos) and mostrarDatos:
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

    if mostrarDatos:
        ax.set_xticks(tiempos)
        ax.set_yticks(velocidades)
    ax.plot(tiempos, velocidades, color="xkcd:cobalt blue")
    
    return fig_to_base64(fig)


def graficaAT(cambiosAceleracion, mostrarDatos=False, unidadD="m", unidadT="s", testing=False, n=""):
    i = 0
    fig, ax = plt.subplots()
    ax.set_ylabel(r"aceleración: a [{0}/${1}^2$]".format(unidadD, unidadT))
    ax.set_xlabel(f"tiempo: t [{unidadT}]")
    ax.spines.top.set(visible=False)
    ax.spines.right.set(visible=False)
    ax.spines.bottom.set(position=("data", 0))
    ax.set_title("Gráfica Aceleración-Tiempo " + n)

    for intervalo in cambiosAceleracion:
        if cambiosAceleracion[intervalo] != 0: i += 1
        ti = float(intervalo.split("-")[0])
        tf = float(intervalo.split("-")[1])
        ax.hlines(cambiosAceleracion[intervalo], ti, tf, color="xkcd:scarlet")
        if mostrarDatos and cambiosAceleracion[intervalo] != 0:
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

    if mostrarDatos:
        ax.set_xticks(cambiosPosicion(cambiosAceleracion)["tiempos"])
        ax.set_yticks(list(cambiosAceleracion.values()))
    
    return fig_to_base64(fig)

def generarParametros(unidadD="", unidadT="", test=False):
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

    if test:
        generarGraficosMRUA(intervalos, xi=xi, vi=vi, unidadD=unidadD, unidadT=unidadT, testing=True)
        generarGraficosMRUA(intervalos, xi=xi, vi=vi, unidadD=unidadD, unidadT=unidadT, testing=True, mostrarDatos=True, n="Solución")

    return {"intervalos": intervalos, "xi": xi, "vi": vi, "unidadD": unidadD, "unidadT": unidadT}

"""test1 = generarParametros()

for parametro in test1:
    print(parametro + ":")
    print(test1[parametro])

"""
generarParametros(test=True)
"""
testing1 = {"0-5": 1, "5-7": 0, "7-10": 2}
testing2 = {"0-10": 0}
testing3 = {"0-5": 1, "5-10": 0}

tests = [testing1, testing2, testing3]

i  = 0
while i < len(tests):
    generarGraficosMRUA(tests[i],testing=True, n=str(i), mostrarDatos=True)
    i += 1
"""


