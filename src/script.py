import numpy as np
import pandas as pd

np.random.seed(42)

entradas = 50000
datos = []

plantilla = {
    "Experiencia": 0,
    "Educación": "",
    "Área": "",
    "C# Unity": 0,
    "C++ Unreal Engine": 0,
    "Flutter": 0,
    "HTML": 0,
    "CSS": 0,
    "React": 0,
    "Angular": 0,
    "JavaScript": 0,
    "Java": 0,
    "Kotlin": 0,
    "Swift": 0,
    "Python": 0,
    "SQL": 0,
    "NoSQL": 0,
    "Puntos": 0,
    "Aptitud": "",
}

areas = {
    "Desarrollo Web": [
        "HTML",
        "CSS",
        "JavaScript",
        "React",
        "Angular",
        "SQL",
        "NoSQL",
    ],
    "Desarrollo Móvil": [
        "Kotlin",
        "Swift",
        "Flutter",
    ],
    "Desarrollo de Juegos": ["C# Unity", "C++ Unreal Engine", "Python"],
}

niveles_educativos = ["Ninguna", "Tecnicatura", "Licenciatura", "Ingeniería"]

probabilidad = {
    "Ninguna": 0.1,
    "Tecnicatura": 0.2,
    "Licenciatura": 0.4,
    "Ingeniería": 0.6,
}


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


def calcular_habilidades(cantidad_habilidades):
    return cantidad_habilidades * 0.2


for _ in range(entradas):
    candidato = plantilla.copy()
    experiencia = np.random.randint(0, 20)
    educacion = np.random.choice(niveles_educativos).strip()
    area = np.random.choice(list(areas.keys())).strip()
    habilidades_deseadas = areas.get(area)
    cantidad_habilidades = 0
    chances = probabilidad.get(educacion)

    for habilidad in habilidades_deseadas:
        candidato[habilidad] = int(np.random.choice([0, 1], p=[1 - chances, chances]))
        if candidato[habilidad] == 1:
            cantidad_habilidades += 1

    candidato["Experiencia"] = experiencia
    candidato["Educación"] = educacion
    candidato["Área"] = area

    puntos_experiencia = calcular_experiencia(experiencia)
    puntos_educacion = calcular_educacion(educacion)
    puntos_habilidades = cantidad_habilidades / len(habilidades_deseadas)

    candidato["Puntos"] = (
        puntos_experiencia + puntos_educacion + puntos_habilidades
    ) / 3
    candidato["Aptitud"] = "Apto" if candidato["Puntos"] >= 0.7 else "No apto"

    datos.append(candidato)

df = pd.DataFrame(datos)
aptos = df[df["Aptitud"] == "Apto"]
no_aptos = df[df["Aptitud"] == "No apto"]

if len(aptos) < len(no_aptos):
    no_aptos = no_aptos.sample(n=len(aptos), random_state=42)
else:
    aptos = aptos.sample(n=len(no_aptos), random_state=42)

df_balanceado = pd.concat([aptos, no_aptos]).sample(frac=1, random_state=42)

df_balanceado.to_csv("./data/candidatos.csv", index=False)
print("Archivo CSV balanceado generado con éxito.")
