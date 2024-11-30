
from constants.constants import *



class Level_1:
    def __init__(self):
        self.bg_color = (0, 0, 0)
        self.worlds = [

        ]
    class World_1:
        def __init__(self):
            self.blocks = [
                pygame.Rect(0, HEIGHT // 2 + 240, 500, 500),
                pygame.Rect(575, HEIGHT // 2 + 200, 50, 50),
                pygame.Rect(700, HEIGHT // 2 + 150, 50, 50)

            ]
            self.spikes = [
                pygame.Rect(200, HEIGHT // 2 + 190, 50, 50),
            ]
            self.special_spikes = [
                pygame.Rect(300, HEIGHT // 2 + 190, 50, 50),
                pygame.Rect(575, HEIGHT // 2 + 150, 50, 50),
            ]
            self.spikes_spritesheet = pygame.image.load('assets/worlds/enemies/16-bit-spike-Sheet.png')
            self.spikes_sprites = []
            for i in range(4):
                sprite = self.spikes_spritesheet.subsurface(pygame.Rect(i * 16, 0, 16, 16))
                sprite = pygame.transform.scale(sprite, (50, 50))
                self.spikes_sprites.append(sprite)
        def draw(self):
            for block in self.blocks:
                pygame.draw.rect(screen, (0, 255, 0), block)
            for spike in self.spikes:
                pygame.draw.rect(screen, (255, 0, 0), spike, 2)
                screen.blit(self.spikes_sprites[0], (spike.x, spike.y))

        def draw_special_spike(self, n):
            pygame.draw.rect(screen, (255, 0, 0), self.special_spikes[n], 2)
            screen.blit(self.spikes_sprites[0], (self.special_spikes[n].x, self.special_spikes[n].y))



