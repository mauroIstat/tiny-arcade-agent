# Tiny Arcade Agent

Tiny Arcade Agent is a small learning project for teaching programming through
classic arcade games.

The first game is Pong. It introduces the basic building blocks of a video game:
state, input, movement, collisions, scoring, and simple computer-controlled
opponents. The next game will be Breakout, where we will start connecting game
mechanics to reinforcement learning ideas.

This README is the starting point for setting up the project. Each game has its
own README with learning goals and classroom activities.

## Recommended environment

For this course, use:

- Python 3.12
- VS Code
- Git
- A Python virtual environment
- pygame 2.6.1

Python 3.12 is the course standard even if your computer already has a newer
Python version installed. New Python releases can take time to work smoothly
with game libraries such as pygame, so using the same version in class avoids
many setup problems.

## Project structure

```text
tiny-arcade-agent/
+-- games/
|   +-- pong/
|   +-- breakout/
+-- play_pong.py
+-- requirements.txt
+-- README.md
```

Pong keeps the two main teaching files at the top of `games/pong/`:

- `config.py`: game parameters such as window size, speed, and max score.
- `game.py`: the main game loop.

The internal building blocks live in `games/pong/core/`:

- `actions.py`: possible actions: up, down, stay.
- `inputs.py`: keyboard input converted into simple data.
- `policies.py`: algorithms used by the virtual opponent.
- `entities.py`: main game objects: paddle, ball, score, and game state.
- `geometry.py`: conversion from game objects to pygame rectangles.
- `physics.py`: movement, collisions, bounces, and ball reset logic.
- `rendering.py`: drawing the current game state on screen.
- `sprites.py`: loading visual assets.

For now, each game has its own launcher. Pong uses `play_pong.py`. Breakout
will later use `play_breakout.py`. A shared launcher can become a useful
refactoring exercise after more than one game is implemented.

## Windows setup, recommended

Most students should use this setup.

### 1. Install the tools

Install:

- Python 3.12 from <https://www.python.org/downloads/>
- Git from <https://git-scm.com/downloads>
- VS Code from <https://code.visualstudio.com/>

During the Python installation, select the option that adds Python to PATH.

### 2. Clone the project

Open PowerShell and run:

```powershell
git clone <PROJECT_URL>
cd tiny-arcade-agent
```

Replace `<PROJECT_URL>` with the URL of this repository.

### 3. Create and activate the virtual environment

```powershell
py -3.12 -m venv .venv
.venv\Scripts\activate
```

After activation, your terminal should show `(.venv)` at the beginning of the
line.

### 4. Install dependencies

```powershell
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

### 5. Run Pong

```powershell
python play_pong.py
```

To see all available options:

```powershell
python play_pong.py --help
```

## WSL setup, optional

Use this path only if you already want a Linux-style workflow on Windows.
For most students, the Windows setup above is simpler.

### 1. Install WSL and Ubuntu

Open PowerShell as administrator and run:

```powershell
wsl --install -d Ubuntu
```

Restart your computer if Windows asks you to.

### 2. Install tools inside Ubuntu

Open Ubuntu from the Start menu and run:

```bash
sudo apt update
sudo apt install git python3.12 python3.12-venv python3-pip
```

Use Python inside WSL for this setup. Do not reuse the Python installed on
Windows.

### 3. Clone, install, and run

```bash
git clone <PROJECT_URL>
cd tiny-arcade-agent
python3.12 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
python play_pong.py
```

Pygame opens a graphical window. On Windows 11, WSLg usually supports this
automatically. If the game window does not appear, use the Windows setup instead.

## macOS and Linux setup

Install Python 3.12, Git, and VS Code using your usual system tools. Then run:

```bash
git clone <PROJECT_URL>
cd tiny-arcade-agent
python3.12 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
python play_pong.py
```

On some Linux distributions, you may need to install Python 3.12 and the
`venv` package from your package manager before creating the virtual environment.

## Playing Pong

Run the default game:

```bash
python play_pong.py
```

Choose a different opponent:

```bash
python play_pong.py --opponent random
python play_pong.py --opponent predictive
```

Choose the opponent speed:

```bash
python play_pong.py --speed slow
python play_pong.py --speed fast
```

Choose the score needed to win:

```bash
python play_pong.py --max-score 3
```

You can combine options:

```bash
python play_pong.py --opponent defensive --speed fast --max-score 7
```

## Troubleshooting

### `python` uses the wrong version

Check the version:

```bash
python --version
```

The course version is Python 3.12. On Windows, use:

```powershell
py -3.12 --version
```

If your virtual environment was created with the wrong Python version, delete
`.venv` and create it again with Python 3.12.

### The virtual environment is not active

If commands fail because pygame is missing, check that `(.venv)` appears in your
terminal.

Activate it again:

```powershell
.venv\Scripts\activate
```

On macOS, Linux, or WSL:

```bash
source .venv/bin/activate
```

### pygame does not install

First check that you are using Python 3.12 and that the virtual environment is
active. Then upgrade pip and reinstall:

```bash
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

### The game window does not open in WSL

Pygame needs a graphical display. WSL on Windows 11 usually includes WSLg, which
can show Linux app windows. If the window does not open, use the Windows setup
instead.

## Games

- [Pong](games/pong/README.md): programming fundamentals and simple opponent
  policies.
- [Breakout](games/breakout/README.md): coming next, with a first introduction
  to reinforcement learning.
