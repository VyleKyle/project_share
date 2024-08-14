import pygame
import random
import sys

pygame.init()

# Screen settings
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)

# Parameters
ANT_COUNT = 100
FOOD_COUNT = 50
ANT_SPEED = 1

class Ant:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def move(self):
        self.x += random.randint(-ANT_SPEED, ANT_SPEED)
        self.x = max(0, min(self.x, WIDTH - 1))
        self.y += random.randint(-ANT_SPEED, ANT_SPEED)
        self.y = max(0, min(self.y, HEIGHT - 1))

    def draw(self, screen):
        pygame.draw.rect(screen, WHITE, (self.x, self.y, 1, 1))

class Food:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def draw(self, screen):
        pygame.draw.rect(screen, RED, (self.x, self.y, 1, 1))

def create_ants(count):
    return [Ant(random.randint(0, WIDTH - 1), random.randint(0, HEIGHT - 1)) for _ in range(count)]

def create_food(count):
    return [Food(random.randint(0, WIDTH - 1), random.randint(0, HEIGHT - 1)) for _ in range(count)]

def main():
    ants = create_ants(ANT_COUNT)
    food = create_food(FOOD_COUNT)
    
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        
        screen.fill(BLACK)
        
        for a in ants:
            a.move()
            a.draw(screen)

        for f in food:
            f.draw(screen)
        
        pygame.display.flip()
        pygame.time.wait(50)

if __name__ == '__main__':
    main()

