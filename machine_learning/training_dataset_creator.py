from pathlib import Path
import random
import numpy as np

from machine_learning.encoder import BoardEncoder
from machine_learning.dataset_loader import load_games


class TrainingDatasetCreator:
    def __init__(
        self,
        requested_games: int = 1000000,
        file_path: str = "lichess_db_standard_rated_2026-08.pgn.zst",
        output_path: str = "data/processed/dataset_1_mil_random_positions_games.npz",
    ):
        self.requested_games = requested_games
        self.file_path = file_path
        self.output_path = Path(output_path)

    def make_training_dataset(self):
        X = []
        y = []

        scanned_games = 0
        accepted_games = 0

        print(
            f"Building dataset from {self.file_path}"
        )
        print(
            f"Target: {self.requested_games:,} accepted games"
        )

        for game in load_games(
                self.file_path,
                max_games=None,
        ):
            scanned_games += 1

            if not self.game_passes_filters(game):

                if scanned_games % 1000 == 0:
                    print(
                        f"Scanned: {scanned_games:,} | "
                        f"Accepted: {accepted_games:,} | "
                        f"Samples: {len(X):,}"
                    )

                continue

            accepted_games += 1

            game_result = self.get_game_result(
                game.headers["Result"]
            )

            board = game.board()
            encoder = BoardEncoder(board=board)
            moves = list(game.mainline_moves())
            random_indices = random.sample(
                range(len(moves)),
                k=min(5, len(moves)),
            )
            for index, move in enumerate(
                    moves
            ):
                board.push(move)
                if index in random_indices:
                    X.append(
                        encoder.encode_board()
                    )
                    y.append(game_result)

            if accepted_games % 100 == 0:
                acceptance_rate = (
                        accepted_games
                        / scanned_games
                        * 100
                )

                progress = (
                        accepted_games
                        / self.requested_games
                        * 100
                )

                print(
                    f"[{progress:5.1f}%] "
                    f"Scanned: {scanned_games:,} | "
                    f"Accepted: {accepted_games:,} | "
                    f"Samples: {len(X):,} | "
                    f"Acceptance: {acceptance_rate:.1f}%"
                )

            if accepted_games >= self.requested_games:
                break

        print("Converting to NumPy...")

        X = np.array(
            X,
            dtype=np.uint8,
        )

        y = np.array(
            y,
            dtype=np.float32,
        )

        self.output_path.parent.mkdir(
            parents=True,
            exist_ok=True,
        )

        print("Saving dataset...")

        np.savez(
            self.output_path,
            X=X,
            y=y,
        )

        print(
            f"Done | "
            f"Scanned: {scanned_games:,} | "
            f"Accepted: {accepted_games:,} | "
            f"Samples: {len(X):,}"
        )

        print(f"X shape: {X.shape}")
        print(f"y shape: {y.shape}")
        print(f"Saved to: {self.output_path}")

        return X, y

    def game_passes_filters(self, game) -> bool:
        white_elo = int(
            game.headers.get(
                "WhiteElo",
                0,
            )
        )

        black_elo = int(
            game.headers.get(
                "BlackElo",
                0,
            )
        )

        if white_elo < 1800 or black_elo < 1800:
            return False

        time_control = game.headers.get(
            "TimeControl",
            "",
        )

        try:
            initial_time, increment = map(
                int,
                time_control.split("+"),
            )

        except ValueError:
            return False

        if initial_time < 600:
            return False

        if (
            game.headers.get("Termination")
            == "Time forfeit"
        ):
            return False

        result = game.headers.get(
            "Result",
            "",
        )

        if result not in {
            "1-0",
            "0-1",
            "1/2-1/2",
        }:
            return False

        return True

    def get_game_result(
        self,
        result_string: str,
    ) -> float:
        if result_string == "1-0":
            return 1.0

        if result_string == "0-1":
            return 0.0

        return 0.5