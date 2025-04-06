import joblib
from tkinter import messagebox
import pandas as pd
from sklearn.preprocessing import MinMaxScaler, OrdinalEncoder, OneHotEncoder


def cargar_modelo(mod):
    modelo = joblib.load(f'./models/{mod}.joblib')
    return modelo


def predecir(modelo, data):
    prediccion = modelo.predict(data)
    return 0

def verificar_var_candidatos(exp, mod,edu, area):
    try:
        experiencia = int(exp)
        if experiencia < 0 or experiencia > 20:
            messagebox.showerror("Error", "La experiencia debe estar entre 0 y 20 años.")
            return None
    except ValueError:
        messagebox.showerror("Error", "Ingrese una experiencia válida (número entero).")
        return None

    if not edu or not area:
        messagebox.showerror("Error", "Seleccione educación y área.")
        return None
    if mod == "Seleccione un modelo":
        messagebox.showerror("Error", "Seleccione un modelo.")
        return None

def procesar_candidato(exp, mod, edu, area, hab_sel):
    """Procesa la información del candidato para la predicción."""
    verificar_var_candidatos(exp, mod, edu, area)
    modelo = cargar_modelo(mod)
    print(exp, mod, edu, area, hab_sel)

    #mms = MinMaxScaler()
    # orer = OrdinalEncoder()
    # ohe = OneHotEncoder()
    #experiencia = mms.fit_transform(exp)
    #print(experiencia)




    # habilidades_lista = sum(habilidades.values(), [])
    # habilidades_vector = [1 if hab in hab_sel else 0 for hab in habilidades_lista]

    # # Crear un DataFrame con la estructura esperada por el modelo
    # data_candidato = pd.DataFrame([[experiencia, edu, area] + habilidades_vector],
    #                               columns=["Experiencia", "Educacion", "Area"] + habilidades_lista)

    # # Codificar las variables categóricas (asumiendo que tu modelo fue entrenado con datos codificados)
    # data_candidato['Educacion'] = label_encoder_educacion.transform(data_candidato['Educacion'])
    # data_candidato['Area'] = label_encoder_area.transform(data_candidato['Area'])

    # # Asegurar el orden de las columnas (importante para algunos modelos)
    # columnas_modelo = list(modelo_cargado.feature_names_in_) if modelo_cargado else []
    # if columnas_modelo and all(col in data_candidato.columns for col in columnas_modelo):
    #     data_candidato = data_candidato[columnas_modelo]
    # elif modelo_cargado:
    #     messagebox.showerror("Error", "Las columnas del candidato no coinciden con las esperadas por el modelo.")
    #     return None

    #return data_candidato
