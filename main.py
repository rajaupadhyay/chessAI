import sys
import gui
import pygame
from pygame.locals import *
import math
import os
import copy
import random
import time

piecesDict = {"ROOK": "R", "KNIGHT": "K", "BISHOP": "B", "QUEEN": "Q", "KING": "KI", "PAWN": "P"}
counter = 0
board = []
attackingPieces1 = ["KI","R","B","Q","K"]
attackingPieces2 = ["ki","r","b","q","k"]

# WHITE PIECES ARE LOWERCASE AND BLACK PIECES ARE UPPERCASE
def initialise():
    row8 = [piecesDict["ROOK"].lower(), piecesDict["KNIGHT"].lower(), piecesDict["BISHOP"].lower(),
            piecesDict["QUEEN"].lower(), piecesDict["KING"].lower(),
            piecesDict["BISHOP"].lower(), piecesDict["KNIGHT"].lower(), piecesDict["ROOK"].lower()]
    board.append(row8)
    row7 = ["p" for _ in range(8)]
    board.append(row7)

    for i in range(4):
        rows3_6 = ['_' for _ in range(8)]
        board.append(rows3_6)
    row8 = [x.upper() for x in row8]
    row7 = [x.upper() for x in row7]
    board.append(row7)
    board.append(row8)
    print("X", end=" ")
    pos = ["a", "b", "c", "d", "e", "f", "g", "h"]
    print(pos, "\n")
    for i in range(8):
        print(i + 1, end=" ")
        print(board[i])

