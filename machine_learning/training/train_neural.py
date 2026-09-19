import numpy as np
import torch
from torch import nn
from torch.utils.data import DataLoader, TensorDataset
from sklearn.model_selection import train_test_split


DATASET_PATH = "./data/processed/dataset_1_mil_random_positions_games.npz"
MODEL_PATH = "machine_learning/models/neural_10000_random_positions_gamess.pt"

BATCH_SIZE = 64
EPOCHS = 20
LEARNING_RATE = 0.001


# -------------------------
# Load dataset
# -------------------------

data = np.load(
    "./data/processed/dataset_1_mil_random_positions_games.npz"
)

X = data["X"]
y = data["y"]

# Randomly select 1,000 positions
rng = np.random.default_rng(42)

indices = rng.choice(
    len(X),
    size=100000,
    replace=False,
)

X = X[indices]
y = y[indices]

print("Selected positions:", len(X))

X = X.astype(np.float32)
y = y.astype(np.float32)


X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42,
)


# -------------------------
# Convert NumPy -> PyTorch
# -------------------------

X_train = torch.tensor(X_train)
y_train = torch.tensor(y_train).unsqueeze(1)

X_test = torch.tensor(X_test)
y_test = torch.tensor(y_test).unsqueeze(1)


# -------------------------
# Dataset + batches
# -------------------------

train_dataset = TensorDataset(
    X_train,
    y_train,
)

train_loader = DataLoader(
    train_dataset,
    batch_size=BATCH_SIZE,
    shuffle=True,
)


# -------------------------
# Neural network
# -------------------------

model = nn.Sequential(
    nn.Linear(769, 128),
    nn.ReLU(),

    nn.Linear(128, 64),
    nn.ReLU(),

    nn.Linear(64, 1),
)


# -------------------------
# Training setup
# -------------------------

loss_function = nn.MSELoss()

optimizer = torch.optim.Adam(
    model.parameters(),
    lr=LEARNING_RATE,
)


# -------------------------
# Training loop
# -------------------------

for epoch in range(EPOCHS):

    model.train()

    total_loss = 0

    for batch_X, batch_y in train_loader:

        predictions = model(batch_X)

        loss = loss_function(
            predictions,
            batch_y,
        )

        optimizer.zero_grad()

        loss.backward()

        optimizer.step()

        total_loss += loss.item()

    average_loss = (
        total_loss
        / len(train_loader)
    )

    print(
        f"Epoch {epoch + 1}/{EPOCHS} "
        f"- Training loss: {average_loss:.4f}"
    )


# -------------------------
# Test
# -------------------------

model.eval()

with torch.no_grad():

    predictions = model(X_test)

    test_loss = loss_function(
        predictions,
        y_test,
    )

print()
print("Training positions:", len(X_train))
print("Test positions:", len(X_test))
print("Test MSE:", test_loss.item())


# -------------------------
# Save model
# -------------------------

torch.save(
    model.state_dict(),
    MODEL_PATH,
)

print(f"Saved model to: {MODEL_PATH}")