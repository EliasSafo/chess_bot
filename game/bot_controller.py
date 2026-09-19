import chess

from bots.base_bot import BaseBot
from game.game import Game


class BotGameController:

    def __init__(
        self,
        game: Game,
        white_bot: BaseBot,
        black_bot: BaseBot,
    ):
        self.game = game
        self.white_bot = white_bot
        self.black_bot = black_bot

    def make_next_move(self) -> chess.Move | None:
        if self.game.is_over():
            return None

        if self.game.board.turn == chess.WHITE:
            bot = self.white_bot
        else:
            bot = self.black_bot

        move = bot.choose_move(self.game.board)

        if self.game.make_move(move):
            return move

        return None