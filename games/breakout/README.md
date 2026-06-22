# Breakout

Breakout is the second game in Tiny Arcade Agent. It builds on the same project
structure used by Pong, then adds the first reinforcement learning ideas:
observations, actions, rewards, episodes, and terminal states.

In this first version, Breakout is both a playable game and a small environment
that can run one step at a time.

## Learning goals

By studying Breakout, students should understand:

- How a richer game state stores a paddle, a ball, bricks, score, and lives.
- How actions move the paddle left, right, or not at all.
- How collisions with walls, the paddle, and bricks change the state.
- How rewards can be connected to visible events.
- How `reset()` starts an episode.
- How `step(action)` advances the environment by one decision.
- How simple policies can control a game without learning yet.

## How to play

From the project root, run:

```bash
python play_breakout.py
```

Controls:

- Left arrow: move the paddle left.
- Right arrow: move the paddle right.
- Space: restart after the episode ends.
- Esc: quit from the end screen.

## Policies

Breakout can also be controlled by simple policies:

```bash
python play_breakout.py --policy random
python play_breakout.py --policy follow
python play_breakout.py --policy noisy
```

Available policies:

- `keyboard`: controlled by the human player.
- `do-nothing`: never moves the paddle.
- `random`: chooses a random action.
- `follow`: moves the paddle toward the ball.
- `noisy`: usually follows the ball, but sometimes makes a random move.

## Environment shape

The environment lives in `core/environment.py`.

It has two important methods:

```python
observation = env.reset()
observation, reward, terminated, truncated, info = env.step(action)
```

For now, the observation is a readable dictionary. This makes it easier to
inspect in class before introducing numeric vectors for Q-learning.

Rewards are tied to visible events:

- breaking a brick gives a positive reward;
- hitting the ball with the paddle gives a small positive reward;
- losing the ball gives a negative reward;
- clearing all bricks gives a larger positive reward.

## Code map

- `config.py`: game settings such as screen size, speeds, layout, and rewards.
- `game.py`: orchestrates pygame input, policies, environment steps, rendering,
  and the main loop.
- `core/actions.py`: the possible actions for the paddle.
- `core/inputs.py`: keyboard input stored in a simple object.
- `core/policies.py`: human and computer decision functions.
- `core/entities.py`: the data objects used by the game.
- `core/environment.py`: `reset()` and `step(action)` environment logic.
- `core/geometry.py`: helpers that create pygame rectangles.
- `core/physics.py`: movement and collision rules.
- `core/rendering.py`: functions that draw the game state.
- `core/sprites.py`: functions that load image assets.

## Sprites and fallback shapes

Breakout is designed to use sprites for the background, paddle, ball, and
bricks. If an image file is missing, the renderer draws a simple geometric shape
instead. This lets the class work on gameplay first and improve the artwork
later.

Expected asset paths:

- `assets/backgrounds/breakout_background.png`
- `assets/paddles/breakout_paddle.png`
- `assets/balls/breakout_ball.png`
- `assets/bricks/breakout_brick.png`

## Classroom activities

Try these small changes:

- Change the number of brick rows or columns.
- Make the paddle wider or narrower.
- Make the ball faster or slower.
- Change the reward for breaking a brick.
- Compare the `random`, `follow`, and `noisy` policies.
- Print the observation returned by `reset()` and discuss what an agent can see.
