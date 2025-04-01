import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer

data_texto = {
    "Descripcion": [
        "Tengo habilidades en Python, Machine Learning y Data Science.",
        "Mi experiencia se centra en Java y desarrollo con Spring Boot.",
        "Soy bueno en Python, SQL para bases de datos y Data Analysis.",
    ]
}

df_texto = pd.DataFrame(data_texto)

vectorizer = CountVectorizer()  # Puedes usar TfidfVectorizer también
X = vectorizer.fit_transform(df_texto["Descripcion"])

df_vectorizado = pd.DataFrame(X.toarray(), columns=vectorizer.get_feature_names_out())

# Unir al DataFrame original si es necesario
df_final_texto = pd.concat([df_texto, df_vectorizado], axis=1)
df_final_texto = df_final_texto.drop(columns=["Descripcion"])

print(df_final_texto)
