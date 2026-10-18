import pygame
import math
import sys

# Initialize Pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 640, 480
FPS = 60

# Set up display
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Mini Doom - Pygame Raycaster")
clock = pygame.time.Clock()

# Map Grid (1 = Wall, 0 = Empty space)
MAP = [
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 0, 1, 1, 0, 1, 1, 0, 0, 1],
    [1, 0, 1, 0, 0, 0, 1, 0, 0, 1],
    [1, 0, 0, 0, 1, 0, 0, 0, 0, 1],
    [1, 0, 1, 0, 1, 0, 1, 1, 0, 1],
    [1, 0, 1, 1, 1, 0, 1, 1, 0, 1],
    [1, 0, 0, 0, 0, 0, 0, 0, 0, 1],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
]

TILE_SIZE = 64

# Player attributes (Fixed spawn point inside an open corridor at row 1, col 1)
player_x = 96.0
player_y = 96.0
player_angle = 0.0
player_speed = 3.0
rot_speed = 0.04

# Raycasting Settings
FOV = math.pi / 3  # 60 degrees field of view
HALF_FOV = FOV / 2
NUM_RAYS = 120     # Resolution of the 3D projection
DELTA_ANGLE = FOV / NUM_RAYS
MAX_DEPTH = 800

def draw_weapon():
    # Draw a simple retro gun barrel at the bottom center of the screen
    gun_color = (00, 00, 00)
    accent_color = (255, 255, 255)
    
    # Gun body base
    base_rect = pygame.Rect(WIDTH // 2 - 40, HEIGHT - 120, 80, 120)
    pygame.draw.rect(screen, gun_color, base_rect)
    
    # Barrel/Sight detail
    barrel_rect = pygame.Rect(WIDTH // 2 - 15, HEIGHT - 180, 30, 80)
    pygame.draw.rect(screen, gun_color, barrel_rect)
    
    # Muzzle accent
    accent_rect = pygame.Rect(WIDTH // 2 - 10, HEIGHT - 190, 20, 20)
    pygame.draw.rect(screen, accent_color, accent_rect)

# Main Game Loop
while True:
    # 1. Event Handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    # Continuous movement controls
    keys = pygame.key.get_pressed()
    sin_a = math.sin(player_angle)
    cos_a = math.cos(player_angle)

    dx, dy = 0, 0
    if keys[pygame.K_w] or keys[pygame.K_UP]:
        dx += player_speed * cos_a
        dy += player_speed * sin_a
    if keys[pygame.K_s] or keys[pygame.K_DOWN]:
        dx -= player_speed * cos_a
        dy -= player_speed * sin_a
    if keys[pygame.K_a]:
        dx += player_speed * sin_a
        dy -= player_speed * cos_a
    if keys[pygame.K_d]:
        dx -= player_speed * sin_a
        dy += player_speed * cos_a

    # Wall collision check for player movement
    next_x = int((player_x + dx) / TILE_SIZE)
    next_y = int((player_y + dy) / TILE_SIZE)
    if MAP[int(player_y / TILE_SIZE)][next_x] == 0:
        player_x += dx
    if MAP[next_y][int(player_x / TILE_SIZE)] == 0:
        player_y += dy

    # Rotation controls
    if keys[pygame.K_LEFT]:
        player_angle -= rot_speed
    if keys[pygame.K_RIGHT]:
        player_angle += rot_speed

    # Keep angle bounded within 0 to 2*pi
    player_angle %= 2 * math.pi

    # 2. Drawing Scene
    screen.fill((40, 40, 40), (0, 0, WIDTH, HEIGHT // 2))       # Ceiling
    screen.fill((80, 80, 80), (0, HEIGHT // 2, WIDTH, HEIGHT // 2))  # Floor

    # 3. Raycasting Engine Core Loop
    ray_angle = player_angle - HALF_FOV
    col_width = WIDTH / NUM_RAYS

    for ray in range(NUM_RAYS):
        sin_ray = math.sin(ray_angle)
        cos_ray = math.cos(ray_angle)

        depth = 0
        while depth < MAX_DEPTH:
            target_x = player_x + depth * cos_ray
            target_y = player_y + depth * sin_ray
            
            grid_x = int(target_x / TILE_SIZE)
            grid_y = int(target_y / TILE_SIZE)

            if grid_x < 0 or grid_x >= len(MAP[0]) or grid_y < 0 or grid_y >= len(MAP):
                break
            if MAP[grid_y][grid_x] == 1:
                # Fix fish-eye lens distortion effect
                depth *= math.cos(player_angle - ray_angle)
                
                proj_height = min(int((TILE_SIZE / (depth + 0.0001)) * 400), HEIGHT * 2)
                
                color_factor = max(255 - int(depth * 0.3), 30)
                wall_color = (color_factor, color_factor // 4, color_factor // 4)
                
                x_pos = ray * col_width
                y_pos = (HEIGHT // 2) - (proj_height // 2)
                pygame.draw.rect(screen, wall_color, (x_pos, y_pos, col_width + 1, proj_height))
                break

            depth += 4

        ray_angle += DELTA_ANGLE

    # 4. Draw HUD / Weapon overlay
    draw_weapon()

    pygame.display.flip()
    clock.tick(FPS)