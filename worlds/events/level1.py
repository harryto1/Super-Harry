
from constants.constants import *

def level1_start():
    screen.fill(BLACK)
    title = pygame.font.Font(None, 72).render('Level 1', 1, (255, 255, 255))
    subtitle = pygame.font.Font(None, 36).render('The Beginning', 1, (255, 255, 255))
    title_rect = title.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 100))
    subtitle_rect = subtitle.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 50))
    screen.blit(title, title_rect)
    screen.blit(subtitle, subtitle_rect)
    pygame.display.flip()
    pygame.time.wait(2000)


def world1_events(player, current_world):
    if player.rect.x < 0:
        player.rect.x = 0
    if player.rect.x > 250:
        current_world.draw_special_spike(0)
    if player.rect.x < 450:
        current_world.draw_special_spike(1)
    if player.rect.x > 500:
        current_world.special_spikes.pop()
        current_world.special_spikes.append(pygame.Rect(0, HEIGHT // 2 + 190, 50, 50))

