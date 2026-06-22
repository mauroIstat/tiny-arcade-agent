from dataclasses import dataclass


@dataclass(frozen=True)
class PlayerInput:
    up: bool = False
    down: bool = False
