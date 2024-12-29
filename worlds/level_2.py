
import pygame.time

from constants.constants import *

class Level2:
    block_sprites = []
    spikes_sprites = []
    lava_sprites = []
    fireball_sprites = []
    door_sprite = []
    unlocked_door_sprite = []
    key_sprites = [
        pygame.transform.scale(pygame.image.load('assets/worlds/objects/door_key_1.png'), (50, 50)),
        pygame.transform.scale(pygame.image.load('assets/worlds/objects/door_key_1(2).png'), (50, 50))
        ]
    bonus_hearts_sprite = pygame.transform.scale(pygame.image.load('assets/characters/ui/heart_scaled_to_256x256.png'), (35, 35))

    def __init__(self):
        self.bg_color = (0, 0, 0)
        self.worlds = [self.World1()]
        self.background_surface = pygame.Surface((WIDTH, HEIGHT))
        self.background_spritesheet = pygame.image.load('assets/worlds/background/Dungeon_brick_wall_blue.png.png')
        self.background_sprite = pygame.transform.scale(self.background_spritesheet.subsurface(pygame.Rect(0, 0, 1920, 1080)), (WIDTH, HEIGHT))
        self.block_spritesheet = pygame.image.load('assets/worlds/blocks/blocks.png')
        self.spikes_spritesheet = pygame.image.load('assets/worlds/enemies/16-bit-spike-Sheet.png')
        self.lava_spritesheet = pygame.image.load('assets/worlds/enemies/spritesheet-burninglava.png')
        self.fireball_spritesheet = pygame.image.load('assets/worlds/enemies/Firebolt SpriteSheet.png')
        self.door_spritesheet = pygame.image.load('assets/worlds/background/Tiles.png')
        for i in range(5):
            sprite = self.block_spritesheet.subsurface(pygame.Rect(i * 32, 0, 32, 32))
            sprite = pygame.transform.scale(sprite, (50, 50))
            self.block_sprites.append(sprite)
        for i in range(4):
            sprite = self.spikes_spritesheet.subsurface(pygame.Rect(i * 16, 0, 16, 16))
            sprite = pygame.transform.scale(sprite, (50, 50))
            self.spikes_sprites.append(sprite)
        for i in range(49):
            if 2 < i % 7 < 6:
                sprite = self.lava_spritesheet.subsurface(pygame.Rect(i * 16, 32, 16, 16))
                sprite = pygame.transform.scale(sprite, (50, 50))
                self.lava_sprites.append(sprite)
        for i in range(4):
            sprite = self.fireball_spritesheet.subsurface(pygame.Rect(i * 48, 0, 48, 48))
            sprite = pygame.transform.rotate(sprite, 90)
            sprite = pygame.transform.scale(sprite, (100, 100))
            self.fireball_sprites.append(sprite)
        door_sprite = self.door_spritesheet.subsurface(pygame.Rect(0, 115, 32, 44))
        door_sprite = pygame.transform.scale(door_sprite, (50, 100))
        self.door_sprite.append(door_sprite)
        unlocked_door_sprite = self.door_spritesheet.subsurface(pygame.Rect(0, 159, 32, 44))
        unlocked_door_sprite = pygame.transform.scale(unlocked_door_sprite, (50, 100))
        self.unlocked_door_sprite.append(unlocked_door_sprite)


    def draw_background_once(self):
        self.background_surface.blit(self.background_sprite, (0, 0))
        self.background_surface.fill((50, 50, 50), special_flags=pygame.BLEND_RGB_MULT)

    def draw_background(self):
        screen.blit(self.background_surface, (0, 0))

    class World1:
        def __init__(self):
            self.start_y = HEIGHT - 240
            self.end_y = HEIGHT - 240

            self.blocks = [
                [pygame.Rect(x, y, 50, 50) for x in range(0, WIDTH, 50) for y in range(HEIGHT - 200, HEIGHT, 50)]
            ]

        def draw(self):
            for block in self.blocks:
                if isinstance(block, list):
                    for b in block:
                        pygame.draw.rect(screen, (0, 255, 0), b)
                        screen.blit(Level2.block_sprites[0], (b.x, b.y))
                else:
                    pygame.draw.rect(screen, (0, 255, 0), block)
                    screen.blit(Level2.block_sprites[0], (block.x, block.y))