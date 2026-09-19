import joblib
import numpy as np

from sklearn.linear_model import Ridge
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error


data = np.load(
    "data/processed/dataset_1_mil_random_positions_games.npz"
)

X = data["X"]
y = data["y"]

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42,
)

model = Ridge(alpha=1.0)

model.fit(
    X_train,
    y_train,
)

predictions = model.predict(X_test)

mse = mean_squared_error(
    y_test,
    predictions,
)

print("Training positions:", len(X_train))
print("Test positions:", len(X_test))
print("Test MSE:", mse)

joblib.dump(
    model,
    "machine_learning/models/linear_1_mil_random_positions_games.joblib",
)