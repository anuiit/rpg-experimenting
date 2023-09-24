import pygame, os

def render_text(screen, text, position, color=(255, 255, 255)):
    # Helper function to render text on the screen
    font = pygame.font.SysFont(None, 28)
    text_surface = font.render(text, True, color)
    screen.blit(text_surface, position)

def mouse_hover(rect):
    return rect.collidepoint(pygame.mouse.get_pos())

def draw_select(screen, scale, rect=None, hover=False, entities=None):
    select = pygame.image.load("rcs/ui/cursor.png")
    select = pygame.transform.scale(select, (int(select.get_width()) * scale, int(select.get_height()) * scale))
    gap = 16

    if rect != None:
        pos = list(rect.bottomright)
        for i, p in enumerate(pos):
            pos[i] += gap
        pos = tuple(pos)

        select_rect = select.get_rect(center=pos)
        screen.blit(select, select_rect)

    if hover and entities:
        for entity in entities:
            if mouse_hover(entity.rect) and not entity.dead:
                pos = list(entity.rect.bottomright)
                for i, p in enumerate(pos):
                    pos[i] += gap
                pos = tuple(pos)
                select_rect = select.get_rect(center=pos)
                screen.blit(select, select_rect)

def draw_indicator_turn(screen, entity, scale):
    select = pygame.image.load("rcs/ui/turn_indicator.png")
    select = pygame.transform.scale(select, (int(select.get_width()) * scale, int(select.get_height()) * scale))

    pos = list(entity.rect.center)
    pos[1] -= entity.rect.height
    pos = tuple(pos)

    select_rect = select.get_rect(center=pos)
    screen.blit(select, select_rect)


class Button:
    def __init__(self, x, y, base_img, hover_image, scale=1, action=None):
        self.width = int(base_img.get_width())
        self.height = int(base_img.get_height())

        self.base_img = pygame.transform.scale(base_img, (self.width * scale, self.height * scale))
        self.hover_image = pygame.transform.scale(hover_image, (self.width * scale, self.height * scale))

        self.rect = self.base_img.get_rect()
        self.rect.x = x
        self.rect.y = y

        self.action = action
        self.inactive = False


    def draw(self, screen, hover=True):
        if mouse_hover(self.rect) and hover:
            screen.blit(self.hover_image, self.rect)
        else:
            screen.blit(self.base_img, self.rect)
        
    def draw_base(self, screen):
        screen.blit(self.base_img, self.rect)

    def is_clicked(self):
        pos = pygame.mouse.get_pos()
        return self.rect.collidepoint(pos)
    
    @staticmethod
    def reposition_horizontal_menu(buttons, x, y, horizontal_gap, scale):
        menu = []
        for i, button in enumerate(buttons): 
            button.x = x + i * (button.width + horizontal_gap)
            button.y = y
            button.base_img = pygame.transform.scale(button.base_img, (button.width * scale, button.height * scale))
            button.hover_image = pygame.transform.scale(button.hover_image, (button.width * scale, button.height * scale))
            button.rect = button.base_img.get_rect()
            button.rect.topleft = (button.x, button.y)
            menu.append(button)
        return menu