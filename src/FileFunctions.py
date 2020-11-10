import os
from os import startfile
from AuxClasses import Board

domainFileName = "tempDomains.txt"

def callBackTrackingInC(domainDict, fileName, boardSize=9):

    writeDomainsToFile(domainDict, boardSize=boardSize)

    currentDirectory = os.path.dirname(os.path.realpath(__file__))
    os.chdir(currentDirectory)
    print("command: "+"g++ BackTrackSolver.cpp -o BackTrackSolver && BackTrackSolver.exe "+fileName)
    os.system("g++ BackTrackSolver.cpp -o BackTrackSolver && BackTrackSolver.exe "+fileName)
    print(currentDirectory)
    os.system("del "+domainFileName)


def writeDomainsToFile(domainDict, boardSize=9):

    print("Writing to file")

    currentDirectory = os.path.dirname(os.path.realpath(__file__))
    os.chdir(currentDirectory)

    f = open(domainFileName, "w")

    for i in range(0, boardSize):
        for k in range(0, boardSize):
            currentTuple = (i,k)
            domainVals = domainDict[currentTuple]

            concatStr = str(i)+","+str(k)+":"

            f.write(concatStr)

            writeString = ""
            for domainVal in domainVals:
                writeString = writeString+(str)(domainVal)+","

            writeString = writeString[:-1]
            f.write(writeString)
            f.write("\n")

    f.close()

