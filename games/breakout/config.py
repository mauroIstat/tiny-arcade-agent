"""
Configuration for the Breakout game.

These values control the size, speed, colors, rewards, and layout of the game.
Changing them is a useful way to create small classroom experiments.
"""

from dataclasses import dataclass


@dataclass
class GameConfig:
    # Window
    width: int = 800
    height: int = 600
    fps: int = 60

    # Colors
    black: tuple[int, int, int] = (0, 0, 0)
    white: tuple[int, int, int] = (255, 255, 255)
    cyan: tuple[int, int, int] = (0, 220, 255)
    orange: tuple[int, int, int] = (255, 150, 60)
    red: tuple[int, int, int] = (255, 90, 90)
    green: tuple[int, int, int] = (100, 240, 140)

    # Paddle
    paddle_width: int = 100
    paddle_height: int = 16
    paddle_bottom_margin: int = 35
    paddle_speed: float = 420
    paddle_bounce_strength: float = 1.4

    # Ball
    ball_size: int = 16
    ball_paddle_gap: int = 4
    ball_speed_x: float = 180
    ball_speed_y: float = -260

    # Bricks
    brick_rows: int = 4
    brick_columns: int = 5
    brick_width: int = 120
    brick_height: int = 26
    brick_gap: int = 10
    brick_top_margin: int = 80

    # Episode
    starting_lives: int = 3

    # Rewards
    brick_reward: float = 1.0
    paddle_hit_reward: float = 0.1
    lost_ball_reward: float = -1.0
    victory_reward: float = 5.0

    @property
    def brick_left_margin(self) -> int:
        grid_width = self.brick_columns * self.brick_width
        gap_width = (self.brick_columns - 1) * self.brick_gap
        return (self.width - grid_width - gap_width) // 2
