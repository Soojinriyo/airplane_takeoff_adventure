import pygame
import random
import sys

# --- Constants ---
WIDTH, HEIGHT = 800, 600
FPS = 60

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (180, 180, 180)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

# Aircraft types
AIRCRAFTS = ['Boeing 737', 'Airbus A320', 'Cessna 172']

# Hazards: S&P 500 기업 로고와 경찰관
HAZARD_IMAGES = [
    'apple', 'google', 'tesla', 'microsoft', 'amazon', 'police'
]
HAZARDS = [name.capitalize() for name in HAZARD_IMAGES]

# --- Asset placeholders ---
# (Replace with actual images/sounds in assets/ or resources/ directory)

# --- Classes ---
class Aircraft:
    def __init__(self, name, x, y):
        self.name = name
        self.x = x
        self.y = y
        self.speed = 5
        self.width = 60
        self.height = 30
        # Load actual aircraft image
        img_path = f"resources/{self.name.replace(' ', '_').lower()}.png"
        try:
            self.image = pygame.image.load(img_path)
            self.image = pygame.transform.scale(self.image, (self.width, self.height))
        except:
            self.image = None  # If image not found, do not draw
    def draw(self, screen):
        if self.image:
            screen.blit(self.image, (self.x, self.y))
        else:
            # Optionally, draw nothing or a placeholder (currently nothing)
            pass

class Hazard:
    def __init__(self, kind, x, y):
        self.kind = kind
        self.x = x
        self.y = y
        self.size = 48
        # Load image for hazard
        img_path = f"resources/{self.kind.lower()}.png"
        try:
            self.image = pygame.image.load(img_path)
            self.image = pygame.transform.scale(self.image, (self.size, self.size))
        except:
            self.image = None
    def draw(self, screen):
        if self.image:
            screen.blit(self.image, (self.x - self.size//2, self.y - self.size//2))
        else:
            # Draw a red circle if image not found
            pygame.draw.circle(screen, RED, (self.x, self.y), self.size//2)
            font = pygame.font.SysFont(None, 20)
            text = font.render(self.kind[0], True, WHITE)
            screen.blit(text, (self.x-8, self.y-10))

# --- Game Functions ---
def draw_text(screen, text, size, x, y, color=BLACK):
    font = pygame.font.SysFont(None, size)
    surface = font.render(text, True, color)
    screen.blit(surface, (x, y))

def select_menu(screen, options, title):
    selected = 0
    while True:
        screen.fill(WHITE)
        draw_text(screen, title, 48, 220, 100)
        for i, opt in enumerate(options):
            color = BLUE if i == selected else BLACK
            draw_text(screen, opt, 36, 250, 200 + i * 50, color)
        pygame.display.flip()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit(); sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    selected = (selected - 1) % len(options)
                elif event.key == pygame.K_DOWN:
                    selected = (selected + 1) % len(options)
                elif event.key in [pygame.K_RETURN, pygame.K_SPACE]:
                    return selected

def main():
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption('Airplane Takeoff Adventure')
    clock = pygame.time.Clock()

    # Menu: Select aircraft
    aircraft_idx = select_menu(screen, AIRCRAFTS, 'Select Aircraft')
    aircraft = Aircraft(AIRCRAFTS[aircraft_idx], WIDTH//2-30, HEIGHT-80)

    # Menu: Select runway (placeholder)
    runway_idx = select_menu(screen, ['Runway A', 'Runway B'], 'Select Runway')

    # Game loop
    hazards = []
    for _ in range(3):
        kind = random.choice(HAZARDS)
        x = random.randint(100, WIDTH-100)
        y = random.randint(150, HEIGHT-250)
        hazards.append(Hazard(kind, x, y))

    running = True
    takeoff = False
    start_ticks = pygame.time.get_ticks()
    score = 0
    avoided_hazards = 0
    collided = False
    while running:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        keys = pygame.key.get_pressed()
        if not takeoff:
            if keys[pygame.K_LEFT]:
                aircraft.x -= aircraft.speed
            if keys[pygame.K_RIGHT]:
                aircraft.x += aircraft.speed
            if keys[pygame.K_UP]:
                aircraft.y -= aircraft.speed
            if keys[pygame.K_DOWN]:
                aircraft.y += aircraft.speed
            if keys[pygame.K_SPACE]:
                takeoff = True

        # Collision check
        for hz in hazards:
            if abs(aircraft.x + aircraft.width//2 - hz.x) < 40 and abs(aircraft.y + aircraft.height//2 - hz.y) < 40:
                collided = True
                draw_text(screen, f'Game Over! Hit: {hz.kind}', 48, 180, 250, RED)
                pygame.display.flip()
                pygame.time.wait(2000)
                running = False
                break

        # Takeoff success
        if takeoff and aircraft.y < 50 and not collided:
            elapsed_sec = (pygame.time.get_ticks() - start_ticks) // 1000
            avoided_hazards = len(hazards)
            score = max(0, 1000 - elapsed_sec * 100 + avoided_hazards * 200)
            draw_text(screen, 'Takeoff Success!', 48, 180, 220, GREEN)
            draw_text(screen, f'Time: {elapsed_sec}s', 36, 250, 300, BLACK)
            draw_text(screen, f'Score: {score}', 36, 250, 350, BLUE)
            pygame.display.flip()
            pygame.time.wait(3000)
            running = False
            break

        # Draw
        screen.fill((200, 220, 255))
        # Draw runway (Haneda style placeholder)
        pygame.draw.rect(screen, GRAY, (100, HEIGHT-100, WIDTH-200, 80))
        draw_text(screen, 'Haneda Airport', 32, 300, HEIGHT-60)
        # Draw hazards
        for hz in hazards:
            hz.draw(screen)
        # Draw aircraft
        aircraft.draw(screen)
        # Timer
        elapsed_sec = (pygame.time.get_ticks() - start_ticks) // 1000
        draw_text(screen, f'Time: {elapsed_sec}s', 24, 650, 10)
        draw_text(screen, 'Arrow keys: Move | SPACE: Takeoff', 24, 10, 10)
        pygame.display.flip()

    pygame.quit()

if __name__ == '__main__':
    main()
