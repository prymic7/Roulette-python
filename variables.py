import pygame
import random
import sys
import time

width = 720
height = 400

table_image_width = 720
table_image_height = 360

bottom_label_height = height - table_image_height
bottom_label_y = width - bottom_label_height

game_font_size = 25
number_font_size = 45

game_font_color = (255, 255, 255)
action_font_color = (255, 255, 0)

black_color = (0, 0, 0)
red_color = (255, 0, 0)
green_color = (0, 255, 0)

window = pygame.display.set_mode((width, height))


