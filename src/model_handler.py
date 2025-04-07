import joblib
from tkinter import messagebox
import pandas as pd
from sklearn.preprocessing import MinMaxScaler, OrdinalEncoder, OneHotEncoder
import constants


def valores_validos(exp, mod, edu, area):
    try:
        experiencia = int(exp)
        if experiencia < 0 or experiencia > 20:
            messagebox.showerror(
                "Error", "La experiencia debe estar entre 0 y 20 años."
            )
            return None
    except ValueError:
        messagebox.showerror("Error", "Ingrese una experiencia válida (número entero).")
        return None
    # if mod.strip().lower() in ["", "seleccione un modelo"]:
    #     messagebox.showerror("Error", "Seleccione un modelo.")
    #     return None
    if mod == "Seleccione un modelo":
        messagebox.showerror("Error", "Seleccione un modelo.")
        return None

    if (
        not edu
        or not area
        or edu == "Seleccione su nivel educativo"
        or area == "Seleccione el área"
    ):
        messagebox.showerror("Error", "Seleccione educación y área.")
        return None
    return True


def procesar_candidato(exp, mod, edu, area, hab_sel):
    print(f"Experiencia: {exp}")
    print(f"Modelo: {mod}")
    print(f"Educación: {edu}")
    print(f"Área: {area}")
    print(f"Habilidades seleccionadas: {hab_sel}")

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
    data.drop(["Puntos", "Aptitud", "Área"], axis=1, inplace=True)

    # print(data)

    prediccion = modelo.predict(data)[0]

    print(prediccion)

    return True
