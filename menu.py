import pygame
from player import Player
from map import Map
from utils import Button

class Menu:
    def __init__(self):
        self.next_state = None  # Variable to handle state transitions

        # Create a custom button for changing cities
        self.city_button = Button(25, 50, pygame.image.load("rcs/ui/btn_map_inactive.png"), pygame.image.load("rcs/ui/btn_map_active.png"), 5)

        # Create custom buttons for other actions (e.g., dungeon, stats, inventory)
        self.inventory_button = Button(25, 120, pygame.image.load("rcs/ui/btn_inventory_inactive.png"), pygame.image.load("rcs/ui/btn_inventory_active.png"), 5)
        self.quests_button = Button(25, 190, pygame.image.load("rcs/ui/btn_quests_inactive.png"), pygame.image.load("rcs/ui/btn_quests_active.png"), 5)
        #self.inventory_button = Button(50, 260, pygame.image.load("btn_inventory.png"), 0.5)

    def handle_events(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if pygame.mouse.get_pressed()[0] == 1:
                if self.city_button.is_clicked():
                    print("Changing City")
                    self.next_state = "map"
                    # Implement logic for changing cities here
                elif self.inventory_button.is_clicked():
                    print("Viewing Statistics")
                    # Implement logic for viewing player statistics here
                elif self.quests_button.is_clicked():
                    print("Combat")
                    self.next_state = "combat"
                    # Implement logic for viewing player inventory here

    def render(self, screen):
        # Render custom buttons on the screen
        self.city_button.draw(screen)
        self.inventory_button.draw(screen)
        self.quests_button.draw(screen)
        #self.inventory_button.draw(screen)
