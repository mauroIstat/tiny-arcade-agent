import argparse

from games.pong.config import GameConfig, OpponentSpeed
from games.pong.game import run_game
from games.pong.core import controllers

OPPONENT_CONTROLLERS = {
    "random": controllers.rand,
    "very-lazy": controllers.very_lazy_follow_ball,
    "lazy": controllers.lazy_follow_ball,
    "sleepy": controllers.sleepy_follow_ball,
    "noisy": controllers.noisy_follow_ball,
    "defensive": controllers.defensive_follow_ball,
    "follow": controllers.follow_ball,
    "predictive": controllers.predictive,
    "predictive-error": controllers.predictive_with_error,
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
        choices=OPPONENT_CONTROLLERS.keys(),
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

    opponent_controller = OPPONENT_CONTROLLERS[args.opponent]
    opponent_speed_level = OPPONENT_SPEEDS[args.speed]

    config = GameConfig(
        opponent_speed_level=opponent_speed_level,
        max_score=args.max_score,
    )

    title = (
        "Tiny Arcade Agents - Pong "
        f"| opponent: {args.opponent} "
        f"| speed: {args.speed}"
    )

    run_game(
        opponent_controller=opponent_controller,
        title=title,
        config=config,
    )


if __name__ == "__main__":
    main()
