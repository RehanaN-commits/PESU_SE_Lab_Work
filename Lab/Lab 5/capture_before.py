
import pygame
import sys
import os

sys.path.insert(0, r"c:\Users\rehan\Documents\lava")
from game.game_engine import GameEngine
from game.world import generate_platforms, draw_lava, PLATFORM_COLOR
from game.player import Player

WIDTH, HEIGHT = 500, 640
FPS = 30
BG = (20, 15, 30)
GROUND_Y = HEIGHT + 200
FRAMES_DIR = r"c:\Users\rehan\Documents\lava\frames_before"
TOTAL_FRAMES = FPS * 12

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Lava Escape - BEFORE")
clock = pygame.time.Clock()
font = pygame.font.SysFont("monospace", 24, bold=True)
big_font = pygame.font.SysFont("monospace", 42, bold=True)

platforms = generate_platforms(WIDTH, GROUND_Y)
player = Player(WIDTH//2-16, GROUND_Y-50)
cam_y = 0
lava_y = GROUND_Y + 60
lava_rise = 0.4
score = 0
game_over = False
won = False
top_y = platforms[-1].y
frame_count = 0
saved = 0

running = True
while running and saved < TOTAL_FRAMES:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    keys = pygame.key.get_pressed()
    
    if not game_over and not won:
        player.update(keys, platforms, WIDTH)
        target = player.rect.centery - HEIGHT//2
        if target < cam_y:
            cam_y = target
        lava_y -= lava_rise
        lava_rise = min(1.2, lava_rise + 0.0003)
        score = max(0, (GROUND_Y - player.rect.y)//10)
        frame_count += 1
        if player.rect.bottom >= lava_y:
            game_over = True
        if player.rect.top <= top_y - 20:
            won = True

    # Draw
    screen.fill(BG)
    for p in platforms:
        dr = p.move(0, -int(cam_y))
        pygame.draw.rect(screen, PLATFORM_COLOR, dr, border_radius=4)
    player.draw(screen, cam_y)
    draw_lava(screen, lava_y, cam_y, WIDTH, HEIGHT, frame_count)
    sc = font.render(f"Height: {score}m  R=Restart", True, (220, 200, 180))
    screen.blit(sc, (8, 10))
    
    # Try to demonstrate the bug: player jumping into platform
    pygame.display.flip()
    
    # Save frame
    frame_path = os.path.join(FRAMES_DIR, f"frame_{saved:05d}.bmp")
    pygame.image.save(screen, frame_path)
    saved += 1
    
    clock.tick(FPS)

pygame.quit()
print(f"Captured {saved} frames")
