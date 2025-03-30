import csv
import random

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


def determinar_apto(experiencia, educacion, habilidad):
    apto = False

    puntaje_exp = determinar_experiencia(experiencia)

    puntaje_edu = {"Técnico": 1, "Licenciado": 3, "Ingeniero": 8}[educacion]

    puntaje_hab = 2 if habilidad == 1 else -10

    puntaje_total = abs(puntaje_exp + puntaje_edu + puntaje_hab) / 10

    return "apto" if puntaje_total >= 0.7 else "no apto", puntaje_total


datos = []
for _ in range(num_entradas):
    experiencia = random.randint(1, 15)
    educacion = random.choice(["Técnico", "Licenciado", "Ingeniero"])
    habilidad = random.choice([1, 0])
    aptitud, puntaje = determinar_apto(experiencia, educacion, habilidad)

    datos.append(
        [
            experiencia,
            educacion,
            habilidad,
            puntaje,
            aptitud,
        ]
    )

with open("./data/dataset.csv", "w", newline="", encoding="utf-8") as archivo:
    writer = csv.writer(archivo)
    writer.writerow(["Experiencia", "Educacion", "Python", "Puntaje", "Aptitud"])
    writer.writerows(datos)
