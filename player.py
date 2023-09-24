import pygame
from utils import render_text
from character import Character

class Player(Character):
    def __init__(self):
        super().__init__("Player", 100, 25, 5, 5, "rcs/Characters/Sworcerer/Idle/0.png", anim_path='rcs/Characters/Sworcerer/', scale=4)
        self.next_state = None  # Variable to handle state transitions
        self.inventory = ["Health Potion", "Mana Potion", "Sword"]

    def handle_events(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_p:
                print("Player: Switching to Map")
                self.next_state = "map"

    '''def render(self, screen):
        # Render player's stats and inventory in the menu
        # Example: Display the player's stats and items
        for i, (stat, value) in enumerate(self.stats.items()):
            stat_text = f"{stat}: {value}"
            render_text(screen, stat_text, (10, 10 + i * 20), (255, 255, 255))
        
        for i, item in enumerate(self.inventory):
            item_text = f"{i + 1}. {item}"
            render_text(screen, item_text, (10, 150 + i * 20), (255, 255, 255))'''
    
    def get(self, stat):
        return self.stats[stat]
