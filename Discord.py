import pygame
import random
import sys # Import sys for a clean exit

# Initialize Pygame
pygame.init()

# --- Constants ---
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 200, 0) # Brighter green for player
BLUE = (0, 0, 255)
GREY = (128, 128, 128)
YELLOW = (255, 255, 0)

PLAYER_CAR_WIDTH = 50
PLAYER_CAR_HEIGHT = 80
PLAYER_CAR_SPEED = 10 # Increased speed for better control

OBSTACLE_CAR_WIDTH = 50
OBSTACLE_CAR_HEIGHT = 80
OBSTACLE_CAR_SPEED_MIN = 5
OBSTACLE_CAR_SPEED_MAX = 10
OBSTACLE_SPAWN_RATE = 60 # Lower number means more frequent spawns (frames)
OBSTACLE_INITIAL_COUNT = 1 # Number of obstacles to start with

ROAD_LINE_WIDTH = 10
ROAD_LINE_HEIGHT = 100
ROAD_LINE_GAP = 50
ROAD_LINE_SPEED = 7

FONT_NAME = pygame.font.match_font('arial') # Get a common font
FONT_SIZE_LARGE = 64
FONT_SIZE_MEDIUM = 32
FONT_SIZE_SMALL = 24

# --- Game Setup ---
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Simple Car Game")
clock = pygame.time.Clock()

# --- Helper Functions ---
def draw_text(surface, text, size, x, y, color=WHITE):
    """Helper function to draw text on the screen."""
    font = pygame.font.Font(FONT_NAME, size)
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect()
    text_rect.midtop = (x, y)
    surface.blit(text_surface, text_rect)

def draw_car(surface, x, y, width, height, color):
    """Draws a simple rectangle representing a car."""
    pygame.draw.rect(surface, color, [x, y, width, height])
    # Add some detail (e.g., darker rectangle for windows)
    pygame.draw.rect(surface, BLACK, [x + width * 0.1, y + height * 0.1, width * 0.8, height * 0.3])
    # Wheels (simple circles)
    wheel_radius = int(height * 0.15)
    pygame.draw.circle(surface, BLACK, (int(x), int(y + height * 0.25)), wheel_radius)
    pygame.draw.circle(surface, BLACK, (int(x + width), int(y + height * 0.25)), wheel_radius)
    pygame.draw.circle(surface, BLACK, (int(x), int(y + height * 0.75)), wheel_radius)
    pygame.draw.circle(surface, BLACK, (int(x + width), int(y + height * 0.75)), wheel_radius)


def draw_road_lines(surface, lines):
    """Draws moving road lines."""
    for line in lines:
        pygame.draw.rect(surface, WHITE, line)

# --- Game Classes ---
class PlayerCar(pygame.sprite.Sprite):
    """Represents the player's car."""
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface([PLAYER_CAR_WIDTH, PLAYER_CAR_HEIGHT])
        # self.image.fill(GREEN) # Simple fill for sprite
        self.rect = self.image.get_rect()
        self.rect.x = SCREEN_WIDTH // 2 - PLAYER_CAR_WIDTH // 2
        self.rect.y = SCREEN_HEIGHT - PLAYER_CAR_HEIGHT - 20 # Start near bottom
        self.speed_x = 0

    def update(self):
        """Updates the player's car position."""
        self.speed_x = 0 # Reset speed each frame, movement is event-driven
        keystate = pygame.key.get_pressed()
        if keystate[pygame.K_LEFT] or keystate[pygame.K_a]:
            self.speed_x = -PLAYER_CAR_SPEED
        if keystate[pygame.K_RIGHT] or keystate[pygame.K_d]:
            self.speed_x = PLAYER_CAR_SPEED

        self.rect.x += self.speed_x

        # Keep player on screen
        if self.rect.left < 0:
            self.rect.left = 0
        if self.rect.right > SCREEN_WIDTH:
            self.rect.right = SCREEN_WIDTH

    def draw(self, surface):
        """Draws the player car with more detail."""
        draw_car(surface, self.rect.x, self.rect.y, PLAYER_CAR_WIDTH, PLAYER_CAR_HEIGHT, GREEN)


