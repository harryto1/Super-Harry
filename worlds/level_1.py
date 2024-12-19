import random

import pygame.time

from constants.constants import *
from worlds.objects.door_key import DoorKey



class Level1:
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
        self.worlds = [self.World1(), self.World2(), self.World3()]
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
            self.start_y = HEIGHT // 2 + 200 # The y-coordinate where the player will be teleported when the world is loaded
            self.end_y = HEIGHT // 2 + 220 # The y-coordinate where the player will be teleported when coming back from a future level

            # IMPORTANT NOTE: The coordinates above are calculated using the y of the first
            # line of blocks in the world - the height of the player rect

            self.blocks_sprites = Level1.block_sprites # This is a list of block sprites
            self.spikes_sprites = Level1.spikes_sprites
            self.blocks = [
                [pygame.Rect(x, HEIGHT // 2 + y, 50, 50) for x in range(0, 500, 50) for y in range(240, HEIGHT, 50)],
                pygame.Rect(575, HEIGHT // 2 + 200, 50, 50),
                pygame.Rect(700, HEIGHT // 2 + 150, 50, 50),
                [pygame.Rect(x, HEIGHT // 2 + y, 50, 50) for x in range(1300, WIDTH, 50) for y in range(260, HEIGHT, 50)]

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
            # The spikes below have a moving functionality when the player reaches them
            self.inverted_spikes = [
                pygame.Rect(WIDTH - 200, -50, 50, 50),
                pygame.Rect(WIDTH - 150, -50, 50, 50),
            ]
            self.moving_spike_activated = False # This is a boolean that checks if the moving spike is activated
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
            if len(self.inverted_spikes) > 0:
                for inverted_spike in self.inverted_spikes:
                    if self.moving_spike_activated:
                        inverted_spike.y += 24
                        if inverted_spike.y > HEIGHT - 280:
                            self.moving_spike_activated = False
                            self.inverted_spikes = []
                    if self.moving_spike_activated:
                        pygame.draw.rect(screen, (255, 0, 0), inverted_spike, 2)
                        screen.blit(self.spikes_sprites[2], (inverted_spike.x, inverted_spike.y))


        def draw_special_spike(self, n):
            pygame.draw.rect(screen, (255, 0, 0), self.special_spikes[n], 2)
            screen.blit(self.spikes_sprites[0], (self.special_spikes[n].x, self.special_spikes[n].y))

    class World2:
        def __init__(self):
            self.start_y = HEIGHT // 2 + 220 # The y-coordinate where the player will be teleported when the world is loaded
            self.end_y = HEIGHT // 2 + 60 # The y-coordinate where the player will be teleported when coming back from a future level

            self.blocks = [
                [pygame.Rect(x, HEIGHT // 2 + y, 50, 50) for x in range(0, 300, 50) for y in range(260, HEIGHT, 50)],
                [pygame.Rect(x, HEIGHT // 2 + 50, 50, 50) for x in range(100, 201, 50)],
                [pygame.Rect(x, HEIGHT // 2 + y, 50, 50) for x in range(WIDTH - 320, WIDTH + 1, 50) for y in range(100, HEIGHT, 50)],
                [pygame.Rect(x, HEIGHT // 2 + 25, 50, 50) for x in range(WIDTH - 600, WIDTH - 451, 50)]
            ]

            self.moving_blocks = [
                [pygame.Rect(400, HEIGHT // 2 + 100, 50, 50), 'down'],
                [pygame.Rect(550, HEIGHT // 2 + 100, 50, 50), 'down'],
                [pygame.Rect(700, HEIGHT // 2 + 100, 50, 50), 'down']
            ]
            self.disappearing_blocks = [
                [pygame.Rect(x, HEIGHT // 2 + 75, 50, 50) for x in range(800, WIDTH // 2 + 200, 50)]
            ]

            self.visible_blocks = self.disappearing_blocks[0]

            self.lava = [
                [pygame.Rect(x, y, 50, 50) for x in range(0, WIDTH, 50) for y in range(HEIGHT, HEIGHT + HEIGHT // 2, 50)]
            ]

            self.bonus_hearts = [
                [pygame.Rect(150, HEIGHT // 2, 50, 50), True]
            ]

            self.fireballs = [
                pygame.Rect(random.randint(300, WIDTH -350), HEIGHT // 2 + 100, 35, 50),
                pygame.Rect(random.randint(300, WIDTH - 350), HEIGHT // 2 + 100, 35, 50),
                pygame.Rect(random.randint(300, WIDTH - 350), HEIGHT // 2 + 100, 35, 50)
            ]

        def draw(self):
            for block in self.moving_blocks:
                pygame.draw.rect(screen, (0, 0, 255), block[0])
                screen.blit(Level1.block_sprites[0], (block[0].x, block[0].y))
                if block[1] == 'down':
                    block[0].y += 3
                if block[0].y > HEIGHT - 50:
                    block[1] = 'up'
                if block[1] == 'up':
                    block[0].y -= 3
                if block[0].y < HEIGHT // 2 + 150:
                    block[1] = 'down'

            for lava in self.lava:
                current_time = pygame.time.get_ticks()
                if isinstance(lava, list):
                    for l in lava:
                        sprite_index = (current_time // 100) % len(Level1.lava_sprites)
                        screen.blit(Level1.lava_sprites[sprite_index], (l.x, l.y))
                        if current_time % 1000 < 50:
                            if lava[0].y > HEIGHT // 2:
                                l.y -= 2
                else:
                    sprite_index = (current_time // 100) % len(Level1.lava_sprites)
                    screen.blit(Level1.lava_sprites[sprite_index], (lava.x, lava.y))
                    if current_time % 1000 < 50:
                        if lava.y > HEIGHT // 2:
                            lava.y -= 2

            for block in self.blocks:
                if isinstance(block, list):
                    for b in block:
                        pygame.draw.rect(screen, (0, 255, 0), b)
                        screen.blit(Level1.block_sprites[0], (b.x, b.y))
                else:
                    pygame.draw.rect(screen, (0, 255, 0), block)
                    screen.blit(Level1.block_sprites[0], (block.x, block.y))

            for block in self.visible_blocks:
                pygame.draw.rect(screen, (0, 255, 0), block)
                screen.blit(Level1.block_sprites[0], (block.x, block.y))


            for heart in self.bonus_hearts:
                if heart[1]:
                    pygame.draw.rect(screen, (255, 0, 0), heart[0], 2)
                    screen.blit(Level1.bonus_hearts_sprite, (
                    heart[0].x + (heart[0].width - Level1.bonus_hearts_sprite.get_width()) // 2,
                    heart[0].y + (heart[0].height - Level1.bonus_hearts_sprite.get_height()) // 2))
            for fireball in self.fireballs:
                current_time = pygame.time.get_ticks()
                sprite_index = (current_time // 100) % len(Level1.fireball_sprites)
                sprite = Level1.fireball_sprites[sprite_index]
                sprite_rect = sprite.get_rect(center=fireball.midbottom)
                sprite_rect.x -= 12.5
                sprite_rect.y -= 10
                fireball.y -= 7
                if fireball.y < -750:
                    fireball.y = self.lava[0][0].y - 25
                    fireball.x = random.randint(300, WIDTH - 350)
                if any(fireball.colliderect(other) for other in self.fireballs if other != fireball):
                    fireball.x = random.randint(300, WIDTH - 350)
                screen.blit(sprite, sprite_rect.topleft)
                pygame.draw.rect(screen, (255, 0, 0), fireball, 2)

        def shake_block(self, block):
            if pygame.time.get_ticks() % 100 < 50:
                block.x += 2
            if 50 < pygame.time.get_ticks() % 100 < 100:
                block.x -= 2

        def regen(self):
            self.moving_blocks = [
                [pygame.Rect(400, HEIGHT // 2 + 100, 50, 50), 'down', True],
                [pygame.Rect(550, HEIGHT // 2 + 100, 50, 50), 'down', True],
                [pygame.Rect(700, HEIGHT // 2 + 100, 50, 50), 'down', True],
            ]

    class World3:
        def __init__(self):

            self.start_y = HEIGHT // 2 + 220 # The y-coordinate where the player will be teleported when the world is loaded

            self.blocks = [
                [pygame.Rect(x, HEIGHT // 2 + y, 50, 50) for x in range(0, 250, 50) for y in range(260, HEIGHT, 50)], # Start blocks
                [pygame.Rect(x, y, 50, 50) for x in range(WIDTH - 200, WIDTH + 1, 50) for y in range(HEIGHT // 3, HEIGHT, 50)], # End blocks
                [pygame.Rect(x, HEIGHT // 3, 50, 50) for x in range(500, WIDTH - 200, 50)] # Debug Blocks
            ]

            self.moving_blocks = [
                [pygame.Rect(350, HEIGHT // 2 + 100, 50, 50), 'up'],
                [pygame.Rect(450, HEIGHT // 3 + 100, 50, 50), 'right'],
                [pygame.Rect(WIDTH // 3 + 200, HEIGHT // 3 + 100 , 50, 50), 'down'],
                [pygame.Rect(WIDTH // 3 + 100, HEIGHT // 2 + 260 , 50, 50), 'left']
            ]

            self.doors = [
                [pygame.Rect(WIDTH - 50, HEIGHT // 3 - 100, 50, 100), 'locked']
            ]

            self.objects = [
                DoorKey('door_key_1', self.doors[0], Level1.key_sprites)
            ]


        def draw(self):
            for block in self.blocks:
                if isinstance(block, list):
                    for b in block:
                        pygame.draw.rect(screen, (0, 255, 0), b)
                        screen.blit(Level1.block_sprites[0], (b.x, b.y))
                else:
                    pygame.draw.rect(screen, (0, 255, 0), block)
                    screen.blit(Level1.block_sprites[0], (block.x, block.y))

            for door in self.doors:
                if door[1] == 'unlocked':
                    pygame.draw.rect(screen, (255, 0, 0), door[0], 2)
                    screen.blit(Level1.unlocked_door_sprite[0], (door[0].x, door[0].y))
                else:
                    pygame.draw.rect(screen, (255, 0, 0), door[0], 2)
                    screen.blit(Level1.door_sprite[0], (door[0].x, door[0].y))

            for obj in self.objects:
                if not obj.in_inventory:
                    obj.draw()

            for i in range(len(self.moving_blocks)):
                pygame.draw.rect(screen, (0, 0, 255), self.moving_blocks[i][0])
                screen.blit(Level1.block_sprites[0], (self.moving_blocks[i][0].x, self.moving_blocks[i][0].y))
                match i:
                    case 0:
                        if self.moving_blocks[i][1] == 'down':
                            self.moving_blocks[i][0].y += 3
                        if self.moving_blocks[i][0].y > HEIGHT // 2 + 260:
                            self.moving_blocks[i][1] = 'up'
                        if self.moving_blocks[i][1] == 'up':
                            self.moving_blocks[i][0].y -= 3
                        if self.moving_blocks[i][0].y < HEIGHT // 3 + 100:
                            self.moving_blocks[i][1] = 'down'
                    case 1:
                        if self.moving_blocks[i][1] == 'right':
                            self.moving_blocks[i][0].x += 3
                        if self.moving_blocks[i][0].x > WIDTH // 3 + 100:
                            self.moving_blocks[i][1] = 'left'
                        if self.moving_blocks[i][1] == 'left':
                            self.moving_blocks[i][0].x -= 3
                        if self.moving_blocks[i][0].x < 450:
                            self.moving_blocks[i][1] = 'right'
                    case 2:
                        if self.moving_blocks[i][1] == 'down':
                            self.moving_blocks[i][0].y += 3
                        if self.moving_blocks[i][0].y > HEIGHT // 2 + 260:
                            self.moving_blocks[i][1] = 'up'
                        if self.moving_blocks[i][1] == 'up':
                            self.moving_blocks[i][0].y -= 3
                        if self.moving_blocks[i][0].y < HEIGHT // 3 + 100:
                            self.moving_blocks[i][1] = 'down'
                    case 3:
                        if self.moving_blocks[i][1] == 'left':
                            self.moving_blocks[i][0].x -= 3
                        if self.moving_blocks[i][0].x < WIDTH // 3 - 50:
                            self.moving_blocks[i][1] = 'right'
                        if self.moving_blocks[i][1] == 'right':
                            self.moving_blocks[i][0].x += 3
                        if self.moving_blocks[i][0].x > WIDTH // 3 + 100:
                            self.moving_blocks[i][1] = 'left'




