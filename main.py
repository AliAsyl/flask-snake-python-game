from engine.entities import Cat, Berry
from ui.ui import GameUI
from engine.core import Vector2D
from database.db import Database

import random

def on_frame_randered():
    if random.random() < 0.01:
        Berry(Vector2D(
            random.randint(
                Berry.BERRY_HITBOX_WIDTH, 
                GameUI.SCREEN_WIDTH - Berry.BERRY_HITBOX_WIDTH
            ), 
            random.randint(
                Berry.BERRY_HITBOX_HEIGHT,
                GameUI.SCREEN_HEIGHT - Berry.BERRY_HITBOX_HEIGHT
            )
        ))

def main():
    Database.init()
    cat = Cat(Vector2D(GameUI.SCREEN_WIDTH//2, GameUI.SCREEN_HEIGHT//2),   5)
    ui = GameUI(cat, on_frame_randered)

    if ui.init_cli():
        ui.init_gui()
        ui.run()

if __name__ == "__main__":
    main()