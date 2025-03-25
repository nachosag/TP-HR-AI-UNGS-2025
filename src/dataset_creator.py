import csv
import random

# Configuración inicial
random.seed(42)
num_entradas = 50
nombre_archivo = 'candidatos_puesto.csv'

# Opciones para cada columna
niveles_educativos = ['Secundario', 'Universitario', 'Maestría', 'Doctorado']
habilidades = [
    'Python', 'Java', 'Gestión de Proyectos', 'Análisis de Datos',
    'Inglés Avanzado', 'SQL', 'Machine Learning', 'Comunicación',
    'Trabajo en Equipo', 'Estadística', 'Power BI', 'AWS',
    'Desarrollo Web', 'Android', 'iOS', 'Francés Básico'
]

# Función para generar habilidades aleatorias
def generar_habilidades():
    num_habilidades = random.randint(2, 5)
    return ', '.join(random.sample(habilidades, num_habilidades))

# Función para determinar la experiencia del candidato
def determinar_experiencia(experiencia):
    if experiencia <= 1:
        return 1
    elif experiencia >= 2 & experiencia <= 5:
        return 3
    elif experiencia >= 6 & experiencia <= 10:
        return 5
    else:
        return 6

# Función para determinar si es apto
def determinar_apto(experiencia, educacion, habilidades):
    apto = False
    
    puntaje_exp = determinar_experiencia(experiencia)

    puntaje_edu = {
        'Secundario': 1,
        'Universitario': 3,
        'Maestría': 5,
        'Doctorado': 6
    }[educacion]

    habilidades_clave = {'Python', 'SQL', 'Machine Learning', 'Gestión de Proyectos'}
    puntaje_hab = len(habilidades_clave.intersection(set(habilidades.split(', ')))) * 2

    puntaje_total = puntaje_exp + puntaje_edu + puntaje_hab
    
    return 'true' if puntaje_total >= 8 else 'false', puntaje_total

datos = []
for _ in range(num_entradas):
    experiencia = random.randint(0,15)
    educacion = random.choice(niveles_educativos)
    habilidades_str = generar_habilidades()
    etiqueta, puntaje_total = determinar_apto(experiencia, educacion, habilidades_str)
    
    datos.append([
        experiencia,
        educacion,
        habilidades_str,
        puntaje_total,
        etiqueta,
    ])

with open(nombre_archivo, 'w', newline='', encoding='utf-8') as archivo:
    writer = csv.writer(archivo)
    writer.writerow(['Experiencia', 'Educacion', 'Habilidades', 'Puntaje', 'Etiqueta'])
    writer.writerows(datos)