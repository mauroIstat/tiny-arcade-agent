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
from .core.inputs import PlayerInput
from .core.rendering import render_game, render_game_over
from .core.sprites import load_sprites
from .core.entities import Ball, GameScreen, GameState, Paddle, Score, Winner
from .core.policies import player_policy

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
        screen=GameScreen.PLAYING,
        winner=None
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


def read_player_input() -> PlayerInput:
    keys = pygame.key.get_pressed()

    return PlayerInput(
        up=keys[pygame.K_UP],
        down=keys[pygame.K_DOWN],
    )


def get_winner(state: GameState, config: GameConfig) -> Winner | None:
    if state.score.player >= config.max_score:
        return Winner.PLAYER

    if state.score.opponent >= config.max_score:
        return Winner.OPPONENT

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
# Main game loop
# =============================================================================
# Every real-time game follows the same fundamental pattern:
#
#   -> Observe state
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
    title: str = "Tiny Pong Game",
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

    sprites = load_sprites(config)

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
        # Input
        # =============================================================================
        # Read the current keyboard state and convert it into a simple
        # PlayerInput object.
        #
        # Pygame stays here, inside the game loop.
        # The player policy receives only clean game input.
        # =============================================================================

        player_input = read_player_input()


        # =============================================================================
        # Actions
        # =============================================================================
        # Ask each policy what action it wants to perform.
        #
        # The human player policy uses PlayerInput.
        # The opponent policy observes the GameState and decides automatically.
        # =============================================================================

        player_action = player_policy(state, config, player_input)
        opponent_action = opponent_policy(state, config)


        # =============================================================================
        # Update simulation
        # =============================================================================
        # Apply actions, move the ball, detect collisions, and update the score.
        # =============================================================================

        move_paddle(state.player, player_action, config, dt)
        move_paddle(state.opponent, opponent_action, config, dt)
        move_ball(state.ball, dt)

        handle_wall_collisions(state.ball, config)
        handle_paddle_collisions(state)

        handle_score(state, config)

        # =============================================================================
        # Screen state
        # =============================================================================
        # Check whether the match is over and switch to the game-over screen.
        # =============================================================================

        winner = get_winner(state, config)

        if winner is not None:
            state.screen = GameScreen.GAME_OVER
            state.winner = winner


        if state.screen == GameScreen.PLAYING:
            render_game(screen, font, state, config, sprites)

        elif state.screen == GameScreen.GAME_OVER:
            render_game_over(screen, font, state, config, sprites)

            if wait_for_restart():
                state = create_initial_state(config)
            else:
                pygame.quit()
                sys.exit()
