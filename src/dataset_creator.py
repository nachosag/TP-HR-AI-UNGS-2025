import csv
import random
import pandas as pd
import numpy as np

random.seed(42)
num_entradas = 5000


def determinar_experiencia(experiencia):
    if experiencia == 1:
        return 1
    elif experiencia >= 2 & experiencia <= 5:
        return 3
    elif experiencia >= 6 & experiencia <= 10:
        return 5
    else:
        return 6


def determinar_apto(experiencia, educacion, puntaje_habs):
    apto = False

    puntaje_exp = determinar_experiencia(experiencia)

    puntaje_edu = {"Técnico": 1, "Licenciado": 3, "Ingeniero": 8}[educacion]

    #puntaje_hab = 2 if habilidad == 1 else -10
    puntaje_hab = puntaje_habs

    puntaje_total = abs(puntaje_exp + puntaje_edu + puntaje_hab) / 10

    return "apto" if puntaje_total >= 0.7 else "no apto", puntaje_total


# Definimos valores posibles
areas = ["Web", "Móvil", "Videojuegos"]

habilidades = {
    "Web": ["HTML_CSS_JS", "React", "SQL", "Python", "Java"],
    "Móvil": ["Kotlin_Swift", "Flutter", "Java"],
    "Videojuegos": ["C#_Unity", "C++_Unreal", "Python"]
}

# Lista de todas las habilidades únicas
todas_las_habilidades = sorted(set(sum(habilidades.values(), [])))

datos = []
for _ in range(num_entradas):
    experiencia = random.randint(1, 21)
    educacion = random.choice(["Técnico", "Licenciado", "Ingeniero"])
    area = random.choice(areas)

    # Inicializar todas las habilidades en 0
    habilidades_candidato = {habilidad: 0 for habilidad in todas_las_habilidades}
    # Factor de aprendizaje por educación (Ingeniero aprende más rápido)
    probabilidad_base = {"Técnico": 0.4, "Licenciado": 0.6, "Ingeniero": 0.8}
    probabilidad = probabilidad_base[educacion]

    # Asignar habilidades del área con una probabilidad dependiente del nivel educativo
    for habilidad in habilidades[area]:
        habilidades_candidato[habilidad] = np.random.choice([0, 1], p=[1 - probabilidad, probabilidad])

    # **Corrección para evitar casos ilógicos**
    habilidades_obtenidas = sum(habilidades_candidato.values())

    # Si tiene mucha experiencia, debería tener habilidades mínimas
    if experiencia > 10 and habilidades_obtenidas == 0:
        habilidad_random = random.choice(habilidades[area])
        habilidades_candidato[habilidad_random] = 1
    if experiencia > 15 and habilidades_obtenidas < 2:
        habilidades_faltantes = np.random.choice(
            [h for h in habilidades[area] if habilidades_candidato[h] == 0], size=2 - habilidades_obtenidas, replace=False
        )
        for h in habilidades_faltantes:
            habilidades_candidato[h] = 1    

    # Recalcular habilidades obtenidas después de la corrección
    habilidades_obtenidas = sum(habilidades_candidato.values())
    total_habilidades_posibles = len(habilidades[area])

    puntaje_habilidades = (habilidades_obtenidas / total_habilidades_posibles) * 10  # Habilidades aportan máximo 10

    aptitud, puntaje = determinar_apto(experiencia, educacion, puntaje_habilidades)

    datos.append(
        [experiencia, educacion, area] + [habilidades_candidato[h] for h in todas_las_habilidades] + [puntaje, aptitud]
    )

#with open("./data/dataset.csv", "w", newline="", encoding="utf-8") as archivo:
    #writer = csv.writer(archivo)
    #writer.writerow(["Experiencia", "Educacion", "Python", "Puntaje", "Aptitud"])
    #writer.writerows(datos)
# Definir las columnas correctamente
columnas = ["Experiencia", "Educacion", "Area"] + todas_las_habilidades + ["Puntaje", "Aptitud"]

# Crear el DataFrame sin errores
candidatos = pd.DataFrame(datos, columns=columnas)

# Mostrar los primeros 10 registros
print(candidatos.head(10))

# Guardar el DataFrame en un archivo CSV
with open("datasetCandidatosFull.csv", "w", newline="", encoding="utf-8") as archivo:
    writer = csv.writer(archivo)
    
    # Escribir la cabecera con todas las columnas correctamente
    writer.writerow(columnas)
    
    # Escribir los datos de los candidatos
    writer.writerows(datos)