from dataclasses import dataclass


@dataclass(frozen=True)
class PlayerInput:
    left: bool = False
    right: bool = False
