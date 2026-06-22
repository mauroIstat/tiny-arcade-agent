"""
Physics helpers for Breakout.

This module moves the paddle and ball, then checks for wall, paddle, and brick
collisions. It returns small event names so the environment can turn visible
events into rewards.
"""

from .actions import Action
from .entities import Ball, GameState, Paddle
from .geometry import make_ball_rect, make_brick_rect, make_paddle_rect
from ..config import GameConfig


def move_paddle(
    paddle: Paddle,
    action: Action,
    config: GameConfig,
    dt: float,
) -> None:
    if action == Action.LEFT:
        paddle.x -= paddle.speed * dt
    elif action == Action.RIGHT:
        paddle.x += paddle.speed * dt

    paddle.x = max(0, min(config.width - paddle.width, paddle.x))


def move_ball(ball: Ball, dt: float) -> None:
    ball.x += ball.vx * dt
    ball.y += ball.vy * dt


def reset_ball_and_paddle(state: GameState, config: GameConfig) -> None:
    state.paddle.x = config.width / 2 - state.paddle.width / 2
    state.paddle.y = config.height - config.paddle_bottom_margin - state.paddle.height
    state.ball.x = config.width / 2 - state.ball.size / 2
    state.ball.y = state.paddle.y - state.ball.size - config.ball_paddle_gap
    state.ball.vx = config.ball_speed_x
    state.ball.vy = config.ball_speed_y


def handle_wall_collisions(ball: Ball, config: GameConfig) -> None:
    if ball.x <= 0:
        ball.x = 0
        ball.vx *= -1  # Bounce off the left wall inverting horizontal velocity.

    if ball.x + ball.size >= config.width:
        ball.x = config.width - ball.size
        ball.vx *= -1  # Bounce off the right wall inverting horizontal velocity.

    if ball.y <= 0:
        ball.y = 0
        ball.vy *= -1  # Bounce off the top wall inverting vertical velocity.


def handle_paddle_collision(state: GameState, config: GameConfig) -> bool:
    ball = state.ball
    paddle = state.paddle

    ball_rect = make_ball_rect(ball)
    paddle_rect = make_paddle_rect(paddle)

    if not ball_rect.colliderect(paddle_rect):
        return False

    if ball.vy <= 0:
        return False

    ball.y = paddle.y - ball.size
    ball.vy = -abs(ball.vy)  # Bounce upward after hitting the paddle.

    hit_position = (ball.center_x - paddle.center_x) / (paddle.width / 2)
    ball.vx = hit_position * config.ball_speed_x * config.paddle_bounce_strength

    return True


def handle_brick_collision(state: GameState) -> bool:
    ball = state.ball
    ball_rect = make_ball_rect(ball)

    for brick in state.bricks:
        if not brick.alive:
            continue

        brick_rect = make_brick_rect(brick)

        if ball_rect.colliderect(brick_rect):
            brick.alive = False
            state.score += 1
            ball.vy *= -1  # Bounce after hitting a brick.
            return True

    return False


def is_ball_lost(ball: Ball, config: GameConfig) -> bool:
    return ball.y > config.height
