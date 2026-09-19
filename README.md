# Chess AI

A Python chess engine with a GUI, multiple bots, ML-based board evaluation, and a tournament runner.

## Requirements

- Python 3.14+
- [uv](https://docs.astral.sh/uv/) (package manager)

## Setup

**1. Install uv** (if you don't have it):

```bash
curl -LsSf https://astral.sh/uv/install.sh | sh
```

**2. Clone the repo and install dependencies:**

```bash
git clone <repo-url>
cd Chess
uv sync
```

This creates a `.venv` and installs all dependencies (PySide6, python-chess, PyTorch, scikit-learn, etc.).

## Running the game

```bash
uv run scripts/run_app.py
```

By default this launches a **human vs bot** game where you play as Black against a MinMax bot with ML evaluation. To switch to bot vs bot, change the `MODE` variable at the top of `app/main.py`:

```python
MODE = "bot_vs_bot"   # watch two bots play
MODE = "human_vs_bot" # play against a bot
```

## Running a tournament

Runs a round-robin tournament between configured bots and prints results:

```bash
uv run scripts/run_tournament.py
```

Edit `scripts/run_tournament.py` to change which bots compete or how many games each matchup plays.

## Training the ML model

The ML pipeline has two steps: generate a dataset, then train.

**Step 1 — Generate training data** (requires the Lichess PGN dataset):

Download the compressed PGN file from [Lichess open database](https://database.lichess.org/) and place it in the project root as:

```
lichess_db_standard_rated_2026-08.pgn.zst
```

Then run:

```bash
uv run scripts/build_dataset.py
```

This processes games and writes a `.npz` dataset to `data/processed/`.

**Step 2 — Train the linear model:**

```bash
uv run machine_learning/training/train_linear.py
```

Saves the trained model to `machine_learning/models/`.

**Step 2 (alternative) — Train the neural model:**

```bash
uv run machine_learning/training/train_neural.py
```

## Running tests

```bash
uv run pytest
```

## Project structure

```
Chess/
├── app/                     # Visual chess application
│   ├── main.py              # App entry point — sets up game mode and runs GUI
│   └── visual_representation.py  # PySide6 GUI
│
├── game/                    # Chess game orchestration
│   ├── game.py
│   ├── controller.py        # Human vs bot controller
│   └── bot_controller.py    # Bot vs bot controller
│
├── bots/                    # Move-selection algorithms
│   ├── base_bot.py
│   ├── random_bot.py
│   ├── material_count_bot.py
│   └── min_max_bot.py       # MinMax with alpha-beta pruning and pluggable evaluator
│
├── evaluation/              # Board evaluation strategies
│   ├── material.py
│   ├── positional.py
│   ├── ml.py                # scikit-learn Ridge model
│   ├── neural.py            # PyTorch neural network model
│   └── piece_square_tables.py
│
├── machine_learning/
│   ├── data/                # Dataset creation and encoding
│   │   ├── encoder.py
│   │   ├── dataset_loader.py
│   │   └── dataset_creator.py
│   ├── training/            # Model training scripts
│   │   ├── train_linear.py
│   │   └── train_neural.py
│   └── models/              # Saved model files (.joblib, .pt)
│
├── tournament/              # Tournament infrastructure
│   ├── match_runner.py
│   ├── tournament_runner.py
│   └── repository.py        # Persists results to JSON
│
├── data/
│   └── processed/           # Generated .npz training datasets
│
├── scripts/                 # Runnable entry points
│   ├── run_app.py
│   ├── build_dataset.py
│   ├── train_model.py
│   └── run_tournament.py
│
└── tests/
```
