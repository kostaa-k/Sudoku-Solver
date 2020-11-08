import random
from copy import deepcopy
from AuxClasses import Board
from AuxClasses import ArcQueue


#MAIN FUNCTIONS


def getAC3(board):
    arcs = initializeArcs(board.board)
    originalArcs = getAllArcs(board.board, arcs)
    arcQueue = ArcQueue(originalArcs)

    resolvedBoard = AC3(board, arcQueue)

    return resolvedBoard

def AC3(board, arcQueue):
    
    #1. remove random Arc from totalArcs
    #2. Call revise function
    #3. If revise is true - 
        # - make sure domain is not empty (if it is then unsolvable)
        # - getNeighbors of Xi -> and add them to the queue
    
    while(arcQueue.isEmpty() == False):
        currentArc = arcQueue.popFromQueue()
        wasRevised, board = revise(board, currentArc[0], currentArc[1])
        if (wasRevised == True):
            if(board.getDomainSizeOfTile(currentArc[0]) == 0):
                return None
            arcQueue.addNeighborsToQueue(currentArc[0], notInclude=currentArc[1])
            
    return board


def revise(board, xI, xJ):
    domainXI = deepcopy(board.domainDict[xI])
    domainXJ = deepcopy(board.domainDict[xJ])
    
    #print("domain of xI: ", domainXI)
    #print("domain of XJ: ", domainXJ)
    
    revised = False
    for val in domainXI:
        satisfied = False
        for val2 in domainXJ:
            if(val2!=val):
                satisfied =True
        
        #Delete element from dictionary
        if(satisfied == False):
            board.domainDict[xI].remove(val)
            revised=True
        
    return revised, board




def initializeArcs(board):
    allArcs = {}
    for i in range(0, len(board)):
        for k in range(0, len(board)):
            allArcs[(i, k)] = []
            
    return allArcs

def addArcToMap(xI, xJ, arcMap):
    
    if(xJ not in arcMap[xI]):
        arcMap[xI].append(xJ)
        
    return arcMap

def getRowColumnArcs(board, allArcs):
    
    
    for i in range(0, len(board)):
        for k in range(0, len(board)):
            if(board[i][k] is None):
                
                #Get row Arcs
                for j in range(0, len(board)):
                    if(board[j][k] is None and i!=j):
                        allArcs = addArcToMap((i, k), (j,k), allArcs)
                
                #Get ColumnArcs
                for j in range(0, len(board[i])):
                    if(board[i][j] is None and k!= j):
                        allArcs = addArcToMap((i, k), (i,j), allArcs)
                                
    return allArcs


def getAllArcs(board, allArcs):
    allArcs = getRowColumnArcs(board, allArcs)
    
    allBoxes = getBoxes(board)
    
    for i in range(0, len(board)):
        for k in range(0, len(board[i])):
            if(board[i][k] is None):
                boxI, boxK = getBoxCoordinates(i, k)

                for x in range(boxI, boxI+3):
                    for y in range(boxK, boxK+3):
                        if(x!= i and k!= y):
                            if(board[x][y] is None):
                                allArcs = addArcToMap((i, k), (x,y), allArcs)
                    
    return allArcs

def getBoxes(board, boxSize=3):
    
    boxesMap = {}
    for x in range(0, len(board)//boxSize):
        for y in range(0, len(board)//boxSize):
            
            topPart = x*boxSize
            bottomPart = topPart+boxSize
            leftPart = y*boxSize
            rightPart = leftPart+boxSize
            
            #print("TOP to Bottom: ", topPart, bottomPart)
            #print("LEFT TO RIGHT: ", leftPart, rightPart)
            aBox = getArray(board, topPart, leftPart, bottomPart, rightPart)
            #printBoard(aBox)
            boxesMap[topPart,leftPart] = aBox
            
    return boxesMap

def getBoxCoordinates(i, k, boxSize=3):
    newI = i-(i%boxSize)
    newK = k-(k%boxSize)
    
    return newI, newK

def getArray(board, top, left, bottom, right):
    
    outputArray = []
    for i in range(top, bottom):
        outputArray.append(board[i][left:right])
                           
    return outputArray