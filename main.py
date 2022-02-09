from random import randint
from pathfinding import aStar
import pygame
# test


class Object:
    def __init__(self, coord, oType):
        self.oType = oType
        self.coord = coord


class Text:
    def __init__(self, txt, rect, color):
        self.text = txt
        self.rect = rect
        self.color = color
        surface = font.render(txt, False, color)
        scr.blit(surface, (rect[0], rect[1]))

    def edit(self, newTxt, newRect, newColor):
        scr.fill((200, 200, 200), self.rect)
        surface = font.render(newTxt, False, newColor)
        scr.blit(surface, (newRect[0], newRect[1]))
        self.text = newTxt
        self.rect = newRect
        self.color = newColor


def constructGrid():
    grid = []
    for r in range(10):
        row = []
        for c in range(10):
            row.append("0")
        grid.append(row)
    return grid


def display(m):
    for i in range(10):
        for j in range(10):
            print(m[i][j], end=" ")
        print(end="\n")


def move(inputM, playerPos, grid):
    if direction == "nil":
        return playerPos
    inputM = inputM.upper()
    if inputM == "W":
        step = [0, -1]
    elif inputM == "A":
        step = [-1, 0]
    elif inputM == "D":
        step = [1, 0]
    elif inputM == "S":
        step = [0, 1]
    else:
        step = [0, 0]
    newPos = [playerPos[0] + step[0], playerPos[1] + step[1]]
    if (newPos[0] <= 9) and (newPos[0] >= 0):
        if (newPos[1] <= 9) and (newPos[1] >= 0):
            if grid[newPos[1]][newPos[0]] != "#":
                playerPos = newPos
    return playerPos


def updateMonster(playerPos, monsterPos, grid):
    global stomped
    step = aStar(monsterPos, playerPos, grid)
    monsterPos = step[1]
    color = scr.get_at((monsterPos[0]*50, (monsterPos[1]*50+200)))
    stomped.fill(color)
    return monsterPos


def generateMonster(grid):
    possible = []
    for i in range(10):
        for j in range(10):
            if grid[j][i] == "0":
                possible.append([i, j])
    index = randint(0, len(possible))
    monsterPos = possible[index]
    return monsterPos


def generateObjects(grid):
    newObjects = []
    possible = []
    for i in range(10):
        for j in range(10):
            if grid[j][i] == "0":
                possible.append([i, j])
    coinTile = pygame.Surface((50, 50))
    coinTile.fill((255, 255, 0))

    trapTile = pygame.Surface((50, 50))
    trapTile.fill((190, 190, 190))

    for i in range(7):
        coin = randint(0, (len(possible)-2))
        possible.remove(possible[coin])
        coord = possible[coin]
        grid[coord[1]][coord[0]] = "C"
        coin = Object(possible[coin], "coin")
        newObjects.append(coin)
        scr.blit(coinTile, ((coord[0]*50), (coord[1]*50+200)))
    for i in range(7):
        trap = randint(0, (len(possible)-2))
        possible.remove(possible[trap])
        coord = possible[trap]
        grid[coord[1]][coord[0]] = "T"
        trap = Object(possible[trap], "trap")
        newObjects.append(trap)
        scr.blit(trapTile, ((coord[0] * 50), (coord[1] * 50 + 200)))
    return newObjects


def detectCollision(obj, p):
    coin = 0
    traps = 0
    for i in obj:
        if i.coord == p:
            if i.oType == "coin":
                coin += 1
                obj.remove(i)
            if i.oType == "trap":
                traps += 1
                obj.remove(i)
    collision = [coin, traps]
    return collision


def constructWalls(wall, grid, screen):
    for i in range(len(wall)):
        for j in wall[i]:
            grid[i][j] = "#"
            surf = pygame.Surface((50, 50))
            surf.fill((0, 0, 0))
            screen.blit(surf, (j * 50, (i * 50)+200))


pygame.font.init()
font = pygame.font.SysFont("Times New Roman", 40)

scr = pygame.display.set_mode([500, 700])
scr.fill((200, 200, 200))
coinText = Text("Coins: 0", (90, 0, 200, 40), (0, 0, 0, 0))

maze = constructGrid()
walls = [[1, 2, 3, 4, 6, 7, 8, 9],
         [3],
         [1, 3, 5, 7, 8, 9],
         [1, 3],
         [3, 5, 7],
         [1, 7],
         [3, 5, 6],
         [1, 2, 3, 7],
         [5, 6],
         [1, 2, 3, 4, 5, 6, 7, 8, 9]]
constructWalls(walls, maze, scr)

coins = 0
player = [0, 0]
maze[player[1]][player[0]] = "P"
playerTile = pygame.Surface((50, 50))
playerTile.fill((0, 255, 0))
scr.blit(playerTile, (player[0]*50, (player[1]*50)+200))

monster = generateMonster(maze)
maze[monster[1]][monster[0]] = "M"
monsterTile = pygame.Surface((50, 50))
monsterTile.fill((255, 0, 0))
scr.blit(monsterTile, (monster[0]*50, (monster[1]*50)+200))

emptyTile = pygame.Surface((50, 50))
emptyTile.fill((200, 200, 200))

objects = generateObjects(maze)

display(maze)
stomped = pygame.Surface((50, 50))
stomped.fill((200, 200, 200))
alive = True
alert = False

while alive:

    if monster == player:
        alive = False
        print("You Have Died")

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            alive = False
        if event.type == pygame.KEYDOWN:
            keypress = False
            direction = "nil"

            if event.key == pygame.K_w:
                direction = "W"
                keypress = True
            elif event.key == pygame.K_a:
                direction = "A"
                keypress = True
            elif event.key == pygame.K_s:
                direction = "S"
                keypress = True
            elif event.key == pygame.K_d:
                direction = "D"
                keypress = True

            scr.blit(emptyTile, (player[0] * 50, (player[1] * 50) + 200))
            player = move(direction, player, maze)
            scr.blit(playerTile, (player[0] * 50, (player[1] * 50) + 200))

            if alert and keypress:
                scr.blit(stomped, (monster[0] * 50, (monster[1] * 50) + 200))
                monster = updateMonster(player, monster, maze)
                scr.blit(monsterTile, (monster[0] * 50, (monster[1] * 50) + 200))

    pygame.display.flip()

    collisions = detectCollision(objects, player)
    if collisions[0] > 0:
        print("Collected a Coin!")
        coins += collisions[0]
        coinText.edit(("Coins: "+str(coins)), coinText.rect, coinText.color)
        if coins == 7:
            alive = False
            print("You Win!")
    if collisions[1] > 0:
        print("Triggered a Trap")
        alert = True
pygame.quit()
