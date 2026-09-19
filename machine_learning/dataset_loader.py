import io

import chess.pgn
import zstandard
def load_games(file_path: str, max_games: int | None = None):
    with open(file_path, "rb") as compressed_file:
        decompressor = zstandard.ZstdDecompressor()

        with decompressor.stream_reader(compressed_file) as stream:
            text_stream = io.TextIOWrapper(
                stream,
                encoding="utf-8",
            )

            games_read = 0

            while True:
                if (
                    max_games is not None
                    and games_read >= max_games
                ):
                    break

                game = chess.pgn.read_game(text_stream)

                if game is None:
                    break

                games_read += 1

                yield game