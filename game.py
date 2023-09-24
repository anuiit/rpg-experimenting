import pygame
import pygame_gui
from player import Player
from map import Map
from menu import Menu
import time
from combat import Combat

class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((1280, 720))
        self.clock = pygame.time.Clock()

        self.player = Player()
        self.player2 = Player()
        self.player3 = Player()
        self.player4 = Player()
        self.party = [self.player, self.player2, self.player3, self.player4]

        self.map_state = Map()
        self.menu_state = Menu()
        self.current_state = self.menu_state

        self.running = True

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

            self.current_state.handle_events(event)

    def change_state(self):
        next_state = self.current_state.next_state

        if next_state:
            if next_state == "map":
                self.current_state = self.map_state
            elif next_state == "player_menu":
                self.current_state = self.player_menu_state
            elif next_state == "menu":
                self.current_state = self.menu_state
            elif next_state == "combat":
                ennemies = []
                self.combat_state = Combat(self.party, ennemies)
                self.current_state = self.combat_state
                
        self.current_state.next_state = None

    def render(self):
        self.screen.fill((16, 16, 16))
        self.current_state.render(self.screen)
        
        pygame.display.flip()

    def run(self):
        while self.running:
            self.handle_events()
            self.change_state()
            self.render()
            self.clock.tick(60)

        pygame.quit()

if __name__ == "__main__":
    game = Game()
    game.run()
