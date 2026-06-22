"""
Sprite management for Breakout.

If image files are present, the game uses them. If an image is missing, rendering
falls back to simple geometric shapes so lessons can continue before the art is
finished.
"""

from dataclasses import dataclass
from pathlib import Path

import pygame

from ..config import GameConfig


@dataclass
class GameSprites:
    background: pygame.Surface | None
    paddle: pygame.Surface | None
    ball: pygame.Surface | None
    brick: pygame.Surface | None


def load_sprite(path: Path, size: tuple[int, int], alpha: bool) -> pygame.Surface | None:
    if not path.exists():
        return None

    image = pygame.image.load(path)

    if alpha:
        image = image.convert_alpha()
    else:
        image = image.convert()

    return pygame.transform.scale(image, size)


def load_sprites(config: GameConfig) -> GameSprites:
    sprites_dir = Path(__file__).resolve().parents[1] / "assets"

    background = load_sprite(
        sprites_dir / "backgrounds" / "breakout_background.png",
        (config.width, config.height),
        alpha=False,
    )

    paddle = load_sprite(
        sprites_dir / "paddles" / "breakout_paddle.png",
        (config.paddle_width, config.paddle_height),
        alpha=True,
    )

    ball = load_sprite(
        sprites_dir / "balls" / "breakout_ball.png",
        (config.ball_size, config.ball_size),
        alpha=True,
    )

    brick = load_sprite(
        sprites_dir / "bricks" / "breakout_brick.png",
        (config.brick_width, config.brick_height),
        alpha=True,
    )

    return GameSprites(
        background=background,
        paddle=paddle,
        ball=ball,
        brick=brick,
    )
