import unittest

from games.breakout.config import GameConfig
from games.breakout.core.actions import Action
from games.breakout.core.entities import GameScreen
from games.breakout.core.environment import BreakoutEnv
from games.breakout.core.physics import handle_paddle_collision, move_paddle


class BreakoutEnvironmentTest(unittest.TestCase):
    def test_reset_creates_starting_state(self):
        config = GameConfig()
        env = BreakoutEnv(config)

        observation = env.reset()

        self.assertEqual(observation["score"], 0)
        self.assertEqual(observation["lives"], config.starting_lives)
        self.assertEqual(observation["bricks_left"], config.brick_rows * config.brick_columns)
        self.assertEqual(observation["screen"], "PLAYING")

    def test_ball_starts_above_paddle_with_configured_gap(self):
        config = GameConfig(ball_paddle_gap=12)
        env = BreakoutEnv(config)

        expected_y = env.state.paddle.y - config.ball_size - config.ball_paddle_gap

        self.assertEqual(env.state.ball.y, expected_y)

    def test_paddle_stays_inside_screen(self):
        config = GameConfig()
        env = BreakoutEnv(config)
        paddle = env.state.paddle

        move_paddle(paddle, Action.LEFT, config, dt=10)
        self.assertEqual(paddle.x, 0)

        move_paddle(paddle, Action.RIGHT, config, dt=10)
        self.assertEqual(paddle.x, config.width - paddle.width)

    def test_paddle_bounce_strength_controls_horizontal_velocity(self):
        config = GameConfig(ball_speed_x=100, paddle_bounce_strength=2.0)
        env = BreakoutEnv(config)

        env.state.ball.x = env.state.paddle.x + env.state.paddle.width - env.state.ball.size
        env.state.ball.y = env.state.paddle.y
        env.state.ball.vy = abs(env.state.ball.vy)

        hit = handle_paddle_collision(env.state, config)

        self.assertTrue(hit)
        self.assertAlmostEqual(env.state.ball.vx, 168.0)

    def test_breaking_a_brick_gives_reward(self):
        config = GameConfig()
        env = BreakoutEnv(config)
        brick = env.state.bricks[0]

        env.state.ball.x = brick.x + brick.width / 2
        env.state.ball.y = brick.y + brick.height / 2
        env.state.ball.vy = -abs(env.state.ball.vy)

        observation, reward, terminated, truncated, info = env.step(Action.STAY)

        self.assertEqual(observation["bricks_left"], config.brick_rows * config.brick_columns - 1)
        self.assertEqual(reward, config.brick_reward)
        self.assertFalse(terminated)
        self.assertFalse(truncated)
        self.assertIn("brick_destroyed", info["events"])

    def test_losing_ball_removes_life_and_resets_ball(self):
        config = GameConfig()
        env = BreakoutEnv(config)

        env.state.ball.y = config.height + 10
        env.state.ball.vy = 0

        observation, reward, terminated, truncated, info = env.step(Action.STAY)

        self.assertEqual(observation["lives"], config.starting_lives - 1)
        self.assertEqual(reward, config.lost_ball_reward)
        self.assertFalse(terminated)
        self.assertFalse(truncated)
        self.assertIn("lost_ball", info["events"])

    def test_clearing_last_brick_ends_episode(self):
        config = GameConfig()
        env = BreakoutEnv(config)

        for brick in env.state.bricks[1:]:
            brick.alive = False

        last_brick = env.state.bricks[0]
        env.state.ball.x = last_brick.x + last_brick.width / 2
        env.state.ball.y = last_brick.y + last_brick.height / 2
        env.state.ball.vy = -abs(env.state.ball.vy)

        observation, reward, terminated, truncated, info = env.step(Action.STAY)

        self.assertEqual(observation["screen"], "VICTORY")
        self.assertEqual(reward, config.brick_reward + config.victory_reward)
        self.assertTrue(terminated)
        self.assertFalse(truncated)
        self.assertIn("victory", info["events"])

    def test_losing_final_life_ends_episode(self):
        config = GameConfig()
        env = BreakoutEnv(config)

        env.state.lives = 1
        env.state.ball.y = config.height + 10
        env.state.ball.vy = 0

        observation, reward, terminated, truncated, info = env.step(Action.STAY)

        self.assertEqual(observation["screen"], "GAME_OVER")
        self.assertEqual(env.state.screen, GameScreen.GAME_OVER)
        self.assertEqual(reward, config.lost_ball_reward)
        self.assertTrue(terminated)
        self.assertFalse(truncated)
        self.assertIn("game_over", info["events"])


if __name__ == "__main__":
    unittest.main()
