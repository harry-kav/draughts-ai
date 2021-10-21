import pygame

WIDTH, HEIGHT = 600,600

ROWS, COLS = 8,8

SQUARE_SIZE = HEIGHT//ROWS

BLUE = (0,0,255)
WHITE = (255,255,255)
BLACK = (0,0,0)
RED = (255,0,0)

CROWN = pygame.transform.scale(pygame.image.load("assets/crown.png"), (44,25))
