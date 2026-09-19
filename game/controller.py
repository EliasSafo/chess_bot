import chess

from bots.base_bot import BaseBot
from game.game import Game


class GameController:

    def __init__(
        self,
        game: Game,
        bot: BaseBot,
        human_color: chess.Color = chess.WHITE,
    ):
        self.game = game
        self.bot = bot
        self.human_color = human_color

    def make_human_move(
        self,
        from_square: chess.Square,
        to_square: chess.Square,
    ) -> chess.Move | None:

        if self.game.board.turn != self.human_color:
            return None

        move = chess.Move(
            from_square=from_square,
            to_square=to_square,
        )

        if self.game.make_move(move):
            return move

        promotion_move = chess.Move(
            from_square=from_square,
            to_square=to_square,
            promotion=chess.QUEEN,
        )

        if self.game.make_move(promotion_move):
            return promotion_move

        return None

    def make_bot_move(self) -> chess.Move | None:
        if self.game.is_over():
            return None

        if self.game.board.turn == self.human_color:
            return None

        move = self.bot.choose_move(self.game.board)

        if self.game.make_move(move):
            return move

        return None