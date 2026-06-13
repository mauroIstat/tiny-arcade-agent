"""
Actions for the Pong game.

An action represents a possible decision made by a controller.
In this game, a paddle can move up, move down, or stay still.
"""

from enum import Enum


class Action(Enum):
    UP = "UP"
    DOWN = "DOWN"
    STAY = "STAY"
