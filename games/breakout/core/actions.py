"""
Actions for the Breakout game.

An action represents a decision made by a human player or by a policy.
"""

from enum import Enum


class Action(Enum):
    LEFT = "LEFT"
    RIGHT = "RIGHT"
    STAY = "STAY"
