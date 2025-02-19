"""@author aeris"""
import pygame
import time
import threading

pygame.init()

WIDTH, HEIGHT = 500, 400
WHITE = (255, 255, 255)
GREEN = (34, 177, 76)
BLACK = (0, 0, 0)
GRAY = (169, 169, 169)
FPS = 60

pygame.font.init()
FONT = pygame.font.Font(None, 36)

class TouchGrass:
    def __init__(self):
        self.grass = 0
        self.gps = 0  # Grass per second
        self.touch_power = 1
        self.double_touch_unlocked = False
        self.dopamine_recovery = 0
        self.running = True
        self.start_gps_thread()

    def start_gps_thread(self):
        def generate_grass():
            while self.running:
                self.grass += self.gps
                time.sleep(1)

        thread = threading.Thread(target=generate_grass, daemon=True)
        thread.start()

    def click(self):
        self.grass += self.touch_power
        self.update_dopamine()

    def update_dopamine(self):
        # Increases dopamine recovery by 1% every 5 clicks
        self.dopamine_recovery = min(self.grass // 5, 100)  # Caps at 100%
        
    def buy_upgrade(self):
        if self.grass >= 20 and not self.double_touch_unlocked:
            self.grass -= 20
            self.touch_power *= 2 
            self.double_touch_unlocked = True

    def run(self):
        screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Touch Grass")
        clock = pygame.time.Clock()

        button_rect = pygame.Rect(WIDTH // 2 - 75, HEIGHT // 2 - 25, 175, 50)
        upgrade_rect = pygame.Rect(WIDTH // 2 - 90, HEIGHT // 2 + 50, 200, 50)

        running = True
        while running:
            screen.fill(WHITE)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    if button_rect.collidepoint(event.pos):
                        self.click()
                    elif self.grass >= 20 and not self.double_touch_unlocked and upgrade_rect.collidepoint(event.pos):
                        self.buy_upgrade()


            # Draw button
            pygame.draw.rect(screen, GREEN, button_rect)
            text = FONT.render("Touch Grass", True, BLACK)
            screen.blit(text, (button_rect.x + 10, button_rect.y + 10))
            
            # Display grass count
            grass_text = FONT.render(f"Grass Touched: {self.grass}", True, BLACK)
            screen.blit(grass_text, (WIDTH // 2 - 100, HEIGHT // 4))

             # Display dopamine recovery
            dopamine_text = FONT.render(f"Dopamine Recovered: {self.dopamine_recovery}%", True, BLACK)
            screen.blit(dopamine_text, (WIDTH // 2 - 150, HEIGHT // 4 + 40))

            # Display upgrade button
            if self.grass >= 20 and not self.double_touch_unlocked:
                pygame.draw.rect(screen, GREEN, upgrade_rect)
                upgrade_text = FONT.render("Two Hand Touch", True, BLACK)
                screen.blit(upgrade_text, (upgrade_rect.x + 2, upgrade_rect.y + 10))

            # Display upgrade status if unlocked
            if self.double_touch_unlocked:
                upgrade_status_text = FONT.render(f"Two Hand Touch: Unlocked!", True, BLACK)
                screen.blit(upgrade_status_text, (WIDTH // 2 - 150, HEIGHT // 4 + 150))

            pygame.display.flip()
            clock.tick(FPS)

        pygame.quit()
        self.running = False

if __name__ == "__main__":
    game = TouchGrass()
    game.run()
