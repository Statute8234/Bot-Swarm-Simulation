import pygame
import random, sys, math, time
import numpy as np
from sklearn.linear_model import LogisticRegression

pygame.init()
current_time = time.time()
random.seed(current_time)
# Seting up the display
screenWidth, screenHeight = 700, 700
screen = pygame.display.set_mode((screenWidth, screenHeight), pygame.RESIZABLE)
pygame.display.set_caption("Evolution")
clock = pygame.time.Clock()
# color
def random_color():
    return (random.randint(0,255),random.randint(0,255),random.randint(0,255))
colors = {
    "RED": (255, 0, 0),
    "GREEN": (0, 255, 0),
    "BLUE": (0, 0, 255),
    "WHITE": (255, 255, 255),
    "BLACK": (0, 0, 0),
    "GOLD": (255,215,0)
}

"""
Convert bot.dataMatrix to be compatible with other_bot.dataMatrix
based on the bot_type.
"""
def convert_data_matrix(bot, other_bot):
    converted_data = []
    for point, label in bot.dataMatrix:
        if bot.bot_type != other_bot.bot_type:
            # Conversion logic if bot types are different
            if label == 2:
                label = 0  # Convert 'good' (2) to 'bad' (0) for the other type
            elif label == 0:
                label = 2  # Convert 'bad' (0) to 'good' (2) for the other type
        converted_data.append((point, label))
    return converted_data

