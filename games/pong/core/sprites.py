from dataclasses import dataclass
from pathlib import Path

import pygame

from ..config import GameConfig


@dataclass
class GameSprites:
    background: pygame.Surface
    paddle: pygame.Surface
    ball: pygame.Surface


def load_sprites(config: GameConfig) -> GameSprites:
    sprites_dir = Path(__file__).resolve().parents[1] / "assets"

    background = pygame.image.load(
        sprites_dir / "backgrounds" / "space_background.png"
    ).convert()

    paddle = pygame.image.load(
        sprites_dir / "paddles" / "space_paddle.png"
    ).convert_alpha()

    ball = pygame.image.load(sprites_dir / "balls" / "space_ball.png").convert_alpha()

    background = pygame.transform.scale(
        background,
        (config.width, config.height),
    )

    paddle = pygame.transform.scale(
        paddle,
        (config.paddle_width, config.paddle_height),
    )

    ball = pygame.transform.scale(
        ball,
        (config.ball_size, config.ball_size),
    )

    return GameSprites(
        background=background,
        paddle=paddle,
        ball=ball,
    )
