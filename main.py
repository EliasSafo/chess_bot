import sys
import joblib

from machine_learning.encoder import BoardEncoder
import chess
from PySide6.QtCore import QTimer
from PySide6.QtWidgets import QApplication

from board_evaluation import positional_evaluation
from board_evaluation.ml_evaluation import MLEvaluation
from board_evaluation.positional_evaluation import PositionalEvaluation
from bot_evaluation.match_runner import MatchRunner
from bot_evaluation.results_store import ResultsStore
from bot_evaluation.tournament_runner import TournamentRunner
from bots.material_count_bot import MaterialCountBot
from bots.min_max_bot import MinMaxBot
from bots.random_bot import RandomBot

from game.bot_controller import BotGameController
from game.controller import GameController
from game.game import Game

from visual_representation import ChessWindow
from board_evaluation.material_evaluation import MaterialEvaluation
# MODE = "bot_vs_bot"
MODE = "human_vs_bot"


def create_bot_vs_bot(game):
    controller = BotGameController(
        game=game,
        white_bot=MinMaxBot(evaluator=MLEvaluation("machine_learning/models/linear_1_mil_random_positions_games.joblib",model_id="10k"), depth=3),
        black_bot=MinMaxBot(evaluator=PositionalEvaluation(),depth=3),
    )

    return controller


def create_human_vs_bot(game):
    controller = GameController(
        game=game,
        bot=MinMaxBot(evaluator=MLEvaluation("machine_learning/models/linear_1_mil_random_positions_games.joblib",model_id="10k"), depth=3),
        human_color=chess.BLACK,
    )

    return controller


def main():
    app = QApplication(sys.argv)
    #
    game = Game()

    if MODE == "bot_vs_bot":
        controller = create_bot_vs_bot(game)

        window = ChessWindow(
            controller,
            interactive=False,
            sound_enabled=True,
        )

        timer = QTimer()

        def play_next_move():


            if game.is_over():

                timer.stop()
                window.update_board()
                return

            move = controller.make_next_move()


            if move is not None:
                window.register_move(move)


            window.update_board()

        timer.timeout.connect(play_next_move)
        timer.start(500)

    elif MODE == "human_vs_bot":

        controller = create_human_vs_bot(game)

        window = ChessWindow(

            controller,

            interactive=True,

            sound_enabled=True,

        )

        if controller.human_color == chess.BLACK:
            QTimer.singleShot(

                500,

                window.make_delayed_bot_move,

        )

        else:
            raise ValueError(f"Unknown mode: {MODE}")

    window.show()

    sys.exit(app.exec())






if __name__ == "__main__":
    main()