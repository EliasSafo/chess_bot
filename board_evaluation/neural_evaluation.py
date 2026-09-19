import chess
import torch
from torch import nn

from machine_learning.encoder import BoardEncoder


class NeuralEvaluation:
    def __init__(
        self,
        model_path: str,
        model_id: str,
        input_size: int = 769,
    ):
        self.model_id = model_id

        self.model = nn.Sequential(
            nn.Linear(input_size, 128),
            nn.ReLU(),
            nn.Linear(128, 64),
            nn.ReLU(),
            nn.Linear(64, 1),
        )

        state_dict = torch.load(
            model_path,
            map_location="cpu",
        )

        self.model.load_state_dict(state_dict)

        self.model.eval()

    @property
    def config_id(self) -> str:
        return self.model_id

    def evaluate_board(self, board: chess.Board) -> float:
        if board.is_checkmate():
            if board.turn == chess.WHITE:
                return -999999

            return 999999

        encoder = BoardEncoder(board)
        vector = encoder.encode_board()

        X = torch.tensor(
            [vector],
            dtype=torch.float32,
        )

        with torch.no_grad():
            prediction = self.model(X).item()

        return (prediction * 2) - 1