"""
Core game loop for Breakout.

This module connects pygame input, policies, the environment step, and
rendering.
"""

import sys
from collections.abc import Callable

import pygame

from .config import GameConfig
from .core.actions import Action
from .core.entities import GameScreen, GameState
from .core.environment import BreakoutEnv
from .core.inputs import PlayerInput
from .core.policies import keyboard_policy
from .core.rendering import render_end_screen, render_game
from .core.sprites import load_sprites

Policy = Callable[[GameState, GameConfig], Action]


def read_player_input() -> PlayerInput:
    keys = pygame.key.get_pressed()

    return PlayerInput(
        left=keys[pygame.K_LEFT],
        right=keys[pygame.K_RIGHT],
    )


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


def run_game(
    policy: Policy | None = None,
    title: str = "Tiny Arcade Agents - Breakout",
    config: GameConfig | None = None,
) -> None:
    if config is None:
        config = GameConfig()

    pygame.init()

    screen = pygame.display.set_mode((config.width, config.height))
    pygame.display.set_caption(title)

    sprites = load_sprites(config)
    clock = pygame.time.Clock()
    font = pygame.font.SysFont(None, 34)

    env = BreakoutEnv(config)

    while True:
        dt = clock.tick(config.fps) / 1000

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        if env.state.screen == GameScreen.PLAYING:
            if policy is None:
                player_input = read_player_input()
                action = keyboard_policy(env.state, config, player_input)
            else:
                action = policy(env.state, config)

            env.step(action, dt)
            render_game(screen, font, env.state, config, sprites)

        else:
            render_end_screen(screen, font, env.state, config, sprites)

            if wait_for_restart():
                env.reset()
            else:
                pygame.quit()
                sys.exit()
