import pandas as pd
from sklearn.preprocessing import MultiLabelBinarizer

data = {
    "Habilidades": [
        ["Python", "Machine Learning", "Data Science"],
        ["Java", "Spring Boot"],
        ["Python", "SQL", "Data Analysis"],
    ]
}

df = pd.DataFrame(data)

mlb = MultiLabelBinarizer()
df_encoded = pd.DataFrame(mlb.fit_transform(df["Habilidades"]), columns=mlb.classes_)

# Unir las columnas one-hot al DataFrame original (si quieres mantener otras columnas)
df_final = pd.concat([df, df_encoded], axis=1)
df_final = df_final.drop(
    columns=["Habilidades"]
)  # Eliminar columna original si no la necesitas

print(df_final)
