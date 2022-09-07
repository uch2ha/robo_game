# Complete your game here
import pygame
from sys import exit
import time
import random

BATTLEGROUND_X = 1000
BATTLEGROUND_Y = 1000
CELL = 50  # Cell size 50x50px


class Robot:
    def __init__(self, parent_screen):
        self.parent_screen = parent_screen
        robot_img = pygame.image.load("robot.png").convert()
        self.robot = pygame.transform.scale(  # scale robot img to 50x50px
            robot_img, (CELL, CELL))
        self.x = 300
        self.y = 300
        self.direction = "down"

    def draw(self):
        self.parent_screen.fill((0, 0, 0))
        self.parent_screen.blit(self.robot, (self.x, self.y))
        pygame.display.flip()

    def move_left(self):
        self.direction = "left"

    def move_right(self):
        self.direction = "right"

    def move_up(self):
        self.direction = "up"

    def move_down(self):
        self.direction = "down"

    def walk(self):
        if self.direction == "up":
            if self.y == 0:
                self.direction = random.choice(["down", "right", "left"])
            else:
                self.y -= CELL
        elif self.direction == "right":
            if self.x == BATTLEGROUND_X-CELL:
                self.direction = random.choice(["down", "up", "left"])
            else:
                self.x += CELL
        elif self.direction == "down":
            if self.y == BATTLEGROUND_Y-CELL:
                self.direction = random.choice(["up", "right", "left"])
            else:
                self.y += CELL
        elif self.direction == "left":
            if self.x == 0:
                self.direction = random.choice(["down", "right", "up"])
            else:
                self.x -= CELL
        self.draw()


class Coin:
    def __init__(self, parent_screen):
        self.parent_screen = parent_screen
        coin_img = pygame.image.load("coin.png").convert()
        self.coin = pygame.transform.scale(  # scale robot img to 50x50px
            coin_img, (CELL, CELL))

        self.x = random.randint(0, 19)*CELL
        self.y = random.randint(0, 19)*CELL

    def draw(self):
        self.parent_screen.blit(self.coin, (self.x, self.y))
        pygame.display.flip()

    def move(self):
        self.x = random.randint(0, 19)*CELL
        self.y = random.randint(0, 19)*CELL


class Game:
    def __init__(self):
        pygame.init()

        self.window = pygame.display.set_mode(
            (BATTLEGROUND_X, BATTLEGROUND_Y))
        self.window.fill((0, 0, 0))
        pygame.display.set_caption("robo_game")

        self.robot = Robot(self.window)
        self.robot.draw()
        self.coin = Coin(self.window)
        self.coin.draw()

        self.coins = 0
        self.game_speed = 0.2

        self.main_loop()

    def is_collision(self, x1, y1, x2, y2):
        if x1 >= x2 and x1 <= x2 + CELL-1:      # CELL-1 fixed bug,
            if y1 >= y2 and y1 <= y2 + CELL-1:  # that robot can raise the coin without touching
                return True
        return False

    def main_loop(self):
        while True:
            self.check_events()

    def display_score(self):
        font = pygame.font.SysFont("Arial", 30)
        score = font.render(
            f"Score: {self.coins} / 100", True, (200, 200, 200))
        self.window.blit(score, (800, 10))

    def play(self):
        self.robot.walk()
        self.coin.draw()
        self.display_score()
        pygame.display.flip()

        if self.is_collision(self.robot.x, self.robot.y, self.coin.x, self.coin.y):
            self.coin.move()
            self.coins += 1
            self.game_speed /= 1.1  # increase game speed

    def check_events(self):
        if self.coins == 100:
            font = pygame.font.SysFont("Arial", 75)
            result = font.render(
                "You are Win! 100 Coins!", True, (255, 255, 255))
            self.window.blit(result, (150, 300))
            pygame.display.flip()
            time.sleep(3)
            exit()  # END OF THE GAME
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    exit()
                if event.key == pygame.K_LEFT:
                    self.robot.move_left()
                if event.key == pygame.K_RIGHT:
                    self.robot.move_right()
                if event.key == pygame.K_UP:
                    self.robot.move_up()
                if event.key == pygame.K_DOWN:
                    self.robot.move_down()
            if event.type == pygame.QUIT:
                exit()

        self.play()
        time.sleep(self.game_speed)


if __name__ == "__main__":
    Game()