class ObstacleCar(pygame.sprite.Sprite):
    """Represents an obstacle car."""
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface([OBSTACLE_CAR_WIDTH, OBSTACLE_CAR_HEIGHT])
        self.color = random.choice([RED, BLUE, YELLOW, GREY]) # Random color for obstacles
        # self.image.fill(self.color) # Simple fill for sprite
        self.rect = self.image.get_rect()
        self.rect.x = random.randrange(0, SCREEN_WIDTH - OBSTACLE_CAR_WIDTH)
        self.rect.y = random.randrange(-300, -OBSTACLE_CAR_HEIGHT) # Start off screen
        self.speed_y = random.randrange(OBSTACLE_CAR_SPEED_MIN, OBSTACLE_CAR_SPEED_MAX)

    def update(self):
        """Updates the obstacle car's position."""
        self.rect.y += self.speed_y
        # Remove obstacle if it goes off the bottom of the screen
        if self.rect.top > SCREEN_HEIGHT:
            self.rect.x = random.randrange(0, SCREEN_WIDTH - OBSTACLE_CAR_WIDTH)
            self.rect.y = random.randrange(-200, -OBSTACLE_CAR_HEIGHT)
            self.speed_y = random.randrange(OBSTACLE_CAR_SPEED_MIN, OBSTACLE_CAR_SPEED_MAX)
            # Return True if reset, to increment score
            return True
        return False # Not reset

    def draw(self, surface):
        """Draws the obstacle car with more detail."""
        draw_car(surface, self.rect.x, self.rect.y, OBSTACLE_CAR_WIDTH, OBSTACLE_CAR_HEIGHT, self.color)


# --- Game State Functions ---
def show_start_screen():
    """Displays the start screen."""
    screen.fill(BLACK)
    draw_text(screen, "Simple Car Game!", FONT_SIZE_LARGE, SCREEN_WIDTH / 2, SCREEN_HEIGHT / 4)
    draw_text(screen, "Use Left/Right Arrow keys or A/D to Move", FONT_SIZE_MEDIUM, SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)
    draw_text(screen, "Press any key to begin", FONT_SIZE_MEDIUM, SCREEN_WIDTH / 2, SCREEN_HEIGHT * 3 / 4)
    pygame.display.flip()
    waiting = True
    while waiting:
        clock.tick(60) # Keep clock ticking
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit() # Clean exit
            if event.type == pygame.KEYUP:
                waiting = False

def show_game_over_screen(score):
    """Displays the game over screen."""
    screen.fill(BLACK)
    draw_text(screen, "GAME OVER", FONT_SIZE_LARGE, SCREEN_WIDTH / 2, SCREEN_HEIGHT / 4)
    draw_text(screen, f"Your Score: {score}", FONT_SIZE_MEDIUM, SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2)
    draw_text(screen, "Press 'R' to Play Again or 'Q' to Quit", FONT_SIZE_MEDIUM, SCREEN_WIDTH / 2, SCREEN_HEIGHT * 3 / 4 - 30)
    pygame.display.flip()
    waiting = True
    while waiting:
        clock.tick(60)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_q:
                    pygame.quit()
                    sys.exit()
                if event.key == pygame.K_r:
                    waiting = False # Will lead to game_loop() restart

