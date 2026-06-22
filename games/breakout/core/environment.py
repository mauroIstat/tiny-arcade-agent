"""
Environment-style Breakout logic.

The environment owns the game state and exposes reset() and step(action). This
lets the same game rules support both a visible pygame game and future learning
agents that run without opening a window.
"""

from .actions import Action
from .entities import Ball, Brick, GameScreen, GameState, Paddle
from .physics import (
    handle_brick_collision,
    handle_paddle_collision,
    handle_wall_collisions,
    is_ball_lost,
    move_ball,
    move_paddle,
    reset_ball_and_paddle,
)
from ..config import GameConfig


class BreakoutEnv:
    def __init__(self, config: GameConfig | None = None):
        if config is None:
            config = GameConfig()

        self.config = config
        self.state = self.create_initial_state()

    def create_initial_state(self) -> GameState:
        config = self.config

        paddle = Paddle(
            x=config.width / 2 - config.paddle_width / 2,
            y=config.height - config.paddle_bottom_margin - config.paddle_height,
            width=config.paddle_width,
            height=config.paddle_height,
            speed=config.paddle_speed,
        )

        ball = Ball(
            x=config.width / 2 - config.ball_size / 2,
            y=paddle.y - config.ball_size - config.ball_paddle_gap,
            size=config.ball_size,
            vx=config.ball_speed_x,
            vy=config.ball_speed_y,
        )

        bricks = []

        for row in range(config.brick_rows):
            for column in range(config.brick_columns):
                x = config.brick_left_margin + column * (
                    config.brick_width + config.brick_gap
                )
                y = config.brick_top_margin + row * (
                    config.brick_height + config.brick_gap
                )

                bricks.append(
                    Brick(
                        row=row,
                        column=column,
                        x=x,
                        y=y,
                        width=config.brick_width,
                        height=config.brick_height,
                    )
                )

        return GameState(
            paddle=paddle,
            ball=ball,
            bricks=bricks,
            score=0,
            lives=config.starting_lives,
            screen=GameScreen.PLAYING,
        )

    def reset(self) -> dict:
        self.state = self.create_initial_state()
        return self.observe()

    def observe(self) -> dict:
        state = self.state

        return {
            "paddle": {
                "x": state.paddle.x,
                "center_x": state.paddle.center_x,
                "y": state.paddle.y,
            },
            "ball": {
                "x": state.ball.x,
                "y": state.ball.y,
                "vx": state.ball.vx,
                "vy": state.ball.vy,
            },
            "bricks": [
                {
                    "row": brick.row,
                    "column": brick.column,
                    "alive": brick.alive,
                }
                for brick in state.bricks
            ],
            "score": state.score,
            "lives": state.lives,
            "bricks_left": state.bricks_left,
            "screen": state.screen.name,
        }

    def step(
        self,
        action: Action,
        dt: float | None = None,
    ) -> tuple[dict, float, bool, bool, dict]:
        config = self.config
        state = self.state

        if dt is None:
            dt = 1 / config.fps

        if state.screen != GameScreen.PLAYING:
            return self.observe(), 0.0, True, False, {"events": []}

        reward = 0.0
        events = []

        move_paddle(state.paddle, action, config, dt)
        move_ball(state.ball, dt)

        handle_wall_collisions(state.ball, config)

        if handle_paddle_collision(state, config):
            reward += config.paddle_hit_reward
            events.append("paddle_hit")

        if handle_brick_collision(state):
            reward += config.brick_reward
            events.append("brick_destroyed")

        if state.bricks_left == 0:
            state.screen = GameScreen.VICTORY
            reward += config.victory_reward
            events.append("victory")

        if is_ball_lost(state.ball, config):
            state.lives -= 1
            reward += config.lost_ball_reward
            events.append("lost_ball")

            if state.lives <= 0:
                state.screen = GameScreen.GAME_OVER
                events.append("game_over")
            else:
                reset_ball_and_paddle(state, config)

        terminated = state.screen != GameScreen.PLAYING
        truncated = False
        info = {"events": events}

        return self.observe(), reward, terminated, truncated, info
