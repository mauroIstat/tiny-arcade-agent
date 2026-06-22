# Pong

Pong is the first game in Tiny Arcade Agent. It is small enough to understand in
one or two lessons, but rich enough to introduce many important programming and
game-development ideas.

There is no reinforcement learning in this first game. Instead, Pong uses simple
opponent policies so students can compare different ways of making a computer
player behave. A policy is a function that looks at the game state and chooses
an action.

## Learning goals

By studying Pong, students should understand:

- How a game loop works.
- How keyboard input becomes player movement.
- How game state stores paddles, the ball, and the score.
- How positions and speeds change over time.
- How collisions with walls and paddles are detected.
- How configuration values make a game easier to tune.
- How simple algorithms can control a virtual opponent.

## How to play

From the project root, run:

```bash
python play_pong.py
```

Controls:

- Up arrow: move the player paddle up.
- Down arrow: move the player paddle down.
- Space: restart after the match ends.
- Esc: quit from the game-over screen.

## The game loop

Pong does not wait for one big event to happen. Instead, it runs the same small
cycle again and again, one frame at a time.

On each frame, the game:

- reads the keyboard input;
- moves the player paddle;
- asks the opponent policy what to do;
- moves the opponent paddle and the ball;
- checks for wall and paddle collisions;
- updates the score if the ball leaves the screen;
- draws the new state on the screen.

Then the next frame starts and the cycle repeats.

The `fps` value in `config.py` means frames per second. With `fps = 60`, the game
tries to run this cycle about 60 times every second. A higher value means the
screen can update more often. A lower value makes each update easier to notice,
which can be useful when studying how the game works.

## Opponent policies

The opponent is controlled by a function that receives the current game state
and returns an action: up, down, or stay.

Available opponents:

- `random`: chooses a random action.
- `very-lazy`: follows the ball only when it is far away.
- `lazy`: follows the ball with a smaller tolerance.
- `sleepy`: reacts only every few frames.
- `noisy`: follows the ball but sometimes makes mistakes.
- `defensive`: follows the ball only when it is coming toward the opponent.
- `follow`: always moves toward the ball.
- `predictive`: predicts where the ball will arrive.
- `predictive-error`: predicts like `predictive`, but sometimes makes mistakes.

Examples:

```bash
python play_pong.py --opponent random
python play_pong.py --opponent sleepy
python play_pong.py --opponent predictive
```

## Speed levels

The opponent can also move at different speeds:

- `very-slow`
- `slow`
- `medium`
- `fast`
- `super`

Examples:

```bash
python play_pong.py --speed slow
python play_pong.py --speed super
```

You can combine opponent and speed:

```bash
python play_pong.py --opponent defensive --speed fast
```

## Match length

Use `--max-score` to choose the score needed to win:

```bash
python play_pong.py --max-score 3
```

## Code map

- `config.py`: game settings such as screen size, speeds, and max score.
- `game.py`: orchestrates setup, input, policies, physics, scoring, rendering,
  and the main loop.
- `core/actions.py`: the possible actions for a paddle.
- `core/inputs.py`: keyboard input stored in a simple object.
- `core/policies.py`: human and computer decision functions.
- `core/entities.py`: the data objects used by the game.
- `core/geometry.py`: helpers that create pygame rectangles.
- `core/physics.py`: movement and collision rules.
- `core/rendering.py`: functions that draw the game state.
- `core/sprites.py`: functions that load image assets.

## Classroom activities

Try these small changes:

- Change `max_score` in `config.py`.
- Make the ball faster or slower.
- Change the paddle height.
- Make the `sleepy` opponent react faster.
- Add a new opponent policy that stays near the center until the ball gets
  close.
- Compare two opponents and write down which one is harder to beat and why.

## Discussion questions

- What information does an opponent need in order to play well?
- Why is `random` easy to beat?
- Why can `predictive` be stronger than `follow`?
- What makes a game feel fair instead of impossible?
