import time
from itertools import combinations

from bots.base_bot import BaseBot
from tournament.match_runner import MatchRunner
from tournament.repository import ResultsStore


class TournamentRunner:

    def __init__(
        self,
        number_of_games: int,
        bots: list[BaseBot],
        results_store: ResultsStore,
    ):
        self.number_of_games = number_of_games
        self.bots = bots
        self.results_store = results_store

    def run_tournament(self) -> list[dict]:
        bot_pairings = self.generate_bot_pairings(
            self.bots
        )

        total_matchups = len(bot_pairings)
        tournament_results = []

        tournament_start = time.perf_counter()

        print()
        print("=== TOURNAMENT START ===")
        print(f"Bots: {len(self.bots)}")
        print(f"Matchups: {total_matchups}")
        print(
            f"Games per matchup: {self.number_of_games}"
        )
        print()

        for matchup_number, (bot_A, bot_B) in enumerate(
            bot_pairings,
            start=1,
        ):
            print(
                f"[{matchup_number}/{total_matchups}] "
                f"{bot_A.config_id} vs {bot_B.config_id}"
            )

            matchup_start = time.perf_counter()

            matcher = MatchRunner(
                number_of_games=self.number_of_games,
                bot_A=bot_A,
                bot_B=bot_B,
            )

            match_results = matcher.run_match()

            matchup_duration = (
                time.perf_counter()
                - matchup_start
            )

            matchup_result = {
                "bot_A": bot_A.config_id,
                "bot_B": bot_B.config_id,
                "games": self.number_of_games,
                "results": match_results,
            }

            tournament_results.append(
                matchup_result
            )

            print(
                f"Completed in "
                f"{matchup_duration:.2f}s"
            )
            print(
                f"Results: {match_results}"
            )
            print()

        self.results_store.append_tournament(
            tournament_results
        )

        tournament_duration = (
            time.perf_counter()
            - tournament_start
        )

        print("=== TOURNAMENT COMPLETE ===")
        print(
            f"Total time: "
            f"{tournament_duration:.2f}s"
        )
        print(
            f"Results saved."
        )
        print()

        return tournament_results

    def generate_bot_pairings(
        self,
        bots: list[BaseBot],
    ):
        return list(
            combinations(bots, 2)
        )