import chess
from machine_learning.dataset_loader import load_games
from machine_learning.encoder import BoardEncoder
from machine_learning.training_dataset_creator import TrainingDatasetCreator

file_path = "lichess_db_standard_rated_2026-08.pgn.zst"

data_maker = TrainingDatasetCreator()
data_maker.make_training_dataset()