import pygame
import random
from pygame.locals import *

class ScoreTracker:
    def __init__(self):
        self.score = 0

    def increase_score(self):
        self.score += 1

    def reset_score(self):
        self.score = 0

    def get_score(self):
        return self.score


score_tracker = ScoreTracker()
score_tracker.increase_score()
print("Current score:", score_tracker.get_score())


class Game:
    def display_score(self):
        font = pygame.font.Font(None, 36)
        text = font.render(f"Score: {self.score}", True, (255, 255, 255))
        self.surface.blit(text, (10, 10))

    def __init__(self):
        pygame.init()
        self.window_width = 800
        self.window_height = 600
        self.surface = pygame.display.set_mode((self.window_width, self.window_height))
        self.surface.fill((110, 110, 5))

        self.clock = pygame.time.Clock()
        self.block_size = 20
        self.block = pygame.Surface((self.block_size, self.block_size))
        self.block.fill((255, 255, 255))

        self.snake = [(200, 200), (180, 200), (160, 200)]
        self.direction = 'RIGHT'

        self.apple_size = 20
        self.apple_pos = (300, 300)
        self.apple = pygame.Surface((self.apple_size, self.apple_size))
        self.apple.fill((255, 0, 0))

        self.score = 0
        self.score_tracker = ScoreTracker()

    def draw_snake(self):
        for pos in self.snake:
            self.surface.blit(self.block, pos)

    def draw_apple(self):
        self.surface.blit(self.apple, self.apple_pos)

    def collision_with_apple(self):
        return self.snake[0] == self.apple_pos

    def collision_with_boundaries(self):
        return (
            self.snake[0][0] in [0, self.window_width - self.block_size]
            or self.snake[0][1] in [0, self.window_height - self.block_size]
        )

    def collision_with_self(self):
        return any(self.snake[0] == block for block in self.snake[1:])

    def change_direction(self, new_direction):
        if new_direction == 'RIGHT' and not self.direction == 'LEFT':
            self.direction = 'RIGHT'
        elif new_direction == 'LEFT' and not self.direction == 'RIGHT':
            self.direction = 'LEFT'
        elif new_direction == 'UP' and not self.direction == 'DOWN':
            self.direction = 'UP'
        elif new_direction == 'DOWN' and not self.direction == 'UP':
            self.direction = 'DOWN'

    def move(self):
        if self.direction == 'RIGHT':
            self.snake.insert(0, (self.snake[0][0] + self.block_size, self.snake[0][1]))
        if self.direction == 'LEFT':
            self.snake.insert(0, (self.snake[0][0] - self.block_size, self.snake[0][1]))
        if self.direction == 'UP':
            self.snake.insert(0, (self.snake[0][0], self.snake[0][1] - self.block_size))
        if self.direction == 'DOWN':
            self.snake.insert(0, (self.snake[0][0], self.snake[0][1] + self.block_size))

        if not self.collision_with_apple():
            self.snake.pop()

    def run(self):
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == QUIT:
                    running = False
                elif event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        running = False
                    elif event.key == K_UP:
                        self.change_direction('UP')
                    elif event.key == K_DOWN:
                        self.change_direction('DOWN')
                    elif event.key == K_LEFT:
                        self.change_direction('LEFT')
                    elif event.key == K_RIGHT:
                        self.change_direction('RIGHT')

            for x in range(0, self.window_width, self.block_size):
                for y in range(0, self.window_height, self.block_size):
                    if (x + y) % (2 * self.block_size) == 0:
                        pygame.draw.rect(self.surface, (50, 50, 50), (x, y, self.block_size, self.block_size))
                    else:
                        pygame.draw.rect(self.surface, (70, 70, 70), (x, y, self.block_size, self.block_size))

            self.draw_snake()
            self.draw_apple()
            self.display_score()
            pygame.display.update()

            if self.collision_with_apple():
                self.score += 1
                self.apple_pos = (random.randrange(1, self.window_width // self.block_size) * self.block_size,
                                  random.randrange(1, self.window_height // self.block_size) * self.block_size)
                if self.collision_with_apple():
                    self.score_tracker.increase_score()

            self.move()

            if self.collision_with_boundaries() or self.collision_with_self():
                running = False

            self.clock.tick(15)

        pygame.quit()

if __name__ == "__main__":
    game = Game()
    game.run()
