"""
Pong launcher.

This script is the entry point of the Pong game.

It parses command-line arguments, creates a game configuration,
selects the opponent policy, and starts the game.

Different opponent policies can be used to demonstrate how
agents make decisions, from simple rule-based behaviors to
more advanced AI techniques introduced later in the project.
"""


import argparse

from games.pong.config import GameConfig, OpponentSpeed
from games.pong.game import run_game
from games.pong.core import policies

OPPONENT_POLICIES = {
    "random": policies.random_policy,
    "very-lazy": policies.very_lazy_follow_ball_policy,
    "lazy": policies.lazy_follow_ball_policy,
    "sleepy": policies.sleepy_follow_ball_policy,
    "noisy": policies.noisy_follow_ball_policy,
    "defensive": policies.defensive_follow_ball_policy,
    "follow": policies.follow_ball_policy,
    "predictive": policies.predictive_policy,
    "predictive-error": policies.predictive_with_error_policy,
}


OPPONENT_SPEEDS = {
    "very-slow": OpponentSpeed.VERY_SLOW,
    "slow": OpponentSpeed.SLOW,
    "medium": OpponentSpeed.MEDIUM,
    "fast": OpponentSpeed.FAST,
    "super": OpponentSpeed.SUPER,
}


def parse_args():
    parser = argparse.ArgumentParser(
        description="Tiny Arcade Agents - play small arcade games with simple agents."
    )

    parser.add_argument(
        "--opponent",
        choices=OPPONENT_POLICIES.keys(),
        default="very-lazy",
        help="Choose the Pong opponent strategy.",
    )

    parser.add_argument(
        "--speed",
        choices=OPPONENT_SPEEDS.keys(),
        default="medium",
        help="Choose the Pong opponent speed.",
    )

    parser.add_argument(
        "--max-score",
        type=int,
        default=5,
        help="Score needed to win the match.",
    )

    return parser.parse_args()


def main():
    args = parse_args()

    # Command-line arguments
    opponent_policy = OPPONENT_POLICIES[args.opponent]
    opponent_speed_level = OPPONENT_SPEEDS[args.speed]
    max_score = args.max_score

    # Game configuration
    config = GameConfig(
        opponent_speed_level=opponent_speed_level,
        max_score=max_score,
    )

    title = (
        "Tiny Arcade Agents - Space Pong "
        f"| opponent: {args.opponent} "
        f"| speed: {args.speed}"
    )

    run_game(
        opponent_policy=opponent_policy,
        title=title,
        config=config,
    )


if __name__ == "__main__":
    main()
