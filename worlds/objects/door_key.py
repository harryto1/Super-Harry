
from constants.constants import *

class DoorKey:
    def __init__(self, id, door, key_sprite):
        self.id = id
        self.door = door
        self.rect = pygame.Rect(500, HEIGHT // 2 + 200, 50, 50)
        self.key_sprite = key_sprite
        self.in_inventory = False # This will be set to True when the player picks up the key

    def draw(self):
        screen.blit(self.key_sprite, self.rect)
