"""
Core game logic for Pong.

This module coordinates the execution of a Pong match.

Its responsibilities include:
- creating the initial game state;
- running the main game loop;
- updating the simulation;
- handling scoring and win conditions;
- rendering the game on screen.

The game loop follows the classic structure used by many
real-time games:

    Observe state
    -> Choose actions
    -> Update game state
    -> Render frame

This module acts as the orchestrator of the game, connecting
policies, physics, game state, and rendering.
"""

import sys
from collections.abc import Callable

import pygame

from .config import GameConfig
from .core.actions import Action
from .core.assets import GameAssets, load_assets
from .core.entities import Ball, GameState, Paddle, Score
from .core.geometry import make_ball_rect, make_paddle_rect
from .core.policies import keyboard_policy as player_policy

from .core.physics import (
    Direction,
    handle_paddle_collisions,
    handle_wall_collisions,
    move_ball,
    move_paddle,
    random_ball_vx,
    random_ball_vy,
    reset_ball,
)

Policy = Callable[[GameState, GameConfig], Action]


def create_initial_state(config: GameConfig) -> GameState:
    player = Paddle(
        x=config.paddle_margin,
        y=config.height / 2 - config.paddle_height / 2,
        width=config.paddle_width,
        height=config.paddle_height,
        speed=config.player_speed,
    )

    opponent = Paddle(
        x=config.width - config.paddle_margin - config.paddle_width,
        y=config.height / 2 - config.paddle_height / 2,
        width=config.paddle_width,
        height=config.paddle_height,
        speed=config.opponent_speed,
    )

    ball = Ball(
        x=config.width / 2 - config.ball_size / 2,
        y=config.height / 2 - config.ball_size / 2,
        size=config.ball_size,
        vx=random_ball_vx(config),
        vy=random_ball_vy(config),
    )

    score = Score()

    return GameState(
        player=player,
        opponent=opponent,
        ball=ball,
        score=score,
    )


def handle_score(state: GameState, config: GameConfig) -> None:
    ball = state.ball

    # Ball exits from the left side: point for opponent.
    if ball.x + ball.size < 0:
        state.score.opponent += 1
        reset_ball(ball, config, Direction.RIGHT)

    # Ball exits from the right side: point for player.
    if ball.x > config.width:
        state.score.player += 1
        reset_ball(ball, config, Direction.LEFT)


def get_winner(state: GameState, config: GameConfig) -> str | None:
    if state.score.player >= config.max_score:
        return "PLAYER"

    if state.score.opponent >= config.max_score:
        return "OPPONENT"

    return None


def wait_for_restart() -> bool:
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return False

                if event.key == pygame.K_SPACE:
                    return True



# =============================================================================
# Rendering
# =============================================================================
# draw_game() converts the current GameState into a visual
# representation that can be displayed on the screen.
#
# At every frame, the screen is cleared and redrawn from
# scratch using the latest game state.
# =============================================================================

def draw_game(
    screen: pygame.Surface,
    font: pygame.font.Font,
    state: GameState,
    config: GameConfig,
    assets: GameAssets,
) -> None:
    
    screen.blit(assets.background, (0, 0))

    draw_center_line(screen, config)

    screen.blit(assets.paddle, make_paddle_rect(state.player))
    screen.blit(assets.paddle, make_paddle_rect(state.opponent))
    screen.blit(assets.ball, make_ball_rect(state.ball))

    score_text = font.render(
        f"{state.score.player}   {state.score.opponent}",
        True,
        config.white,
    )

    score_rect = score_text.get_rect(center=(config.width / 2, 40))
    screen.blit(score_text, score_rect)

    pygame.display.flip()


def draw_game_over(
    screen: pygame.Surface,
    font: pygame.font.Font,
    state: GameState,
    config: GameConfig,
    winner: str,
) -> None:
    screen.fill(config.black)

    if winner == "PLAYER":
        message = "You win!"
    else:
        message = "Computer wins!"

    score_message = f"Final score: {state.score.player} - {state.score.opponent}"
    restart_message = "Press SPACE to play again or ESC to quit"

    message_text = font.render(message, True, config.white)
    score_text = font.render(score_message, True, config.white)
    restart_text = pygame.font.SysFont(None, 32).render(
        restart_message,
        True,
        config.white,
    )

    message_rect = message_text.get_rect(
        center=(config.width / 2, config.height / 2 - 60)
    )
    score_rect = score_text.get_rect(center=(config.width / 2, config.height / 2))
    restart_rect = restart_text.get_rect(
        center=(config.width / 2, config.height / 2 + 60)
    )

    screen.blit(message_text, message_rect)
    screen.blit(score_text, score_rect)
    screen.blit(restart_text, restart_rect)

    pygame.display.flip()


def draw_center_line(
    screen: pygame.Surface,
    config: GameConfig,
) -> None:
    neon_blue = (0, 220, 255)

    for y in range(0, config.height, 30):

        # Glow
        pygame.draw.rect(
            screen,
            neon_blue,
            (config.width // 2 - 4, y, 6, 15),
        )

        # Core
        pygame.draw.rect(
            screen,
            config.white,
            (config.width // 2 - 2, y, 4, 15),
        )


# =============================================================================
# Main game loop
# =============================================================================
# Every real-time game follows the same fundamental pattern:
#
#   Observe state
#   -> Choose actions
#   -> Update game state
#   -> Draw a new frame
#
# This cycle is repeated many times per second, creating the
# illusion of continuous motion.
#
# run_game() coordinates all these steps and keeps the
# simulation running until the player exits the game.
# =============================================================================

def run_game(
    opponent_policy: Policy,
    title: str = "Tiny Pong Agents",
    config: GameConfig | None = None,
) -> None:
    if config is None:
        config = GameConfig()

    # =============================================================================
    # Pygame initialization
    # =============================================================================
    # Pygame provides the game window, keyboard input handling,
    # graphics rendering, text drawing, and timing utilities.
    #
    # Here we create the game window and initialize the resources
    # needed by the game loop.
    # =============================================================================
    
    pygame.init()

    screen = pygame.display.set_mode((config.width, config.height))

    assets = load_assets(config)

    pygame.display.set_caption(title)

    clock = pygame.time.Clock()
    font = pygame.font.SysFont(None, 48)

    state = create_initial_state(config)

    while True:

        # =============================================================================
        # Frame timing
        # =============================================================================
        # Measure the time elapsed since the previous frame and limit
        # the maximum frame rate.
        #
        # The elapsed time (dt) is used to make movement independent
        # from the frame rate:
        #
        #     displacement = speed × time
        #
        # This ensures that the game runs at the same speed on both
        # fast and slow computers.
        # =============================================================================

        dt = clock.tick(config.fps) / 1000

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        # =============================================================================
        # Actions
        # =============================================================================
        
        # Ask each policy what action it wants to perform
        player_action = player_policy(state, config)
        opponent_action = opponent_policy(state, config)

        # Apply the chosen actions to the paddles
        move_paddle(state.player, player_action, config, dt)
        move_paddle(state.opponent, opponent_action, config, dt)
        move_ball(state.ball, dt)

        handle_wall_collisions(state.ball, config)
        handle_paddle_collisions(state)

        handle_score(state, config)

        winner = get_winner(state, config)

        if winner is not None:
            draw_game_over(screen, font, state, config, winner)

            if wait_for_restart():
                state = create_initial_state(config)
            else:
                pygame.quit()
                sys.exit()
        else:
            draw_game(screen, font, state, config, assets)
