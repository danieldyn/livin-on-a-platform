# Python Project for Applied Informatics 4

## Platformer Game

## Table of Contents

- [Software Documentation](#software-architecture-document)
    - [Introduction](#introduction)
    - [System Overview](#system-overview)
    - [Detailed Component Design](#detailed-component-design)
    - [Deployment and Testing](#deployment-and-testing)
    - [Conclusions](#conclusions)
- [Playing the Game](#playing-the-game)

## Software Documentation

### Introduction

&nbsp; &nbsp; &nbsp; &nbsp; This project consists of a 2D platformer video game developed in Python.
It is an assignment for a subject called Applied Informatics 4 (also referred to as Python Project
Development). The goal is to create a team project that can be mostly or fully implemented using various
features of the Python programming language. Also, using Git as a version control system and providing a
thorough documentation written in English are both key requirements for this assignment, so as to follow
the standards of the IT industry as much as possible.

&nbsp; &nbsp; &nbsp; &nbsp; The video game will be designed to run on a PC (Windows/Mac/Linux), having an
interactive Graphical User Interface and requiring a small degree of command line activity to start up.
It is addressed to any gamer curious to put their sharpness and reflexes to a test with a retro-style
video game inspired by the indie platformers that defined a generation. There is no need of advanced skills
or experience with PC gaming, because only a few intuitively chosen keys are necessary to play through the
levels. The player will have to control a character through various levels, avoiding obstacles and enemies,
collecting objects and reaching each level's precise ending. The gameplay will include:
- player lateral movement, jumping and gravity
- collision with platforms, walls and dangerous entities
- score tracking based on completion time and total collectables
- several levels of increasing difficulty
- a main menu with options to view instructions, start or quit the game

&nbsp; &nbsp; &nbsp; &nbsp; The fundamental functionalities use the Pygame library from Python version 3.11
and above. For highscore tracking and storing level world codifications, JSON and plain text files will be
used. There is no need of internet connection to play the game. It runs completely locally at a steady
frequency of 60 FPS even on modest hardware. There will be a fixed game window screen resolution, with
no option to rescale it in-game.

### System Overview
prezentare generală a sistemului, a componentelor acestuia (e.g., client/server, frontend/backend, protocoale folosite de comunicație, structură bază de date…); tot aici, de menționat ce limbaje / biblioteci / framework-uri veți folosi pentru implementare, precum și design patterns / paradigme de coding (dacă e cazul, + argumentare) etc.

### Detailed Component Design:
câte un subcapitol pentru fiecare componentă majoră a sistemului, de descris funcționalitatea și modul de implementare (ce module / clase / funcții principale vor fi implementate, etc.), relațiile / modurile de interfațare / comunicare cu celelalte module interne sau externe ale aplicației (e.g., folosire HTTP între frontend și backend, biblioteca Y pentru baza de date externă / API / aplicație / dispozitiv extern etc…);

### Deployment and Testing (dacă e cazul)
cerințele de rulare a aplicației (server / domeniu / GPUs / abonamente la servicii externe folosite în cod, e.g. mail / LLMs etc.), decizii de containerizare (e.g., volume, variabile de configurație etc.) cât și strategia de testare (dacă este cazul, altfel scrieți că veți face testare manuală);

### Conclusions
exprimare liberă aici, puteți sumariza cele prezentate în document, expune păreri despre complexitatea previzionată a acestuia, nr de ore de lucru, cunoștințe necesare de învățat etc.;


> Anything under this line can be rewritten or integrated in the documentation above, if needed.

## Level Structure

> There is only one **Player** instance that progresses from level to level, retaining its stats from the previous level.

- **Player**
    - **Level**
        - **World**
            - **Object list** (e.g., coins, fruits, …)
            - **Block list** (e.g., grass, dirt, water, …)
        - **background image**

> When a new **Level** object is created, it is assigned a **World** (which contains the object and block lists) and a **background image**, allowing for easier design and management of separate levels.

## Playing the Game

Running the game requires the module `pygame`, which is not a standard one.
It is recommended to create a **virtual environment** and install `pygame` there.
Ensure you have `virtualenv` installed:

```c
sudo apt install virtualenv
```

Then, create the virtual environment, activate it and install the module:

```c
virtualenv .venv
source ./.venv/bin/activate
pip install pygame
```

If you are using an IDE like VSCode, you may need to change the Python interpreter to the one located inside the virtual environment: 
`./.venv/bin/python`

The game can be played by entering the `src/` directory and using the command:
```c
python main.py
```
