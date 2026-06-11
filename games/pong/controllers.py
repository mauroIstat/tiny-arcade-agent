import random

from .actions import Action
from .config import GameConfig
from .entities import GameState


def do_nothing(state: GameState, config: GameConfig) -> Action:
    return Action.STAY


def rand(state: GameState, config: GameConfig) -> Action:
    return random.choice([Action.UP, Action.DOWN, Action.STAY])


def follow_ball(state: GameState, config: GameConfig) -> Action:
    ball = state.ball
    opponent = state.opponent

    if ball.center_y < opponent.center_y:
        return Action.UP

    if ball.center_y > opponent.center_y:
        return Action.DOWN

    return Action.STAY


def lazy_follow_ball(state: GameState, config: GameConfig) -> Action:
    ball = state.ball
    opponent = state.opponent
    tolerance = 25

    if ball.center_y < opponent.center_y - tolerance:
        return Action.UP

    if ball.center_y > opponent.center_y + tolerance:
        return Action.DOWN

    return Action.STAY


def predictive(state: GameState, config: GameConfig) -> Action:
    ball = state.ball
    opponent = state.opponent

    # If the ball is moving away from the opponent,
    # the opponent returns to the center.
    if ball.vx < 0:
        target_y = config.height / 2

    else:
        distance_x = opponent.x - ball.x

        if ball.vx == 0:
            target_y = ball.center_y
        else:
            time_to_reach = distance_x / ball.vx
            target_y = ball.center_y + ball.vy * time_to_reach

        # Approximate reflection on top/bottom walls.
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


def predictive_with_error(state: GameState, config: GameConfig) -> Action:
    # 10% of the time, make a random move.
    if random.random() < 0.10:
        return random.choice([Action.UP, Action.DOWN, Action.STAY])

    return predictive(state, config)


def sleepy_follow_ball(state: GameState, config: GameConfig) -> Action:
    """
    Opponent with slow reflexes.
    It updates its decision only every N frames.
    """
    ball = state.ball
    opponent = state.opponent

    # This controller is stateful: it remembers its frame counter and previous
    # action between calls, so it reacts only once every reaction interval.
    if not hasattr(sleepy_follow_ball, "counter"):
        sleepy_follow_ball.counter = 0
        sleepy_follow_ball.current_action = Action.STAY

    sleepy_follow_ball.counter += 1

    reaction_interval = 20  # Higher values make the opponent easier to beat.

    if sleepy_follow_ball.counter >= reaction_interval:
        sleepy_follow_ball.counter = 0

        if ball.center_y < opponent.center_y:
            sleepy_follow_ball.current_action = Action.UP
        elif ball.center_y > opponent.center_y:
            sleepy_follow_ball.current_action = Action.DOWN
        else:
            sleepy_follow_ball.current_action = Action.STAY

    return sleepy_follow_ball.current_action


def defensive_follow_ball(state: GameState, config: GameConfig) -> Action:
    """
    Opponent follows the ball only when the ball is moving toward it.
    Otherwise, it slowly returns to the center.
    """
    ball = state.ball
    opponent = state.opponent

    center_y = config.height / 2
    tolerance = 20

    # Ball moving toward opponent on the right.
    if ball.vx > 0:
        if ball.center_y < opponent.center_y - tolerance:
            return Action.UP
        if ball.center_y > opponent.center_y + tolerance:
            return Action.DOWN
        return Action.STAY

    # Ball moving away: return to center.
    if opponent.center_y < center_y - tolerance:
        return Action.DOWN
    if opponent.center_y > center_y + tolerance:
        return Action.UP

    return Action.STAY


def very_lazy_follow_ball(state: GameState, config: GameConfig) -> Action:
    """
    Opponent follows the ball, but only if the ball is far from the paddle center.
    """
    ball = state.ball
    opponent = state.opponent

    tolerance = 60  # Higher values make the opponent lazier and easier.

    if ball.center_y < opponent.center_y - tolerance:
        return Action.UP

    if ball.center_y > opponent.center_y + tolerance:
        return Action.DOWN

    return Action.STAY


def noisy_follow_ball(state: GameState, config: GameConfig) -> Action:
    """
    Opponent follows the ball, but sometimes makes mistakes.
    """
    mistake_probability = 0.20  # 20% chance of making a mistake.

    if random.random() < mistake_probability:
        return random.choice([Action.UP, Action.DOWN, Action.STAY])

    return follow_ball(state, config)
