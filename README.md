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
uv run main.py
```

By default this launches a **human vs bot** game where you play as Black against a MinMax bot with ML evaluation. To switch to bot vs bot, change the `MODE` variable at the top of `main.py`:

```python
MODE = "bot_vs_bot"   # watch two bots play
MODE = "human_vs_bot" # play against a bot
```

## Running a tournament

Runs a round-robin tournament between configured bots and prints results:

```bash
uv run run_tournament.py
```

Edit `run_tournament.py` to change which bots compete or how many games each matchup plays.

## Training the ML model

The ML pipeline has two steps: generate a dataset, then train.

**Step 1 — Generate training data** (requires the Lichess PGN dataset):

Download the compressed PGN file from [Lichess open database](https://database.lichess.org/) and place it in the project root as:

```
lichess_db_standard_rated_2026-08.pgn.zst
```

Then run:

```bash
uv run run.py
```

This processes games and writes a `.npz` dataset to `data/processed/`.

**Step 2 — Train the linear model:**

```bash
uv run machine_learning/train_model.py
```

Saves the trained model to `machine_learning/models/`.

**Step 2 (alternative) — Train the neural model:**

```bash
uv run machine_learning/train_neural_model.py
```

## Running tests

```bash
uv run pytest
```

## Project structure

```
Chess/
├── main.py                  # Entry point — launches the GUI
├── run.py                   # Generates the training dataset from PGN
├── run_tournament.py        # Runs a bot tournament
├── bots/                    # Bot implementations
│   ├── base_bot.py
│   ├── random_bot.py
│   ├── material_count_bot.py
│   └── min_max_bot.py       # MinMax with pluggable evaluator
├── board_evaluation/        # Evaluator strategies
│   ├── material_evaluation.py
│   ├── positional_evaluation.py
│   ├── ml_evaluation.py     # scikit-learn model
│   └── neural_evaluation.py # PyTorch model
├── machine_learning/        # Dataset creation and model training
│   ├── encoder.py
│   ├── dataset_loader.py
│   ├── training_dataset_creator.py
│   ├── train_model.py       # Trains Ridge regression model
│   └── train_neural_model.py
├── bot_evaluation/          # Tournament infrastructure
│   ├── match_runner.py
│   ├── tournament_runner.py
│   └── results_store.py
├── game/                    # Game loop and controllers
├── utils/                   # Piece-square tables etc.
├── tests/
└── visual_representation.py # PySide6 GUI
```
