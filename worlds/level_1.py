
from constants.constants import *



class Level1:
    block_sprites = []
    spikes_sprites = []

    def __init__(self):
        self.bg_color = (0, 0, 0)
        self.worlds = [self.World1(), self.World2()]
        self.block_spritesheet = pygame.image.load('assets/worlds/blocks/blocks.png')
        self.spikes_spritesheet = pygame.image.load('assets/worlds/enemies/16-bit-spike-Sheet.png')
        for i in range(5):
            sprite = self.block_spritesheet.subsurface(pygame.Rect(i * 32, 0, 32, 32))
            sprite = pygame.transform.scale(sprite, (50, 50))
            self.block_sprites.append(sprite)
        for i in range(4):
            sprite = self.spikes_spritesheet.subsurface(pygame.Rect(i * 16, 0, 16, 16))
            sprite = pygame.transform.scale(sprite, (50, 50))
            self.spikes_sprites.append(sprite)

    class World1:
        def __init__(self):
            self.blocks_sprites = Level1.block_sprites # This is a list of block sprites
            self.spikes_sprites = Level1.spikes_sprites
            self.blocks = [
                [pygame.Rect(x, HEIGHT // 2 + y, 50, 50) for x in range(0, 500, 50) for y in range(240, HEIGHT, 50)],
                pygame.Rect(575, HEIGHT // 2 + 200, 50, 50),
                pygame.Rect(700, HEIGHT // 2 + 150, 50, 50),
                [pygame.Rect(x, HEIGHT // 2 + y, 50, 50) for x in range(1300, 1600, 50) for y in range(260, HEIGHT, 50)]

            ]
            self.moving_blocks = [
                [pygame.Rect(800, HEIGHT // 2 + 100, 50, 50), 'right'],
            ]
            self.spikes = [
                pygame.Rect(200, HEIGHT // 2 + 190, 50, 50),
            ]
            self.special_spikes = [
                pygame.Rect(300, HEIGHT // 2 + 190, 50, 50),
                pygame.Rect(575, HEIGHT // 2 + 150, 50, 50),
            ]
        def draw(self):
            for block in self.blocks:
                if isinstance(block, list):
                    for b in block:
                        pygame.draw.rect(screen, (0, 255, 0), b)
                        screen.blit(self.blocks_sprites[0], (b.x, b.y))
                else:
                    pygame.draw.rect(screen, (0, 255, 0), block)
                    screen.blit(self.blocks_sprites[0], (block.x, block.y))
            for spike in self.spikes:
                pygame.draw.rect(screen, (255, 0, 0), spike, 2)
                screen.blit(self.spikes_sprites[0], (spike.x, spike.y))
            for moving_block in self.moving_blocks:
                pygame.draw.rect(screen, (0, 0, 255), moving_block[0])
                screen.blit(self.blocks_sprites[0], (moving_block[0].x, moving_block[0].y))
                if moving_block[1] == 'right':
                    moving_block[0].x += 3 # Move the block to the right
                if moving_block[1] == 'left':
                    moving_block[0].x -= 3 # Move the block to the left
                if moving_block[0].x > 1100:
                    moving_block[1] = 'left'
                if moving_block[0].x < 800:
                    moving_block[1] = 'right'





        def draw_special_spike(self, n):
            pygame.draw.rect(screen, (255, 0, 0), self.special_spikes[n], 2)
            screen.blit(self.spikes_sprites[0], (self.special_spikes[n].x, self.special_spikes[n].y))

    class World2:
        def __init__(self):
            self.blocks = [
                [pygame.Rect(x, HEIGHT // 2 + y, 300, 200) for x in range(0, 300, 50) for y in range(260, HEIGHT, 50)]
            ]
        def draw(self):
            for block in self.blocks:
                pygame.draw.rect(screen, (0, 255, 0), block)
                screen.blit(Level1.block_sprites[0], (block.x, block.y))

