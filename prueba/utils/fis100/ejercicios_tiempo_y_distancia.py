#mish/prueba/utils/ejercicios_tiempo_y_distancio
import pprint
import random

def desarrollo_id_3(periodo1,periodo2,persona1,persona2):
    num1= float(periodo1)
    num2=float(periodo2)
    tiempo= round((num1*num2)/(abs(num1-num2)),2)
    r = { "desarrollo" : f"""A partir del enunciado se tiene que {persona1} tiene un periodo de {periodo1}[s], y tambien que {persona2} tiene un periodo de {periodo2}[s]\n
    luego se hara una tabla con los instantes que cada persona que encuentra en la izquierda y derecha\n
    """}
    #parte de desarrollo de la persona1
    value = 1
    valor =0
    while True:
        if value // 2 == 0 :
            lado = "izquierda"
        else:
            lado = "derecha"
        if valor == 0:
            r["desarrollo"] += f"Para {persona1}, tenemos los siguientes datos:\n"
        r["desarrollo"] += f"En {round(valor,1)}[s] esta en {lado}\n"
        
        valor += num1/2
        value +=1
        if round(float(valor)-num1/2,2) == tiempo:
            break
    
    #para persona2
    value = 1
    valor = 0 
    while True:
        if value // 2 == 0 :
            lado = "derecha"
        else:
            lado = "izquierda"
        if valor == 0:
            r["desarrollo"]+= f"Ahora para {persona2}, tenemos los siguientes datos:\n"
        
        r["desarrollo"]+= f"En {round(valor,1)}[s] esta en {lado}\n"
        
        valor +=num2/2
        value+=1
        
        if round(float(valor)-num2/2,2)== tiempo:
            break
    #conclucion final 
    r["desarrollo"]+= f"A partir de lo anterior, concluye que {persona1} y {persona2} se encontrararn a la maxima distancia en t = {tiempo}[s]. "
    return r




def generar_ejercicios_tiempo_y_distancia():
    ejercicios = [#aqui iran todos los ejercicios que pueden salir al azar 
        {
            "id": 1,
            "enunciado": "Un afinador de guitarra emite un tono de frecuencia {f} Hz. Calcula el periodo de oscilación correspondiente a dicho tono.",
            "formula": "T=1/f",
            "resolver": lambda f: round(1 / (f/1000), 2),
            "variable_pedir": "periodo",
            "unidades": {"f": "Hz", "resultado": "s"},
            "imagen": 'img/fis100_guitarra.png'
        },
        {
            "id": 2,
            "enunciado": "Un detector de ondas sísmicas registra una señal periódica que se repite cada {T} ms. Calcula la frecuencia de dicha señal.",
            "formula": "f = 1 / T, y para pasarlo a [Hz] se multiplica por 1000",
            "resolver": lambda T: round(1 / (T / 1000), 2),
            "variable_pedir": "frecuencia",
            "unidades": {"T": "ms", "resultado": "Hz"},
            "imagen" : 'img/fis100_ondas.png'
        },{
            
            "id":3,
            "enunciado": """Los trapecistas {persona1} y {persona2} oscilan con periodos de {periodo1}[s] y {periodo2}[s] respectivamente. Si en t=0, los
trapecistas se encuentran en las fases mostrada en la figura, calcula el instante en que la distancia entre
Juan y Rocío será la maxima por primera vez luego de t=0.""",
            "formula":"periodo1 x periodo2/ |periodo1 - periodo2|, cabe recalcar que esta formula es solo para que verifiquen su resultado, el DEFIS, espera su desarrollo mediante la tabla de valores.",
            "resolver" : lambda periodo1= None, periodo2= None :round((periodo1 * periodo2)/(abs(periodo2-periodo1)),2),
            "variable_pedir" : "tiempo",
            "unidades" : {"resultado": "s"},
            "imagen" : 'img/trapesistas.png',
        }
    ]

    ejercicio = random.choice(ejercicios)#se elige un ejercicio al azar 

    if ejercicio["id"] == 1:
        f = random.choice([220, 330, 440, 550, 660, 880])#f toma un valor ramdom para el ejercicio de id = 1 
        sp= f*1000
        valor_correcto = ejercicio["resolver"](f=f)# decimos que la variable "valor_correcto" va a hacer = ejercicio["resolver"], y eso es = a la funcion lambda, y le decimos que a la f de lambda,lo cambiamos por la f del cual tenemos el valor
        enunciado = ejercicio["enunciado"].format(f=f)#lo mismo variable = "unidades" = ejerciico["enunciado"], osea que es igual a al enunciado, el cual tiene una variablre {f} y por eso usamos el .format(f=f), osea que cambieamos la f del enunciado por la f del valor que tenemos
        unidades = ejercicio["unidades"] #en aqui decimos que la variable unidades, es igual a las udidades del ejercicio, es cual tiene 2 unidades la del f y la del resultado
        variable_pedir = ejercicio["variable_pedir"]#ya esto es obio
        formula = ejercicio["formula"]#tmb obio
        desarrollo = {"desarrollpo": f"A partir de: T=1/f, se tiene 1/{f}[Hz], y eso es {valor_correcto}[s], pero ademas el resultado se puede escribir usando usando un prefijo, por lo tanto el resultado que como {sp}[ms]."}
    elif ejercicio["id"] == 2:#mismo formato, en resumen, lo que hacemos es elegir un valor ramdom, y eso lo ponemos en el enunciado, lo guardamos, segun la f, calculamos el valor correcto y guardamos, y lo demas lo guardamos, 
        T = random.choice([10, 15, 20, 25, 30, 35, 40, 45, 50, 55])
        valor_correcto = ejercicio["resolver"](T=T)
        enunciado = ejercicio["enunciado"].format(T=T)
        unidades = ejercicio["unidades"]
        variable_pedir = ejercicio["variable_pedir"]
        formula = ejercicio["formula"]
        desarrollo = {"desarrollo": f"A partir de f = 1/T, queda como 1/{T}[ms], entonces considerando el valor del prefijol tendremos {valor_correcto}[Hz]"}
    elif ejercicio["id"] == 3:
        persona1 = random.choice(["carlos","Evi","Gustavo","Vicente","jhoel","Thomas","Amaru","Etiel","Gonzalo","Bastian"])
        persona2 = random.choice(["Ana","Estefany","Renata","Rocio","Antonia","Sofia","Isabella","Martina","Isidora","Sara"])
        periodo1 = random.choice([2,4,6,8,10])
        periodo2= random.choice([3,5,7,9,11])
        valor_correcto= ejercicio["resolver"](periodo1=periodo1,periodo2=periodo2)
        enunciado = ejercicio["enunciado"].format(persona1=persona1,persona2=persona2,periodo1=periodo1, periodo2=periodo2)
        unidades= ejercicio["unidades"]
        variable_pedir= ejercicio["variable_pedir"]
        formula= ejercicio["formula"]
        desarrollo = desarrollo_id_3(periodo1,periodo2,persona1,persona2)
        
    resultado_final = {#aqui lo mismo, guardamos lo que teniamos guardado, en un diccionario
        "id": ejercicio["id"],
        "enunciado": enunciado,
        "formula": formula,
        "variable_pedir": variable_pedir,
        "unidades": unidades,
        "valor_correcto": valor_correcto,
        "desarrollo": desarrollo.get("desarrollo",""),
        "imagen": ejercicio["imagen"]  #"imagen": ejercicio.get("imagen", None)
    }

    pprint.pprint(resultado_final)# usamos el pprint, (prety print), se usa mostrar el diccionario en formato mas legible, pues el return es un diccionario
    return resultado_final