replay = 0
def play():
    game = gui.ChessGUI_pygame()
    while True:  # Implement while(boardCheck()) where boardCheck() checks if game has ended
        global counter
        global replay
        global board
        print(counter)
        occ = 0
        if counter % 2 == 0:
            print("PLAYER 1s TURN (WHITE)")
            game.PrintMessage("BLACK TO PLAY") #Alternate
            player = "WHITE"
            flag = 1
        else:
            print("PLAYER 2s TURN (BLACK)")
            game.PrintMessage("WHITE TO PLAY")
            player = "BLACK"
            flag = 2

        # GET USER INPUT - piece coordinates and the target coordinates - b7b5
        # stringVal = str(input())
        # piecePosy = ord(stringVal[0]) - ord('a')
        # piecePosx = int(stringVal[1]) - 1
        # targetPosy = ord(stringVal[2]) - ord('a')
        # targetPosx = int(stringVal[3]) - 1

        if flag == 1:
            x=0
            while x == 0:
                pygame.event.set_blocked(MOUSEMOTION)
                e = pygame.event.wait()
                if e.type is MOUSEBUTTONDOWN:
                    (mouseX, mouseY) = pygame.mouse.get_pos()
                    piecePosx, piecePosy = game.GetClickedSquare(mouseX, mouseY)
                    piecePosx, piecePosy = math.floor(piecePosx), math.floor(piecePosy)
                    if piecePosx == -1 and piecePosy == -1:
                        print("ERROR1")
                        game.PrintMessage("INVALID - {} TRY AGAIN".format(player))
                        counter -= 1
                    x = 1
                if e.type is QUIT:  # the "x" kill button
                    pygame.quit()
                    sys.exit(0)

            x = 0
            while x == 0:
                pygame.event.set_blocked(MOUSEMOTION)
                e = pygame.event.wait()
                if e.type is MOUSEBUTTONDOWN:
                    (mouseX, mouseY) = pygame.mouse.get_pos()
                    targetPosx, targetPosy = game.GetClickedSquare(mouseX, mouseY)
                    targetPosx, targetPosy = math.floor(targetPosx), math.floor(targetPosy)
                    if targetPosx == -1 and targetPosy == -1:
                        print("ERROR2")
                        game.PrintMessage("INVALID - {} TRY AGAIN".format(player))
                        counter -= 1
                    x = 1
                if e.type is QUIT:  # the "x" kill button
                    pygame.quit()
                    sys.exit(0)
        else: # Random AI
            val = 0
            while val == 0:
                checked, attacker, myKingPos = checkKingSafe(board,flag,attackingPieces2)
                if checked == 1:
                    piecePosx, piecePosy = myKingPos[0], myKingPos[1]
                else:
                    piecePosx = random.randint(0,7)
                    pieceList = [piece for piece in attackingPieces1+["P"] if piece in board[piecePosx]]
                    if pieceList:
                        piecePosy = board[piecePosx].index(pieceList[random.randint(0,len(pieceList)-1)])

                targetList = moveGenerator(piecePosx, piecePosy, flag)
                print("TARGETS:", targetList)
                if targetList:
                    randMove = targetList[random.randint(0,len(targetList)-1)]
                    print(randMove)
                    if board[randMove[0]][randMove[1]].islower() or board[randMove[0]][randMove[1]] == '_':
                        targetPosx = randMove[0]
                        targetPosy = randMove[1]
                        val = 1



        buffer = board[targetPosx][targetPosy]
        # CHECK IF POSITIONS DEFINED ARE VALID
        boardCopy = copy.deepcopy(board)
        if board[piecePosx][piecePosy] != '_' and flag == 1:
            if board[piecePosx][piecePosy].islower():
                # Logic for moving to target pos (new func)
                if board[targetPosx][targetPosy].islower() and board[targetPosx][targetPosy] != '_':
                    print("CAN NOT MOVE PIECE TO SPECIFIED COORDINATES (PREOCCUPIED BY YOUR PIECE)")
                    game.PrintMessage("INVALID - {} TRY AGAIN".format(player))
                    occ = 1
                    counter -= 1
                else:
                    # validateAndMove(board,piecePosx, piecePosy, targetPosx, targetPosy, flag, attackingPieces2)
                    if boardCheck(board,piecePosx,piecePosy,targetPosx,targetPosy,flag,attackingPieces2) == 1:
                        board[piecePosx][piecePosy], board[targetPosx][targetPosy] = "_", board[piecePosx][piecePosy]
                    checkVal, attackerPos, kingPos = checkKingSafe(board,flag, attackingPieces1)
                    print("CHECKVAL: {}".format(checkVal))
                    if checkVal == 1:
                        board = boardCopy
                        # game.PrintMessage("INVALID (CHECKED) - {} TRY AGAIN".format(player))
                        print("CHECKED - PLAY TO PROTECT KING")
                        occ = 1
                        counter -= 1
            else:
                print("YOU CAN NOT MOVE YOUR OPPONENTS PIECE")

        elif board[piecePosx][piecePosy] != '_' and flag == 2:
            if board[piecePosx][piecePosy].isupper():
                # Logic for moving to target pos (new func)
                if board[targetPosx][targetPosy].isupper():
                    print("CAN NOT MOVE PIECE TO SPECIFIED COORDINATES (PREOCCUPIED BY YOUR PIECE)")
                    # game.PrintMessage("INVALID - {} TRY AGAIN".format(player))
                    occ = 1
                    counter -= 1
                else:
                    # validateAndMove(board,piecePosx, piecePosy, targetPosx, targetPosy, flag, attackingPieces1)
                    if boardCheck(board, piecePosx, piecePosy, targetPosx, targetPosy, flag, attackingPieces1) == 1:
                        board[piecePosx][piecePosy], board[targetPosx][targetPosy] = "_", board[piecePosx][piecePosy]
                    checkVal, attackerPos, kingPos = checkKingSafe(board, flag, attackingPieces2)
                    print("CHECKVAL: {}".format(checkVal))
                    if checkVal == 1:
                        board = boardCopy
                        # game.PrintMessage("INVALID (CHECKED) - {} TRY AGAIN".format(player))
                        print("CHECKED - PLAY TO PROTECT KING")
                        occ = 1
                        counter -= 1
            else:
                print("YOU CAN NOT MOVE YOUR OPPONENTS PIECE")

        else:
            print("NO PIECE PRESENT AT THE POSITION SPECIFIED")

        if board[targetPosx][targetPosy] == buffer and occ == 0:
            if flag == 1:
                game.PrintMessage("INVALID - {} TRY AGAIN".format(player))
            counter -= 1
