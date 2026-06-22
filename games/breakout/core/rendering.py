"""
Rendering utilities for Breakout.

Rendering displays the current game state but does not change it.
"""

import pygame

from .entities import Ball, Brick, GameScreen, GameState, Paddle
from .geometry import make_ball_rect, make_brick_rect, make_paddle_rect
from .sprites import GameSprites
from ..config import GameConfig


def render_background(
    screen: pygame.Surface,
    config: GameConfig,
    sprites: GameSprites,
) -> None:
    if sprites.background is None:
        screen.fill(config.black)
    else:
        screen.blit(sprites.background, (0, 0))


def render_paddle(
    screen: pygame.Surface,
    config: GameConfig,
    paddle: Paddle,
    sprite: pygame.Surface | None,
) -> None:
    if sprite is None:
        pygame.draw.rect(screen, config.cyan, make_paddle_rect(paddle))
    else:
        screen.blit(sprite, (paddle.x, paddle.y))


def render_ball(
    screen: pygame.Surface,
    config: GameConfig,
    ball: Ball,
    sprite: pygame.Surface | None,
) -> None:
    if sprite is None:
        pygame.draw.ellipse(screen, config.white, make_ball_rect(ball))
    else:
        screen.blit(sprite, (ball.x, ball.y))


def render_brick(
    screen: pygame.Surface,
    config: GameConfig,
    brick: Brick,
    sprite: pygame.Surface | None,
) -> None:
    if not brick.alive:
        return

    if sprite is None:
        colors = [config.orange, config.red, config.green, config.cyan]
        pygame.draw.rect(screen, colors[brick.row % len(colors)], make_brick_rect(brick))
    else:
        screen.blit(sprite, (brick.x, brick.y))


def render_hud(
    screen: pygame.Surface,
    font: pygame.font.Font,
    state: GameState,
    config: GameConfig,
) -> None:
    message = f"Score: {state.score}   Lives: {state.lives}"
    text = font.render(message, True, config.white)
    screen.blit(text, (20, 20))


def render_game(
    screen: pygame.Surface,
    font: pygame.font.Font,
    state: GameState,
    config: GameConfig,
    sprites: GameSprites,
) -> None:
    render_background(screen, config, sprites)

    for brick in state.bricks:
        render_brick(screen, config, brick, sprites.brick)

    render_paddle(screen, config, state.paddle, sprites.paddle)
    render_ball(screen, config, state.ball, sprites.ball)
    render_hud(screen, font, state, config)

    pygame.display.flip()


def render_end_screen(
    screen: pygame.Surface,
    font: pygame.font.Font,
    state: GameState,
    config: GameConfig,
    sprites: GameSprites,
) -> None:
    render_background(screen, config, sprites)

    overlay = pygame.Surface((config.width, config.height), pygame.SRCALPHA)
    overlay.fill((0, 0, 0, 180))
    screen.blit(overlay, (0, 0))

    if state.screen == GameScreen.VICTORY:
        message = "YOU CLEARED THE BRICKS!"
        color = config.green
    else:
        message = "GAME OVER"
        color = config.red

    title_font = pygame.font.SysFont(None, 56)
    info_font = pygame.font.SysFont(None, 38)

    title_text = title_font.render(message, True, color)
    score_text = info_font.render(f"Final score: {state.score}", True, config.white)
    restart_text = info_font.render("Press SPACE to play again", True, config.white)
    quit_text = info_font.render("Press ESC to quit", True, config.white)

    screen.blit(title_text, title_text.get_rect(center=(config.width // 2, 210)))
    screen.blit(score_text, score_text.get_rect(center=(config.width // 2, 280)))
    screen.blit(restart_text, restart_text.get_rect(center=(config.width // 2, 340)))
    screen.blit(quit_text, quit_text.get_rect(center=(config.width // 2, 385)))

    pygame.display.flip()
