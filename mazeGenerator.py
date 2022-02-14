from random import randint

def display(list):
    for row in list:
        for column in row:
            if column == "0":
                print("_", end=" ")
            if column == "1":
                print("#", end=" ")
        print()

def mazeGenerator(xSize, ySize):
    maze = []
    nodes = []
    for y in range(ySize):
        maze.append([])
        for x in range(xSize):
            if (x%2 == 1) and (y%2 == 1):
                maze[y].append("0")
                nodes.append([x, y])
                continue
            maze[y].append("1")
    
    visited = []
    current = nodes[randint(0, len(nodes)-1)]
    visited.append(current)

    while len(visited) < len(nodes):
        nextNodes = []
        for dx in range(-2,3,2):
            for dy in range(-2,3,2):
                if abs(dx) == abs(dy):
                    continue
                if (current[0]+dx < 0 or current[0]+dx > xSize-1) or (current[1]+dy < 0 or current[1]+dy > ySize-1):
                    continue
                if [current[0]+dx, current[1]+dy] in visited:
                    continue
                nextNodes.append([current[0]+dx, current[1]+dy])
        if len(nextNodes) != 0:
            choice = nextNodes[randint(0, len(nextNodes)-1)]
            wall = [int(current[0]+((choice[0]-current[0])/2)), int(current[1]+((choice[1]-current[1])/2))]
            maze[wall[1]][wall[0]] = "0"
            current = choice
            visited.append(current)
        else:
            current = visited[visited.index(current)-1]
    return maze