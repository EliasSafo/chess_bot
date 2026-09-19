from abc import ABC, abstractmethod

import chess


class BaseBot(ABC):

    @property
    def config_id(self) -> str:
        return (
            f"minmax_"
            f"{self.evaluator.config_id}_"
            f"d{self.depth}"
        )

    @abstractmethod
    def choose_move(self, board: chess.Board) -> chess.Move:
        pass