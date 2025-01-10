import sys
from constants.constants import *
class PauseMenu:
    def __init__(self):
        self.screen = screen
        self.bg_color = bg_color
        self.title_font = pygame.font.Font(None, 72)
        self.font = pygame.font.Font(None, 36)
        self.font_color = GRAY
        self.menu_items = ['Resume', 'Levels', 'Quit']
        self.selected_item = 0
        self.clock = pygame.time.Clock()
        self.menu_loop = True

    def draw(self):
        self.screen.fill(self.bg_color)
        for i, item in enumerate(self.menu_items):
            if i == self.selected_item:
                label = self.font.render(item, 1, (255, 255, 255))
            else:
                label = self.font.render(item, 1, self.font_color)
            label_rect = label.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 50 + i * 50))
            self.screen.blit(label, label_rect)
        pygame.display.flip()

    def run(self):
        while self.menu_loop:
            self.clock.tick(60)
            self.draw()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_UP:
                        self.selected_item = (self.selected_item - 1) % len(self.menu_items)
                    if event.key == pygame.K_DOWN:
                        self.selected_item = (self.selected_item + 1) % len(self.menu_items)
                    if event.key == pygame.K_RETURN:
                        self.menu_loop = False
        return self.selected_item