import joblib
from tkinter import messagebox
import pandas as pd
from sklearn.preprocessing import MinMaxScaler, OrdinalEncoder, OneHotEncoder
import constants


def cargar_modelo(mod):
    modelo = joblib.load(f"./models/{mod}.joblib")
    return modelo


def predecir(modelo, data):
    prediccion = modelo.predict(data)
    return 0


def verificar_var_candidatos(exp, mod, edu, area):
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
    if mod == 'Seleccione un modelo':
        messagebox.showerror("Error", "Seleccione un modelo.")
        return None    
    
    if not edu or not area or edu == "Seleccione su nivel educativo" or area == "Seleccione el área":
        messagebox.showerror("Error", "Seleccione educación y área.")
        return None
    return True



def procesar_candidato(exp, mod, edu, area, hab_sel):
    """Procesa la información del candidato para la predicción."""
    if verificar_var_candidatos(exp, mod, edu, area) is None:
        return False  # Importante: detener ejecución si hay error
    modelo = cargar_modelo(mod)
    print(exp, mod, edu, area, hab_sel)

    data_nuevo = {"Experiencia": [exp], "Educacion": [edu], "Area": [area]}
    for hab in list(set(sum(constants.areas.values(), []))):
        data_nuevo[hab] = [1 if hab in hab_sel else 0]
    df = pd.DataFrame(data_nuevo)

    mms = MinMaxScaler()
    edu_encoder = OrdinalEncoder(edu)
    #ohe = OneHotEncoder(sparse_output=False).set_output(transform="pandas")

    ohe = OneHotEncoder(sparse_output=False)
    area_encoded = ohe.fit_transform(df[["Area"]])
    #area_encoded_df = pd.DataFrame(area_encoded, columns=ohe.get_feature_names_out(["Area"]))

    df["Experiencia"] = mms.fit_transform(df["Experiencia"])
    df["Educacion"] = edu_encoder.fit_transform(df["Educacion"])

    #prediccion = modelo.predict(nuevo_candidato_pred_input)
    prediccion = modelo.predict(df)
    aptitud = "Apto" if prediccion[0] == 1 else "No apto"
    messagebox.showinfo("Éxito", f"Candidato agregado correctamente.\nPredicción: {aptitud}")

    return True





    # try:
    #     nuevo_candidato_pred_input = df.copy()
    #     nuevo_candidato_pred_input["Educacion"] = edu_encoder.transform(nuevo_candidato_pred_input["Educacion"])
    #     nuevo_candidato_pred_input["Area"] = ohe.fit_transform(nuevo_candidato_pred_input["Area"])
    #     columnas_requeridas_modelo = list(modelo.feature_names_in_)
    #     for col in columnas_requeridas_modelo:
    #             if col not in nuevo_candidato_pred_input.columns: nuevo_candidato_pred_input[col] = 0
    #     nuevo_candidato_pred_input = nuevo_candidato_pred_input[columnas_requeridas_modelo]
    # except Exception as e:
    #     messagebox.showerror("Error de Preparación", f"Error al preparar datos para predicción: {e}\nVerifica la definición de COLUMNAS_MODELO_ENTRENADO.")
    #     return False