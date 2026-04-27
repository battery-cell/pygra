import pygame

pygame.init()
pygame.mixer.init()

screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Objects test")

pygame.mixer.music.load("testbg.ogg")
pygame.mixer.music.play(-1)

clock = pygame.time.Clock()
font = pygame.font.SysFont(None, 30)

colors = [(255, 0, 0), (0, 255, 0), (0, 0, 255)]
color_index = 0

menu_colors = [(200, 0, 0), (0, 200, 0), (0, 0, 200)]
menu_color_index = 0

menu_open = False
rect_visible = True  # kwadrat przy myszce

objects = []  # [x, y, color_index]

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:

            if event.key == pygame.K_SPACE:
                color_index = (color_index + 1) % len(colors)

            if event.key == pygame.K_ESCAPE:
                menu_open = not menu_open
                if menu_open:
                    menu_color_index = (color_index + 1) % len(menu_colors)

            if event.key == pygame.K_q:
                next_color = len(objects) % len(colors)
                objects.append([400, 300, next_color])

            if event.key == pygame.K_BACKSPACE:
                objects.clear()

            if event.key in (pygame.K_LSHIFT, pygame.K_RSHIFT):
                if menu_open:
                    menu_color_index = (menu_color_index + 1) % len(menu_colors)

        if event.type == pygame.MOUSEBUTTONDOWN:
            rect_visible = not rect_visible

    # ruch ostatniego obiektu
    keys = pygame.key.get_pressed()
    if objects:
        if keys[pygame.K_LEFT]:
            objects[-1][0] -= 5
        if keys[pygame.K_RIGHT]:
            objects[-1][0] += 5
        if keys[pygame.K_UP]:
            objects[-1][1] -= 5
        if keys[pygame.K_DOWN]:
            objects[-1][1] += 5

    # tło
    screen.fill(colors[color_index])

    # kule
    for obj in objects:
        pygame.draw.circle(
            screen,
            colors[obj[2]],
            (obj[0], obj[1]),
            20
        )

    # --- PROSTOKĄT ZA MYSZĄ ---
    mouse_x, mouse_y = pygame.mouse.get_pos()

    mouse_rect = pygame.Rect(mouse_x - 20, mouse_y - 20, 40, 40)

    if rect_visible:
        pygame.draw.rect(screen, (255, 255, 255), mouse_rect)

    # --- TRIGGER PROSTOKĄT ---
    trigger_rect = pygame.Rect(300, 200, 200, 150)
    pygame.draw.rect(screen, (100, 100, 100), trigger_rect, 2)

    # jeśli kolizja → ukryj kwadrat
    if rect_visible and mouse_rect.colliderect(trigger_rect):
        rect_visible = False

    # menu
    if menu_open:
        pygame.draw.rect(
            screen,
            menu_colors[menu_color_index],
            (200, 150, 400, 300)
        )

    # FPS
    fps = clock.get_fps()
    fps_text = font.render(f"FPS: {int(fps)}", True, (255, 255, 255))
    screen.blit(fps_text, (10, 10))

    pygame.display.update()
    clock.tick(60)

pygame.quit()