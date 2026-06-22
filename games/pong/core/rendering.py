"""
Rendering utilities for Pong.

This module is responsible for drawing the current game state
on the screen.

Rendering converts the internal simulation state into visual
elements that the player can see, including:
- the background;
- paddles and ball;
- score information;
- game-over screens.

The rendering system does not modify the game state.
Its only purpose is to display a visual representation of
the current match.
"""

import pygame

from ..config import GameConfig
from .sprites import GameSprites
from .entities import Ball, GameState, Paddle, Winner


def render_background(
    screen: pygame.Surface,
    assets: GameSprites,
) -> None:
    screen.blit(assets.background, (0, 0))


def render_center_line(
    screen: pygame.Surface,
    config: GameConfig,
) -> None:
    neon_blue = (0, 220, 255)

    for y in range(0, config.height, 30):
        pygame.draw.rect(
            screen,
            neon_blue,
            (config.width // 2 - 3, y, 6, 15),
        )

        pygame.draw.rect(
            screen,
            config.white,
            (config.width // 2 - 1, y, 2, 15),
        )


def render_paddle(
    screen: pygame.Surface,
    paddle: Paddle,
    sprite: pygame.Surface,
) -> None:
    screen.blit(sprite, (paddle.x, paddle.y))


def render_ball(
    screen: pygame.Surface,
    ball: Ball,
    sprite: pygame.Surface,
) -> None:
    screen.blit(sprite, (ball.x, ball.y))


def render_score(
    screen: pygame.Surface,
    font: pygame.font.Font,
    state: GameState,
    config: GameConfig,
) -> None:
    score = f"{state.score.player}   {state.score.opponent}"
    score_text = font.render(score, True, config.white)
    score_rect = score_text.get_rect(center=(config.width / 2, 40))

    screen.blit(score_text, score_rect)


def render_game(
    screen: pygame.Surface,
    font: pygame.font.Font,
    state: GameState,
    config: GameConfig,
    sprites: GameSprites,
) -> None:
    render_background(screen, sprites)
    render_center_line(screen, config)

    render_paddle(screen, state.player, sprites.paddle)
    render_paddle(screen, state.opponent, sprites.paddle)

    render_ball(screen, state.ball, sprites.ball)
    render_score(screen, font, state, config)

    pygame.display.flip()


def render_game_over(
    screen: pygame.Surface,
    font: pygame.font.Font,
    state: GameState,
    config: GameConfig,
    sprites: GameSprites,
) -> None:

    # Background
    render_background(screen, sprites)

    # Dark overlay
    overlay = pygame.Surface(
        (config.width, config.height),
        pygame.SRCALPHA,
    )

    overlay.fill((0, 0, 0, 180))

    screen.blit(overlay, (0, 0))

    # Messages
    if state.winner == Winner.PLAYER:
        message = "YOU WIN!"
        message_color = (0, 255, 255)
    else:
        message = "COMPUTER WINS!"
        message_color = (255, 100, 100)

    score_message = f"Final score: " f"{state.score.player} - {state.score.opponent}"

    restart_message = "Press SPACE to play again"

    quit_message = "Press ESC to quit"

    # Fonts
    title_font = pygame.font.SysFont(None, 56)
    info_font = pygame.font.SysFont(None, 40)

    glow_color = (255, 100, 100)

    # Render text
    title_text = title_font.render(
        message,
        True,
        message_color,
    )

    score_text = info_font.render(
        score_message,
        True,
        config.white,
    )

    restart_text = info_font.render(
        restart_message,
        True,
        config.white,
    )

    quit_text = info_font.render(
        quit_message,
        True,
        config.white,
    )

    # Position
    title_rect = title_text.get_rect(center=(config.width // 2, 180))

    score_rect = score_text.get_rect(center=(config.width // 2, 250))

    restart_rect = restart_text.get_rect(center=(config.width // 2, 320))

    quit_rect = quit_text.get_rect(center=(config.width // 2, 360))

    # Draw
    screen.blit(title_text, title_rect)
    screen.blit(score_text, score_rect)
    screen.blit(restart_text, restart_rect)
    screen.blit(quit_text, quit_rect)

    pygame.display.flip()
