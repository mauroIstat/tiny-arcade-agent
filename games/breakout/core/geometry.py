"""
Geometry helpers for Breakout.

Pygame rectangles are useful both for drawing geometric fallback shapes and for
detecting collisions.
"""

import pygame

from .entities import Ball, Brick, Paddle


def make_paddle_rect(paddle: Paddle) -> pygame.Rect:
    return pygame.Rect(
        int(paddle.x),
        int(paddle.y),
        paddle.width,
        paddle.height,
    )


def make_ball_rect(ball: Ball) -> pygame.Rect:
    return pygame.Rect(
        int(ball.x),
        int(ball.y),
        ball.size,
        ball.size,
    )


def make_brick_rect(brick: Brick) -> pygame.Rect:
    return pygame.Rect(
        int(brick.x),
        int(brick.y),
        brick.width,
        brick.height,
    )