all_sprites = pygame.sprite.Group()
# bots
class BotCircle(pygame.sprite.Sprite):
    def __init__(self, radius, color):
        super().__init__()
        self.radius = radius
        self.color = color
        self.image = pygame.Surface((2 * radius, 2 * radius), pygame.SRCALPHA)
        self.rect = self.image.get_rect()
        Dx, Dy = random.randint(self.radius,screenWidth -  self.radius),random.randint(self.radius,screenHeight - self.radius)
        self.dataMatrix = [((Dx, Dy), 2), ((Dx // 2, Dy // 2), 0), ((Dx // 4, Dy // 4), 1)]
        self.newPoint = (0, 0)
        self.direction = (1, 0)
        self.draw_shape()
        self.changePosition()
        self.bot_type = random.choice(["meat","plant","star"])

    def draw_shape(self):
        pygame.draw.circle(self.image, self.color, (self.radius, self.radius), self.radius)
        pygame.draw.circle(self.image, colors["WHITE"], (self.radius, self.radius), self.radius, 3)
        self.rect = self.image.get_rect()
    
    def changePosition(self):
        X = np.array([point for point, label in self.dataMatrix])
        y = np.array([label for point, label in self.dataMatrix])
        model = LogisticRegression(multi_class='multinomial', solver='lbfgs', max_iter=5000)
        model.fit(X, y)

        # Generate multiple points and check probabilities
        probability_data = -1
        while probability_data < 0:
            Nx, Ny = random.randint(self.radius, screenWidth - self.radius), random.randint(self.radius, screenHeight - self.radius)
            new_point = np.array([[Nx, Ny]])
            probability = model.predict_proba(new_point)
            # Consider 'Good' (2) as the positive class
            probability_data = probability[0][model.classes_ == 2]
        self.newPoint = (Nx, Ny)

    def move(self):
        self.speed = 1
        if self.rect.center != self.newPoint:
            if self.rect.centerx < self.newPoint[0]:
                self.rect.centerx += self.speed
                self.direction = (1, 0)  # Moving right
            elif self.rect.centerx > self.newPoint[0]:
                self.rect.centerx -= self.speed
                self.direction = (-1, 0)  # Moving left

            if self.rect.centery < self.newPoint[1]:
                self.rect.centery += self.speed
                self.direction = (0, 1)  # Moving down
            elif self.rect.centery > self.newPoint[1]:
                self.rect.centery -= self.speed
                self.direction = (0, -1)  # Moving up
        else:
            self.changePosition()

        # Draw and detect line in front of the circle
        line_end = (self.rect.centerx + 10 * self.direction[0], self.rect.centery + 10 * self.direction[1])
        pygame.draw.line(self.image, colors["WHITE"], self.rect.center, line_end, 2)

        # Check for collision with food
        self.detect_food(line_end)
    
    def detect_food(self, line_end):
        for food in food_list:
            # Create a rectangle around the food
            food_rect = pygame.Rect(food.rect.x, food.rect.y, food.radius * 2, food.radius * 2)
            # Create a line segment representing the extended line
            line_segment = pygame.draw.line(self.image, colors["WHITE"], self.rect.center, line_end, 2)
            # Check if the line intersects with the food
            if pygame.draw.line(self.image, colors["WHITE"], self.rect.center, line_end, 2).colliderect(food_rect):
                # Add detected color to the dataMatrix
                if food.color == colors["RED"] and self.bot_type == "meat":
                    color_label = 2
                elif food.color == colors["GREEN"] and self.bot_type == "plant":
                    color_label = 2
                elif food.color == colors["GOLD"] and self.bot_type == "star":
                    color_label = 2
                else:
                    color_label = 0  # Treat all other colors as "bad"
                self.dataMatrix.append([(self.rect.center), color_label])
                
bot_list = pygame.sprite.Group()
def add_bots(amount, generation_dataMatrix = None):
    for _ in range(amount):
        bot = BotCircle(10,random_color())
        bot.rect.center = (random.randint(10,screenWidth -  10),random.randint(10,screenHeight - 10))
        if generation_dataMatrix is not None:
            bot.dataMatrix += convert_data_matrix(bot, generation_dataMatrix)
        bot_list.add(bot)
add_bots(10)

#food
class FoodCircle(pygame.sprite.Sprite):
    def __init__(self, radius, color):
        super().__init__()
        self.radius = radius
        self.color = color
        self.image = pygame.Surface((2 * radius, 2 * radius), pygame.SRCALPHA)
        self.rect = self.image.get_rect()
        self.dataMatrix = [[(0, 0), 2], [(0, 1), 0]]
        self.newPoint = (0, 0)
        self.draw_shape()
        self.changePosition()

    def draw_shape(self):
        pygame.draw.circle(self.image, self.color, (self.radius, self.radius), self.radius)
        pygame.draw.circle(self.image, colors["WHITE"], (self.radius, self.radius), self.radius, 3)
        self.rect = self.image.get_rect()
    
    def changePosition(self):
        Nx, Ny = random.randint(self.radius, screenWidth - self.radius), random.randint(self.radius, screenHeight - self.radius)
        self.rect.center = Nx, Ny
food_list = pygame.sprite.Group()
def add_food(amount):
    for _ in range(amount):
        food = FoodCircle(10,random.choice([colors['RED'],colors['GREEN'],colors['GOLD']]))
        if food.color == colors['RED']:
            food.rect.center = (random.randint(10,345),random.randint(10,screenHeight - 10))
        elif food.color == colors['GREEN']:
            food.rect.center = (random.randint(345,700 - 10),random.randint(10,screenHeight - 10))
        else:
            food.rect.center = (random.randint(10,screenWidth - 10),random.randint(10,screenHeight - 10))
        food_list.add(food)
add_food(20)
all_sprites.add(bot_list, food_list)

# main
def main():
    global screen, generation_dataMatrix
    running = True
    time = 0
    while running:
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                running = False
                sys.exit()
            elif event.type == pygame.VIDEORESIZE:
                screen = pygame.display.set_mode((event.w, event.h), pygame.RESIZABLE)
        screen.fill(colors["BLACK"])
        all_sprites.update()
        all_sprites.draw(screen)

        # update bots
        for bot in bot_list:
            bot.move()
            # get food
            hit_collider = pygame.sprite.groupcollide(bot_list, food_list, False, True)
            for food in hit_collider:
                if food.color == colors["RED"] and bot.bot_type == "meat":
                    bot.dataMatrix.append([(bot.rect.center), 2])
                # Check plant
                elif food.color == colors["GREEN"] and bot.bot_type == "plant":
                    bot.dataMatrix.append([(bot.rect.center), 2])
                elif food.color == colors["GOLD"] and bot.bot_type == "star" or bot.bot_type == "plant" or bot.bot_type == "meat":
                    for _ in range(3):
                        bot.dataMatrix.append([(bot.rect.center), 2])
                else:
                    bot.dataMatrix.append([(bot.rect.center), 0])
            else:
                bot.dataMatrix.append([(bot.rect.center), 1])
            # collide with other bots
            remove_bots = pygame.sprite.spritecollide(bot, bot_list, False)
            for other_bot in remove_bots:
                if other_bot != bot:
                    converted_data = convert_data_matrix(bot, other_bot)
                    other_bot.dataMatrix += converted_data
                    bot.kill()
        # Adding more food to the scene
        time += 1
        if time % 1000 == 0:
            add_food(20)
            all_sprites.add(food_list)

        if (len(bot_list) <= 2):
            for bot in bot_list:
                add_bots(5, bot)
            all_sprites.add(bot_list)
        # This is to update the scene
        clock.tick(64)
        pygame.display.flip()
        pygame.display.update()

# loop
if __name__ == "__main__":
    main()
