"""
Policies for the Pong game.

A policy is a function that observes the current game state
and returns an action.

This module contains:
- a human policy, based on keyboard input;
- several rule-based computer policies.

Later, learning-based policies can be added to introduce
reinforcement learning.
"""

import random

import pygame

from .actions import Action
from .entities import GameState
from ..config import GameConfig

# =============================================================================
# Human policies
# =============================================================================
# A human policy reads input from the keyboard and converts it into an Action.
# In this game, the human player can move the paddle up, down, or keep it still.
# =============================================================================


def keyboard_policy(state: GameState, config: GameConfig) -> Action:
    keys = pygame.key.get_pressed()

    if keys[pygame.K_UP]:
        return Action.UP

    if keys[pygame.K_DOWN]:
        return Action.DOWN

    return Action.STAY


# =============================================================================
# Rule-based computer policies
# =============================================================================
# A computer policy looks at the current GameState and chooses an Action.
# These policies do not learn: their behavior is entirely defined by rules.
#
# Later, in other games, we will replace rule-based policies with learning
# policies, such as reinforcement learning agents.
# =============================================================================
def do_nothing_policy(state: GameState, config: GameConfig) -> Action:
    """Always keep the paddle still."""
    return Action.STAY


def random_policy(state: GameState, config: GameConfig) -> Action:
    """Choose a random action."""
    return random.choice([Action.UP, Action.DOWN, Action.STAY])


def very_lazy_follow_ball_policy(state: GameState, config: GameConfig) -> Action:
    """Follow the ball only if it is far from the paddle center."""
    ball = state.ball
    opponent = state.opponent

    tolerance = 60

    if ball.center_y < opponent.center_y - tolerance:
        return Action.UP

    if ball.center_y > opponent.center_y + tolerance:
        return Action.DOWN

    return Action.STAY


def lazy_follow_ball_policy(state: GameState, config: GameConfig) -> Action:
    """Follow the ball with a small tolerance around the paddle center."""
    ball = state.ball
    opponent = state.opponent

    tolerance = 25

    if ball.center_y < opponent.center_y - tolerance:
        return Action.UP

    if ball.center_y > opponent.center_y + tolerance:
        return Action.DOWN

    return Action.STAY


def follow_ball_policy(state: GameState, config: GameConfig) -> Action:
    """Always move toward the current vertical position of the ball."""
    ball = state.ball
    opponent = state.opponent

    if ball.center_y < opponent.center_y:
        return Action.UP

    if ball.center_y > opponent.center_y:
        return Action.DOWN

    return Action.STAY


def noisy_follow_ball_policy(state: GameState, config: GameConfig) -> Action:
    """Follow the ball, but sometimes make a random mistake."""
    mistake_probability = 0.20

    if random.random() < mistake_probability:
        return random.choice([Action.UP, Action.DOWN, Action.STAY])

    return follow_ball_policy(state, config)


def sleepy_follow_ball_policy(state: GameState, config: GameConfig) -> Action:
    """
    Follow the ball with slow reflexes.

    The policy updates its decision only every few frames.
    """
    ball = state.ball
    opponent = state.opponent

    if not hasattr(sleepy_follow_ball_policy, "counter"):
        sleepy_follow_ball_policy.counter = 0
        sleepy_follow_ball_policy.current_action = Action.STAY

    sleepy_follow_ball_policy.counter += 1

    reaction_interval = 20

    if sleepy_follow_ball_policy.counter >= reaction_interval:
        sleepy_follow_ball_policy.counter = 0

        if ball.center_y < opponent.center_y:
            sleepy_follow_ball_policy.current_action = Action.UP
        elif ball.center_y > opponent.center_y:
            sleepy_follow_ball_policy.current_action = Action.DOWN
        else:
            sleepy_follow_ball_policy.current_action = Action.STAY

    return sleepy_follow_ball_policy.current_action


def defensive_follow_ball_policy(state: GameState, config: GameConfig) -> Action:
    """
    Follow the ball only when it is moving toward the opponent.

    Otherwise, slowly return to the center.
    """
    ball = state.ball
    opponent = state.opponent

    center_y = config.height / 2
    tolerance = 20

    if ball.vx > 0:
        if ball.center_y < opponent.center_y - tolerance:
            return Action.UP
        if ball.center_y > opponent.center_y + tolerance:
            return Action.DOWN
        return Action.STAY

    if opponent.center_y < center_y - tolerance:
        return Action.DOWN

    if opponent.center_y > center_y + tolerance:
        return Action.UP

    return Action.STAY


def predictive_policy(state: GameState, config: GameConfig) -> Action:
    """Predict where the ball will reach the opponent paddle."""
    ball = state.ball
    opponent = state.opponent

    if ball.vx < 0:
        target_y = config.height / 2
    else:
        distance_x = opponent.x - ball.x

        if ball.vx == 0:
            target_y = ball.center_y
        else:
            time_to_reach = distance_x / ball.vx
            target_y = ball.center_y + ball.vy * time_to_reach

        while target_y < 0 or target_y > config.height:
            if target_y < 0:
                target_y = -target_y
            elif target_y > config.height:
                target_y = 2 * config.height - target_y

    if target_y < opponent.center_y:
        return Action.UP

    if target_y > opponent.center_y:
        return Action.DOWN

    return Action.STAY


def predictive_with_error_policy(state: GameState, config: GameConfig) -> Action:
    """Use the predictive policy, but sometimes make a random mistake."""
    if random.random() < 0.10:
        return random.choice([Action.UP, Action.DOWN, Action.STAY])

    return predictive_policy(state, config)