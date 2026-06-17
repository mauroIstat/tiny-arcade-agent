"""
Game entities for Pong.

This module defines the main objects that exist in the game:
paddles, ball, score, and the overall game state.

Entities store information about the game world, such as positions,
sizes, speeds, and scores.
"""

from dataclasses import dataclass
from enum import Enum, auto

class Winner(Enum):
    PLAYER = auto()
    OPPONENT = auto()

class GameScreen(Enum):
    PLAYING = auto()
    GAME_OVER = auto()

@dataclass
class Paddle:
    x: float
    y: float
    width: int
    height: int
    speed: float

    @property
    def center_y(self) -> float:
        return self.y + self.height / 2


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
class Score:
    player: int = 0
    opponent: int = 0


@dataclass
class GameState:
    player: Paddle
    opponent: Paddle
    ball: Ball
    score: Score
    screen: GameScreen = GameScreen.PLAYING
    winner: Winner | None = None
