import pygame
from engine.core import GameObject, Vector2D, Rect2D
from engine.entities import Cat, Berry

class GameUI:
    SCREEN_WIDTH = 800
    SCREEN_HEIGHT = 600
    def __init__(self, player, frame_render_handler):
        pygame.init()
        self.screen = pygame.display.set_mode((GameUI.SCREEN_WIDTH, GameUI.SCREEN_HEIGHT))
        pygame.display.set_caption("Cat and Berries")
        
        self.player = player
        self.game_running = True

        self.cat_image = pygame.image.load("ui/assets/cat.png").convert_alpha()
        self.berry_image = pygame.image.load("ui/assets/berry.png").convert_alpha()

        self.clock = pygame.time.Clock()

        self.frame_render_handler = frame_render_handler
        self.score_font = pygame.font.SysFont("Arial", 16)

        self.screen_rect = Rect2D(
            Vector2D(0, 0), 
            GameUI.SCREEN_WIDTH, 
            GameUI.SCREEN_HEIGHT
        )

    def run(self):
        while self.game_running:
            self.clock.tick(60)
            self.handle_events()
            self.render()
            self.frame_render_handler()
        pygame.quit()

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.game_running = False

        keys = pygame.key.get_pressed()
        direction = Vector2D(0, 0)
        if keys[pygame.K_w]:
            direction = direction + Vector2D.UP
        if keys[pygame.K_s]:
            direction = direction + Vector2D.DOWN
        if keys[pygame.K_a]: 
            direction = direction + Vector2D.LEFT
        if keys[pygame.K_d]:
            direction = direction + Vector2D.RIGHT

        future_hitbox = self.player.hitbox.copy()
        future_hitbox.position += direction * self.player.move_speed
        if self.screen_rect.is_inner_rect(future_hitbox):
            self.player.move_and_collide(direction, self.player.move_speed)


    def render(self):
        self.screen.fill((50, 50, 50))
        for obj in GameObject.GAME_OBJECTS:
            pos = obj.hitbox.position
            if isinstance(obj, Cat):
                self.screen.blit(self.cat_image, (pos.x, pos.y))
            elif isinstance(obj, Berry):
                self.screen.blit(self.berry_image, (pos.x, pos.y))
            else:
                pygame.draw.rect(self.screen, (200, 200, 200),
                                 (pos.x, pos.y, obj.hitbox.width, obj.hitbox.height))
        
        text_surface = self.score_font.render(f"Score: {self.player.collected_points}, Berries Collected: {self.player.collected_berries}", True, (255, 255, 255))
        self.screen.blit(text_surface, (20, 20))  # top-left corner
        pygame.display.flip()
