import joblib
import chess
from machine_learning.encoder import BoardEncoder


class MLEvaluation:
    def __init__(self, model_path: str, model_id: str):
        self.model = joblib.load(model_path)
        self.model_id = model_id

    @property
    def config_id(self) -> str:
        return self.model_id

    def evaluate_board(self,board: chess.Board) -> float:
        encoder = BoardEncoder(board)
        vector = encoder.encode_board()
        prediction = self.model.predict([vector])[0]
        value = (prediction*2) - 1
        return value
