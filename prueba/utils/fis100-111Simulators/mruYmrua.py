from matplotlib.patches import FancyArrowPatch
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
from matplotlib.patches import Rectangle
from matplotlib.patches import Polygon

import numpy as np

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

def generarGraficosMRUA(cambiosAceleracion, xi=0, vi=0, mostrarDatos=False, unidadD="m", unidadT="s", testing=False):
    #estroboscopico(cambiosAceleracion, xi, vi, mostrarDatos, unidadD, unidadT)
    mrua = False
    for intervalo in cambiosAceleracion:
        if cambiosAceleracion[intervalo] != 0: mrua = True

    if not mrua: grafDt = graficaDT(cambiosAceleracion, xi, vi, mostrarDatos, unidadD, unidadT, testing)
    grafVt = graficaVT(cambiosAceleracion, vi, mostrarDatos, unidadD, unidadT, testing)
    grafAt = graficaAT(cambiosAceleracion, mostrarDatos, unidadD, unidadT, testing)

"""def estroboscopico(cambiosAceleracion, xi=0, vi=0, mostrarDatos=False, unidadD="m", unidadT="s"):
    fig, ax = plt.subplots()
    ax.spines.top.set(visible=False)
    ax.spines.left.set(visible=False)
    ax.spines.right.set(visible=False)

    tiemposUnitarios = []
    velocidadesMapeadas = []
    aceleracionesMapeadas = []
    for intervalo in cambiosAceleracion:
        ti = float(intervalo.split("-")[0])
        tf = float(intervalo.split("-")[1])

        if tf - ti != 1:"""


def graficaDT(cambiosAceleracion, xi=0, vi=0, mostrarDatos=False, unidadD="m", unidadT="s", testing=False):
    fig, ax = plt.subplots()
    ax.set_ylabel(f"posición: x [{unidadD}]")
    ax.set_xlabel(f"tiempo: t [{unidadT}]")
    ax.spines.top.set(visible=False)
    ax.spines.right.set(visible=False)
    ax.spines.bottom.set(position=("data", 0))

    tiempos = cambiosPosicion(cambiosAceleracion, vi, xi)["tiempos"]
    posiciones = cambiosPosicion(cambiosAceleracion, vi, xi)["posiciones"]
    
    ax.set_xticks(tiempos)
    ax.set_yticks(posiciones)
    ax.plot(tiempos, posiciones)

    fig.savefig("mruaDT.png")
    if testing: plt.show()

def graficaVT(cambiosAceleracion, vi=0, mostrarAreas=False, unidadD="m", unidadT="s", testing=False):
    fig, ax = plt.subplots()
    ax.set_ylabel(f"velocidad: v [{unidadD}/{unidadT}]")
    ax.set_xlabel(f"tiempo: t [{unidadT}]")
    ax.spines.top.set(visible=False)
    ax.spines.right.set(visible=False)
    ax.spines.bottom.set(position=("data", 0))

    tiempos = cambiosVelocidad(cambiosAceleracion, vi)["tiempos"]
    velocidades = cambiosVelocidad(cambiosAceleracion, vi)["velocidades"]

    i = 1
    while i < len(tiempos) and mostrarAreas:
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

    ax.set_xticks(tiempos)
    ax.set_yticks(velocidades)
    ax.plot(tiempos, velocidades, color="xkcd:cobalt blue")
    
    fig.savefig("mruaVT.png")
    if testing: plt.show()

def graficaAT(cambiosAceleracion, mostrarAreas=False, unidadD="m", unidadT="s", testing=False):
    i = 0
    fig, ax = plt.subplots()
    ax.set_ylabel(r"aceleración: a [{0}/${1}^2$]".format(unidadD, unidadT))
    ax.set_xlabel(f"tiempo: t [{unidadT}]")
    ax.spines.top.set(visible=False)
    ax.spines.right.set(visible=False)
    ax.spines.bottom.set(position=("data", 0))

    for intervalo in cambiosAceleracion:
        if cambiosAceleracion[intervalo] != 0: i += 1
        ti = float(intervalo.split("-")[0])
        tf = float(intervalo.split("-")[1])
        ax.hlines(cambiosAceleracion[intervalo], ti, tf, color="xkcd:scarlet")
        if mostrarAreas and cambiosAceleracion[intervalo] != 0:
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

    ax.set_xticks(cambiosPosicion(cambiosAceleracion)["tiempos"])
    ax.set_yticks(list(cambiosAceleracion.values()))
    fig.savefig("mruaAT.png")
    if testing: plt.show()

testing1 = {"0-5": 1, "5-7": 0, "7-10": -2, "10-14": 0.5}
testing2 = {"0-10": 0}

generarGraficosMRUA(testing1, 0, mostrarDatos=True)
