import pygame

pygame.init()
screen = pygame.display.set_mode((pygame.display.Info().current_w, pygame.display.Info().current_h),
                                 pygame.DOUBLEBUF)
HEIGHT = screen.get_height()
WIDTH = screen.get_width()
bg_color = (0, 0, 0)

BLACK = (0, 0, 0)
GRAY = (128, 128, 128)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
DARK_RED = (169, 0, 0)
