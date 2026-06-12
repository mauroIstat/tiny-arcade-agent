import random
from enum import Enum

from .actions import Action
from ..config import GameConfig
from .entities import Ball, GameState, Paddle
from .geometry import make_ball_rect, make_paddle_rect


class Direction(Enum):
    LEFT = -1
    RIGHT = 1


def random_ball_vx(config: GameConfig) -> float:
    return random.choice([-1, 1]) * config.ball_speed_x


def random_ball_vy(config: GameConfig) -> float:
    return random.choice([-1, 1]) * random.randint(
        config.ball_speed_y_min,
        config.ball_speed_y_max,
    )


def reset_ball(ball: Ball, config: GameConfig, direction: Direction) -> None:
    ball.x = config.width / 2 - ball.size / 2
    ball.y = config.height / 2 - ball.size / 2
    ball.vx = direction.value * config.ball_speed_x
    ball.vy = random_ball_vy(config)


def move_paddle(paddle: Paddle, action: Action, config: GameConfig, dt: float) -> None:
    if action == Action.UP:
        paddle.y -= paddle.speed * dt
    elif action == Action.DOWN:
        paddle.y += paddle.speed * dt

    paddle.y = max(0, min(config.height - paddle.height, paddle.y))


def move_ball(ball: Ball, dt: float) -> None:
    ball.x += ball.vx * dt
    ball.y += ball.vy * dt


def handle_wall_collisions(ball: Ball, config: GameConfig) -> None:
    if ball.y <= 0:
        ball.y = 0
        ball.vy *= -1

    if ball.y + ball.size >= config.height:
        ball.y = config.height - ball.size
        ball.vy *= -1


def handle_paddle_collisions(state: GameState) -> None:
    player_rect = make_paddle_rect(state.player)
    opponent_rect = make_paddle_rect(state.opponent)
    ball_rect = make_ball_rect(state.ball)

    ball = state.ball

    if ball_rect.colliderect(player_rect) and ball.vx < 0:
        ball.x = state.player.x + state.player.width
        ball.vx *= -1

    if ball_rect.colliderect(opponent_rect) and ball.vx > 0:
        ball.x = state.opponent.x - ball.size
        ball.vx *= -1
