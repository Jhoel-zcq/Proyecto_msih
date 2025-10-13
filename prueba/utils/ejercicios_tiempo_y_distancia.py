#mish/prueba/utils/ejercicios_tiempo_y_distancio
import pprint
import random

def generar_ejercicios_tiempo_y_distancia():
    ejercicios = [
        {
            "id": 1,
            "enunciado": "Un afinador de guitarra emite un tono de frecuencia {f} Hz. Calcula el periodo de oscilación correspondiente a dicho tono.",
            "formula": "T = 1 / f",
            "resolver": lambda f=None, T=None: round(1 / f, 6),
            "variable_pedir": "periodo",
            "unidades": {"f": "Hz", "resultado": "s"},
        },
        {
            "id": 2,
            "enunciado": "Un detector de ondas sísmicas registra una señal periódica que se repite cada {T} ms. Calcula la frecuencia de dicha señal.",
            "formula": "f = 1 / T",
            "resolver": lambda f=None, T=None: round(1 / (T / 1000), 2),
            "variable_pedir": "frecuencia",
            "unidades": {"T": "ms", "resultado": "Hz"},
        },
    ]

    ejercicio = random.choice(ejercicios)

    if ejercicio["id"] == 1:
        f = random.choice([220, 330, 440, 550, 660, 880])
        valor_correcto = ejercicio["resolver"](f=f)
        enunciado = ejercicio["enunciado"].format(f=f)
        unidades = ejercicio["unidades"]
        variable_pedir = ejercicio["variable_pedir"]
        formula = ejercicio["formula"]
    elif ejercicio["id"] == 2:
        T = random.choice([10, 15, 20, 25, 30, 35, 40, 45, 50, 55])
        valor_correcto = ejercicio["resolver"](T=T)
        enunciado = ejercicio["enunciado"].format(T=T)
        unidades = ejercicio["unidades"]
        variable_pedir = ejercicio["variable_pedir"]
        formula = ejercicio["formula"]

    resultado_final = {
        "id": ejercicio["id"],
        "enunciado": enunciado,
        "formula": formula,
        "variable_pedir": variable_pedir,
        "unidades": unidades,
        "valor_correcto": valor_correcto,
    }

    pprint.pprint(resultado_final)
    return resultado_final
