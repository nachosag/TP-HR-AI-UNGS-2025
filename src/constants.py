# Plantilla base que representa la estructura de un candidato.
# Todos los campos comienzan vacíos o en cero y se completan al generar los datos o al ingresar un candidato.
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

# Diccionario que agrupa habilidades requeridas por cada área de desarrollo.
areas = {
    "Desarrollo Móvil": [
        "Kotlin",
        "Swift",
        "Flutter",
    ],
    "Desarrollo Web": [
        "HTML",
        "CSS",
        "JavaScript",
        "React",
        "Angular",
        "SQL",
        "NoSQL",
    ],
    "Desarrollo de Juegos": ["C# Unity", "C++ Unreal Engine", "Python"],
}

# Lista ordenada de niveles educativos posibles para un candidato.
niveles_educativos = ["Ninguna", "Tecnicatura", "Licenciatura", "Ingeniería"]

# Probabilidad de que un candidato tenga una habilidad según su nivel educativo.
# Se usa para simular candidatos y ajustar el peso del conocimiento técnico.
probabilidad = {
    "Ninguna": 0.1,
    "Tecnicatura": 0.2,
    "Licenciatura": 0.4,
    "Ingeniería": 0.6,
}

# Mapeo de predicciones del modelo: 1 corresponde a "apto" y 0 a "no apto".
mapeo = {1: "apto", 0: "no apto"}
