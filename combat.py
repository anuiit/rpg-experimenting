import pygame
from utils import Button, render_text, draw_select, mouse_hover, draw_indicator_turn
from player import Player
from character import *

clock = pygame.time.Clock()
fps = 30
width = 1280
height = 720

class Combat:
    def __init__(self, players, enemies, player_turn=True, background='battleback8'): # ajouter enemies plus tard (liste d'ennemis)
        self.next_state = None
        self.running = True
        self.selected_entity = None
        self.player_turn = player_turn

        self.health_max_anim_cooldown = 10
        self.health_anim_cooldown = 0

        self.action_wait_time = 40
        self.action_cooldown = 20

        self.party = players
        self.enemy_party = [Fireskull("Fireskull", 50, 30, 10, 10, scale=4) for _ in range(4)]

        self.current_fighter = 0
        self.characters = self.party + self.enemy_party

        self.map_reduce_width = 180
        self.map_reduce_height = 220

        self.map_window_width = width - self.map_reduce_width * 2
        self.map_window_height = height - self.map_reduce_height
        self.map_window_rect = pygame.Rect(180, 40, self.map_window_width, self.map_window_height )

        self.background = pygame.image.load(f"rcs/backgrounds/{background}.png")
        self.background = pygame.transform.scale(self.background, (self.map_window_width, self.map_window_height))

        self.buttonsList = [Button(50, 650, pygame.image.load("rcs/ui/btn_map_inactive.png"), pygame.image.load("rcs/ui/btn_map_active.png"), 5, "Attack"),
                            Button(250, 550, pygame.image.load("rcs/ui/btn_map_inactive.png"), pygame.image.load("rcs/ui/btn_map_active.png"), 5, "Skills"),
                            Button(450, 550, pygame.image.load("rcs/ui/btn_map_inactive.png"), pygame.image.load("rcs/ui/btn_map_active.png"), 5, "Items")]

        self.menu = Button.reposition_horizontal_menu(self.buttonsList, (self.map_window_rect.width // len(self.buttonsList) - self.buttonsList[0].rect.width // 2), 550, 200, scale=5)

        self.characters_positions = self.calculate_characters_positions()

    def handle_events(self, event):
        # Gérez les événements liés au combat ici, tels que les actions du joueur (attaquer, utiliser une compétence, etc.).
        if event.type == pygame.MOUSEBUTTONDOWN and self.player_turn:
            for idx, entity in enumerate(self.enemy_party):
                if mouse_hover(entity.rect) and pygame.mouse.get_pressed()[0] == 1 and not entity.dead:
                    self.selected_entity = idx
                    print(self.selected_entity)
                
            for button in self.buttonsList:
                if button.is_clicked():
                    if button.action == "Attack" and self.selected_entity is not None:
                        print('Attack')
                        self.party[self.current_fighter].attack_target(self.enemy_party[self.selected_entity])

                        self.current_fighter += 1    
                        self.action_cooldown = 0
                        self.selected_entity = None

                        if self.current_fighter >= len(self.party) and len(self.party) >= 1:
                            self.player_turn = False
                            self.selected_entity = None

                    elif button.action == "Skills":
                        print("Skills")
                        # menu skills
                    elif button.action == "Items":
                        print("Items")
                        # menu Items
                
        elif event.type == pygame.QUIT:
            pygame.quit()

    def calculate_characters_positions(self):
        available_width = self.map_window_width // 2
        available_height = self.map_reduce_height // 2

        slot_width = available_width // len(self.characters)
        slot_height = available_height // len(self.characters)

        x_positions = [0 for _ in range(len(self.characters))]
        y_positions = [0 for _ in range(len(self.characters))]

        for idx, entity in enumerate(self.characters):
            gen_idx = idx

            temp_idx_party = idx - (len(self.party)) // 2
            temp_idx_ennemy = idx - len(self.party)
            temp_idx_ennemy2 = temp_idx_ennemy - (len(self.enemy_party)) // 2

            line_gap_x = 0
            line_gap_y = 0
            player_x = 220

            calc = slot_width * 1.5 - slot_width * gen_idx
            
            # TODO 
            # Utiliser modulo
            # parce que la c'est pas top 
            # si il y a 2 player le deuxieme se retrouve derriere et pas en dessous
            if idx >= len(self.party) / 2 and entity in self.party:
                gen_idx = temp_idx_party
                line_gap_x = (-160)
                line_gap_y = 14
                calc = slot_width * 1.5 - slot_width * gen_idx
            elif idx >= len(self.party):
                reverse = True
                player_x = -220
                gen_idx = temp_idx_ennemy
                calc = -(slot_width * 1.5 + slot_width * gen_idx)
                if gen_idx >= len(self.enemy_party) // 2:
                    gen_idx = temp_idx_ennemy2
                    line_gap_x = 160
                    line_gap_y = 14
                    calc = -(slot_width * 1.5 + slot_width * gen_idx)

            x_position = self.map_reduce_width + available_width + (+calc) + line_gap_x - player_x
            y_position = self.map_window_height // 2 + slot_height * gen_idx * 8 + line_gap_y

            if entity in self.enemy_party:
                x_position = self.map_reduce_width + self.map_window_width // 2 + slot_width * 1.5 + slot_width * gen_idx + line_gap_x

            print(f'gen_idx: {gen_idx}, temp_idx_party: {temp_idx_party}, temp_idx_ennemy: {temp_idx_ennemy}, temp_idx_en2: {temp_idx_ennemy2}')
            print(f'gap_x: {line_gap_x}, gap_y: {line_gap_y}')
            print(f'slot_w: {slot_width}, calc: {calc}')
            print(f"posx: {x_position}, posy: {y_position}")

            x_positions[idx] = x_position
            y_positions[idx] = y_position

        return [(x, y) for x, y in zip(x_positions, y_positions)]

    def render_characters(self, screen):
        for idx, entity in enumerate(self.characters):
            x, y = self.characters_positions[idx]

            entity.set_position(x, y)
            screen.blit(entity.img, entity.rect)
    
    def health_bars_pos(self):
        master_list = []
        self.health_anim_cooldown += 2
        x_gap = 0
        right_gap = 146

        for idx, entity in enumerate(self.characters):
            if idx >= len(self.party):
                idx = idx - len(self.party)
                x_gap = 1100

            self.health_anim_cooldown += 1
            x_container, y_container = (x_gap + 15, 120 + 120 * idx)
            x_hp, y_hp = (x_gap + 17, 122 + 122 * idx - 2 * idx)

            hp_container = pygame.Rect(x_container, y_container, 150, 25)
            hp_width  = (entity.hp / entity.max_hp) * right_gap

            prev_hp_width = (entity.prev_hp / entity.max_hp) * right_gap
            prev_hp_rect = pygame.Rect(x_hp, y_hp, prev_hp_width, 21)

            print(f'hp : {hp_width}, prev_hp {prev_hp_width}')

            if entity.hp < entity.prev_hp and self.health_anim_cooldown >= self.health_max_anim_cooldown:
                entity.prev_hp -= 1
                self.health_anim_cooldown = 0
                self.action_cooldown = 0

            master_list.append([hp_container, prev_hp_rect])

        return master_list

    def draw_ui(self, screen):
        pygame.draw.rect(screen, (255, 255, 255), self.map_window_rect, 2)

        for idx, bar in enumerate(self.health_bars_pos()):
            render_text(screen, self.characters[idx].name, (bar[0].x, bar[0].y - 30))
            render_text(screen, str(self.characters[idx].hp), (bar[0].bottomright[0] - 30, bar[0].y - 30))

            pygame.draw.rect(screen, (222, 222, 222), bar[0], 0)
            pygame.draw.rect(screen, (0, 0, 0), bar[1], 0)

        # TODO 
        # Group buttons ?
        # pygame.group.draw(groupbuttons) ?
        for button in self.buttonsList:
            if self.player_turn:
                button.draw(screen, True)
            else:
                button.draw(screen, False)

        if self.player_turn:
            if self.selected_entity == None:
                draw_select(screen, 3, hover=True, entities=self.enemy_party)
            else:
                draw_select(screen, 3, self.enemy_party[self.selected_entity].rect, hover=True, entities=self.enemy_party)

            if self.action_cooldown >= self.action_wait_time:
                draw_indicator_turn(screen, self.characters[self.current_fighter], 3)

    def handle_turns(self):
        if self.action_cooldown >= self.action_wait_time:
            print('0')
            if self.current_fighter < len(self.party):
                player = self.party[self.current_fighter]
                print('2')
                if not player.dead:
                    print('3')
                    for event in pygame.event.get():
                        self.handle_events(event)
                else:
                    print('4')
                    self.current_fighter += 1
            elif self.current_fighter - len(self.party) < len(self.enemy_party):
                
                enemy = self.enemy_party[self.current_fighter - (len(self.party))]
                print('5')
                if not enemy.dead:
                    print('6')
                    enemy.attack_target(self.party[0])
                    print('enemy attack')
                    self.action_cooldown = 0

                self.current_fighter += 1
            elif self.current_fighter >= len(self.party) + len(self.enemy_party):
                print('7')
                self.current_fighter = 0
                self.player_turn = True
            else:
                print('bizarre')
        
        self.action_cooldown += 1

        print('current fighter: ' + str(self.current_fighter))
        print(f'action_cooldown : {self.action_cooldown} / {self.action_wait_time}')

    def render(self, screen):
        while self.running:
            screen.fill((20, 20, 20))
            clock.tick(45)
            screen.blit(self.background, self.map_window_rect.topleft)
            
            self.draw_ui(screen)

            self.render_characters(screen)
            
            for entity in self.characters:
                entity.update()
            
            self.handle_turns()
            self.check_finished()
            pygame.display.update()

    def check_finished(self):
        dead_count_enemy = [enemy for enemy in self.enemy_party if enemy.dead == True]
        print("deads: " + str(len(dead_count_enemy)))
        if len(dead_count_enemy) == len(self.enemy_party) and self.action_cooldown >= self.action_wait_time:
            print("You have won!")
            self.running = False
            self.next_state = "menu"

        dead_count_party = [player for player in self.party if player.dead == True]
        if len(dead_count_party) == len(self.party) and self.action_cooldown >= self.action_wait_time:
            print("You have been defeated!")
            self.running = False
            self.next_state = "menu"

    def end_screen():
        pass

    def ai_turn():
        pass