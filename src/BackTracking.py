from AuxClasses import Board
import random
from copy import deepcopy


def backTrackHelper(board):

    #Get first variable to choose
    firstTile = board.emptyTiles[0]
    for tile in board.emptyTiles:
        if(getDegreeOfTile(tile, board) > getDegreeOfTile(firstTile, board)):
            firstTile = tile

    board = backTrack(board, tile=firstTile)

    if(board is not None):
        if (board.isCompleteBoardSolved()):
            print("SOLVED!")
            board.printBoard()

    return board


def backTrack(board, tile=None):

    if(board.isSolved() == True):
        return board

    if(tile is None):
        tile = chooseVariable(board.emptyTiles, board.domainDict)

    orderedValues = getValueOrdering(tile, board)
    for val in orderedValues:
        #tempBoard = deepcopy(board)
        newBoard = Board(deepcopy(board.board))

        newBoard.setValueOfTile(tile, val)
        newBoard.getDomainOfBoard()

        if (newBoard.isViolated() == False):
            answerBoard = backTrack(newBoard)
            if(answerBoard is not None):
                return answerBoard

    return None


#Minimum Remaining Values heuristic
#Vairable choosing
def chooseVariable(emptyTiles, domainDictionary):

    tileToChoose = emptyTiles[0]
    minValues = len(domainDictionary[tileToChoose])
    for tile in emptyTiles:
        if(len(domainDictionary[tile]) < minValues):
            minValues = len(domainDictionary[tile])
            tileToChoose = tile

    return tileToChoose



def getValueOrdering(tile, board):
    neighborTiles = board.getNeighborTiles(tile)

    valueCounts = {}
    orderedValues = []

    for curTile in neighborTiles:
        for value in board.domainDict[curTile]:
            if(value in board.domainDict[tile]):
                if(value in valueCounts):
                    valueCounts[value] = valueCounts[value]+1
                else:
                    valueCounts[value] = 1

    for curTile in sorted(valueCounts, key=valueCounts.get):
        orderedValues.append(curTile)

    return orderedValues

def getDegreeOfTile(tile, board):
    return len(board.getNeighborTiles(tile))