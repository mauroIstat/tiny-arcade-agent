"""
Policies for the Breakout game.

A policy observes the current game state and returns an action.
"""

import random

from .actions import Action
from .entities import GameState
from .inputs import PlayerInput
from ..config import GameConfig


def keyboard_policy(
    state: GameState,
    config: GameConfig,
    player_input: PlayerInput,
) -> Action:
    if player_input.left:
        return Action.LEFT

    if player_input.right:
        return Action.RIGHT

    return Action.STAY


def do_nothing_policy(state: GameState, config: GameConfig) -> Action:
    return Action.STAY


def random_policy(state: GameState, config: GameConfig) -> Action:
    return random.choice([Action.LEFT, Action.RIGHT, Action.STAY])


def follow_ball_policy(state: GameState, config: GameConfig) -> Action:
    if state.ball.center_x < state.paddle.center_x:
        return Action.LEFT

    if state.ball.center_x > state.paddle.center_x:
        return Action.RIGHT

    return Action.STAY


def noisy_follow_ball_policy(state: GameState, config: GameConfig) -> Action:
    if random.random() < 0.15:
        return random_policy(state, config)

    return follow_ball_policy(state, config)
