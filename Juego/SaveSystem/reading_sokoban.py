# José Carlos de la Torre Hernández
# A01235953
# ICT
# reading_sokoban.py
# Entrada
# un archivo .txt de nivel
# Salida
# listas para la posicion del jugador, bloques, paredes, y objetivos
# Version utilzada de python: 3.8.5

import os

def openLevel(fileName):
    file = open(fileName, "r")
    lines = file.readlines()
    #print(lines)
    file.close()
    playerLine = lines[0].split()
    blockLine = lines[1].split()
    wallLine = lines[2].split()
    goalLine = lines[3].split()
    level = int(lines[4])
    playerMatrix = makeMatrix(playerLine)
    blockMatrix = makeMatrix(blockLine)
    wallMatrix = makeMatrix(wallLine)
    goalMatrix = makeMatrix(goalLine)
    return playerMatrix, blockMatrix, wallMatrix, goalMatrix, level

def emptyMatrix(row, column):
    matriz = []
    for ren in range(row):
        matriz.append([0]*column)
    return matriz
def makeMatrix(line):
    row = int(line[0])
    column = 2
    length = 1
    matriz = emptyMatrix(row, column)
    for ren in range(row):
        for col in range(column):
            matriz[ren][col] = int(line[length])
            length = length + 1
    return matriz
def makeLine(matriz):
    line = []
    row = len(matriz)
    column = 2
    line.append(str(len(matriz))+" ")
    for ren in range(row):
        for col in range(column):
            line.append(str(matriz[ren][col])+" ")
    line.append("\n")
    return line
def savingLevel(dir, player, block, wall, goal, level):
    playerLine = makeLine(player)
    blockLine = makeLine(block)
    wallLine = makeLine(wall)
    goalLine = makeLine(goal)
    file = open(os.path.join(dir, "saving.txt"), "w")
    file.writelines(playerLine)
    file.writelines(blockLine)
    file.writelines(wallLine)
    file.writelines(goalLine)
    file.writelines(str(level))
    file.close()
def main():
    openLevel("nivel.txt")
    player, block, wall, goal, level = openLevel("nivel.txt")
    print("Player: ", end="")
    print(player)
    print("Block: ", end="")
    print(block)
    print("Wall: ", end="")
    print(wall)
    print("Goal: ", end="")
    print(goal)
    print("Level: ", end="")
    print(level)
    savingLevel(player, block, wall, goal, level)

if __name__ == "__main__":
    main()