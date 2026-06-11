# Pong

Pong is the first game in Tiny Arcade Agent. It is small enough to understand in
one or two lessons, but rich enough to introduce many important programming and
game-development ideas.

There is no reinforcement learning in this first game. Instead, Pong uses simple
opponent controllers so students can compare different ways of making a computer
player behave.

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
python play.py
```

Controls:

- Up arrow: move the player paddle up.
- Down arrow: move the player paddle down.
- Space: restart after the match ends.
- Esc: quit from the game-over screen.

## Opponent controllers

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
python play.py --opponent random
python play.py --opponent sleepy
python play.py --opponent predictive
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
python play.py --speed slow
python play.py --speed super
```

You can combine opponent and speed:

```bash
python play.py --opponent defensive --speed fast
```

## Match length

Use `--max-score` to choose the score needed to win:

```bash
python play.py --max-score 3
```

## Code map

- `actions.py`: the possible actions for a paddle.
- `config.py`: game settings such as screen size, speeds, and max score.
- `entities.py`: the data objects used by the game.
- `geometry.py`: helpers that create pygame rectangles.
- `physics.py`: movement and collision rules.
- `controllers.py`: opponent algorithms.
- `game.py`: setup, drawing, input, scoring, and the main loop.

## Classroom activities

Try these small changes:

- Change `max_score` in `config.py`.
- Make the ball faster or slower.
- Change the paddle height.
- Make the `sleepy` opponent react faster.
- Add a new opponent controller that stays near the center until the ball gets
  close.
- Compare two opponents and write down which one is harder to beat and why.

## Discussion questions

- What information does an opponent need in order to play well?
- Why is `random` easy to beat?
- Why can `predictive` be stronger than `follow`?
- What makes a game feel fair instead of impossible?
