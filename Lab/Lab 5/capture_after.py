"""
Script to run the UPDATED game and capture frames for the after.mp4 video.
The capture script directly runs the game loop and saves frames.
"""
import pygame
import sys
import os
import math
import random

os.environ.setdefault("SDL_VIDEODRIVER", "windows")  # use real display

sys.path.insert(0, r"c:\Users\rehan\Documents\lava")

from game.world import generate_platforms, draw_lava, PLATFORM_COLOR, Platform
from game.player import Player

WIDTH, HEIGHT = 500, 640
FPS = 30
BG = (20, 15, 30)
GROUND_Y = HEIGHT + 200
FRAMES_DIR = r"c:\Users\rehan\Documents\lava\frames_after"
OUTPUT = r"c:\Users\rehan\Documents\lava\after.mp4"
TOTAL_FRAMES = FPS * 14  # 14 seconds

os.makedirs(FRAMES_DIR, exist_ok=True)

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Lava Escape - AFTER")
clock = pygame.time.Clock()
font = pygame.font.SysFont("monospace", 24, bold=True)
small_font = pygame.font.SysFont("monospace", 16, bold=True)
big_font = pygame.font.SysFont("monospace", 42, bold=True)

# Game state
platforms = generate_platforms(WIDTH, GROUND_Y)
player = Player(WIDTH//2-16, GROUND_Y-50)
cam_y = 0
lava_y = GROUND_Y + 60
lava_rise_base = 0.4
score = 0
game_over = False
won = False
top_y = platforms[-1].y
frame_count = 0
saved = 0

SURGE_INTERVAL = 200   # shorter for demo video
SURGE_DURATION = 90
SURGE_MULTIPLIER = 3.0
surge_timer = 0
surge_active = False
surge_frame = 0

running = True
while running and saved < TOTAL_FRAMES:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN and event.key == pygame.K_r:
            platforms = generate_platforms(WIDTH, GROUND_Y)
            player = Player(WIDTH//2-16, GROUND_Y-50)
            cam_y = 0; lava_y = GROUND_Y+60; lava_rise_base = 0.4
            game_over = False; won = False; frame_count = 0
            surge_timer = 0; surge_active = False; surge_frame = 0

    keys = pygame.key.get_pressed()

    if not game_over and not won:
        player.update(keys, platforms, WIDTH)
        target = player.rect.centery - HEIGHT//2
        if target < cam_y:
            cam_y = target

        lava_rise_base = min(1.2, lava_rise_base + 0.0003)
        if surge_active:
            surge_frame += 1
            if surge_frame >= SURGE_DURATION:
                surge_active = False
                surge_frame = 0
                surge_timer = 0
        else:
            surge_timer += 1
            if surge_timer >= SURGE_INTERVAL:
                surge_active = True
                surge_frame = 0

        lava_speed = lava_rise_base * SURGE_MULTIPLIER if surge_active else lava_rise_base
        lava_y -= lava_speed
        score = max(0, (GROUND_Y - player.rect.y)//10)
        frame_count += 1

        for p in platforms:
            p.update()
        platforms = [p for p in platforms if not p.dead]

        if player.rect.bottom >= lava_y:
            game_over = True
        if player.rect.top <= top_y - 20:
            won = True

    # Draw
    screen.fill(BG)
    for p in platforms:
        p.draw(screen, cam_y)
    player.draw(screen, cam_y)
    draw_lava(screen, lava_y, cam_y, WIDTH, HEIGHT, frame_count)
    sc = font.render(f"Height: {score}m  R=Restart", True, (220, 200, 180))
    screen.blit(sc, (8, 10))

    # Danger HUD
    danger = min(1.0, (lava_rise_base - 0.4) / 0.8 * 0.5 + (0.5 if surge_active else 0))
    bar_x = WIDTH - 22; bar_h = 140; bar_y = HEIGHT//2 - bar_h//2; bar_w = 14
    pygame.draw.rect(screen, (50, 30, 30), (bar_x-1, bar_y-1, bar_w+2, bar_h+2), border_radius=4)
    fill_h = int(bar_h * danger)
    if fill_h > 0:
        fill_y = bar_y + (bar_h - fill_h)
        r = int(min(1, danger * 2) * 220)
        g = int(max(0, 1 - danger * 2) * 200)
        pygame.draw.rect(screen, (r, g, 0), (bar_x, fill_y, bar_w, fill_h), border_radius=3)
    pygame.draw.rect(screen, (180, 100, 60), (bar_x-1, bar_y-1, bar_w+2, bar_h+2), 2, border_radius=4)
    lbl = small_font.render("DANGER", True, (180, 120, 80))
    screen.blit(lbl, (bar_x - lbl.get_width()//2 + bar_w//2, bar_y - 20))
    if surge_active:
        pulse = int(abs(math.sin(frame_count * 0.2)) * 200) + 55
        surge_lbl = small_font.render("SURGE!", True, (255, pulse, 0))
        screen.blit(surge_lbl, (bar_x - surge_lbl.get_width()//2 + bar_w//2, bar_y + bar_h + 6))

    if game_over:
        ov = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        ov.fill((0, 0, 0, 150)); screen.blit(ov, (0, 0))
        m = big_font.render("LAVA GOT YOU!", True, (220, 80, 40))
        s = font.render("Press R to Play Again", True, (200, 200, 200))
        screen.blit(m, (WIDTH//2 - m.get_width()//2, HEIGHT//2 - 40))
        screen.blit(s, (WIDTH//2 - s.get_width()//2, HEIGHT//2 + 20))
    if won:
        ov = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        ov.fill((0, 0, 0, 150)); screen.blit(ov, (0, 0))
        m = big_font.render("ESCAPED!", True, (80, 220, 100))
        s = font.render("Press R to Play Again", True, (200, 200, 200))
        screen.blit(m, (WIDTH//2 - m.get_width()//2, HEIGHT//2 - 40))
        screen.blit(s, (WIDTH//2 - s.get_width()//2, HEIGHT//2 + 20))

    pygame.display.flip()

    frame_path = os.path.join(FRAMES_DIR, f"frame_{saved:05d}.bmp")
    pygame.image.save(screen, frame_path)
    saved += 1

    clock.tick(FPS)

pygame.quit()
print(f"Captured {saved} frames")

# Compile with ffmpeg
import subprocess
frames = sorted(f for f in os.listdir(FRAMES_DIR) if f.endswith(".bmp"))
print(f"Compiling {len(frames)} frames to {OUTPUT}...")
result = subprocess.run([
    "ffmpeg", "-y",
    "-framerate", str(FPS),
    "-i", os.path.join(FRAMES_DIR, "frame_%05d.bmp"),
    "-c:v", "libx264",
    "-preset", "fast",
    "-pix_fmt", "yuv420p",
    OUTPUT
], capture_output=True, text=True)
if os.path.exists(OUTPUT):
    print(f"SUCCESS: after.mp4 created ({os.path.getsize(OUTPUT)} bytes)")
else:
    print("ERROR:", result.stderr[-500:])

for f in frames:
    os.remove(os.path.join(FRAMES_DIR, f))
os.rmdir(FRAMES_DIR)
