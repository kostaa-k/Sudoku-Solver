import random
from copy import deepcopy

class Board():
    
    domainDict = {}
    board = None
    
    def __init__(self, board):
        self.board = board
        
        
    def getDomainOfBoard(self, possibleValues=[1,2,3,4,5,6,7,8,9]):
        
        for i in range(0, len(self.board)):
            for k in range(0, len(self.board[i])):
                if(self.board[i][k] is None):
                    currentDomain = self.getDomainOfTile(i, k, possibleValues)
                    self.domainDict[(i,k)] = currentDomain
                else:
                    self.domainDict[(i,k)] = []
        
    def getDomainOfTile(self, i, k, possibleValues=[1,2,3,4,5,6,7,8,9]):
    
        totalValues = []
        for x in possibleValues:
            totalValues.append(x)
        #Remove values from row
        for j in range(0, len(self.board)):
            if (self.board[i][j] is not None):
                if(self.board[i][j] in totalValues):
                    totalValues.remove(self.board[i][j])

        for j in range(0, len(self.board[i])):
            if(self.board[j][k] is not None):
               if(self.board[j][k] in totalValues):
                    totalValues.remove(self.board[j][k])


        if(self.board[i][k] is None):
            boxI, boxK = self.getBoxCoordinates(i, k)
            for x in range(boxI, boxI+3):
                for y in range(boxK, boxK+3):
                    if(self.board[x][y] is not None and self.board[x][y] in totalValues):
                        totalValues.remove(self.board[x][y])
    
        return totalValues
    
    def removeFromDomain(self, theTile, valueToRemove):
        if(valueToRemove in self.domainDict[theTile]):
            self.domainDict[theTile].remove(valueToRemove)
            return True
        else:
            print("Value: ", valueToRemove, " not in tile: ", theTile, "'s domain'")
        return False
    
    def getDomainSizeOfTile(self, theTile):
        return len(self.domainDict[theTile])


    def getBoxCoordinates(self, i, k, boxSize=3):
        newI = i-(i%boxSize)
        newK = k-(k%boxSize)
        
        return newI, newK


class ArcQueue():
    
    originalArcs = {}
    arcDictionary = {}
    
    def __init__(self, arcDictionary):
        self.arcDictionary = arcDictionary
        self.originalArcs = deepcopy(arcDictionary)
        
    def popFromQueue(self):
        
        found = False
        for key in self.arcDictionary.keys():
            if(len(self.arcDictionary[key]) > 0):
                toPop = self.arcDictionary[key][0]
                self.arcDictionary[key].remove(toPop)
                
                return [key, toPop]
        #xI, xJ = random.choice(list(d.items()))
        
    def isEmpty(self):
        for key in self.arcDictionary.keys():
            if(len(self.arcDictionary[key]) > 0):
                return False
            
        return True
    
    def addToQueue(self, xI, xJ):
        
        if(xJ not in self.arcDictionary[xI] and xI not in self.arcDictionary[xJ]):
            self.arcDictionary[xI].append(xJ)
            
    def addNeighborsToQueue(self, xI, notInclude=None): 
        for value in self.originalArcs[xI]:
            if(value not in self.arcDictionary[xI]):
                if(notInclude is None):
                    self.arcDictionary[xI].append(value)
                else:
                    if(value != notInclude):
                        self.arcDictionary[xI].append(value)
                
                
    def getQueueLength(self):
        
        totalCount = 0 
        
        for key in self.arcDictionary.keys():
            totalCount = totalCount+len(self.arcDictionary[key])
            
        return totalCount

