from variables import *

class Chip:
    def __init__(self, color, type, center, active):
        self.value = 0
        self.color = color
        self.type = type # "example" or "play"
        self.image = self.set_chip()
        self.image_rect = self.image.get_rect()
        self.image_rect.center = center
        self.active = active
        self.position = center
        if self.type == "example":
            self.font = pygame.font.Font(None, 20)
        elif self.type == "bet":
            self.font = pygame.font.Font(None, 13)

        self.create_value_text()

    def set_chip(self):
        if self.type == "example":
            if self.color == "yellow":
                self.value = 1
                return pygame.image.load("img/yellowChip.png")
            elif self.color == "red":
                self.value = 2
                return pygame.image.load("img/redChip.png")
            elif self.color == "blue":
                self.value = 5
                return pygame.image.load("img/blueChip.png")
            elif self.color == "orange":
                self.value = 10
                return pygame.image.load("img/orangeChip.png")
            elif self.color == "green":
                self.value = 25
                return pygame.image.load("img/greenChip.png")
        elif self.type == "bet":
            if self.color == "yellow":
                self.value = 1
                return pygame.image.load("img/yellowChip2.png")
            elif self.color == "red":
                self.value = 2
                return pygame.image.load("img/redChip2.png")
            elif self.color == "blue":
                self.value = 5
                return pygame.image.load("img/blueChip2.png")
            elif self.color == "orange":
                self.value = 10
                return pygame.image.load("img/orangeChip2.png")
            elif self.color == "green":
                self.value = 25
                return pygame.image.load("img/greenChip2.png")



    def create_value_text(self):
        self.value_text_surface = self.font.render(str(self.value), True, (0, 0, 0))
        self.value_text_rect = self.value_text_surface.get_rect()
        self.value_text_rect.topleft = (self.position[0] - self.value_text_rect.width / 2), (self.position[1] - self.value_text_rect.height / 2)

    def draw(self):
        window.blit(self.image, self.image_rect)
        window.blit(self.value_text_surface, self.value_text_rect)