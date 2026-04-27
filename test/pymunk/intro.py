import pymunk
import pymunk.pygame_util
import pygame

GRAY = (220, 220, 220)
space = pymunk.Space()
space.gravity = (0, 900)
b0 = space.static_body

class App:
    size = 1024, 768
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode(self.size)
        self.draw_options = pymunk.pygame_util.DrawOptions(self.screen)
        self.draw_options.flip_y = True
        self.running = True
        self.dragged_body = None
        self.mouse_body = pymunk.Body(body_type=pymunk.Body.KINEMATIC)
        self.mouse_joint = None
        self.clock = pygame.time.Clock()


    def run(self):
        while self.running:
            mouse_pos = pygame.mouse.get_pos()
            p = pymunk.pygame_util.from_pygame(mouse_pos, self.screen)
            self.mouse_body.position = p  # THIS is what makes it feel physical
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                    pygame.image.save(self.screen, 'intro.png')
                if event.type == pygame.MOUSEBUTTONDOWN:
                    hit = space.point_query_nearest(p, 50, pymunk.ShapeFilter())
                    if hit and hit.shape.body.body_type == pymunk.Body.DYNAMIC:
                        self.dragged_body = hit.shape.body
                        self.mouse_joint = pymunk.PivotJoint(
                            self.mouse_body,
                            self.dragged_body,
                            (0, 0),
                            self.dragged_body.world_to_local(p)
                        )
                        self.mouse_joint.max_force = 50000
                        self.mouse_joint.error_bias = (1 - 0.15) ** 60  # makes it “soft”
                        space.add(self.mouse_joint)
                if event.type == pygame.MOUSEBUTTONUP:
                    if self.mouse_joint:
                        space.remove(self.mouse_joint)
                        self.mouse_joint = None
                        self.dragged_body = None
            self.screen.fill(GRAY)
            space.debug_draw(self.draw_options)
            pygame.display.update()
            space.step(1/60)
            dt = self.clock.tick(60) / 1000.0
            space.step(dt)
        pygame.quit()


def add_boundaries(space, width, height, thickness=5):
    static_body = space.static_body

    walls = [
        pymunk.Segment(static_body, (0, height), (width, height), thickness),
        pymunk.Segment(static_body, (0, 0), (width, 0), thickness),
        pymunk.Segment(static_body, (0, 0), (0, height), thickness),
        pymunk.Segment(static_body, (width, 0), (width, height), thickness),
    ]

    for wall in walls:
        wall.elasticity = 0.9
        wall.friction = 1.0

    space.add(*walls)

if __name__ == '__main__':
    p0, p1 = (0, 230), (700, 230)
    segment = pymunk.Segment(b0, p0, p1, 4)
    segment.elasticity = 1
    body = pymunk.Body(mass=1, moment=float('inf'))
    body.position = (100, 100)
    box = pymunk.Poly.create_box(body, (50,50))
    box.elasticity = 0.01
    box.friction=1.0
    space.add(body, box, segment)
    body.angular_velocity = 0
    body.angular_velocity_limit = 0
    body.angular_damping = 0.999
    add_boundaries(space, 700, 240)
    
    App().run()