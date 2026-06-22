"""
Breakout launcher.

This script is the entry point for the Breakout game.
"""

import argparse

from games.breakout.config import GameConfig
from games.breakout.game import run_game
from games.breakout.core import policies


POLICIES = {
    "keyboard": None,
    "do-nothing": policies.do_nothing_policy,
    "random": policies.random_policy,
    "follow": policies.follow_ball_policy,
    "noisy": policies.noisy_follow_ball_policy,
}


def parse_args():
    parser = argparse.ArgumentParser(
        description="Tiny Arcade Agents - play Breakout with simple policies."
    )

    parser.add_argument(
        "--policy",
        choices=POLICIES.keys(),
        default="keyboard",
        help="Choose the Breakout policy.",
    )

    return parser.parse_args()


def main():
    args = parse_args()

    config = GameConfig()
    policy = POLICIES[args.policy]

    title = f"Tiny Arcade Agents - Breakout | policy: {args.policy}"

    run_game(
        policy=policy,
        title=title,
        config=config,
    )


if __name__ == "__main__":
    main()
