
import pandas as pd
import numpy as np
import joblib

from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, r2_score

np.random.seed(42)

data = pd.DataFrame({
    "temperature": np.random.randint(18, 42, 500),
    "occupants": np.random.randint(1, 7, 500),
    "appliances": np.random.randint(2, 15, 500),
    "hour": np.random.randint(0, 24, 500),
    "weekend": np.random.randint(0, 2, 500)
})

data["energy_kwh"] = (
    data["temperature"] * 0.15
    + data["occupants"] * 0.8
    + data["appliances"] * 0.6
    + data["hour"] * 0.1
    + data["weekend"] * 0.5
    + np.random.normal(0, 0.5, 500)
)

data.to_csv("dataset/energy_data.csv", index=False)

X = data.drop("energy_kwh", axis=1)
y = data["energy_kwh"]

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

model = RandomForestRegressor(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

predictions = model.predict(X_test)

print("MAE:", round(mean_absolute_error(y_test, predictions), 2))
print("R2 Score:", round(r2_score(y_test, predictions), 2))

joblib.dump(model, "energy_model.pkl")

print("Model Training Completed!")
print("Model Saved Successfully!")

