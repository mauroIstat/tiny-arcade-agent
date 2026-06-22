"""
Game entities for Breakout.

Entities store the current game state. They do not draw themselves and they do
not decide how to move; other modules do that work.
"""

from dataclasses import dataclass
from enum import Enum, auto


class GameScreen(Enum):
    PLAYING = auto()
    GAME_OVER = auto()
    VICTORY = auto()


@dataclass
class Paddle:
    x: float
    y: float
    width: int
    height: int
    speed: float

    @property
    def center_x(self) -> float:
        return self.x + self.width / 2


@dataclass
class Ball:
    x: float
    y: float
    size: int
    vx: float
    vy: float

    @property
    def center_x(self) -> float:
        return self.x + self.size / 2

    @property
    def center_y(self) -> float:
        return self.y + self.size / 2


@dataclass
class Brick:
    row: int
    column: int
    x: float
    y: float
    width: int
    height: int
    alive: bool = True


@dataclass
class GameState:
    paddle: Paddle
    ball: Ball
    bricks: list[Brick]
    score: int = 0
    lives: int = 3
    screen: GameScreen = GameScreen.PLAYING

    @property
    def bricks_left(self) -> int:
        return sum(1 for brick in self.bricks if brick.alive)
