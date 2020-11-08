from copy import deepcopy
import os
import AC3Functions
from AuxClasses import ArcQueue
from AuxClasses import Board


def main():

    #Get currentDirectory and filename
    fileName = "top_left_one.txt"
    currentDirectory = os.path.dirname(os.path.realpath(__file__))
    fileName = os.path.join(currentDirectory,"../test_boards/"+fileName)

    #2d Array of board, with None in empty places
    startingBoard = parseInputFile(fileName)

    board = Board(startingBoard)

    #Print the starting board
    print("Starting Board:")
    printBoard(startingBoard)

    #Run AC3 Algorithm
    resolvedBoard = AC3Functions.getAC3(board)
    if(resolvedBoard == None):
        print("Board Not solvable!")
        return None

    resolvedBoard.printDomain()
    

def parseInputFile(fileName):

    #Read contents of file
    f = open(fileName, "r")

    allLines = f.readlines()

    theBoard = []

    for line in allLines:
        currentRow = []
        splitLine = line.split(",")
        for x in splitLine:
            if(x.isnumeric()):
                currentRow.append((int)(x))
            else:
                currentRow.append(None)

        theBoard.append(currentRow)
    f.close()

    return theBoard
    
def printBoard(board):

    for i in range(0, len(board)):
        for k in range(0, len(board[i])):
            print(board[i][k], " ", end="")

        print()

if __name__ == "__main__":
    main()