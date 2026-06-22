"""
Configuration for the Pong game.

This module contains the parameters used to customize the game,
such as window size, paddle size, ball speed, opponent speed,
and maximum score.

Changing these values allows us to create easier or harder versions
of the same game.
"""

from dataclasses import dataclass
from enum import Enum


class OpponentSpeed(Enum):
    VERY_SLOW = 0.30
    SLOW = 0.60
    MEDIUM = 0.80
    FAST = 1.00
    SUPER = 1.20


@dataclass
class GameConfig:
    # Window
    width: int = 800
    height: int = 500
    fps: int = 60

    # Colors
    black: tuple[int, int, int] = (0, 0, 0)
    white: tuple[int, int, int] = (255, 255, 255)

    # Paddle
    paddle_width: int = 10
    paddle_height: int = 80
    paddle_margin: int = 30

    # Speeds: pixels per second
    player_speed: float = 350
    opponent_speed_level: OpponentSpeed = OpponentSpeed.MEDIUM

    # Ball
    ball_size: int = 20
    ball_speed_x: float = 250
    ball_speed_y_min: int = 120
    ball_speed_y_max: int = 220

    # Match
    max_score: int = 5

    @property
    def opponent_speed(self) -> float:
        return self.player_speed * self.opponent_speed_level.value
