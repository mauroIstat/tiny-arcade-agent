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
opponents.

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

- Keep game state, physics/rules, controllers or agents, rendering, and command
  line entrypoints separated where practical.
- Use `pygame` for playable visualizations, but design future reinforcement
  learning logic so it can run without opening a window.
- Keep modules focused and names beginner-friendly.
- Prefer explicit data objects and functions over metaprogramming or deeply
  nested class hierarchies.
- Do not add large dependencies unless they clearly support a learning goal.
- Preserve the existing student-facing README style: direct, plain, and
  activity-oriented.

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

## Contribution Guidance

- When adding a new mechanic, also consider adding a small classroom activity or
  discussion prompt.
- Keep examples runnable from the project root where possible.
- Make code changes easy for students to trace from input to state update to
  screen output.
- Avoid premature optimization. Clarity is more important than squeezing out
  performance in these small games.