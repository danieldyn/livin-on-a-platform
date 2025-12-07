# Python Project for Applied Informatics 4

## Description

&nbsp; &nbsp; &nbsp; &nbsp; This project consists of a **2D platformer video game** developed in Python. It is an assignment for a subject called Applied Informatics 4 (also referred to as Python Project Development). The goal is to create a **team project** that can be mostly or fully implemented using various features of the Python programming language. Also, using **Git** as a version control system and providing a thorough documentation written in English are both key requirements for this assignment, so as to follow the standards of the IT industry as much as possible.

&nbsp; &nbsp; &nbsp; &nbsp; The video game will be designed to run on a **PC** (Windows/Mac/Linux), having an interactive **Graphical User Interface** and requiring a small degree of command line activity to start up. It is addressed to any gamer curious to put their sharpness and reflexes to a test with a retro-style video game inspired by the indie platformers that defined a generation. There is no need of advanced skills or experience with PC gaming, because only a few intuitively chosen keys are necessary to play through the levels. The player will have to control a **character** through various **levels**, avoiding **obstacles** and **enemies**, collecting **objects** and reaching each level's precise ending. The gameplay will include:

- player lateral movement, jumping and gravity, plus a rolling/crouching system
- collision with platforms, walls and dangerous entities
- score tracking based on completion time and total collectables
- several levels of increasing difficulty
- a main menu with options to view features, start or quit the game

&nbsp; &nbsp; &nbsp; &nbsp; The fundamental functionalities use the **Pygame** library from Python version 3.11 and above. For highscore tracking and storing level world codifications, **JSON** and plain text files will be used. There is no need of internet connection to play the game. It runs completely **locally** at a steady frequency of **60 FPS** even on modest hardware. There will be a fixed game window screen resolution, with no option to rescale it in-game.

## Running the Game

Ensure you have cloned the Git repository:

```
    git clone https://github.com/danieldinu2030/python-project-ai4
```

It is best to set up a **virtual environment** in order to play the game:

```bash
    sudo apt install virtualenv
    virtualenv .venv
    source .venv/bin/activate
```

Install all dependencies using the provided file, including `pygame`:

```bash
    pip install -r requirements.txt
```

Enter the `src/` directory and run the game:

```bash
    python main.py
```

## Contributions

&nbsp; &nbsp; &nbsp; &nbsp; Both members of the team contributed across all parts of the game, be it the actual Python source code or the assets (images, sounds, sprites etc.) However, if we were to summarise the dozens of commits in the project and the main roles, it would look like this:

- **danieldinu2030**:
    - Game State & Meta-Systems: built the wrapper systems around the core gameplay; this includes the Save/Load system (autosaves), the Highscore system (JSON), the Hearts/Lives mechanic, and the transitions between levels (Game Loop, State management).
    - Level Design & Content: heavily populated the game, including via a Bash script for procedural generation (world matrix), added manually edited underground tiles, and implemented half of the Worlds; also handled the "decoration" on every submenu of the Main Menu.
    - UI, Audio & Polish: made the game feel like a complete product; implemented the Main Menu, Help Screens, Story Text, Victory/Game Over screens, and used a lot of instances of the Button class; also integrated all sound effects and background music.
    - DevOps & Code Quality: maintained the code health, reorganising the file tree (creating the `src` directory), seting up pylint, writing the documentation, and creating `requirements.txt`; also refined the physics engine to fix specific bugs (like the elevator problem and the collision search optimisation from O(n) to O(1)).

- **TodeMihai123**:
    - Core Physics & Collisions: implemented the fundamental movement logic, handled the "hard math" tasks like pixel-perfect collision and implementing specific character mechanics like crouching, rolling, and 1-block gap movement.
    - Entity & Object Architecture: established the Object-Oriented structure for the game world, creating the SolidObject, DangerousObject (spikes/slimes); defined how the player interacts with the world (e.g., dying on spikes, defeated by enemies).
    - Tools & Level Creation: built the fully functional World Editor, allowing the team to visually design levels rather than just coding them manually; also implemented the logic for secret levels and the Button class.
    - Visual States: handled the character animations (Idle vs. Rolling) and sprite management (flipping images).

## Difficulties

&nbsp; &nbsp; &nbsp; &nbsp; Having had no previous experience with Python, we had to rely on the Pygame documentation and an inspiration Youtube video to get properly started. We quickly became comfortable writing our own code and playtesting the new features, which leads to the next obstacle: deciding which features are actually feasible and relevant for the type of game we want. That was solved by small brainstorming sessions and a lot of playtesting. To some extent, generating worlds was cumbersome, so we sought automation via a Bash script and an interactive and fully functional world editor.

&nbsp; &nbsp; &nbsp; &nbsp; The real challenge was making the project as much OOP as possible, given that we started understanding the concepts through the university coursework. On two occasions, we had to deal with making sure that the newly separated code was fully functional, although there wasn't anything new in terms of functionalities. That took plenty of careful planning and incremental testing, reading errors and exceptions.
