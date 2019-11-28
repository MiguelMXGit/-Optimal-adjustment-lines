from flask import request, jsonify
from app import app
from app.utils.util_polinomios import generate_Polinomios, generate_Random_Index, mejor_Polinomio, get_rest_index
from flask_cors import CORS, cross_origin
import pandas as pd
import numpy as np

# variables
PUNTOS_USUARIO = pd.DataFrame()
PUNTOS_FUNCION = pd.DataFrame()
FUNCION = ""
ERROR_RELATIVO = 0.0


@app.route('/grafica', methods=['GET', 'POST'])
@cross_origin()
def all_grafica():
    global PUNTOS_USUARIO
    global PUNTOS_FUNCION
    global FUNCION
    global ERROR_RELATIVO
    response_object = {'status': 'success'}
    if (request.method == 'POST'):
        post_data = request.get_json(force=True)
        # obtener arreglos de la peticion
        user_X_list = np.fromstring(post_data['listaX'], dtype=int, sep=',')
        user_Y_list = np.fromstring(post_data['listaY'], dtype=int, sep=',')
        # obtener index de los puntos que formaran la funcion
        random_index = generate_Random_Index(user_X_list)
        # obtener index de los puntos restantes para probar el error
        rest_index = get_rest_index(random_index, len(user_X_list))
        # obtener los puntos que formaran la funcion
        puntos_funcion_X = user_X_list[random_index]
        puntos_funcion_Y = user_Y_list[random_index]
        # puntos restantes para probar el error de la funcion
        puntos_reales_X = user_X_list[rest_index]
        puntos_reales_Y = user_Y_list[rest_index]
        # obtener polinomios de grado 1 al 6
        polinomios = generate_Polinomios(puntos_funcion_X, puntos_funcion_Y)
        # obtener mejor polinomio y su error relativo
        # infoMejorPolinomio es un arreglo que contiene ['mejorPolinomio','error relativo']
        infoMejorPolinomio = mejor_Polinomio(
            polinomios, puntos_reales_X, puntos_reales_Y)
        f = infoMejorPolinomio[0]
        ERROR_RELATIVO = infoMejorPolinomio[1]
        # calcular nuevas x's & y's
        x_new = np.linspace(min(user_X_list)-3, max(user_X_list)+3, 50)
        y_new = f(x_new)
        # preparar datos para el response
        PUNTOS_USUARIO = pd.DataFrame({'X': user_X_list, 'Y': user_Y_list})
        PUNTOS_FUNCION = pd.DataFrame({'X': x_new, 'Y': y_new})
        FUNCION = str(f)
        # preparar response
        response_object['puntosUsuario'] = PUNTOS_USUARIO.to_dict(
            orient='records')
        response_object['puntosFuncion'] = PUNTOS_FUNCION.to_dict(
            orient='records')
        response_object['funcion'] = FUNCION
        response_object['errorRelativo'] = ERROR_RELATIVO
    else:
        response_object['puntosUsuario'] = PUNTOS_USUARIO.to_dict(
            orient='records')
        response_object['puntosFuncion'] = PUNTOS_FUNCION.to_dict(
            orient='records')
        response_object['funcion'] = FUNCION
        response_object['errorRelativo'] = ERROR_RELATIVO

    return jsonify(response_object)
