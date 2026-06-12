from dataclasses import dataclass


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