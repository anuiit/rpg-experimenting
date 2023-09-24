import pygame
import os
from utils import render_text

class Character:
    def __init__(self, name, hp, attack, defense, speed, img_path=None, anim_path=None, scale=1):
        self.name = name
        self.hp = hp
        self.max_hp = hp
        self.attack = attack
        self.defense = defense
        self.speed = speed
        self.dead = False
        self.prev_hp = hp

        self.animation_list = []
        
        self.img_path = img_path
        self.img = pygame.image.load(img_path)

        self.width = self.img.get_width()
        self.height = self.img.get_height()

        self.img = pygame.transform.scale(self.img, (self.width * scale, self.height * scale))

        self.rect = self.img.get_rect()

        self.action = 0
        self.frame_index = 1
        self.update_time = pygame.time.get_ticks()

        temp_list = []

        for file in os.listdir(os.path.join(anim_path, 'Idle')):
            img = pygame.image.load(os.path.join(anim_path, 'Idle', file))
            img = pygame.transform.scale(img, (img.get_width() * scale, img.get_height() * scale))
            temp_list.append(img)

        self.animation_list.append(temp_list)
        #load attack images
        temp_list = []
        for file in os.listdir(os.path.join(anim_path, 'Attack')):
            img = pygame.image.load(os.path.join(anim_path, 'Attack', file))
            img = pygame.transform.scale(img, (img.get_width() * scale, img.get_height() * scale))
            temp_list.append(img)

        self.animation_list.append(temp_list)
        

        temp_list = []
        for file in os.listdir(os.path.join(anim_path, 'Dead')):
            img = pygame.image.load(os.path.join(anim_path, 'Dead', file))
            img = pygame.transform.scale(img, (img.get_width() * scale, img.get_height() * scale))
            temp_list.append(img)


        self.animation_list.append(temp_list)
        self.img = self.animation_list[self.action][self.frame_index]

    def update(self):
        animation_cooldown = 100
        self.img = self.animation_list[self.action][self.frame_index]
        
        if self.dead:
            if self.frame_index >= len(self.animation_list[self.action]) - 1:
                self.img = self.animation_list[self.action][-1]
            else:
                # check if enough time has passed since the last update
                if pygame.time.get_ticks() - self.update_time > animation_cooldown:
                    self.update_time = pygame.time.get_ticks()
                    self.frame_index += 1
        else:
            # check if enough time has passed since the last update
            if pygame.time.get_ticks() - self.update_time > animation_cooldown:
                self.update_time = pygame.time.get_ticks()
                self.frame_index += 1
                # if the animation has run out then reset back to the start
                if self.frame_index >= len(self.animation_list[self.action]):
                    self.idle_start()

    def set_position(self, x, y):
        self.rect.x = x
        self.rect.y = y

    def draw(self, screen):
        screen.blit(self.img, self.rect)
        pygame.draw.rect(screen, (255, 0, 0), (self.rect.x, self.rect.y - 20, self.rect.width, 10))

    def idle_start(self):
        self.action = 0
        self.frame_index = 0
        self.update_time = pygame.time.get_ticks()
    
    def dead_start(self):
        self.action = 2
        self.frame_index = 0
        self.update_time = pygame.time.get_ticks()

    def attack_target(self, target):
        target.prev_hp = target.hp
        target.hp -= self.attack
        
        if target.hp <= 0:
            target.hp = 0
            if not target.dead:
                target.dead = True
                target.dead_start()

        self.action = 1
        self.frame_index = 0
        self.update_time = pygame.time.get_ticks()
        
    
'''class Skeleton(Character):
    def __init__(self, name, hp, attack, defense, speed, img_path='rcs/Monster Creature Pack/Goblin/Idle/0.png', anim_path='rcs/Monster Creature Pack/Goblin/', scale=3):
        super().__init__("Goblin", hp, attack, defense, speed, img_path, anim_path, scale)

class Wolf(Character):
    def __init__(self, name, hp, attack, defense, speed, img_path='rcs/characters/Wolf/Idle/0.png', anim_path='rcs/Characters/Wolf/', scale=3):
        super().__init__("Goblin", hp, attack, defense, speed, img_path, anim_path, scale)'''

class Fireskull(Character):
    def __init__(self, name, hp, attack, defense, speed, img_path='rcs/characters/Goblin/Idle/0.png', anim_path='rcs/Characters/Goblin/', scale=3):
        super().__init__("Goblin", hp, attack, defense, speed, img_path, anim_path, scale)