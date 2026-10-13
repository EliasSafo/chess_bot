import sqlite3
from pathlib import Path


class TournamentRepository:
    def __init__(self, db_path: Path):
        self.db_path = db_path
        self._create_tables()

    def _connect(self):
        connection = sqlite3.connect(self.db_path)
        connection.execute("PRAGMA foreign_keys = ON")
        return connection

    def _create_tables(self):
        with self._connect() as connection:
            connection.execute(
                """
                CREATE TABLE IF NOT EXISTS tournament (
                    id INTEGER PRIMARY KEY,
                    name TEXT NOT NULL,
                    created_at TEXT NOT NULL
                )
                """
            )

            connection.execute(
                """
                CREATE TABLE IF NOT EXISTS model (
                    id INTEGER PRIMARY KEY,
                    name TEXT NOT NULL,
                    created_at TEXT NOT NULL
                )
                """
            )

            connection.execute(
                """
                CREATE TABLE IF NOT EXISTS bot (
                    id INTEGER PRIMARY KEY,
                    name TEXT NOT NULL,
                    algorithm TEXT NOT NULL,
                    model_id INTEGER,

                    FOREIGN KEY (model_id)
                        REFERENCES model(id)
                )
                """
            )

            connection.execute(
                """
                CREATE TABLE IF NOT EXISTS game (
                    id INTEGER PRIMARY KEY,
                    tournament_id INTEGER NOT NULL,
                    created_at TEXT NOT NULL,
                    white_bot_id INTEGER NOT NULL,
                    black_bot_id INTEGER NOT NULL,
                    outcome TEXT NOT NULL,

                    FOREIGN KEY (tournament_id)
                        REFERENCES tournament(id),

                    FOREIGN KEY (white_bot_id)
                        REFERENCES bot(id),

                    FOREIGN KEY (black_bot_id)
                        REFERENCES bot(id)
                )
                """
            )

    def create_tournament(
        self,
        name: str,
        created_at: str,
    ):
        with self._connect() as connection:
            cursor = connection.execute(
                """
                INSERT INTO tournament (
                    name,
                    created_at
                )
                VALUES (?, ?)
                """,
                (
                    name,
                    created_at,
                ),
            )

            return cursor.lastrowid

    def create_model(
        self,
        name: str,
        created_at: str,
    ):
        with self._connect() as connection:
            cursor = connection.execute(
                """
                INSERT INTO model (
                    name,
                    created_at
                )
                VALUES (?, ?)
                """,
                (
                    name,
                    created_at,
                ),
            )

            return cursor.lastrowid

    def create_bot(
        self,
        name: str,
        algorithm: str,
        model_id: int | None = None,
    ):
        with self._connect() as connection:
            cursor = connection.execute(
                """
                INSERT INTO bot (
                    name,
                    algorithm,
                    model_id
                )
                VALUES (?, ?, ?)
                """,
                (
                    name,
                    algorithm,
                    model_id,
                ),
            )

            return cursor.lastrowid

    def create_game(
        self,
        tournament_id: int,
        created_at: str,
        white_bot_id: int,
        black_bot_id: int,
        outcome: str,
    ):
        with self._connect() as connection:
            cursor = connection.execute(
                """
                INSERT INTO game (
                    tournament_id,
                    created_at,
                    white_bot_id,
                    black_bot_id,
                    outcome
                )
                VALUES (?, ?, ?, ?, ?)
                """,
                (
                    tournament_id,
                    created_at,
                    white_bot_id,
                    black_bot_id,
                    outcome,
                ),
            )

            return cursor.lastrowid