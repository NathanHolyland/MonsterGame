from random import randint
from pathfinding import aStar
from mazeGenerator import mazeGenerator
import time
import pygame

class Entity:
    def __init__(self, x, y, colour, alive):
        self.x = x
        self.y = y
        self.colour = colour
        self.alive = alive

    def move(self, vec):
        self.x += vec[0]
        self.y += vec[1]

    def draw(self, screen, res):
        pygame.draw.rect(screen, self.colour, [(self.x*res[1]/21), self.y*res[1]/21, res[1]/21, res[1]/21], 4)


class Object:
    def __init__(self, x, y, colour):
        self.x = x
        self.y = y
        self.colour = colour

    def draw(self, screen, res, fill):
        if fill:
            pygame.draw.rect(screen, self.colour, [(self.x*res[1]/21), self.y*res[1]/21, res[1]/21, res[1]/21], 0)
        else:
            pygame.draw.rect(screen, self.colour, [(self.x*res[1]/21), self.y*res[1]/21, res[1]/21, res[1]/21], 4)
        


def generateObjects(noTraps, noCoins):
    coins = []
    traps = []
    walls = []
    maze = mazeGenerator(21, 21)
    for row in range(len(maze)):
        for column in range(len(maze[row])):
            if maze[row][column] == "1":
                new_wall = Object(column, row, (255, 255, 255))
                walls.append(new_wall)
    
    for i in range(noCoins):
        repeat = True
        while repeat:
            x = randint(0, 21)
            y = randint(0, 21)
            repeat = False
            for coin in coins:
                if ([x, y] == [coin.x, coin.y]):
                    repeat = True
            for wall in walls:
                if ([x, y] == [wall.x, wall.y]):
                    repeat = True
            if not repeat:
                newCoin = Object(x, y, (255, 255, 0))
                coins.append(newCoin)

    for i in range(noTraps):
        repeat = True
        while repeat:
            x = randint(0, 21)
            y = randint(0, 21)
            repeat = False
            for coin in coins:
                if ([x, y] == [coin.x, coin.y]):
                    repeat = True
            for trap in traps:
                if ([x, y] == [trap.x, trap.y]):
                    repeat = True
            for wall in walls:
                if ([x, y] == [wall.x, wall.y]):
                    repeat = True
            if not repeat:
                newTrap = Object(x, y, (100, 0, 0))
                traps.append(newTrap)

    return coins, traps, walls, maze

def generateMonster(walls, coins, traps, player):
    repeat = True
    while repeat:
        x = randint(0, 21)
        y = randint(0, 21)
        repeat = False
        for coin in coins:
            if ([x, y] == [coin.x, coin.y]):
               repeat = True
        for wall in walls:
            if ([x, y] == [wall.x, wall.y]):
                repeat = True
        for trap in traps:
            if ([x, y]) == [trap.x, trap.y]:
                repeat = True
        if ([x, y] == [player.x, player.y]):
            repeat = True
        if not repeat:
            monster = Entity(x, y, (255, 0, 0), False)
            return monster


def collisions(player, monster, coins, traps, money):
    # very simplified, since coordinates are on a very static grid
    collisions = {
        "coins": [],
        "traps": []
    }
    for coin in coins:
        if ([player.x, player.y] == [coin.x, coin.y]):
            collisions["coins"].append(coin)
    for trap in traps:
        if ([player.x, player.y] == [trap.x, trap.y]):
            collisions["traps"].append(trap)
    if ([player.x, player.y] == [monster.x, monster.y]):
        player.alive = False
    
    for trap in collisions["traps"]:
        traps.remove(trap)
        monster.alive = True
    return collisions

def wallCollide(player, step, walls):
    new_coord = [player.x+step[0],player.y+step[1]]
    valid = True
    for wall in walls:
        if [wall.x, wall.y] == new_coord:
            valid = False
    return valid

def monsterStep(player, monster, maze):
    path = aStar([monster.x, monster.y], [player.x, player.y], maze)
    return path[1]
    
def draw(screen, res, player, monster, coins, walls, traps):
    for trap in traps:
        trap.draw(screen, res, False)
    for coin in coins:
        coin.draw(screen, res, False)
    for wall in walls:
        wall.draw(screen, res, True)
    player.draw(screen, res)
    monster.draw(screen, res)


resolution = [500, 500]
screen = pygame.display.set_mode(resolution)

player = Entity(1, 1, (0, 0, 255), True)
coins, traps, walls, maze = generateObjects(4, 10)
monster = generateMonster(walls, coins, traps, player)

money = 0

running = True
while running:
    screen.fill((0, 0, 0))
    draw(screen, resolution, player, monster, coins, walls, traps)
    pygame.display.flip()

    collided = collisions(player, monster, coins, traps, money)
    
    for coin in collided["coins"]:
        coins.remove(coin)
        money += 1

    print(money)
    if money > 6:
        running = False
        screen.fill((0, 255, 0))
        pygame.display.flip()
        time.sleep(1)

    if player.alive == False:
        running = False
        screen.fill((255, 0, 0))
        pygame.display.flip()
        time.sleep(1)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            step = [0, 0]
            if event.key == pygame.K_w:
                if player.y > 0:
                    step = [0, -1]
            if event.key == pygame.K_s:
                if player.y < 21:
                    step = [0, 1]
            if event.key == pygame.K_d:
                if player.x < 21:
                    step = [1, 0]
            if event.key == pygame.K_a:
                if player.x > 0:
                    step = [-1, 0]
            if monster.alive:
                mStep = monsterStep(player, monster, maze)
                monster.x = mStep[0]
                monster.y = mStep[1]
            if wallCollide(player, step, walls):
                player.move(step)
pygame.quit()
