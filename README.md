# Python Project for Applied Informatics 4

## Platformer Game -- Software Documentation

## Table of Contents

- [Introduction](#1-introduction)
- [System Overview](#2-system-overview)
- [Detailed Component Design](#3-detailed-component-design)
    - [Game Loop](#31-game-loop)
    - [Game Logic](#32-game-logic)
    - [Graphics](#33-graphics)
    - [User Input](#34-user-input)
    - [Story Mode and Help Module](#35-story-mode-and-help-module)
    - [Audio](#36-audio)
- [Deployment and Testing](#4-deployment-and-testing)
    - [Runtime Requirements](#41-runtime-requirements)
    - [Testing Strategy](#42-testing-strategy)
    - [Deployment Strategy](#43-deployment-strategy)
- [Conclusions](#5-conclusions)

### 1. Introduction

&nbsp; &nbsp; &nbsp; &nbsp; This project consists of a **2D platformer video game** developed in Python. It is an assignment for a subject called Applied Informatics 4 (also referred to as Python Project Development). The goal is to create a **team project** that can be mostly or fully implemented using various features of the Python programming language. Also, using **Git** as a version control system and providing a thorough documentation written in English are both key requirements for this assignment, so as to follow the standards of the IT industry as much as possible.

&nbsp; &nbsp; &nbsp; &nbsp; The video game will be designed to run on a **PC** (Windows/Mac/Linux), having an interactive **Graphical User Interface** and requiring a small degree of command line activity to start up. It is addressed to any gamer curious to put their sharpness and reflexes to a test with a retro-style video game inspired by the indie platformers that defined a generation. There is no need of advanced skills or experience with PC gaming, because only a few intuitively chosen keys are necessary to play through the levels. The player will have to control a **character** through various **levels**, avoiding **obstacles** and **enemies**, collecting **objects** and reaching each level's precise ending. The gameplay will include:

- player lateral movement, jumping and gravity
- collision with platforms, walls and dangerous entities
- score tracking based on completion time and total collectables
- several levels of increasing difficulty
- a main menu with options to view features, start or quit the game

&nbsp; &nbsp; &nbsp; &nbsp; The fundamental functionalities use the **Pygame** library from Python version 3.11 and above. For highscore tracking and storing level world codifications, **JSON** and plain text files will be used. There is no need of internet connection to play the game. It runs completely **locally** at a steady frequency of **60 FPS** even on modest hardware. There will be a fixed game window screen resolution, with no option to rescale it in-game.

### 2. System Overview

&nbsp; &nbsp; &nbsp; &nbsp; The game is built as a **standalone application**, running entirely on a **local client**.

- **Game Loop** – controls the main update and render cycle of the game.  
- **Game Logic** – handles all gameplay mechanics such as pixel-perfect collision detection, score display, time tracking, and management of different game states.
- **Graphics** – responsible for sprite loading, animations, masking, and rendering of collectible and interactable objects (including chests, coins, spikes, finish flag, ...).  
- **User Input** – processes keyboard, mouse, and button interactions, which affect the player's movement and ability to interact with objects.
- **Story Mode** – accessible from the main screen, to present the game’s narrative.
- **Help Module** – accessible from the main screen, providing gameplay instructions and controls.  
- **Audio** – manages all sound effects and music, including background sound, object interaction and collection cues, death sounds, and victory sounds.

### 3. Detailed Component Design:

&nbsp; &nbsp; &nbsp; &nbsp; This section covers the game's architecture in depth, breaking down each major component that was presented in the previous section.

#### 3.1 Game Loop

&nbsp; &nbsp; &nbsp; &nbsp; This is the core of the application. It will be implemented as a single, continuous `while` loop that runs as long as the game is active, belonging to a `Game` class. Its primary responsibilities are:

- Time Management: Using `pygame.time.Clock().tick(FPS)` to ensure the game runs at a consistent 60 Frames Per Second (FPS).
- Event Polling: Calling the **User Input** component to process the event queue (keyboard, mouse, quit signals) at the start of each frame, in order to properly decide the flow of the game depending on user interaction.
- State Updating: Calling the `update()` method of the currently active game state, such as the level that is currently being played, in which actually acts as a wrapper.
- Rendering: Calling the `draw()` method (or wrappers to it) of the **Graphics** component to render the updated game state to the screen, calling `screen.blit()` on certain surfaces and calling `pygame.display.update()` to display the new frame.

&nbsp; &nbsp; &nbsp; &nbsp; The implementation will be done using the class `Game` (with an event handler, state updater and display drawer as fundamental methods) and the `main.py` module to initialise Pygame, create the game window, and contain the main loop, where methods from classes in other modules will be used to better maintain the code and reduce the LoC for `main.py`. Game Loop's interfaces include:

- Calling **User Input** component to get all events from different sources.
- Calling **Game Logic** component based on the current game state.
- Receiving a "quit" signal from **User Input** component to terminate the loop and perform a clean exit.

#### 3.2 Game Logic

&nbsp; &nbsp; &nbsp; &nbsp; This component manages the game's state and rules, being responsible for what happens in the game, state transitions, processing dynamic information based on its interface with the **Game Loop** component and ensuring a smooth experience for the user in all cases. Thus, the following roles are fulfilled:

- State Management: A simple set of classes derived from an abstract State class will be created to manage the application's current state (Gameplay, Main Menu, Story Mode, Help Mode, etc.). The `main.py` module will contain a dictionary of all instantiations of these Classes, letting the `states.py` module to take care of all Level objects to better manage and cycle through them, also handling control changes between levels and from level to intermediary menus or the main menu. 
- Physics Engine: A simple physics handler inside the `update()` method of the `Player` class, applying constant gravity, handling jump impulses, and managing lateral velocity. It has been our choice to handle gravity as close to a "realistic" one (quadratic) as possible, rather than an exponential implementation.
- Collision Detection: This is critical for any platformer game to ensure a sense of difficulty, progress and reward when playing through the levels. It will use `pygame.mask` for pixel-perfect collisions between the player and dangerous entities (like spikes, or enemies which have their own mask) and standard `pygame.mask.overlap()` for interactions with platforms, walls, and collectables. Since the world is make out of blocks, masking everything and checking for relevant overlaps is a sound choice for collisions.
- Level Management: Loading level data from text files, instantiating obstacles, enemies, and collectables based on that data. It also tracks when a level's state changes (the player interacts with the "finish flag" to complete it, falls to their death or runs out of lives due to collisions with dangerous entities) and displays further options in an intermediary victory/loss screen.
- Score and Time: Tracks the player's score (based on collectables) and the time elapsed for the current level, all handles inside `levels.py` in separate methods.

&nbsp; &nbsp; &nbsp; &nbsp; In terms of implementation, a `Level` class will be run and dynamically change states to control the game's flow. Fundamental changes will be detected by the **Game Loop** component, while minor changes will be handled within the `Level` class methods, coordinated by a `run_level()` method. To further split the high load of information needed for levels, a `World` class will interpret and generate worlds that are directly passed to the `Level` constructor. A `Player` class will encapsulate player logic (movement, health, physics) and all states the player can find themselves in at some point in the level. In connection with other components, Game Logic:

- Receives processed commands from **User Input** (movement, explicit object interactions).
- Sends commands to the **Audio** component tailored for each situation (`play_sound('jump_sound')`, `play_sound('coin_sound')`).
- Provides all state information (player position, score, level objects) to the **Graphics** component for rendering.
- Reads from/writes to the file system (`JSON`) to handle highscore saving/loading, depending on live player performance.

#### 3.3 Graphics

&nbsp; &nbsp; &nbsp; &nbsp; A component responsible for all visual output, working solely based on instructions from **Game Logic**. Among its responsibilities, we mention:

- Asset Loading: Loads all sprites (player, enemies, tiles, collectables, UI elements - `Button` objects) from image files (`.jpg` or `.png`) at startup. Spritesheets will be used for animations in the same fashion old cartoons were made from a series of many photos that were cycled thorugh quickly.
- Animation: Manages player and enemy animations by cycling through images in a spritesheet based on the entity's state ('running', 'idle', 'jumping'). Enemies have a predetermined course, while the player's depends on the information captured by **User Input**.
- Rendering Engine: A series of `draw()` functions or wrappers that clear the screen and then draw all visible components together and in a specific order: background, level tiles, enemies, collectables and the player, creating the User Interface (UI). The numerous `screen.blit()` calls help with rendering text and images on precise surfaces.
- UI Rendering: Draws all static text (like "Score:") and dynamic text (the score value itself, level completion time) using `pygame.font`, placing it in a specific position on the display.

&nbsp; &nbsp; &nbsp; &nbsp;Graphics will be integrated in the core classes `Level`, `World` and `Player` through global variables, class methods and wrappers. Interfacing other components, it will:
- Receive the game state (all objects and their positions) from **Game Logic**.
- Render everything to the main display surface created by the **Game Loop**.

#### 3.4 User Input

&nbsp; &nbsp; &nbsp; &nbsp; Captures and translates all raw user input into game-specific commands. The useful input is fully documented in the **Help Mode** component for the player to discover when first playing the game. As far as the implementation is concerned, it will feature a dedicated part in the `update()` method for the `Player` class and also in the `while` loop from the `main.py` module. Most of the input will be captured using `pygame.key.get_pressed()`. Additionally, the `Button` class will be instantiated on the main menu and intermediary menus to control the flow of the game according to the player's clicks. The important keys are as follows:

- `KEYLEFT` / `KEYRIGHT` (Left Arrow and Right Arrow) will be tracked to manage continuous movement.
- `KEYSPACE` will be used for jumping, with further presses being ignored while the jump animation takes place.
- `KEYRETURN` (Enter) will be used to interact with certain objects (chests and end-of-level flags).
- `pygame.mouse.get_pressed()[0]` will be used to check for left mouse click when the mouse collides with a button's surface.
- `QUIT` event (closing the window) will be caught to signal the **Game Loop** to exit.

&nbsp; &nbsp; &nbsp; &nbsp; The only significant interface with another component is passing game commands (`{'action': 'move', 'direction': 'left'}`) or UI interactions (`{'action': 'click', 'button': 'start'}`) to the **Game Logic** component.

#### 3.5 Story Mode and Help Module

&nbsp; &nbsp; &nbsp; &nbsp; These are simple, dedicated game states. They display static information (narrative text or instructions) to the user only when explicitly requested using dedicated buttons on the main menu. Each will have its own screen that conforms to the state interface (i.e., has an `update()` and `draw()` method). They will primarily render text and/or images and have a `Return` button to the main menu, the only place where the levels can be started. Esentially, once in any of these separate screens, the game will just listen for the button click from the **User Input** module. These components connect to the others as follows:

- Triggered by **Game Logic** when selected from the main menu.
- Uses the **Graphics** module to render text.
- Receives input from the **User Input** module to return to the main menu.

#### 3.6 Audio

&nbsp; &nbsp; &nbsp; &nbsp; This component manages all sound and music, using global importable variables stored in the `settings.py` module to ensure all sounds are managed in one place and used anywhere needed. It will use `pygame.mixer.music` and `pygame.Sound` instantiations to load all sound files (`.mp3` and `.wav`) into a dictionary contained by a `SoundAsset` class at startup. `pygame.mixer.music` will be used for the continuous background soundtrack. The two fundamental methods are:
- `play_sound(sound_name)`: Plays a specific, short sound effect ('jump', 'death', 'coin_collectd').
- `play_music(track_name, loop=-1)`: Starts or changes the background music, ensuring it plays in a loop.

&nbsp; &nbsp; &nbsp; &nbsp; Audio receives simple string-based commands from **Game Logic** (`SoundAsset.play_sound('player_death')`) when necessary, directly from the core methods that run levels or wait for use input on UI elements.

### 4. Deployment and Testing

&nbsp; &nbsp; &nbsp; &nbsp; This section presents the projected strategy for deployment and testing. Surely, these steps can suffer modifications in the late staged of development for reasons that are presently hard to forsee.

#### 4.1 Runtime Requirements

&nbsp; &nbsp; &nbsp; &nbsp; The application is a standalone desktop game with minimal dependencies:
- **Hardware:** Runs on standard PC hardware (Windows, macOS, Linux). No dedicated GPU is required. Requires a keyboard and mouse.
- **Software:**
    * Python 3.11 or newer.
    * Pygame 2.x library (installable from the provided `requirements.txt` file).
    * No internet connection is required to play.

#### 4.2 Testing Strategy

&nbsp; &nbsp; &nbsp; &nbsp; Given the scope of the project, testing will be primarily **manual (playtesting)**. Whenever a new major feature is added, all parts of the game will undergo incremental testing to check lapses in the Game Logic component with respect to the new feature:

- **Core Gameplay:** Repeatedly playing levels to ensure physics feel right (jump height, gravity), and collisions are accurate and fair (especially pixel-perfect spike and enemy mask collisions). This will also include different rates of interaction with objects to test sounds, animations and whether the Game Loop and Game Logic reset and process them correctly.
- **Level Progression:** Playing through all levels in order to ensure they load correctly and the difficulty curve is appropriate.
- **UI/Menu Navigation:** Clicking all buttons in the main menu (Start, Help, Quit, Story) to ensure they lead to the correct game state and that returning to the menu works as expected: Story and Help need to lead to "dead ends", while the Main Menu needs to remain the very heart of the game.
- **Edge Case Testing:** Intentionally attempting to break the game (jumping into corners / ceilings, pausing movement at random moments, checking score calculation with zero collectables, remaining idle on edges/very close to enemies that are patrolling around the platform).

#### 4.3 Deployment Strategy

&nbsp; &nbsp; &nbsp; &nbsp; As this is a local client application, there is no server-side deployment. The primary goal is to provide an easy-to-run executable for end-users on their own system with a minimal setup.

1.  **Running from Source (Development):** The game can be run directly from its source code by following several steps:
    - cloning the Git repository 
    - ensuring `virtualenv` is installed
    - creating a new virtual environment (`virtualenv .venv`) and activating it using `source ./.venv/bin/activate`
    - using `pip install -r requirements.txt` (which will contain `pygame` and all other dependencies)
    - entering the `src/` directory and running the command `python main.py`.

2.  **Standalone Executable (Production):** For the final submission and for non-technical users, we will use **PyInstaller** or **cx_Freeze**. This tool will bundle the Python interpreter, all script files (`.py`), and all game assets (images, sounds, fonts, level files) into a single executable file (`game.exe` on Windows) or an application bundle (`.app` on macOS). This executable can be run by any user without needing to install Python or any libraries.

### 5. Conclusions

&nbsp; &nbsp; &nbsp; &nbsp; This document layed out the design for a 2D retro-platformer, a project that serves as a practical application of Python programming, Pygame library usage, and version control with Git. Both members of the team had never used Python any seriously before taking up this project.

&nbsp; &nbsp; &nbsp; &nbsp; The game, while seemingly simple, involves several complex components. The most significant challenges are anticipated to be the implementation of a robust and fair physics and collision engine (particularly the pixel-perfect masking) and the design of engaging levels. There are many legendary video games out in the public domain to get inspiration from, but the priority is ensuring that every new piece added to the game is reliable and does not represent a drawback in quality and user experience. Managing the game's various states (menu, game, pause) cleanly will also require careful architectural planning.

&nbsp; &nbsp; &nbsp; &nbsp; The estimated workload is considerable (roughly 30-35 hours per member, working in parallel), requiring not only coding but also significant time for searching through documentation, asset creation (or sourcing ones with free-licence), level design, and thorough playtesting to ensure the game is "fun" and not just "functional". Successfully completing this project will demonstrate a strong understanding of **Object-Oriented Programming (OOP)** in Python, experience with a major game development library, practical skills in **software documentation**, and the ability to collaborate on a codebase using **Git** in a logical way. As its goal suggests, the assignment encapsulates many skills relevant to the IT industry, from initial design to final deployment. We are confident that the planned architecture provides a sound foundation for building the intended game.
