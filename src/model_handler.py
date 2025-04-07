import joblib
import pandas as pd
from sklearn.preprocessing import MinMaxScaler, OrdinalEncoder
import constants
from script import calcular_experiencia, calcular_educacion


def procesar_candidato(exp, mod, edu, area, hab_sel):
    modelo = joblib.load(f"models/{mod}.joblib")
    data = pd.DataFrame(constants.plantilla, index=[0])

    data["Experiencia"] = exp
    data["Educación"] = edu

    for habilidad in hab_sel:
        data[habilidad] = 1

    for clave in constants.areas.keys():
        data[f"{clave}"] = 0

    data[area] = 1

    mms = MinMaxScaler()
    edu_encoder = OrdinalEncoder(categories=[constants.niveles_educativos])

    data[["Experiencia"]] = mms.fit_transform(data[["Experiencia"]])
    data[["Educación"]] = edu_encoder.fit_transform(data[["Educación"]])
    puntos_exp = calcular_experiencia(int(exp))
    puntos_edu = calcular_educacion(edu)
    puntos_hab = len(hab_sel) / len(constants.areas[area])
    data["Puntos"] = (puntos_exp + puntos_edu + puntos_hab) / 3
    data.drop(["Aptitud", "Área"], axis=1, inplace=True)
    prediccion = modelo.predict(data)[0]
    aptitud = constants.mapeo[prediccion]

    return aptitud
