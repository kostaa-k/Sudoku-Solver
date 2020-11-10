#include <stdio.h>
#include <stdlib.h>
#include <malloc.h>
#include <bits/stdc++.h> 
#include <iostream> 
#include <sstream>  // for string streams 
#include <string>
#include <stack>
#include <iterator>
#include <algorithm>
#include <fstream>

using namespace std;


//Value for Board Configurations
#define BOARDSIZE 9
#define BOXSIZE 3


int POSSIBLE_VALS[] = {1,2,3,4,5,6,7,8,9};


typedef struct Tile {
    int domain[BOARDSIZE];
    int value;
    int i;
    int k;

} tile;

typedef struct BoardNode {
    tile board[BOARDSIZE][BOARDSIZE];
    bool isViolating;
    bool isSolved;
} boardNode;


boardNode setValueOfTile(boardNode theBoard, tile toReplace);
int getLengthOfDomain(int theDomain[BOARDSIZE]);
tile getTiletoReplace(boardNode theBoard);
bool isBoardViolated(boardNode theBoard);
int getDomainValueToSet(tile theTile);
tile getNewTile(tile oldTile, int value);
boardNode runBackTrack(boardNode theBoard);

void printSimpleDomain(tile theTile);

bool isBoardSolved(boardNode);

boardNode createEmptyBoard();

list<tile> getEmptyTiles(boardNode theBoard);

tile chooseTile(boardNode theBoard);

boardNode setBoardValuesFromFile(boardNode theBoard, string fileName);

void printBoardDomains(tile aboard[BOARDSIZE][BOARDSIZE]);
void printBoard(tile aboard[BOARDSIZE][BOARDSIZE]);


boardNode copyBoard(boardNode aBoard);

boardNode getBoardDomainsFromFile(string fileName);



int main(int argc, char *argv[]) {

    boardNode startNode;


    if(argc > 1){
        cout << "Found fileName: \n";
        string fileName = argv[1];
        cout << fileName;
        cout << "\n";
        string domainFileName = "tempDomains.txt";
        boardNode boardFromFile = getBoardDomainsFromFile(domainFileName);
        startNode = setBoardValuesFromFile(boardFromFile, "../test_boards/"+fileName);
    }
    else{
        cout << "No arguments \n";
        startNode = createEmptyBoard();
    }


    printf("\n");
    printf("Starting Board: \n");
    printBoard(startNode.board);

    // printf("\n");
    // printf("Starting Board Domains: \n");
    // printBoardDomains(startNode.board);

    boardNode completeBoard = runBackTrack(startNode);

    printBoard(completeBoard.board);

    return 0;
}


boardNode setBoardValuesFromFile(boardNode theBoard, string fileName){
    string myText;
    ifstream MyReadFile(fileName);


    int columnCount = 0;
    int rowCount = 0;

    int totalRowCount = 0;
    while (getline (MyReadFile, myText)) {
        //cout << myText;
        //cout << "\n";
        if(totalRowCount%2 == 0){

        }
        for (int x=0;x<myText.length();x++){
            if(myText[x] != ','){
                if(isdigit(myText[x])){
                    
                    int tempValue = myText[x] - '0';
                    
                    //cout << tempValue;
                    theBoard.board[rowCount][columnCount].value = tempValue;
                }
                else{
                    theBoard.board[rowCount][columnCount].value = -1;
                }

                columnCount++;
            }
        }

        //cout << "\n";

        if(totalRowCount%2 == 1){
            rowCount++;
        }
    }

    theBoard.isSolved = false;
    theBoard.isViolating = false;


    return theBoard;
}

boardNode getBoardDomainsFromFile(string fileName){


    boardNode startNode;

    string myText;
    ifstream MyReadFile(fileName);
    while (getline (MyReadFile, myText)) {
        // Output the text from the file

        std::string startToken = myText.substr(0, myText.find(":"));
        std::string token1 = myText.substr(0, startToken.find(","));
        std::string token2 = myText.substr(startToken.find(",")+1, startToken.length()-2);

        std::string lastToken = myText.substr(myText.find(":"), myText.length());


        tile newTile;
        
        int iVal = token1[0] - '0';
        int kVal = token2[0] - '0';
        
        newTile.i = iVal;
        newTile.k = kVal;

        for (int x = 0;x<BOARDSIZE;x++){
            newTile.domain[x] = 0;
        }



        for(int i=0;i<lastToken.length();i++){
            if(isdigit(lastToken[i])){
                int tempNum = lastToken[i] - '0';
                newTile.domain[tempNum-1] = 1;
            }
        }

        startNode.board[iVal][kVal] = newTile;
    }

    return startNode;


}

