
import numpy as np
import math 
from random import randrange

def generate_Polinomios(X_list, Y_list):
    polinomios = []
    for i in range(1,7):
        z = np.polyfit(X_list, Y_list, i)
        polinomios.append(np.poly1d(z))
    return polinomios

def generate_Random_Index(lista):
    random_index = []
    mitad = len(lista)/2
    mitad =  int(mitad)

    while(len(random_index)<=mitad):
        aux = randrange(0,len(lista))
        if not(aux in lista):
            random_index.append(aux)

    return random_index

def mejor_Polinomio(polinomios,puntos_reales_x, puntos_reales_y):
    infoMejorPolinomio = []
    menorError = -1.0
   
    for f in polinomios:
        erroresAbsolutos = 0.0
        erroresRelativos = 0.0
        for i in range(0,len(puntos_reales_x)):
            # obtener el error absoluto
            erroresAbsolutos += math.fabs(puntos_reales_y[i] - f(puntos_reales_x[i])) 
            try:
                erroresRelativos += ((math.fabs(puntos_reales_y[i] - f(puntos_reales_x[i])))/math.fabs(puntos_reales_y[i]))*100
            except ZeroDivisionError:
                pass

        if (erroresAbsolutos < menorError) or (menorError < 0.0):
            menorError=erroresAbsolutos
            erroresRelativos = erroresRelativos/len(puntos_reales_x)
            infoMejorPolinomio = [f,erroresRelativos]
    return infoMejorPolinomio

def get_rest_index(random_index, longitud_lista):
    rest_index=[]
    for i in range(0,longitud_lista):
        if not i in random_index:
            rest_index.append(i)
    return rest_index