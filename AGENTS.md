# AGENTS.md

## Project Purpose

Tiny Arcade Agent is a learning project for teaching coding and reinforcement
learning through small Atari-style arcade games.

The target audience is mixed: secondary-school students and undergraduates. Code
should therefore be approachable for beginners while still leaving room for more
advanced students to ask deeper questions about algorithms, game state, and
learning agents.

Pong is the first game. It introduces the core programming ideas behind games:
state, input, movement, collisions, scoring, and simple computer-controlled
opponents. In Pong, use the word `policy` for functions that choose actions
from game state and input.

Breakout is the intended next step. It should connect game mechanics to the
first reinforcement learning ideas: observations, actions, rewards, episodes,
terminal states, and eventually simple Q-learning.

## Teaching Philosophy

- Treat games as teaching material first and software second.
- Prefer simple, readable Python over clever abstractions.
- Keep important concepts visible in the code: state, actions, update loops,
  collisions, rewards, and episodes.
- Write code that students can inspect, modify, and discuss in class.
- Favor small changes that create useful classroom experiments.
- Avoid introducing frameworks or patterns that hide the lesson being taught.

## Architecture Guidelines

- Keep game state, physics/rules, policies or agents, rendering, and command
  line entrypoints separated where practical.
- Use `pygame` for playable visualizations, but design future reinforcement
  learning logic so it can run without opening a window.
- Prefer sprites for visible game objects. If an expected sprite file is
  missing, render a simple geometric fallback so the game still runs.
- Keep modules focused and names beginner-friendly.
- Prefer explicit data objects and functions over metaprogramming or deeply
  nested class hierarchies.
- Do not add large dependencies unless they clearly support a learning goal.
- Preserve the existing student-facing README style: direct, plain, and
  activity-oriented.

## Launcher Guidelines

- Keep launchers separate while each game is still being introduced.
- Pong is launched with `play_pong.py`.
- Breakout should be launched with `play_breakout.py` when it is implemented.
- Do not create a shared `play.py` launcher yet. A shared launcher can be added
  later as a classroom refactoring exercise after students have seen at least
  two separate launchers.

## Breakout Progression

Build Breakout in stages. Do not skip directly to neural networks or large RL
frameworks.

1. Playable Breakout: one paddle, one ball, a grid of bricks, wall collisions,
   paddle collisions, brick collisions, score, lives, game over, and victory.
   Use sprites for the visible paddle, ball, bricks, and background, following
   the same spirit as Pong.
2. Policy-based Breakout: add policies that choose `LEFT`, `RIGHT`, or `STAY`
   from the current game state.
3. Environment-style Breakout: add `reset()` and `step(action)` so the game can
   run without a visible window and return observations, rewards, terminal
   states, and extra info.
4. Q-table agent: introduce state discretization, epsilon-greedy exploration,
   and the Bellman update.
5. MLP-based Deep Q-Learning: replace the Q-table with a small neural network
   that receives numeric features and returns Q-values.
6. Image-based DQN is a future extension only. Do not design the first Breakout
   implementation around image observations.

## Reinforcement Learning Direction

Breakout should become the first game that behaves like a simple environment:

- `reset` starts a new episode.
- `step(action)` advances the world by one decision and returns the information
  needed to learn from that decision.
- Observations describe the current game state in a form a beginner can
  understand.
- Rewards should be tied to visible events, such as breaking a brick, losing a
  life, or clearing the board.
- Terminal states should make it clear when an episode is over.

This project may use a Gymnasium-like shape for future environments, but
Gymnasium should not be required yet. The first learning-agent milestone is
simple Q-learning, not deep reinforcement learning.

For the first Breakout environment milestone:

- Prefer a readable dictionary observation before numeric vectors.
- One `step(action)` should advance the world by one frame.
- Use beginner-friendly rewards tied to visible events:
  - positive reward for breaking a brick;
  - small positive reward for hitting the ball with the paddle;
  - negative reward for losing the ball;
  - larger positive reward for clearing the board.
- Keep brick identities stable by row and column so future Q-table and DQN
  examples can refer to bricks consistently.
- Do not require Gymnasium, PyTorch, TensorFlow, or other RL libraries for the
  first Breakout stages.

## Documentation Guidance

- When adding or renaming entrypoints, update both the root README and the
  game-specific README.
- Keep game READMEs aligned with the actual module names in the repository.
- Prefer the term `policy` for simple decision functions. Use `agent` when code
  starts to store learning state, such as a Q-table or neural network.

## Contribution Guidance

- When adding a new mechanic, also consider adding a small classroom activity or
  discussion prompt.
- Keep examples runnable from the project root where possible.
- Make code changes easy for students to trace from input to state update to
  screen output.
- Avoid premature optimization. Clarity is more important than squeezing out
  performance in these small games.
