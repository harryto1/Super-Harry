from constants.constants import *
# Silver Phantom

class Sword:
    def __init__(self, id, sprite, rect):
        self.id = id
        self.rect = rect
        self.sprite = sprite
        self.in_inventory = False # This will be set to True when the player picks up the key

    def draw(self):
        if isinstance(self.sprite, list):
            current_sprite = self.sprite[pygame.time.get_ticks() // 500 % len(self.sprite)]
            screen.blit(current_sprite, self.rect)
        else:
            screen.blit(self.sprite, self.rect)
