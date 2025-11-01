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
        if round(float(valor)-num1/2,2) >= tiempo:
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
        
        if round(float(valor)-num2/2,2)>= tiempo:
            break
    #conclucion final 
    r["desarrollo"]+= f"A partir de lo anterior, concluye que {persona1} y {persona2} se encontrararn a la maxima distancia en t = {tiempo}[s]. "
    return r

def verific(periodo1, periodo2):
    
    while True:
        lista = [3, 5, 7, 9, 11,13,15,14,12,10,8,6,4,2]
        if abs(periodo1-periodo2) != 0:
            correcto= (periodo1* periodo2)/abs(periodo2-periodo1)
            if correcto % 1 == 0: #verifico si es entero
                return {'periodo1':periodo1 ,'periodo2' :periodo2}
            else:#si no eligo otros valores
                periodo1=random.choice([2, 4, 6, 8, 10,12,14,15,13,11,9,7,5,3,])
                lista.remove(periodo1)
                periodo2= random.choice(lista)
        else:
                periodo1=random.choice([2, 4, 6, 8, 10,12,14,15,13,11,9,7,5,3,])
                lista.remove(periodo1)
                periodo2= random.choice(lista)