from constants.constants import *

def level2_start():
    screen.fill(BLACK)
    title = pygame.font.Font('assets/font/Monocraft.ttf', 72).render('Level 2', 1, (255, 255, 255))
    subtitle = pygame.font.Font('assets/font/Monocraft.ttf', 36).render('Placeholder for a level description', 1, (255, 255, 255))
    title_rect = title.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 100))
    subtitle_rect = subtitle.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 50))
    screen.blit(title, title_rect)
    screen.blit(subtitle, subtitle_rect)
    pygame.display.flip()
    pygame.time.wait(2000)