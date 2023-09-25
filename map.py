import pygame, random
from utils import Button

# TODO 
# Img cities are not centered on their rect (check collision) probably because of the text



class Map:
    def __init__(self):
        self.font = pygame.font.SysFont("None", 32)
        self.next_state = None  # Variable to handle state transitions
        self.transition_to_menu = False
        self.back_button = Button(25, 520, pygame.image.load("rcs/ui/btn_map_inactive.png"), pygame.image.load("rcs/ui/btn_map_active.png"), 5)

        self.selected_city = 0
        self.cities = [
            {
                "name": "Ville 1",
                "description": "C'est la première ville.",
                "population": 1000,
                "position": (random.randint(0, 800), random.randint(0, 600)),  # (x, y) coordinates
                "image": "rcs/Map/tile009.png"
            },
            {
                "name": "Ville 2",
                "description": "Une ville en bord de mer.",
                "population": 1500,
                "position": (random.randint(0, 800), random.randint(0, 600)),  # (x, y) coordinates
                "image": "rcs/Map/tile007.png"
            },
            {
                "name": "Ville 3",
                "description": "La capitale du royaume.",
                "population": 3000,
                "position": (random.randint(0, 800), random.randint(0, 600)),  # (x, y) coordinates
                "image": "rcs/Map/tile008.png"
            },
        ]

        self.points_of_interest = [
            {
                "name": "Point of Interest 1",
                "description": "Un endroit intéressant.",
                "position": (random.randint(0, 800), random.randint(0, 600)),  # (x, y) coordinates
                "image": "rcs/map/tile010.png"
            },
            {
                "name": "Point of Interest 2",
                "description": "Un autre endroit intéressant.",
                "position": (random.randint(0, 800), random.randint(0, 600)),  # (x, y) coordinates
                "image": "rcs/map/tile011.png"
            },
        ]

        # Define the size and position of the map window
        self.map_window_width = 760
        self.map_window_height = 400
        self.map_window_rect = pygame.Rect(20, 20, self.map_window_width, self.map_window_height)

        self.place_locations()


    def place_locations(self):
    # Place cities and points of interest randomly on the map
    # but make sure they are not too close to each other
    # and that they are not outside the map window
        for city in self.cities + self.points_of_interest:
            min_distance_from_edge = 60  # Minimum distance from the edge of the map window
            x = random.randint(self.map_window_rect.left + min_distance_from_edge, self.map_window_rect.right - min_distance_from_edge)
            y = random.randint(self.map_window_rect.top + min_distance_from_edge, self.map_window_rect.bottom - min_distance_from_edge)
            city["position"] = (x, y)

            # Check if the city is too close to another city or point of interest
            # and if it is, move it to a new random position
            colliding = True
            while colliding:
                colliding = False
                for other_city in self.cities + self.points_of_interest:
                    if other_city != city:
                        other_rect = pygame.Rect(other_city["position"], (0, 0))
                        if other_rect.colliderect(pygame.Rect(city["position"], (0, 0))):
                            colliding = True
                            break
                if colliding:
                    x = random.randint(self.map_window_rect.left + min_distance_from_edge, self.map_window_rect.right - min_distance_from_edge)
                    y = random.randint(self.map_window_rect.top + min_distance_from_edge, self.map_window_rect.bottom - min_distance_from_edge)
                    city["position"] = (x, y)

    def handle_events(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if pygame.mouse.get_pressed()[0] == 1:
                if self.back_button.is_clicked():
                    print("Back to menu")
                    # Set the transition flag to True
                    self.next_state = "menu"

    def get_selected_city_info(self):
        return self.cities[self.selected_city]

    def move_to_city(self, index):
        if 0 <= index < len(self.cities):
            self.selected_city = index

    def render(self, screen):
        # Clear the screen
        screen.fill((0, 0, 0))
        pygame.draw.rect(screen, (255, 255, 255), self.map_window_rect, 2)

        # Display city names and images on the screen
        for i, city in enumerate(self.cities):
            city_name = city["name"]
            city_position = city["position"]
            city_image = pygame.image.load(city["image"])  # Load the city image
            text_surface = self.font.render(city_name, True, (255, 255, 255))  # White text
            text_rect = text_surface.get_rect(center=city_position)
            image_rect = city_image.get_rect(center=(city_position[0], city_position[1] + 10 + city_image.get_height() // 2))
            combined_rect = text_rect.union(image_rect)

            select = pygame.image.load("rcs/ui/select.png")
            select = pygame.transform.scale(select, (int(select.get_width()) * 2.5, int(select.get_height()) * 2.5))

            # Check if the mouse is hovering over the city or image
            if combined_rect.collidepoint(pygame.mouse.get_pos()):
                # Draw the select image with the city image centered
                select_rect = select.get_rect(center=image_rect.center)
                select_rect.y -= 10
                screen.blit(select, select_rect)

            screen.blit(city_image, image_rect)  # Draw the city image on the screen

        '''# Display points of interest on the screen
        for point_of_interest in self.points_of_interest:
            point_of_interest_name = point_of_interest["name"]
            point_of_interest_position = point_of_interest["position"]
            point_of_interest_image = pygame.image.load(point_of_interest["image"])  # Load the point of interest image
            point_of_interest_rect = point_of_interest_image.get_rect(center=point_of_interest_position)

            screen.blit(point_of_interest_image, point_of_interest_rect)  # Draw the point of interest image on the screen'''

        self.back_button.draw(screen)
        pygame.display.flip()