###################################################################################################################################################

        getOutOfCheck(flag)

        # GAME OVER

        counter += 1
        print("X", end=" ")
        pos = ["a", "b", "c", "d", "e", "f", "g", "h"]
        print(pos, "\n")

        for i in range(8):
            print(i + 1, end=" ")
            print(board[i])

        game.Draw(board)

#############################################################################################################################################
# Function checks if the king is under attack - returns 1 if True else 0
def checkKingSafe(board1, playerNo, attackingPieces):
    KINGX, KINGY = -1,-1
    init = 0
    if attackingPieces[0].islower():
        tempKing = attackingPieces[0].upper()
    else:
        tempKing = attackingPieces[0].lower()

    for i in range(8):
        if tempKing in board1[i]:
            KINGX, KINGY = i, board1[i].index(tempKing)
    print(KINGX,KINGY)

    if init == 0:
        if playerNo == 1:
            if KINGX + 1 < 8:
                if KINGY - 1 >= 0:
                    if board1[KINGX+1][KINGY-1] == 'P':
                        print('here1')
                        return 1, (KINGX+1,KINGY-1), (KINGX,KINGY)
                if KINGY + 1 < 8:
                    if board1[KINGX+1][KINGY+1] == 'P':
                        print('here2')
                        return 1, (KINGX+1,KINGY+1), (KINGX,KINGY)
        else:
            if KINGX - 1 >= 0:
                if KINGY - 1 >= 0:
                    if board1[KINGX - 1][KINGY - 1] == 'p':
                        return 1, (KINGX-1,KINGY-1), (KINGX,KINGY)
                if KINGY + 1 < 8:
                    if board1[KINGX - 1][KINGY + 1] == 'p':
                        return 1, (KINGX-1,KINGY+1), (KINGX,KINGY)


    if KINGY-1>=0:
        if KINGX-2>=0:
            if board1[KINGX-2][KINGY-1] == attackingPieces[4]:
                print('here19')
                return 1, (KINGX-2,KINGY-1), (KINGX,KINGY)
        if KINGX+2<8:
            if board1[KINGX+2][KINGY-1] == attackingPieces[4]:
                print('here20')
                return 1, (KINGX+2,KINGY-1), (KINGX,KINGY)
    if KINGY-2>=0:
        if KINGX-1>=0:
            if board1[KINGX-1][KINGY-2] == attackingPieces[4]:
                print('here21')
                return 1, (KINGX-1,KINGY-2), (KINGX,KINGY)
        if KINGX+1<8:
            if board1[KINGX+1][KINGY-2] == attackingPieces[4]:
                print('here22')
                return 1, (KINGX+1,KINGY-2), (KINGX,KINGY)

    if KINGY+1<8:
        if KINGX-2>=0:
            if board1[KINGX-2][KINGY+1] == attackingPieces[4]:
                print('here23')
                return 1, (KINGX-2,KINGY+1), (KINGX,KINGY)
        if KINGX+2<8:
            if board1[KINGX+2][KINGY+1] == attackingPieces[4]:
                print('here24')
                return 1, (KINGX+2,KINGY+1), (KINGX,KINGY)

    if KINGY+2<8:
        if KINGX-1>=0:
            if board1[KINGX-1][KINGY+2] == attackingPieces[4]:
                print('here25')
                return 1, (KINGX-1,KINGY+2), (KINGX,KINGY)
        if KINGX+1<8:
            if board1[KINGX+1][KINGY+2] == attackingPieces[4]:
                print('here26')
                return 1, (KINGX+1,KINGY+2), (KINGX,KINGY)


    leftY = KINGY-1
    while leftY>=0:
        if board1[KINGX][leftY] != "_":
            if board1[KINGX][leftY] in attackingPieces[:-1]:
                return 1, (KINGX,leftY), (KINGX,KINGY)
            else:
                break
        leftY -= 1

    rightY = KINGY+1
    while rightY<8:
        if board1[KINGX][rightY] != "_":
            if board1[KINGX][rightY] in attackingPieces[:-1]:
                return 1, (KINGX, rightY), (KINGX,KINGY)
            else:
                break
        rightY += 1

    topX = KINGX-1
    while topX>=0:
        if board1[topX][KINGY] != "_":
            if board1[topX][KINGY] in attackingPieces[:-1]:
                return 1, (topX, KINGY), (KINGX, KINGY)
            else:
                break
        topX -= 1

    bottomX = KINGX+1
    while bottomX<8:
        if board1[bottomX][KINGY] != "_":
            if board1[bottomX][KINGY] in attackingPieces[:-1]:
                return 1, (bottomX,KINGY), (KINGX, KINGY)
            else:
                break
        bottomX += 1

    bottomLeftX, bottomLeftY = KINGX+1, KINGY-1
    while bottomLeftX<8 and bottomLeftY>=0:
        if board1[bottomLeftX][bottomLeftY] != "_":
            if board1[bottomLeftX][bottomLeftY] in attackingPieces[:-1]:
                return 1, (bottomLeftX,bottomLeftY), (KINGX, KINGY)
            else:
                break
        bottomLeftX += 1
        bottomLeftY -= 1

    bottomRightX, bottomRightY = KINGX+1,KINGY+1
    while bottomRightX<8 and bottomRightY<8:
        if board1[bottomRightX][bottomRightY] != "_":
            if board1[bottomRightX][bottomRightY] in attackingPieces[:-1]:
                return 1, (bottomRightX, bottomRightY), (KINGX, KINGY)
            else:
                break
        bottomRightX += 1
        bottomRightY += 1

    topLeftX, topLeftY = KINGX-1,KINGY-1
    while topLeftX>=0 and topLeftY>=0:
        if board1[topLeftX][topLeftY] != "_":
            if board1[topLeftX][topLeftY] in attackingPieces[:-1]:
                return 1, (topLeftX, topLeftY), (KINGX, KINGY)
            else:
                break
        topLeftX -= 1
        topLeftY -= 1

    topRightX, topRightY = KINGX-1, KINGY+1
    while topRightX>=0 and topRightY<8:
        if board1[topRightX][topRightY] != "_":
            if board1[topRightX][topRightY] in attackingPieces[:-1]:
                return 1, (topRightX, topRightY), (KINGX, KINGY)
            else:
                break
        topRightX -= 1
        topRightY += 1

    return 0, (-1,-1), (KINGX,KINGY)



