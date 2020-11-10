from copy import deepcopy
import os
import AC3Functions
from AuxClasses import ArcQueue
from AuxClasses import Board
import BackTracking
import FileFunctions

engine = "C"

def main():

    #Get currentDirectory and filename
    originalFileName = "board2.txt"
    currentDirectory = os.path.dirname(os.path.realpath(__file__))
    fileName = os.path.join(currentDirectory,"../test_boards/"+originalFileName)

    #2d Array of board, with None in empty places
    startingBoard = parseInputFile(fileName)

    board = Board(startingBoard)

    #Print the starting board
    print("Starting Board:")
    printBoard(startingBoard)

    #Run AC3 Algorithm
    print("Calling AC3 Algorithmn")
    resolvedBoard = AC3Functions.getAC3(board)
    print("AC3 Finished")
    if(resolvedBoard == None):
        print("Board Not solvable!")
        return None


    print()
    print()
    print("Calling backtracking")
    print()

    if(engine.lower() == "c"):
        FileFunctions.callBackTrackingInC(resolvedBoard.domainDict, originalFileName)
    else:
        BackTracking.backTrackHelper(board)
    
    #resolvedBoard.printDomain()
    #BackTracking.backTrackHelper(board)
    

def parseInputFile(fileName):

    #Read contents of file
    f = open(fileName, "r")

    allLines = f.readlines()

    theBoard = []

    for line in allLines:
        currentRow = []
        splitLine = line.split(",")
        for x in splitLine:
            xSrtipped = x.strip()
            if(xSrtipped.isnumeric()):
                currentRow.append((int)(xSrtipped))
            else:
                currentRow.append(None)

        theBoard.append(currentRow)
    f.close()

    return theBoard
    

#This is to make sure board is correct size, and fits possible values
def checkBoard(board, boardSize=9, possibleValues=[1,2,3,4,5,6,7,8,9]):

    for i in range(0, len(board)):
        if(len(board[i]) != boardSize):
            return False

    return True


def printBoard(board):

    for i in range(0, len(board)):
        for k in range(0, len(board[i])):
            if(board[i][k] is None):
                print("_  ", end="")
            else:
                print(board[i][k], " ", end="")

        print()

if __name__ == "__main__":
    main()