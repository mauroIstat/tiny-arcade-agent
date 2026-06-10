## Project structure

The Pong game is split into small files, each with a clear responsibility:

- `actions.py`: defines the possible actions: up, down, stay.
- `config.py`: contains the game parameters, such as window size, speed, and max score.
- `entities.py`: defines the main game objects: paddle, ball, score, and game state.
- `geometry.py`: converts game objects into geometric shapes used by pygame.
- `physics.py`: updates positions and handles collisions and bounces.
- `opponents.py`: contains the algorithms used by the virtual opponent.
- `game.py`: runs the main game loop.