import pygame
import random, sys, math
pygame.init()
# Set up the display
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()
# color
def BLEND_COLORS(color1, color2):
    r1, g1, b1 = color1
    r2, g2, b2 = color2
    blended_r = (r1 + r2) // 2
    blended_g = (g1 + g2) // 2
    blended_b = (b1 + b2) // 2
    return (blended_r, blended_g, blended_b)
def RANDOM_COLOR():
    return (random.randint(0,255),random.randint(0,255),random.randint(0,255))
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
WHITE = (255, 255, 255)
BLACK = (0,0,0)
# generate a circle
class circle(pygame.sprite.Sprite):
    def __init__(self, radius, color):
        super().__init__()
        self.radius = radius
        self.color = color
        self.image = pygame.Surface((2 * radius, 2 * radius), pygame.SRCALPHA)
        self.rect = self.image.get_rect()
        self.draw_shape()
        self.speed = 1
        self.newPoint = (random.randint(0,WIDTH - (radius * 2)), random.randint(0,HEIGHT - (radius * 2)))
        self.pointsList = []
        self.memory(self.newPoint)

    def draw_shape(self):
        pygame.draw.circle(self.image, self.color, (self.radius, self.radius), self.radius)
        pygame.draw.circle(self.image, WHITE, (self.radius, self.radius), self.radius, 3)
        self.rect = self.image.get_rect()
        
    def memory(self, point):
        if point not in self.pointsList:
            self.pointsList.append(point)
            return True
        else:
            return False
        
    def move_towards_food(self):
        # move
        if self.rect.x != self.newPoint[0] and self.rect.x != self.newPoint[1]:
            if self.rect.y < self.newPoint[1]:
                self.rect.y += 1
            elif self.rect.y > self.newPoint[1]:
                self.rect.y -= 1
            if self.rect.x < self.newPoint[0]:
                self.rect.x += 1
            elif self.rect.x > self.newPoint[0]:
                self.rect.x -= 1
        else:
            while not(self.memory(self.newPoint)):
                self.newPoint = (random.randint(0,WIDTH - (self.radius * 2)), random.randint(0,HEIGHT - (self.radius * 2)))
# add
food_list = pygame.sprite.Group()
def addFood(amount):
    for _ in range(amount):
        food = circle(5,WHITE)
        food.rect.topleft = (random.randint(0,WIDTH - 10),random.randint(0,HEIGHT - 10))
        food_list.add(food)

bot_list = pygame.sprite.Group()
def addBots(amount, memory = None, colors = None):
    for _ in range(amount):
        if colors:
            color = BLEND_COLORS(colors[0],colors[1])
            memory = memory
        else:
            color = RANDOM_COLOR()
            memory = []
        bot = circle(10,RANDOM_COLOR())
        bot.rect.topleft = (random.randint(0,WIDTH - 20),random.randint(0,HEIGHT - 20))
        bot.pointsList = memory
        bot_list.add(bot)
addFood(100)
addBots(2)
all_sprites = pygame.sprite.Group()
all_sprites.add(bot_list, food_list)
time = 0
# loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            sys.exit()
    screen.fill(BLACK)
    all_sprites.update()
    all_sprites.draw(screen)
    # move
    for bot in bot_list:
        bot.move_towards_food()
        # collide with food
        hit_list = pygame.sprite.spritecollide(bot, food_list, True)
        for collider in hit_list:
            all_sprites.remove(collider)
        # repopulate
        repopulate = pygame.sprite.spritecollide(bot, bot_list, False)
        for other_bot in repopulate:
            if other_bot != bot:
                if random.randint(0,10 * len(bot_list)) == 0:
                    addBots(1, bot.pointsList + other_bot.pointsList, (bot.color, other_bot.color))
                    all_sprites.add(bot_list)
                if random.randint(0,10 * len(bot_list)) == 100:
                    all_sprites.remove(other_bot)
    # add more food
    time += 1
    if time % 1000 == 0:
        addFood(100)
        all_sprites.add(food_list)
    # update
    clock.tick(64)
    pygame.display.flip()
    pygame.display.update()