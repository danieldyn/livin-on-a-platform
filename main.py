import asyncio
import sys
from pathlib import Path

import pygame

pygame.init()

sys.path.insert(0, str(Path(__file__).parent / "src"))

import main as game_entry

if __name__ == "__main__":
    asyncio.run(game_entry.main())
