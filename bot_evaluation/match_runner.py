from game.game import Game
from bots.base_bot import BaseBot
from game.bot_controller import BotGameController


class MatchRunner():
    def __init__(self, number_of_games:int, bot_A:BaseBot, bot_B:BaseBot):
        self.number_of_games = number_of_games
        self.bot_A = bot_A
        self.bot_B = bot_B

    def run_match(self):
        results=[]
        for game_number in range(self.number_of_games):
            game = Game()
            if game_number % 2 == 0:
                controller = BotGameController(
                    game=game,
                    white_bot=self.bot_A,
                    black_bot=self.bot_B,
                )
                while not game.is_over():
                    move =   controller.make_next_move()
                result = self.save_result(white=self.bot_A,black=self.bot_B,result=game.board.result())
                results.append(result)

            else:
                controller = BotGameController(
                    game=game,
                    white_bot=self.bot_B,
                    black_bot=self.bot_A,
                )
                while not game.is_over():
                    move = controller.make_next_move()
                result = self.save_result(white=self.bot_B,black=self.bot_A,result=game.board.result())
                results.append(result)
        return results

    def save_result(self, white: BaseBot, black: BaseBot, result: str):
        if result == "1-0":
            return f"{white.config_id}_win"
        elif result == "0-1":
            return f"{black.config_id}_win"
        else:
            return "Draw"