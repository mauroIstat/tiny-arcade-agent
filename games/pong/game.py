import sys
from collections.abc import Callable

import pygame

from .config import GameConfig
from .core.actions import Action
from .core.entities import Ball, GameState, Paddle, Score

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

from .core.geometry import make_ball_rect, make_paddle_rect


OpponentStrategy = Callable[[GameState, GameConfig], Action]


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


def get_player_action() -> Action:
    keys = pygame.key.get_pressed()

    if keys[pygame.K_UP]:
        return Action.UP

    if keys[pygame.K_DOWN]:
        return Action.DOWN

    return Action.STAY


def draw_center_line(screen: pygame.Surface, config: GameConfig) -> None:
    for y in range(0, config.height, 30):
        pygame.draw.rect(
            screen,
            config.white,
            (config.width // 2 - 2, y, 4, 15),
        )


def draw_game(
    screen: pygame.Surface,
    font: pygame.font.Font,
    state: GameState,
    config: GameConfig,
) -> None:
    screen.fill(config.black)

    draw_center_line(screen, config)

    pygame.draw.rect(screen, config.white, make_paddle_rect(state.player))
    pygame.draw.rect(screen, config.white, make_paddle_rect(state.opponent))
    pygame.draw.rect(screen, config.white, make_ball_rect(state.ball))

    score_text = font.render(
        f"{state.score.player}   {state.score.opponent}",
        True,
        config.white,
    )

    score_rect = score_text.get_rect(center=(config.width / 2, 40))
    screen.blit(score_text, score_rect)

    pygame.display.flip()


def draw_game_over(
    screen: pygame.Surface,
    font: pygame.font.Font,
    state: GameState,
    config: GameConfig,
    winner: str,
) -> None:
    screen.fill(config.black)

    if winner == "PLAYER":
        message = "You win!"
    else:
        message = "Computer wins!"

    score_message = f"Final score: {state.score.player} - {state.score.opponent}"
    restart_message = "Press SPACE to play again or ESC to quit"

    message_text = font.render(message, True, config.white)
    score_text = font.render(score_message, True, config.white)
    restart_text = pygame.font.SysFont(None, 32).render(
        restart_message,
        True,
        config.white,
    )

    message_rect = message_text.get_rect(
        center=(config.width / 2, config.height / 2 - 60)
    )
    score_rect = score_text.get_rect(
        center=(config.width / 2, config.height / 2)
    )
    restart_rect = restart_text.get_rect(
        center=(config.width / 2, config.height / 2 + 60)
    )

    screen.blit(message_text, message_rect)
    screen.blit(score_text, score_rect)
    screen.blit(restart_text, restart_rect)

    pygame.display.flip()


def get_winner(state: GameState, config: GameConfig) -> str | None:
    if state.score.player >= config.max_score:
        return "PLAYER"

    if state.score.opponent >= config.max_score:
        return "OPPONENT"

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


def run_game(
    opponent_strategy: OpponentStrategy,
    title: str = "Tiny Pong Agents",
    config: GameConfig | None = None,
) -> None:
    if config is None:
        config = GameConfig()

    pygame.init()

    screen = pygame.display.set_mode((config.width, config.height))
    pygame.display.set_caption(title)

    clock = pygame.time.Clock()
    font = pygame.font.SysFont(None, 48)

    state = create_initial_state(config)

    while True:
        dt = clock.tick(config.fps) / 1000

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        player_action = get_player_action()
        move_paddle(state.player, player_action, config, dt)

        opponent_action = opponent_strategy(state, config)
        move_paddle(state.opponent, opponent_action, config, dt)

        move_ball(state.ball, dt)
        handle_wall_collisions(state.ball, config)
        handle_paddle_collisions(state)
        handle_score(state, config)

        winner = get_winner(state, config)

        if winner is not None:
            draw_game_over(screen, font, state, config, winner)

            if wait_for_restart():
                state = create_initial_state(config)
            else:
                pygame.quit()
                sys.exit()
        else:
            draw_game(screen, font, state, config)
