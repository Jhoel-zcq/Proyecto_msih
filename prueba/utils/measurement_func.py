from pmeasurement.measures import Distance, Mass, Speed, Time
import random 

## Funciones basicas de conversion que reciben la unidad de origen, unidad de destino y el valor a convertir
## Retornan el valor convertido redondeado a 3 decimales
## Ejemplo: convertir_distancia("km", 10, "mi") -> 6.214
## Para utilizarlo instalar measurement: pip install measurement
## Unidades soportadas:
## Distancia: "km", "m", "mi", "ft"
## Masa: "kg", "g", "lb", "oz"
## Tiempo: "s", "min", "hr", "day"
## Para la velocidad se debe escribir de la siguiente manera: "unidad_distancia/unidad_tiempo"
## Se transformara solo a la forma correcta que requiere el codigo

def convertir_distancia(valor_inicial, unidad_origen, unidad_destino):
    try:
        distancia = Distance(**{unidad_origen: valor_inicial})
        return round(getattr(distancia, unidad_destino), 3)
    except:
        return "Error en las unidades de distancia, intenta de nuevo."

def convertir_masa(valor_inicial, unidad_origen, unidad_destino):
    try:
        masa = Mass(**{unidad_origen:valor_inicial})
        masa_final= round(getattr(masa, unidad_destino), 3)
        return masa_final, valor_inicial, unidad_origen, unidad_destino
    except:
        return "Error en las unidades de masa, intenta de nuevo."

def convertir_velocidad(valor_inicial, unidad_origen, unidad_destino):
    try:
        velocidad_origen = formato_velocidad(unidad_origen)
        velocidad_destino = formato_velocidad(unidad_destino)
        velocidad = Speed(**{velocidad_origen: valor_inicial})
        velocidad_final = round(getattr(velocidad, velocidad_destino), 3)
        return velocidad_final, valor_inicial, unidad_origen, unidad_destino
    except:
        return "Error en las unidades de velocidad, intenta ingresando con el siguiente formato: 'distancia/tiempo' como 'km/hr'."

def convertir_tiempo(valor_inicial, unidad_origen, unidad_destino):
    try:
        tiempo = Time(**{unidad_origen: valor_inicial})
        tiempo_final = round(getattr(tiempo, unidad_destino), 3)
        return tiempo_final, valor_inicial, unidad_origen, unidad_destino
    except:
        return "Error en las unidades de tiempo, intenta de nuevo usando una de las siguientes formas de escribir las unidades: 's', 'min', 'hr', 'day'."
    

##Solo para cuando uno le este ingresando la velocidad manualmente 
def formato_velocidad(unidad):
    try:
        distancia, tiempo = unidad.split("/")
        correcto = f"{distancia}__{tiempo}"
        return correcto
    except:
        return "formato incorrecto de velocidad. Usa 'distancia/tiempo' como 'km/hr'."
##

def random_masa():
    unidades = ["kg", "g", "lb", "oz"]
    unidad_inicial = random.choice(unidades)
    valor = round(random.uniform(1, 100), 2)
    unidad_final = random.choice(unidades)
    return valor, unidad_inicial, unidad_final

def random_distancia():
    unidades = ["km", "m", "mi", "ft"]
    unidad_inicial = random.choice(unidades)
    valor = round(random.uniform(1, 100), 2)
    unidad_final = random.choice(unidades)
    return valor, unidad_inicial, unidad_final

def random_tiempo():    
    unidades = ["s", "min", "hr", "day"]
    unidad_inicial = random.choice(unidades)
    valor = round(random.uniform(1, 100), 2)
    unidad_final = random.choice(unidades)
    return valor, unidad_inicial, unidad_final

def random_velocidad(unidad_distancia_i, unidad_tiempo_i, unidad_distancia_f, unidad_tiempo_f):
    valor = round(random.uniform(1,100),2)
    unidad_origen = f"{unidad_distancia_i}__{unidad_tiempo_i}"
    unidad_destino = f"{unidad_distancia_f}__{unidad_tiempo_f}"
    return valor, unidad_origen, unidad_destino


def verificar_respuesta(valor_usuario, valor_correcto):
    try:
        valor_usuario = float(valor_usuario)
        if abs(valor_usuario - valor_correcto) <= 0.1:
            return True
        else:
            return False
    except:
        return False


print(convertir_masa(random_masa()[0], random_masa()[1], random_masa()[2]))