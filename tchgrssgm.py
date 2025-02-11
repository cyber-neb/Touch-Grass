import pygame
import time
import threading

# Initialize Pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 500, 400
WHITE = (255, 255, 255)
GREEN = (34, 177, 76)
BLACK = (0, 0, 0)
GRAY = (169, 169, 169)
FPS = 60

# Font
FONT = pygame.font.Font(None, 36)

class TouchGrass:
    def __init__(self):
        self.grass = 0
        self.gps = 0  # Grass per second
        self.touch_power = 1  # Base touch power
        self.double_touch_unlocked = False  # Upgrade status
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

    def buy_upgrade(self):
        if self.grass >= 20 and not self.double_touch_unlocked:
            self.grass -= 20
            self.touch_power *= 2  # Double the touch power
            self.double_touch_unlocked = True

    def run(self):
        screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("Touch Grass")
        clock = pygame.time.Clock()

        button_rect = pygame.Rect(WIDTH // 2 - 75, HEIGHT // 2 - 25, 150, 50)
        upgrade_rect = pygame.Rect(WIDTH // 2 - 75, HEIGHT // 2 + 50, 150, 50)

        running = True
        while running:
            screen.fill(WHITE)

            # Event handling
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
            screen.blit(text, (button_rect.x + 2, button_rect.y + 10))
            
            # Display grass count
            grass_text = FONT.render(f"Grass Touched: {self.grass}", True, BLACK)
            screen.blit(grass_text, (WIDTH // 2 - 100, HEIGHT // 4))

            # Display upgrade button **only if player has at least 20 grass touched**
            if self.grass >= 20 and not self.double_touch_unlocked:
                pygame.draw.rect(screen, GREEN, upgrade_rect)
                upgrade_text = FONT.render("Two Hand Touch", True, BLACK)
                screen.blit(upgrade_text, (upgrade_rect.x - 20, upgrade_rect.y + 10))

            # Display upgrade status if unlocked
            if self.double_touch_unlocked:
                upgrade_status_text = FONT.render(f"Two Hand Touch: Unlocked!", True, BLACK)
                screen.blit(upgrade_status_text, (WIDTH // 2 - 150, HEIGHT // 4 + 40))

            pygame.display.flip()
            clock.tick(FPS)

        pygame.quit()
        self.running = False

if __name__ == "__main__":
    game = TouchGrass()
    game.run()
