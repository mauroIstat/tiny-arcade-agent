import pygame

from games.pong.entities import Ball, Paddle


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