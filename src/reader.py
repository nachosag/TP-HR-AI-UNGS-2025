import pandas as pd
from sklearn.preprocessing import OneHotEncoder, MinMaxScaler
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from joblib import dump

data = pd.read_csv("./data/dataset.csv")
data.drop_duplicates(inplace=True)

mms = MinMaxScaler()
data[["Experiencia", "Puntaje"]] = mms.fit_transform(data[["Experiencia", "Puntaje"]])

ohe = OneHotEncoder(sparse_output=False).set_output(transform="pandas")
edu_encoded = ohe.fit_transform(data[["Educacion"]])

data["Aptitud"] = data["Aptitud"].map({"apto": 1, "no apto": 0})
data = pd.concat([data, edu_encoded], axis=1).drop(columns=["Educacion"])

x = data.drop(columns=["Aptitud"])
y = data["Aptitud"]

# Partición 60% (train) y 40% (test)
x_train, x_rest, y_train, y_rest = train_test_split(
    x, y, test_size=0.4, random_state=321
)

# Partición "rest" en 2 mitades
x_val, x_test, y_val, y_test = train_test_split(
    x_rest, y_rest, test_size=0.5, random_state=123
)

model = LogisticRegression()
model.fit(x_train, y_train)

print(f"Exactitud promedio entrenamiento: {model.score(x_train,y_train)}")
print(f"Exactitud promedio validación: {model.score(x_val, y_val)}")

y_pred = model.predict(x_test)
print("Datos reales:\n", y_test)
print("Datos predichos:\n", y_pred)

with open("./models/model.joblib", "wb") as f:
    dump(model, f)
