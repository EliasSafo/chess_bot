import json
from pathlib import Path


class ResultsStore:
    def __init__(self, file_path: str = "tournament/results.json"):
        self.file_path = Path(file_path)

        self.file_path.parent.mkdir(
            parents=True,
            exist_ok=True,
        )

    def load_results(self) -> list[dict]:
        if not self.file_path.exists():
            return []

        with self.file_path.open("r") as file:
            return json.load(file)

    def save_results(self, results: list[dict]) -> None:
        with self.file_path.open("w") as file:
            json.dump(
                results,
                file,
                indent=4,
            )

    def append_tournament(self, tournament_results: list[dict]) -> None:
        existing_results = self.load_results()

        existing_results.extend(tournament_results)

        self.save_results(existing_results)