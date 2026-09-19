import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import joblib

from evaluation.neural import NeuralEvaluation
from machine_learning.data.encoder import BoardEncoder
import chess
from PySide6.QtCore import QTimer
from PySide6.QtWidgets import QApplication

from evaluation import positional
from evaluation.ml import MLEvaluation
from evaluation.positional import PositionalEvaluation
from tournament.match_runner import MatchRunner
from tournament.repository import ResultsStore
from tournament.tournament_runner import TournamentRunner
from bots.material_count_bot import MaterialCountBot
from bots.min_max_bot import MinMaxBot
from bots.random_bot import RandomBot

from game.bot_controller import BotGameController
from game.controller import GameController
from game.game import Game


bots = [
    MinMaxBot(
        evaluator=MLEvaluation(
            "machine_learning/models/linear_1_mil_random_positions_games.joblib",
            model_id="ml_linear_1_mil_random_positions_games",
        ),
        depth=1,
    ),

    MinMaxBot(
        evaluator=NeuralEvaluation(
            "machine_learning/models/neural_10000_random_positions_gamess.pt",
            model_id="neural_model_v2",
        ),
        depth=3,
    ),
    MinMaxBot(
        evaluator=PositionalEvaluation(),
        depth=1,
    )
]
store = ResultsStore()

tournament = TournamentRunner(
    number_of_games=10,
    bots=bots,
    results_store=store,
)

results = tournament.run_tournament()
print(results)