# Function validates move
def boardCheck(board1,pieceX,pieceY,targetX,targetY,playerNo,attackingPieces):
    if board1[pieceX][pieceY] == 'p' or board1[pieceX][pieceY] == 'P':
        print("000")
        if playerNo == 1:
            if board1[pieceX][pieceY] == 'p':
                if targetY == pieceY:
                    if board1[pieceX + 1][pieceY] == '_':
                        if pieceX == 1 and targetX == 3:
                            return 1
                        elif targetX - pieceX == 1:
                            return 1
                    else:
                        return 0

                elif abs(targetY - pieceY) == 1 and (targetX - pieceX) == 1:
                    if board1[targetX][targetY].isupper():
                        return 1

        if playerNo == 2:
            if board1[pieceX][pieceY] == 'P':
                if targetY == pieceY:
                    if board1[pieceX - 1][pieceY] == '_':
                        if pieceX == 6 and targetX == 4:
                            return 1
                        elif targetX - pieceX == -1:
                            return 1
                    else:
                        return 0

                elif abs(targetY - pieceY) == 1 and (targetX - pieceX) == -1:
                    if board1[targetX][targetY].islower():
                        return 1

    elif board1[pieceX][pieceY] == attackingPieces[0]:
        print("101")
        if targetY == pieceY or targetY == pieceY - 1 or targetY == pieceY + 1:
            if pieceX - targetX == 1:
                return 1
            elif pieceX - targetX == 0:
                return 1
            elif pieceX - targetX == -1:
                return 1
            else:
                return 0
        else:
            return 0

    elif board1[pieceX][pieceY] == attackingPieces[1]:
        print("202")
        if targetX == pieceX:
            if targetY - pieceY >= 0:
                for i in range(abs(targetY - pieceY) - 1):
                    if board1[pieceX][pieceY + i + 1] != '_':
                        print("INVALID MOVE")
                        return 0
                return 1
            else:
                for i in range(abs(targetY - pieceY) - 1):
                    if board1[targetX][targetY + i + 1] != '_':
                        print("INVALID MOVE")
                        return 0
                return 1
        elif targetY == pieceY:
            if targetX - pieceX >= 0:
                for i in range(abs(targetX - pieceX) - 1):
                    if board1[pieceX + i + 1][pieceY] != '_':
                        print("INVALID MOVE")
                        return 0
                return 1
            else:
                for i in range(abs(targetX - pieceX) - 1):
                    if board[targetX + i + 1][targetY] != '_':
                        print("INVALID MOVE")
                        return 0
                return 1

    elif board1[pieceX][pieceY] == attackingPieces[2] or board1[pieceX][pieceY] == attackingPieces[3]:
        print("303")
        buffer = board1[pieceX][pieceY]
        if abs(pieceX - targetX) == abs(pieceY - targetY):
            print(pieceX, targetX)
            if targetX < pieceX:
                if targetY < pieceY:
                    for x in range(pieceX - targetX - 1):
                        if board1[pieceX - x - 1][pieceY - x - 1] != '_':
                            print("INVALID MOVE")
                            return 0
                    return 1
                else:
                    for x in range(pieceX - targetX - 1):
                        if board1[pieceX - x - 1][pieceY + x + 1] != '_':
                            print("INVALID MOVE")
                            return 0
                    return 1
            else:
                if targetY < pieceY:
                    for x in range(targetX - pieceX - 1):
                        if board1[pieceX + x + 1][pieceY - x - 1] != '_':
                            print("INVALID MOVE")
                            return 0
                    return 1
                else:
                    for x in range(targetX - pieceX - 1):
                        if board1[pieceX + x + 1][pieceY + x + 1] != '_':
                            print("INVALID MOVE")
                            return 0
                    return 1
        else:
            if board1[pieceX][pieceY] == attackingPieces[3]:
                if targetX == pieceX:
                    if targetY - pieceY >= 0:
                        for i in range(abs(targetY - pieceY) - 1):
                            if board1[pieceX][pieceY + i + 1] != '_':
                                print("INVALID MOVE")
                                return 0
                        return 1
                    else:
                        for i in range(abs(targetY - pieceY) - 1):
                            if board1[targetX][targetY + i + 1] != '_':
                                print("INVALID MOVE")
                                return 0
                        return 1
                elif targetY == pieceY:
                    if targetX - pieceX >= 0:
                        for i in range(abs(targetX - pieceX) - 1):
                            if board1[pieceX + i + 1][pieceY] != '_':
                                print("INVALID MOVE")
                                return 0
                        return 1
                    else:
                        for i in range(abs(targetX - pieceX) - 1):
                            if board1[targetX + i + 1][targetY] != '_':
                                print("INVALID MOVE")
                                return 0
                        return 1
                else:
                    return 0
            else:
                return 0

    elif board1[pieceX][pieceY] == attackingPieces[4]:
        print("404")
        if (targetY == pieceY - 1 or targetY == pieceY + 1) and (targetX == pieceX - 2 or targetX == pieceX + 2):
            return 1
        elif (targetY == pieceY - 2 or targetY == pieceY + 2) and (targetX == pieceX - 1 or targetX == pieceX + 1):
            return 1
        else:
            return 0



