from AuxClasses import Board
import random
from copy import deepcopy


def backTrackHelper(board):

    board = backTrack(board)

    if(board is not None):
        print("SOLVED!")
        board.printBoard()

    return board


def backTrack(board):

    if(board.isSolved() == True):
        return board

    tile = board.emptyTiles[0]
    for val in board.domainDict[tile]:
        #tempBoard = deepcopy(board)
        newBoard = Board(deepcopy(board.board))

        newBoard.setValueOfTile(tile, val)
        newBoard.getDomainOfBoard()

        if (newBoard.isViolated() == False):
            answerBoard = backTrack(newBoard)
            if(answerBoard is not None):
                return answerBoard

    return None