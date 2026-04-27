import pymunk
import pygame
import pymunk.pygame_util

pygame.init()
GRAY = (128, 128, 128)
size = 640, 240
screen = pygame.display.set_mode(size)
draw_options = pymunk.pygame_util.DrawOptions(screen)

space = pymunk.Space()
space.gravity = 0, -900

b0 = space.static_body
segment = pymunk.Segment(b0, (0, 0), (640, 0), 4)
segment.elasticity = 1

body = pymunk.Body(mass=1, moment=10)
body.position = 100, 200

circle = pymunk.Circle(body, radius=20)
circle.elasticity = 0.95

space.add(body, circle, segment)

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    screen.fill(GRAY)
    space.debug_draw(draw_options)
    pygame.display.update()
    space.step(0.01)

pygame.quit()