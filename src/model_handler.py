import joblib
import pandas as pd
from sklearn.preprocessing import MinMaxScaler, OrdinalEncoder
import constants
from script import calcular_experiencia, calcular_educacion


def procesar_candidato(exp, mod, edu, area, hab_sel):
    # Procesa los datos de un candidato, realiza el preprocesamiento necesario,
    # calcula el puntaje total y usa un modelo de ML para predecir la aptitud del candidato.

    # Parámetros:
    #     exp (int): Años de experiencia del candidato
    #     mod (str): Nombre del archivo del modelo a cargar (sin extensión)
    #     edu (str): Nivel educativo del candidato
    #     area (str): Área laboral seleccionada
    #     hab_sel (list): Lista de habilidades seleccionadas por el candidato

    # Carga el modelo previamente entrenado desde el archivo .joblib correspondiente
    modelo = joblib.load(f"models/{mod}.joblib")

    # Crea un DataFrame con la estructura base (plantilla) para un solo candidato
    data = pd.DataFrame(constants.plantilla, index=[0])

    # Asigna los valores de experiencia y educación al DataFrame
    data["Experiencia"] = exp
    data["Educación"] = edu

    # Marca como presentes (1) las habilidades seleccionadas
    for habilidad in hab_sel:
        data[habilidad] = 1

    # Inicializa todas las columnas de áreas laborales como 0
    for clave in constants.areas.keys():
        data[f"{clave}"] = 0

    # Activa (1) la columna correspondiente al área seleccionada
    data[area] = 1

    # Preprocesamiento: normaliza la experiencia a un rango de 0 a 1
    mms = MinMaxScaler()
    data[["Experiencia"]] = mms.fit_transform(data[["Experiencia"]])

    # Codifica el nivel educativo como un valor ordinal 
    edu_encoder = OrdinalEncoder(categories=[constants.niveles_educativos])
    data[["Educación"]] = edu_encoder.fit_transform(data[["Educación"]])

    # Calcula los puntos según experiencia, educación y habilidades
    puntos_exp = calcular_experiencia(int(exp))
    puntos_edu = calcular_educacion(edu)
    puntos_hab = len(hab_sel) / len(constants.areas[area])

    # Promedia los tres factores para obtener el puntaje final
    data["Puntos"] = (puntos_exp + puntos_edu + puntos_hab) / 3

    # Elimina las columnas no necesarias para la predicción
    data.drop(["Aptitud", "Área"], axis=1, inplace=True)

    # Realiza la predicción con el modelo
    prediccion = modelo.predict(data)[0]

    # Traduce la predicción numérica a texto ("Apto" o "No apto") usando el mapeo definido en constants
    aptitud = constants.mapeo[prediccion]

    return aptitud  #Retorna la aptitud del candidato