# moveGen for AI - Could have also used this function to check if a move is valid or not but stuck with boardCheck since it's more optimal
def moveGenerator(pieceX, pieceY, playerNo):
    possibleMoves = []
    if playerNo == 1 and board[pieceX][pieceY] == 'p':
        if pieceX+1<8:
            possibleMoves.append((pieceX+1, pieceY))
            if pieceY-1>=0:
                possibleMoves.append((pieceX+1, pieceY-1))
            if pieceY+1<8:
                possibleMoves.append((pieceX+1, pieceY+1))
        if pieceX+2<8:
            possibleMoves.append((pieceX+2, pieceY))

        return possibleMoves

    if playerNo == 2 and board[pieceX][pieceY] == 'P':
        if pieceX - 1 >= 0:
            possibleMoves.append((pieceX-1, pieceY))
            if pieceY - 1 >= 0:
                possibleMoves.append((pieceX - 1, pieceY - 1))
            if pieceY + 1 < 8:
                possibleMoves.append((pieceX - 1, pieceY + 1))
        if pieceX - 2 >= 0:
            possibleMoves.append((pieceX - 2, pieceY))

        return possibleMoves

    if board[pieceX][pieceY].lower() == 'r' or board[pieceX][pieceY].lower() == 'q':
        if pieceY+1<8:
            possibleMoves.extend([(pieceX,y) for y in range(pieceY+1,8)])
        if pieceY-1>=0:
            possibleMoves.extend([(pieceX, y) for y in range(0,pieceY)])
        if pieceX+1<8:
            possibleMoves.extend([(x, pieceY) for x in range(pieceX+1,8)])
        if pieceX-1>=0:
            possibleMoves.extend([(x, pieceY) for x in range(0,pieceX)])
        if board[pieceX][pieceY].lower() == "r":
            return possibleMoves

    if board[pieceX][pieceY].lower() == 'k':
        if pieceX+2<8:
            if pieceY+1<8:
                possibleMoves.append((pieceX+2,pieceY+1))
            if pieceY-1>=0:
                possibleMoves.append((pieceX+2,pieceY-1))
        if pieceX-2>=0:
            if pieceY + 1 < 8:
                possibleMoves.append((pieceX - 2, pieceY + 1))
            if pieceY - 1 >= 0:
                possibleMoves.append((pieceX - 2, pieceY - 1))
        if pieceY-2>=0:
            if pieceX-1>=0:
                possibleMoves.append((pieceX-1,pieceY-2))
            if pieceX+1<8:
                possibleMoves.append((pieceX+1,pieceY-2))
        if pieceY+2<8:
            if pieceX-1>=0:
                possibleMoves.append((pieceX-1,pieceY+2))
            if pieceX+1<8:
                possibleMoves.append((pieceX+1,pieceY+2))

        return possibleMoves

    if board[pieceX][pieceY].lower() == "b" or board[pieceX][pieceY].lower() == "q":
        x, y = pieceX+1, pieceY-1
        while x<8 and y>=0:
            possibleMoves.append((x, y))
            x += 1
            y -= 1
        x, y = pieceX+1, pieceY+1
        while x<8 and y<8:
            possibleMoves.append((x, y))
            x += 1
            y += 1
        x, y = pieceX - 1, pieceY - 1
        while x >= 0 and y >= 0:
            possibleMoves.append((x, y))
            x -= 1
            y -= 1
        x, y = pieceX - 1, pieceY + 1
        while x >= 0 and y < 8:
            possibleMoves.append((x, y))
            x -= 1
            y += 1

        return possibleMoves

    if board[pieceX][pieceY].lower() == "ki":
        if pieceX+1<8:
            if pieceY-1>=0:
                possibleMoves.append((pieceX+1,pieceY-1))
                possibleMoves.append((pieceX,pieceY-1))
            if pieceY+1<8:
                possibleMoves.append((pieceX + 1, pieceY + 1))
                possibleMoves.append((pieceX,pieceY+1))
            possibleMoves.append((pieceX+1,pieceY))
        if pieceX-1>=0:
            if pieceY-1>=0:
                possibleMoves.append((pieceX-1,pieceY-1))
            if pieceY+1<8:
                possibleMoves.append((pieceX-1,pieceY+1))
            possibleMoves.append((pieceX-1,pieceY))

        return possibleMoves