boardNode createEmptyBoard(){
    boardNode startNode;

    startNode.isViolating = false;
    startNode.isSolved = false;

    for(int i=0;i<BOARDSIZE;i++){
        for(int k = 0;k<BOARDSIZE;k++){
            startNode.board[i][k].value = -1;
            startNode.board[i][k].i = i;
            startNode.board[i][k].k = k;

            for(int x = 0;x<BOARDSIZE;x++){
                startNode.board[i][k].domain[x] = 1;
            }
        }

    }
    return startNode;
}




boardNode runBackTrack(boardNode theBoard){

    // for(int counter=0;counter<20;counter++){
    //     tile toReplaceTile = getTiletoReplace(theBoard);
    //     int valueToSet = getDomainValueToSet(toReplaceTile);

    //     tile newTile = getNewTile(toReplaceTile, valueToSet);

    //     printf("Replacing tile %d %d \n", toReplaceTile.i, toReplaceTile.k);
    //     theBoard = setValueOfTile(theBoard, newTile);

    //     printf("NEW BOARD: \n");
    //     printBoard(theBoard.board);
    //     printf("\n");
    //     printf("BOARD DOMAIN: \n");
    //     printBoardDomains(theBoard.board);
    //     printf("\n");
    // }


    if(isBoardSolved(theBoard) == true){
        printf("Solved! \n");
        theBoard.isSolved = true;
        return theBoard;
    }


    tile toReplace = chooseTile(theBoard);
    for (int x=0;x<BOARDSIZE;x++){
        if(toReplace.domain[x] > 0){

            boardNode boardCpy = copyBoard(theBoard);
        
            //printf("From Tile (%d, %d), picking value: %d from domain: ", toReplace.i, toReplace.k, x+1);
            //printSimpleDomain(toReplace);
            tile newTile = getNewTile(toReplace, x+1);
            boardNode newBoard = setValueOfTile(theBoard, newTile);
            if(isBoardViolated(newBoard) == false){
                boardNode finishedBoard = runBackTrack(newBoard);
                if(finishedBoard.isSolved == true){
                    return finishedBoard;
                }
            }
        }        
        
    }

    return theBoard;
}

boardNode copyBoard(boardNode aBoard){

    boardNode newBoard;

    newBoard.isSolved = aBoard.isSolved;
    newBoard.isViolating = aBoard.isViolating;

    for (int i=0;i<BOARDSIZE;i++){
        for (int k=0;k<BOARDSIZE;k++){
            
            tile tempTile;
            for (int x;x<BOARDSIZE;x++){
                tempTile.domain[x] = aBoard.board[i][k].domain[x];
            }
            
            tempTile.i = i;
            tempTile.k = k;
            tempTile.value = aBoard.board[i][k].value;
            newBoard.board[i][k] = tempTile;    
        }
    }

    return newBoard;
}


void printSimpleDomain(tile theTile){

    for(int i = 0;i<BOARDSIZE;i++){
        if(theTile.domain[i] > 0){
            printf(" %d ", i+1);
        }
    }

    printf("\n");
}

// Min Remaining values  heuristic
tile chooseTile(boardNode theBoard){

    tile tileToReplace = getTiletoReplace(theBoard);
    int minCount = getLengthOfDomain(tileToReplace.domain);

    for(int i =0;i<BOARDSIZE;i++){
        for(int k=0;k<BOARDSIZE;k++){
            if(theBoard.board[i][k].value == -1){
                int domainLength = getLengthOfDomain(theBoard.board[i][k].domain);
                if(domainLength < minCount){
                    tileToReplace = theBoard.board[i][k];
                    minCount = domainLength;
                }
            }
        }
    }

    return tileToReplace;
}



