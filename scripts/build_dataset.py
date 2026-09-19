import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import chess
from machine_learning.data.dataset_loader import load_games
from machine_learning.data.encoder import BoardEncoder
from machine_learning.data.dataset_creator import TrainingDatasetCreator

file_path = "lichess_db_standard_rated_2026-08.pgn.zst"

data_maker = TrainingDatasetCreator()
data_maker.make_training_dataset()