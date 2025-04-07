import numpy as np
import pandas as pd
from constants import (
    plantilla,            # Diccionario base con las claves de habilidades inicializadas en 0
    areas,                # Diccionario que asocia cada área con un conjunto de habilidades requeridas
    niveles_educativos,   # Lista de niveles educativos disponibles
    probabilidad,         # Diccionario que asigna a cada nivel educativo una probabilidad de tener habilidades
)

# Fijamos la semilla aleatoria para reproducibilidad
np.random.seed(42)

# Cantidad de candidatos a generar
entradas = 50000
datos = []


# FUNCIONES DE CÁLCULO DE PUNTAJE

def calcular_experiencia(experiencia):
    if experiencia == 0:
        return 0.0
    elif experiencia > 0 and experiencia <= 3:
        return 0.2
    elif experiencia > 3 and experiencia <= 6:
        return 0.5
    elif experiencia > 6 and experiencia <= 10:
        return 0.8
    else:
        return 1.0


def calcular_educacion(educacion):
    if educacion == "Ninguna":
        return 0.0
    elif educacion == "Tecnicatura":
        return 0.5
    elif educacion == "Licenciatura":
        return 0.8
    else:
        return 1.0




# BLOQUE PRINCIPAL

if __name__ == "__main__":
    for _ in range(entradas):
        candidato = plantilla.copy()  # Creamos una copia de la plantilla base
        experiencia = np.random.randint(0, 20)  # Años de experiencia aleatorios entre 0 y 19
        educacion = np.random.choice(niveles_educativos).strip()  # Nivel educativo aleatorio
        area = np.random.choice(list(areas.keys())).strip()       # Área profesional aleatoria

        habilidades_deseadas = areas.get(area)  # Lista de habilidades requeridas por el área
        cantidad_habilidades = 0
        chances = probabilidad.get(educacion)   # Probabilidad de tener habilidades según educación

        # Simulamos si el candidato posee o no cada habilidad deseada
        for habilidad in habilidades_deseadas:
            candidato[habilidad] = int(
                np.random.choice([0, 1], p=[1 - chances, chances])
            )
            if candidato[habilidad] == 1:
                cantidad_habilidades += 1

        # Asignamos valores al candidato
        candidato["Experiencia"] = experiencia
        candidato["Educación"] = educacion
        candidato["Área"] = area

        # Calculamos los puntos de evaluación
        puntos_experiencia = calcular_experiencia(experiencia)
        puntos_educacion = calcular_educacion(educacion)
        puntos_habilidades = cantidad_habilidades / len(habilidades_deseadas)

        # Promedio de los tres factores
        candidato["Puntos"] = (puntos_experiencia + puntos_educacion + puntos_habilidades) / 3

        # Determinamos si es apto o no
        candidato["Aptitud"] = "Apto" if candidato["Puntos"] >= 0.7 else "No apto"

        datos.append(candidato)

    # Creamos el DataFrame con todos los candidatos
    df = pd.DataFrame(datos)

    # Dividimos entre aptos y no aptos
    aptos = df[df["Aptitud"] == "Apto"]
    no_aptos = df[df["Aptitud"] == "No apto"]

    # Balanceamos el dataset para que haya la misma cantidad de aptos y no aptos
    if len(aptos) < len(no_aptos):
        no_aptos = no_aptos.sample(n=len(aptos), random_state=42)
    else:
        aptos = aptos.sample(n=len(no_aptos), random_state=42)

    # Mezclamos ambos grupos y lo guardamos en un archivo CSV
    df_balanceado = pd.concat([aptos, no_aptos]).sample(frac=1, random_state=42)

    df_balanceado.to_csv("./data/candidatos.csv", index=False)
    print("Archivo CSV generado con éxito.")