tile getNewTile(tile oldTile, int value){
    tile newTile;
    newTile.i = oldTile.i;
    newTile.k = oldTile.k;
    newTile.value = value;

    for(int x= 0;x<BOARDSIZE;x++){
        newTile.domain[x] = 0;
    }

    return newTile;

}



tile getTiletoReplace(boardNode theBoard){
    for(int i =0;i<BOARDSIZE;i++){
        for(int k=0;k<BOARDSIZE;k++){
            if(theBoard.board[i][k].value == -1){
                return theBoard.board[i][k];
            }
        }
    }

    tile nullTile;
    nullTile.i = -2;
    nullTile.k = -2;
    return nullTile;
}

int getDomainValueToSet(tile theTile){
    for (int x = 0;x<BOARDSIZE;x++){
        if(theTile.domain[x] > 0){
            return x+1;
        }
    }

    return -2;
}

boardNode setValueOfTile(boardNode theBoard, tile toReplace) {

    int countReplaced = 0;

    for(int i =0;i<BOARDSIZE;i++){
        countReplaced++;
        if(theBoard.board[i][toReplace.k].value == -1 && i!=toReplace.i){
            theBoard.board[i][toReplace.k].domain[toReplace.value-1] = 0;
        }
    }


    for(int k =0;k<BOARDSIZE;k++){
        countReplaced++;
        if(theBoard.board[toReplace.i][k].value == -1 && k!=toReplace.k){
            theBoard.board[toReplace.i][k].domain[toReplace.value-1] = 0;
        }
    }


    int boxI = toReplace.i - (toReplace.i%BOXSIZE);
    int boxK = toReplace.k - (toReplace.k%BOXSIZE);

    for(int i =boxI;i<boxI+BOXSIZE;i++){
        for(int k=boxK;k<boxK+BOXSIZE;k++){
            countReplaced++;
            if(i != toReplace.i && k != toReplace.k){
                theBoard.board[i][k].domain[toReplace.value-1] = 0;
            }
        }
    }


    theBoard.board[toReplace.i][toReplace.k] = toReplace;

    return theBoard;
}


int getLengthOfDomain(int theDomain[BOARDSIZE]) {

    int theLength = 0;
    for(int i =0;i<BOARDSIZE;i++){
        if(theDomain[i] != 0){
            theLength++;
        }
    }    

    return theLength;
}

bool isBoardViolated(boardNode theBoard){
    for(int i =0;i<BOARDSIZE;i++){
        for(int k=0;k<BOARDSIZE;k++){
            if( theBoard.board[i][k].value == -1){
                if(getLengthOfDomain(theBoard.board[i][k].domain) == 0){
                    //printf("Violated by (%d, %d)", i, k);
                    return true;
                }
            }
        }
    }

    return false;
}

bool isBoardSolved(boardNode theBoard) {
    for(int i =0;i<BOARDSIZE;i++){
        for(int k=0;k<BOARDSIZE;k++){
            if( theBoard.board[i][k].value == -1){
                return false;
            }
        }
    }

    return true;
}


void printBoard(tile aboard[BOARDSIZE][BOARDSIZE]){
    printf("\n");
    for(int i =0;i<BOARDSIZE;i++){
        for(int k=0;k<BOARDSIZE;k++){
            printf("%d ", aboard[i][k].value);
        }
        printf("\n");
    }
}


void printBoardDomains(tile aboard[BOARDSIZE][BOARDSIZE]){
    printf("\n");
    for(int i =0;i<BOARDSIZE;i++){
        for(int k=0;k<BOARDSIZE;k++){
            printf("Domain of %d %d :  ", i, k);
            for(int x=0; x<BOARDSIZE;x++){
                if(aboard[i][k].domain[x] != 0){
                    printf(" %d,", x+1);
                }
            }
            printf("\n");
        }
    }
}


list<tile> getEmptyTiles(boardNode theBoard){

    list<tile> returnNodes;

    for(int i =0;i<BOARDSIZE;i++){
        for(int k=0;k<BOARDSIZE;k++){
            if(theBoard.board[i][k].value == -1){
                tile newTile;
                newTile.i = i;
                newTile.k = i;
                newTile.value = -1;
                returnNodes.push_back(newTile);
            }
        }
    }


    return returnNodes;
}