# --- Main Game Loop ---
def game_loop():
    """The main loop where the game runs."""
    all_sprites = pygame.sprite.Group()
    obstacles = pygame.sprite.Group()

    player = PlayerCar()
    all_sprites.add(player)

    for _ in range(OBSTACLE_INITIAL_COUNT): # Start with a few obstacles
        obstacle = ObstacleCar()
        all_sprites.add(obstacle)
        obstacles.add(obstacle)

    # Road lines setup
    road_lines = []
    for i in range(int(SCREEN_HEIGHT / (ROAD_LINE_HEIGHT + ROAD_LINE_GAP)) + 2):
        line_y = i * (ROAD_LINE_HEIGHT + ROAD_LINE_GAP) - ROAD_LINE_HEIGHT
        road_lines.append(pygame.Rect(SCREEN_WIDTH // 3 - ROAD_LINE_WIDTH // 2, line_y, ROAD_LINE_WIDTH, ROAD_LINE_HEIGHT))
        road_lines.append(pygame.Rect(SCREEN_WIDTH * 2 // 3 - ROAD_LINE_WIDTH // 2, line_y, ROAD_LINE_WIDTH, ROAD_LINE_HEIGHT))


    score = 0
    obstacle_spawn_timer = 0
    running = True
    game_over = False

    while running:
        if game_over:
            show_game_over_screen(score)
            # After game over screen, reset for a new game
            game_over = False # Reset flag
            all_sprites.empty()
            obstacles.empty()

            player = PlayerCar()
            all_sprites.add(player)

            for _ in range(OBSTACLE_INITIAL_COUNT):
                obstacle = ObstacleCar()
                all_sprites.add(obstacle)
                obstacles.add(obstacle)
            score = 0
            obstacle_spawn_timer = 0
            # No need to call game_loop() again, just reset state and continue loop

        # --- Event Handling ---
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # --- Game Logic (Update) ---
        if not game_over:
            all_sprites.update() # Calls update on player

            # Update obstacles and check for scoring
            for obstacle in list(obstacles): # Iterate over a copy for safe removal/modification
                if obstacle.update(): # obstacle.update() returns True if it went off screen
                    score += 10 # Increase score for dodging an obstacle
                    # Optionally, increase difficulty
                    # OBSTACLE_CAR_SPEED_MIN = min(20, OBSTACLE_CAR_SPEED_MIN + 0.1)
                    # OBSTACLE_CAR_SPEED_MAX = min(25, OBSTACLE_CAR_SPEED_MAX + 0.1)

            # Spawn new obstacles (simple timer based)
            obstacle_spawn_timer += 1
            if obstacle_spawn_timer >= OBSTACLE_SPAWN_RATE and len(obstacles) < 10: # Limit max obstacles
                obstacle = ObstacleCar()
                all_sprites.add(obstacle)
                obstacles.add(obstacle)
                obstacle_spawn_timer = 0

            # Collision detection
            # We need to check collision between player.rect and obstacle.rect
            # Pygame's spritecollide works on the sprite's self.rect
            hits = pygame.sprite.spritecollide(player, obstacles, False, pygame.sprite.collide_rect)
            if hits:
                # For simplicity, we use player.rect and hits[0].rect for visual collision
                # For pixel-perfect, you'd use pygame.sprite.collide_mask if you had masks
                # The player collided with an obstacle. End the game.
                game_over = True


            # Update road lines
            for line in road_lines:
                line.y += ROAD_LINE_SPEED
                if line.top > SCREEN_HEIGHT:
                    line.bottom = 0 # Wrap around

        # --- Drawing ---
        screen.fill(BLACK) # Fill background

        # Draw road lines
        draw_road_lines(screen, road_lines)

        # Draw all sprites (player and obstacles)
        # We draw them individually for the custom draw method
        player.draw(screen)
        for obstacle in obstacles:
            obstacle.draw(screen)

        # Draw score
        draw_text(screen, str(score), FONT_SIZE_SMALL, SCREEN_WIDTH - 50, 10)

        # --- Flip Display ---
        pygame.display.flip()

        # --- Control Game Speed ---
        clock.tick(60) # Limit frame rate to 60 FPS

    pygame.quit()
    sys.exit() # Ensure clean exit

# --- Run the Game ---
show_start_screen()
game_loop()
player_rect_for_collision = pygame.Rect(player.rect.x, player.rect.y, PLAYER_CAR_WIDTH, PLAYER_CAR_HEIGHT)
if player_rect_for_collision.colliderect(hits[0].rect):
    game_over = True