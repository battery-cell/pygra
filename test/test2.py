import pygame

pygame.init()
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Physics test")

clock = pygame.time.Clock()

# kula
ball = {
    "x": 400,
    "y": 100,
    "vy": 0
}

radius = 20

# fizyka
gravity = 0.5
dragging = False

# powierzchnie (obok siebie + dolna warstwa)
surfaces = [
    {"rect": pygame.Rect(0, 450, 266, 100), "type": "solid"},
    {"rect": pygame.Rect(266, 450, 266, 100), "type": "liquid"},
    {"rect": pygame.Rect(532, 450, 268, 100), "type": "bounce"},
    {"rect": pygame.Rect(0, 550, 800, 50), "type": "bottom"}  # dolna powierzchnia
]

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # klik - złapanie kuli
        if event.type == pygame.MOUSEBUTTONDOWN:
            mx, my = pygame.mouse.get_pos()
            dx = mx - ball["x"]
            dy = my - ball["y"]

            if dx*dx + dy*dy <= radius*radius:
                dragging = True

        # puszczenie
        if event.type == pygame.MOUSEBUTTONUP:
            dragging = False

    # przeciąganie
    if dragging:
        mx, my = pygame.mouse.get_pos()
        ball["x"] = mx
        ball["y"] = my
        ball["vy"] = 0
    else:
        # grawitacja
        ball["vy"] += gravity
        ball["y"] += ball["vy"]

    ball_rect = pygame.Rect(ball["x"] - radius, ball["y"] - radius, radius*2, radius*2)

    # kolizje
    for s in surfaces:
        if ball_rect.colliderect(s["rect"]):

            # klasyczne zatrzymanie
            if s["type"] in ["solid", "bottom"]:
                ball["y"] = s["rect"].top - radius
                ball["vy"] = 0

            elif s["type"] == "liquid":
                ball["vy"] *= 0.9  # spowolnienie

            elif s["type"] == "bounce":
                ball["y"] = s["rect"].top - radius
                ball["vy"] = -ball["vy"] * 0.8

    # rysowanie
    screen.fill((30, 30, 30))

    for s in surfaces:
        if s["type"] == "solid":
            color = (150, 100, 50)
        elif s["type"] == "liquid":
            color = (50, 100, 200)
        elif s["type"] == "bounce":
            color = (50, 200, 100)
        elif s["type"] == "bottom":
            color = (100, 100, 100)

        pygame.draw.rect(screen, color, s["rect"])

    pygame.draw.circle(screen, (255, 255, 255), (int(ball["x"]), int(ball["y"])), radius)

    pygame.display.update()
    clock.tick(60)

pygame.quit()