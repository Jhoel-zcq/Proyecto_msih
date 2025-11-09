#mish/prueba/utils/fis100/funciones_medicion.py
from random import choice
import random
from math import sqrt
def valores_medicion_1(num_palitos):
    num_palitos = int(num_palitos)#lo comvertimos entero 
    i=0
    l_palito = random.randint(3,9)#longitud "ideal" del palito
    valores_l_palito = {}
    valores_frecuencia = {}#aquiiran los valores de los periodos
    actual= num_palitos
    while True:
        n = random.randint(1,7)#escogemos un valor aleatorio del pweiodo 
        if n >= actual:#parq que no sea negativo
            n = actual
            valores_frecuencia[i] = n#guardomos en el diccionario
            break
        actual -=n #el valor actual se va reduciendo
        valores_frecuencia[i] = n#guardamos en el diccionario
        i +=1
    
    numero_de_frecuencia = len(valores_frecuencia)
    
    u=0
    lista = [-0.25,-0.22,-0.23,-0.20,-0.18,-0.17,-0.15,-0.13,-0.12,-0.10,-0.07,-0.06,-0.05,0,0.05,0.07,0.08,0.1,0.13,0.14,0.15,0.17,0.18,0.20,0.23,0.22,0.25]
    while u < numero_de_frecuencia:
        error = choice(lista)
        lista.remove(error)
        var = l_palito + error
        valores_l_palito[u] = var
        u +=1
    
    suma = 0
    x = 0
    while x < numero_de_frecuencia:
        suma += valores_l_palito[x] * valores_frecuencia[x]
        x += 1
    
    promedio = round(suma / num_palitos,2)
    
    diferencia = {}
    
    for y in range(numero_de_frecuencia):
        l = valores_l_palito[y]
        dif = round((l - promedio),3)
        diferencia[y] = dif
    
    fre_dif_2= {}
    z = 0
    while z < numero_de_frecuencia:
        dif = diferencia[z]
        frec = valores_frecuencia[z]
        resu = round(((dif**2)*frec),6)
        fre_dif_2[z] = resu
        z +=1
    
    suma_frec_dif_2 = 0
    a =0
    while a < numero_de_frecuencia:
        suma_frec_dif_2 += fre_dif_2[a]
        a +=1 
    suma_frec_dif_2 = round(suma_frec_dif_2,5)
    
    desviacion = round(sqrt(suma_frec_dif_2/num_palitos),8)
    
    desarrollo_promedio = "("
    x = 0
    while x < numero_de_frecuencia:
        a = valores_l_palito[x]
        b = valores_frecuencia[x]
        desarrollo_promedio += f"{b}*{a}"
        if x != (numero_de_frecuencia -1):
            desarrollo_promedio += "+"
        x +=1
        
    desarrollo_promedio +=f")/{num_palitos} = {promedio}"
    
    desarrollo_desviacion = "|Longitud en [cm] (li) | Frecuencia (Ni) |  Ni * li[cm] | (li - xi)[cm] | Ni*(li-xi)**2 [cm**2]|\n"
    x= 0
    while x < numero_de_frecuencia:
        longitud = valores_l_palito[x]
        frecuencia = valores_frecuencia[x]
        li_fre = round((longitud * frecuencia),2)
        dif = diferencia[x]
        dif_fre_2 = fre_dif_2[x]
        desarrollo_desviacion += f"|    {longitud:<4.2f}              |     {frecuencia:4d}        | {li_fre:<8.3f}     | {dif:8.4f}      | {dif_fre_2:8.4f}             |\n"
        x += 1
    
    desarrollo_desviacion += f"|                      |        𝜇        |       {promedio:<4.2f}   |      Suma     |   {suma_frec_dif_2:<8.4f}           |\n"
    desarrollo_desviacion += f"|                      |                 |              |       σ       |   {desviacion:<8.4f}           |\n"
    v = -1
    tabla_aux=""
    while v < numero_de_frecuencia:
        if v > -1:
            fre = valores_frecuencia[v]
            largo = valores_l_palito[v]
        if v == -1:
            tabla_aux += "| Frecuencia   |Longitud en [cm]\n"
        else:
            tabla_aux+=f"| {fre}            | {largo}\n"
        v +=1
    datos = {
        'valores_frecuencia' : valores_frecuencia,
        'valores_palito' : valores_l_palito,
        'promedio' : promedio,
        'desarrollo_promedio' : desarrollo_promedio,
        'diferencia' : diferencia,
        'frec_dif_2' : fre_dif_2,
        'suma_frec_dif_2' : suma_frec_dif_2,
        'desviacion_estandar' :  desviacion,
        'desarrollo_desviacion' : desarrollo_desviacion,
        'tabla_aux' : tabla_aux,
    }
    return datos