def getOutOfCheck(flag):
    # use boardCheck to check if opponent can make a move (If player 1 then check if player 2 can still make a move else game over.)
    # checkKingSafe if valid move found
    # Knight can jump over pieces
    # Implement diagonal checking for Queen and Bishop
    # Get array(spaces) between king and attacker
    # 1st check - try move king to either of 8 positions to avoid check
    # 2nd check - try attack the attacker
    # 3rd check - try intercept attacker by placing a piece in between attacker and king (EXCEPT IF ATTACKER = KNIGHT)
    # If all 3 checks fail declare game over

    # Get position of attacker
    # Generate array of spaces between attacker and king unless attacker is within radius of 1

    # attackerPos stores coordinates of attacking piece
    if flag == 1:
        binVal, attackerpos, kingPos = checkKingSafe(board, 2, attackingPieces2)
    else:
        binVal, attackerpos, kingPos = checkKingSafe(board, 1, attackingPieces1)
    tempBoard = copy.deepcopy(board)
    print("attacker Position: {}".format(attackerpos))
    print("King position: {}".format(kingPos))

    # 1st check
    if flag == 1:
        tempPlayer = 2
        tempAttackingPieces = attackingPieces2
        yourPieces = attackingPieces1
    else:
        tempPlayer = 1
        tempAttackingPieces = attackingPieces1
        yourPieces = attackingPieces2

    binVal1, q1, q2 = checkKingSafe(tempBoard, tempPlayer, tempAttackingPieces)

    if binVal1 == 1:

        playerSafe = 0

        eightMoves = []
        eightMoves.extend([(kingPos[0], kingPos[1] - 1), (kingPos[0], kingPos[1] + 1), (kingPos[0] - 1, kingPos[1] - 1),
                           (kingPos[0] - 1, kingPos[1]), (kingPos[0] - 1, kingPos[1] + 1), (kingPos[0] + 1, kingPos[1]),
                           (kingPos[0] + 1, kingPos[1] - 1), (kingPos[0] + 1, kingPos[1] + 1)])

        print("YOUR PIECES: ", yourPieces)
        eightMoves = [move for move in eightMoves if (0 <= move[0] < 8 and 0 <= move[1] < 8 and
                                                      ((tempBoard[move[0]][move[1]].islower() and tempBoard[kingPos[0]][
                                                          kingPos[1]].isupper()) or
                                                       (tempBoard[move[0]][move[1]].isupper() and tempBoard[kingPos[0]][
                                                           kingPos[1]].islower())))]
        print("THE MOVES:", eightMoves)
        for move in eightMoves:
            print("MOVE:", move)
            if boardCheck(tempBoard, kingPos[0], kingPos[1], move[0], move[1], tempPlayer, yourPieces) == 1:
                print("BOARD CHECK PASS FOR MOVE:", move)
                subBoard = copy.deepcopy(tempBoard)
                # validateAndMove(subBoard,kingPos[0],kingPos[1],move[0],move[1],tempPlayer,tempAttackingPieces)
                subBoard[move[0]][move[1]] = subBoard[kingPos[0]][kingPos[1]]
                subBoard[kingPos[0]][kingPos[1]] = "_"
                a, b, c = checkKingSafe(subBoard, tempPlayer, tempAttackingPieces)
                if a == 0:
                    playerSafe = 1  # Player is safe
                    print("SAFE CHECK 1")
                    break

        # 2nd check - derive structure from playerSafe variable - build position board for all pieces.

        possibleRetaliations = []
        if playerSafe == 0:
            # Get all pieces by checking in tempAttackingPieces - store coordinates - check if still in check
            for i in range(len(tempBoard)):
                for j in range(len(tempBoard[0])):
                    if tempBoard[i][j] != '_' and tempBoard[i][j] not in tempAttackingPieces:
                        possibleRetaliations.append((i, j))
                        if boardCheck(tempBoard, i, j, attackerpos[0], attackerpos[1], tempPlayer, yourPieces) == 1:
                            subBoard = copy.deepcopy(tempBoard)
                            # validateAndMove(subBoard,i,j,attackerpos[0], attackerpos[1], tempPlayer,tempAttackingPieces)
                            subBoard[i][j], subBoard[attackerpos[0]][attackerpos[1]] = "_", subBoard[i][j]
                            a, b, c = checkKingSafe(subBoard, tempPlayer, tempAttackingPieces)
                            if a == 0:
                                playerSafe = 2
                                break

        # 3rd Check - Try intercept attacker
        intermediatePositions = []
        if playerSafe == 0 and tempBoard[attackerpos[0]][attackerpos[1]].lower() != 'k':
            if attackerpos[0] < kingPos[0]:
                if attackerpos[1] > kingPos[1]:
                    yVal = attackerpos[1] - 1
                    for m in range(attackerpos[0] + 1, kingPos[0]):
                        intermediatePositions.append((m, yVal))
                        yVal -= 1

                elif attackerpos[1] == kingPos[1]:
                    for m in range(attackerpos[0] + 1, kingPos[0]):
                        intermediatePositions.append((m, kingPos[1]))

                else:
                    yVal = attackerpos[1] + 1
                    for m in range(attackerpos[0] + 1, kingPos[0]):
                        intermediatePositions.append((m, yVal))
                        yVal += 1

            elif attackerpos[0] > kingPos[0]:
                if attackerpos[1] > kingPos[1]:
                    yVal = kingPos[1] + 1
                    for m in range(kingPos[0] + 1, attackerpos[0]):
                        intermediatePositions.append((m, yVal))
                        yVal += 1

                elif attackerpos[1] == kingPos[1]:
                    for m in range(kingPos[0] + 1, attackerpos[0]):
                        intermediatePositions.append((m, kingPos[1]))

                else:
                    yVal = kingPos[1] - 1
                    for m in range(kingPos[0] + 1, attackerpos[0]):
                        intermediatePositions.append((m, yVal))
                        yVal -= 1

            else:
                if kingPos[1] < attackerpos[1]:
                    intermediatePositions[:] = [(kingPos[0], y) for y in range(kingPos[1] + 1, attackerpos[1])]
                else:
                    intermediatePositions[:] = [(kingPos[0], y) for y in range(attackerpos[1] + 1, kingPos[1])]

            for ret in possibleRetaliations:
                for pos in intermediatePositions:
                    if boardCheck(tempBoard, ret[0], ret[1], pos[0], pos[1], tempPlayer, yourPieces) == 1:
                        subBoard = copy.deepcopy(tempBoard)
                        # validateAndMove(subBoard, ret[0], ret[1], pos[0], pos[1], tempPlayer, tempAttackingPieces)
                        subBoard[ret[0]][ret[1]], subBoard[pos[0]][pos[1]] = "_", subBoard[ret[0]][ret[1]]
                        a, b, c = checkKingSafe(subBoard, tempPlayer, tempAttackingPieces)
                        if a == 0:
                            playerSafe = 3
                            break

        print("***PLAYER SAFE: {}".format(playerSafe))

        if playerSafe == 0:
            game.PrintMessage("GAME OVER")
            game.Draw(board)
            print("**************GAME OVER**************")
            time.sleep(30)
            pygame.quit()
            sys.exit(0)


#############################################################################################################################################
if __name__ == "__main__":
    game = gui.ChessGUI_pygame()
    testBoard = [['r', 'k', 'b', 'q', 'ki', 'b', 'k', 'r'],
                 ['p', 'p', 'p', 'p', 'p', 'p', 'p', 'p'],
                 ['e', 'e', 'e', 'e', 'e', 'e', 'e', 'e'],
                 ['e', 'e', 'e', 'e', 'e', 'e', 'e', 'e'],
                 ['e', 'e', 'e', 'e', 'e', 'e', 'e', 'e'],
                 ['e', 'e', 'e', 'e', 'e', 'e', 'e', 'e'],
                 ['P', 'P', 'P', 'P', 'P', 'P', 'P', 'P'],
                 ['R', 'K', 'B', 'Q', 'KI', 'B', 'K', 'R']]

    game.Draw(testBoard)
    initialise()
    play()
