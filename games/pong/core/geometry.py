"""
Geometry helpers for Pong.

This module converts game entities into geometric shapes used by pygame.

For now, paddles and the ball are represented as rectangles.
These rectangles are used both for drawing objects on the screen
and for detecting collisions.
"""

import pygame

from .entities import Ball, Paddle


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
