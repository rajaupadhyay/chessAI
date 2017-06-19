import sys
import gui
import pygame
from pygame.locals import *
import math
import os
import copy
piecesDict = {"ROOK": "R", "KNIGHT": "K", "BISHOP": "B", "QUEEN": "Q", "KING": "KI", "PAWN": "P"}

# for k in piecesDict:
#     print(k, piecesDict[k])

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
        x=0
        while(x == 0):
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
        while (x == 0):
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
                    validateAndMove(piecePosx, piecePosy, targetPosx, targetPosy, flag, attackingPieces2)
                    checkVal = checkKingSafe(board,flag, attackingPieces1)
                    if checkVal == 1:
                        board = boardCopy
                        game.PrintMessage("INVALID (CHECKED) - {} TRY AGAIN".format(player))
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
                    game.PrintMessage("INVALID - {} TRY AGAIN".format(player))
                    occ = 1
                    counter -= 1
                else:
                    validateAndMove(piecePosx, piecePosy, targetPosx, targetPosy, flag, attackingPieces1)
                    checkVal = checkKingSafe(board, flag, attackingPieces2)
                    if checkVal == 1:
                        board = boardCopy
                        game.PrintMessage("INVALID (CHECKED) - {} TRY AGAIN".format(player))
                        print("CHECKED - PLAY TO PROTECT KING")
                        occ = 1
                        counter -= 1
            else:
                print("YOU CAN NOT MOVE YOUR OPPONENTS PIECE")

        else:
            print("NO PIECE PRESENT AT THE POSITION SPECIFIED")

        if board[targetPosx][targetPosy] == buffer and occ == 0:
            game.PrintMessage("INVALID - {} TRY AGAIN".format(player))
            counter -= 1


        counter += 1
        print("X", end=" ")
        pos = ["a", "b", "c", "d", "e", "f", "g", "h"]
        print(pos, "\n")

        for i in range(8):
            print(i + 1, end=" ")
            print(board[i])

        game.Draw(board)


def validateAndMove(pieceX, pieceY, targetX, targetY, playerNo, attackingPieces):
    if board[pieceX][pieceY] == 'p' or board[pieceX][pieceY] == 'P':
        print("000")
        if playerNo == 1:
            if board[pieceX][pieceY] == 'p':
                if targetY == pieceY:
                    if board[pieceX + 1][pieceY] == '_':
                        if pieceX == 1 and targetX == 3:
                            board[pieceX][pieceY] = '_'
                            board[targetX][targetY] = 'p'
                        elif targetX - pieceX == 1:
                            board[pieceX][pieceY] = '_'
                            board[targetX][targetY] = 'p'
                    else:
                        print("INVALID MOVE")

                elif abs(targetY - pieceY) == 1 and (targetX - pieceX) == 1:
                    if board[targetX][targetY].isupper():
                        board[pieceX][pieceY] = '_'
                        board[targetX][targetY] = 'p'

        if playerNo == 2:
            if board[pieceX][pieceY] == 'P':
                if targetY == pieceY:
                    if board[pieceX - 1][pieceY] == '_':
                        if pieceX == 6 and targetX == 4:
                            board[pieceX][pieceY] = '_'
                            board[targetX][targetY] = 'P'
                        elif targetX - pieceX == -1:
                            board[pieceX][pieceY] = '_'
                            board[targetX][targetY] = 'P'
                    else:
                        print("INVALID MOVE")

                elif abs(targetY - pieceY) == 1 and (targetX - pieceX) == -1:
                    if board[targetX][targetY].islower():
                        board[pieceX][pieceY] = '_'
                        board[targetX][targetY] = 'P'

    elif board[pieceX][pieceY] == attackingPieces[0]:
        print("101")
        if targetY == pieceY or targetY == pieceY - 1 or targetY == pieceY + 1:
            if pieceX - targetX == 1:
                board[pieceX][pieceY] = '_'
                board[targetX][targetY] = attackingPieces[0]
            elif pieceX - targetX == 0:
                board[pieceX][pieceY] = '_'
                board[targetX][targetY] = attackingPieces[0]
            elif pieceX - targetX == -1:
                board[pieceX][pieceY] = '_'
                board[targetX][targetY] = attackingPieces[0]
            else:
                print("INVALID MOVE")
        else:
            print("INVALID MOVE")

    elif board[pieceX][pieceY] == attackingPieces[1]:
        print("202")
        if targetX == pieceX:
            if targetY - pieceY >= 0:
                for i in range(abs(targetY - pieceY) - 1):
                    if board[pieceX][pieceY + i + 1] != '_':
                        print("INVALID MOVE")
                        return
                board[pieceX][pieceY] = '_'
                board[targetX][targetY] = attackingPieces[1]
            else:
                for i in range(abs(targetY - pieceY) - 1):
                    if board[targetX][targetY + i + 1] != '_':
                        print("INVALID MOVE")
                        return
                board[pieceX][pieceY] = '_'
                board[targetX][targetY] = attackingPieces[1]
        elif targetY == pieceY:
            if targetX - pieceX >= 0:
                for i in range(abs(targetX - pieceX) - 1):
                    if board[pieceX + i + 1][pieceY] != '_':
                        print("INVALID MOVE")
                        return
                board[pieceX][pieceY] = '_'
                board[targetX][targetY] = attackingPieces[1]
            else:
                for i in range(abs(targetX - pieceX) - 1):
                    if board[targetX + i + 1][targetY] != '_':
                        print("INVALID MOVE")
                        return
                board[pieceX][pieceY] = '_'
                board[targetX][targetY] = attackingPieces[1]

    elif board[pieceX][pieceY] == attackingPieces[2] or board[pieceX][pieceY] == attackingPieces[3]:
        print("303")
        buffer = board[pieceX][pieceY]
        if abs(pieceX - targetX) == abs(pieceY - targetY):
            print(pieceX, targetX)
            if targetX < pieceX:
                if targetY < pieceY:
                    for x in range(pieceX - targetX - 1):
                        if board[pieceX - x - 1][pieceY - x - 1] != '_':
                            print("INVALID MOVE")
                            return
                    board[pieceX][pieceY] = '_'
                    board[targetX][targetY] = buffer
                else:
                    for x in range(pieceX - targetX - 1):
                        if board[pieceX - x - 1][pieceY + x + 1] != '_':
                            print("INVALID MOVE")
                            return
                    board[pieceX][pieceY] = '_'
                    board[targetX][targetY] = buffer
            else:
                if targetY < pieceY:
                    for x in range(targetX - pieceX - 1):
                        if board[pieceX + x + 1][pieceY - x - 1] != '_':
                            print("INVALID MOVE")
                            return
                    board[pieceX][pieceY] = '_'
                    board[targetX][targetY] = buffer
                else:
                    for x in range(targetX - pieceX - 1):
                        if board[pieceX + x + 1][pieceY + x + 1] != '_':
                            print("INVALID MOVE")
                            return
                    board[pieceX][pieceY] = '_'
                    board[targetX][targetY] = buffer
        else:
            if board[pieceX][pieceY] == attackingPieces[3]:
                if targetX == pieceX:
                    if targetY - pieceY >= 0:
                        for i in range(abs(targetY - pieceY) - 1):
                            if board[pieceX][pieceY + i + 1] != '_':
                                print("INVALID MOVE")
                                return
                        board[pieceX][pieceY] = '_'
                        board[targetX][targetY] = attackingPieces[3]
                    else:
                        for i in range(abs(targetY - pieceY) - 1):
                            if board[targetX][targetY + i + 1] != '_':
                                print("INVALID MOVE")
                                return
                        board[pieceX][pieceY] = '_'
                        board[targetX][targetY] = attackingPieces[3]
                elif targetY == pieceY:
                    if targetX - pieceX >= 0:
                        for i in range(abs(targetX - pieceX) - 1):
                            if board[pieceX + i + 1][pieceY] != '_':
                                print("INVALID MOVE")
                                return
                        board[pieceX][pieceY] = '_'
                        board[targetX][targetY] = attackingPieces[3]
                    else:
                        for i in range(abs(targetX - pieceX) - 1):
                            if board[targetX + i + 1][targetY] != '_':
                                print("INVALID MOVE")
                                return
                        board[pieceX][pieceY] = '_'
                        board[targetX][targetY] = attackingPieces[3]
                else:
                    print("INVALID MOVE")
            else:
                print("INVALID MOVE")

    elif board[pieceX][pieceY] == attackingPieces[4]:
        print("404")
        if (targetY == pieceY - 1 or targetY == pieceY + 1) and (targetX == pieceX - 2 or targetX == pieceX + 2):
            board[pieceX][pieceY] = '_'
            board[targetX][targetY] = attackingPieces[4]
        elif (targetY == pieceY - 2 or targetY == pieceY + 2) and (targetX == pieceX - 1 or targetX == pieceX + 1):
            board[pieceX][pieceY] = '_'
            board[targetX][targetY] = attackingPieces[4]
        else:
            print("INVALID MOVE")



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
                        return 1
                if KINGY + 1 < 8:
                    if board1[KINGX+1][KINGY+1] == 'P':
                        print('here2')
                        return 1
        else:
            if KINGX - 1 >= 0:
                if KINGY - 1 >= 0:
                    if board1[KINGX - 1][KINGY - 1] == 'p':
                        return 1
                if KINGY + 1 < 8:
                    if board1[KINGX - 1][KINGY + 1] == 'p':
                        return 1

    leftY = KINGY-1
    if leftY >=0:
        while leftY>0 and board1[KINGX][leftY] == '_':
            leftY -= 1
        print(leftY)
        if board1[KINGX][leftY] == attackingPieces[1] or board1[KINGX][leftY] == attackingPieces[3]:
            print('here3')
            return 1

    rightY = KINGY+1
    if rightY<8:
        while rightY<7 and board1[KINGX][rightY] == '_':
            rightY += 1
        if board1[KINGX][rightY] == attackingPieces[1] or board1[KINGX][leftY] == attackingPieces[3]:
            print('here4')
            return 1

    top = KINGX-1
    if top>=0:
        while top>0 and board1[top][KINGY] == '_':
            top -= 1
        if board1[top][KINGY] == attackingPieces[1] or board1[top][KINGY] == attackingPieces[3]:
            print('here5')
            return 1

    bottom = KINGX+1
    if bottom <8:
        while bottom<7 and board1[bottom][KINGY] == '_':
            bottom += 1
        if board1[bottom][KINGY] == attackingPieces[1] or board1[bottom][KINGY] == attackingPieces[3]:
            print('here6')
            return 1

    # DIAGONAL CHECKS FOR OPPONENTS ATTACKING QUEEN OR BISHOP
    topDiagonalX, topRightDiagonalY = KINGX-1, KINGY+1
    if topDiagonalX>=0 and topRightDiagonalY<8:
        while topDiagonalX>0 and topRightDiagonalY<7 and board1[topDiagonalX][topRightDiagonalY] == '_':
            topDiagonalX -= 1
            topRightDiagonalY += 1
        print(topDiagonalX, topRightDiagonalY)
        if board1[topDiagonalX][topRightDiagonalY] == attackingPieces[2] or board1[topDiagonalX][topRightDiagonalY] == attackingPieces[3]:
            print('here7')
            return 1

    topDiagonalX, topLeftDiagonalY = KINGX-1, KINGY-1
    if topDiagonalX>=0 and topLeftDiagonalY>=0:
        while topDiagonalX>0 and topLeftDiagonalY>0 and board1[topDiagonalX][topLeftDiagonalY] == '_':
            topDiagonalX -= 1
            topLeftDiagonalY -= 1
        if board1[topDiagonalX][topLeftDiagonalY] == attackingPieces[2] or board1[topDiagonalX][topLeftDiagonalY] == attackingPieces[3]:
            print('here8')
            return 1

    bottomDiagonalX, bottomRightDiagonalY = KINGX+1, KINGY+1
    if bottomDiagonalX <8 and bottomRightDiagonalY<8:
        while bottomDiagonalX<7 and bottomRightDiagonalY<7 and board1[bottomDiagonalX][bottomRightDiagonalY] == '_':
            bottomDiagonalX += 1
            bottomRightDiagonalY += 1
        if board1[bottomDiagonalX][bottomRightDiagonalY] == attackingPieces[2] or board1[bottomDiagonalX][bottomRightDiagonalY] == attackingPieces[3]:
            print('here9')
            return 1

    bottomDiagonalX, bottomLeftDiagonalY = KINGX+1, KINGY-1
    if bottomDiagonalX<8 and bottomLeftDiagonalY>=0:
        while bottomDiagonalX<7 and bottomLeftDiagonalY>0 and board1[bottomDiagonalX][bottomLeftDiagonalY] == '_':
            bottomDiagonalX += 1
            bottomLeftDiagonalY -= 1
        if board1[bottomDiagonalX][bottomLeftDiagonalY] == attackingPieces[2] or board1[bottomDiagonalX][bottomLeftDiagonalY] == attackingPieces[3]:
            print('here10')
            return 1

    if KINGY-1>=0:
        if board1[KINGX][KINGY-1] == attackingPieces[0]:
            print('here11')
            return 1

    if KINGY+1<8:
        if board1[KINGX][KINGY+1] == attackingPieces[0]:
            print('here12')
            return 1

    if KINGX-1>=0:
        if KINGY-1>=0:
            if board1[KINGX-1][KINGY-1] == attackingPieces[0]:
                print('here13')
                return 1
        if KINGY+1<8:
            if board1[KINGX-1][KINGY+1] == attackingPieces[0]:
                print('here14')
                return 1
        if board1[KINGX-1][KINGY] == attackingPieces[0]:
            print('here15')
            return 1

    if KINGX+1<8:
        if board1[KINGX+1][KINGY] == attackingPieces[0]:
            print('here16')
            return 1
        if KINGY-1>=0:
            if board1[KINGX+1][KINGY-1] == attackingPieces[0]:
                print('here17')
                return 1
        if KINGY+1<8:
            if board1[KINGX+1][KINGY+1] == attackingPieces[0]:
                print('here18')
                return 1

    if KINGY-1>=0:
        if KINGX-2>=0:
            if board1[KINGX-2][KINGY-1] == attackingPieces[4]:
                print('here19')
                return 1
        if KINGX+2<8:
            if board1[KINGX+2][KINGY-1] == attackingPieces[4]:
                print('here20')
                return 1
    if KINGY-2>=0:
        if KINGX-1>=0:
            if board1[KINGX-1][KINGY-2] == attackingPieces[4]:
                print('here21')
                return 1
        if KINGX+1<8:
            if board1[KINGX+1][KINGY-2] == attackingPieces[4]:
                print('here22')
                return 1

    if KINGY+1<8:
        if KINGX-2>=0:
            if board1[KINGX-2][KINGY+1] == attackingPieces[4]:
                print('here23')
                return 1
        if KINGX+2<8:
            if board1[KINGX+2][KINGY+1] == attackingPieces[4]:
                print('here24')
                return 1

    if KINGY+2<8:
        if KINGX-1>=0:
            if board1[KINGX-1][KINGY+2] == attackingPieces[4]:
                print('here25')
                return 1
        if KINGX+1<8:
            if board1[KINGX+1][KINGY+2] == attackingPieces[4]:
                print('here26')
                return 1

    return 0


# def moveToProtect(board1,pieceX,pieceY,targetX,targetY,playerNo,attackingPieces):
#     if playerNo == 1:
#         if board[pieceX][pieceY] == 'p':
#             if targetY == pieceY:
#                 if board[pieceX + 1][pieceY] == '_':
#                     if pieceX == 1 and targetX == 3:
#                         board[pieceX][pieceY] = '_'
#                         board[targetX][targetY] = 'p'
#                     elif targetX - pieceX == 1:
#                         board[pieceX][pieceY] = '_'
#                         board[targetX][targetY] = 'p'
#                 else:
#                     print("INVALID MOVE")
#
#             elif abs(targetY - pieceY) == 1 and (targetX - pieceX) == 1:
#                 if board[targetX][targetY].isupper():
#                     board[pieceX][pieceY] = '_'
#                     board[targetX][targetY] = 'p'
#
#     if playerNo == 2:
#         if board[pieceX][pieceY] == 'P':
#             if targetY == pieceY:
#                 if board[pieceX - 1][pieceY] == '_':
#                     if pieceX == 6 and targetX == 4:
#                         board[pieceX][pieceY] = '_'
#                         board[targetX][targetY] = 'P'
#                     elif targetX - pieceX == -1:
#                         board[pieceX][pieceY] = '_'
#                         board[targetX][targetY] = 'P'
#                 else:
#                     print("INVALID MOVE")
#
#             elif abs(targetY - pieceY) == 1 and (targetX - pieceX) == -1:
#                 if board[targetX][targetY].islower():
#                     board[pieceX][pieceY] = '_'
#                     board[targetX][targetY] = 'P'
#
#
#     if board[pieceX][pieceY] == attackingPieces[0]:
#         if targetY == pieceY or targetY == pieceY - 1 or targetY == pieceY + 1:
#             if pieceX - targetX == 1:
#                 board[pieceX][pieceY] = '_'
#                 board[targetX][targetY] = attackingPieces[0]
#             elif pieceX - targetX == 0:
#                 board[pieceX][pieceY] = '_'
#                 board[targetX][targetY] = attackingPieces[0]
#             elif pieceX - targetX == -1:
#                 board[pieceX][pieceY] = '_'
#                 board[targetX][targetY] = attackingPieces[0]
#             else:
#                 print("INVALID MOVE")
#         else:
#             print("INVALID MOVE")
#
#     elif board[pieceX][pieceY] == attackingPieces[1]:
#         if targetX == pieceX:
#             if targetY - pieceY >= 0:
#                 for i in range(abs(targetY - pieceY) - 1):
#                     if board[pieceX][pieceY + i + 1] != '_':
#                         print("INVALID MOVE")
#                         return
#                 board[pieceX][pieceY] = '_'
#                 board[targetX][targetY] = attackingPieces[1]
#             else:
#                 for i in range(abs(targetY - pieceY) - 1):
#                     if board[targetX][targetY + i + 1] != '_':
#                         print("INVALID MOVE")
#                         return
#                 board[pieceX][pieceY] = '_'
#                 board[targetX][targetY] = attackingPieces[1]
#         elif targetY == pieceY:
#             if targetX - pieceX >= 0:
#                 for i in range(abs(targetX - pieceX) - 1):
#                     if board[pieceX + i + 1][pieceY] != '_':
#                         print("INVALID MOVE")
#                         return
#                 board[pieceX][pieceY] = '_'
#                 board[targetX][targetY] = attackingPieces[1]
#             else:
#                 for i in range(abs(targetX - pieceX) - 1):
#                     if board[targetX + i + 1][targetY] != '_':
#                         print("INVALID MOVE")
#                         return
#                 board[pieceX][pieceY] = '_'
#                 board[targetX][targetY] = attackingPieces[1]
#
#     elif board[pieceX][pieceY] == attackingPieces[2] or board[pieceX][pieceY] == attackingPieces[3]:
#         buffer = board[pieceX][pieceY]
#         if abs(pieceX - targetX) == abs(pieceY - targetY):
#             print(pieceX, targetX)
#             if targetX < pieceX:
#                 if targetY < pieceY:
#                     for x in range(pieceX - targetX - 1):
#                         if board[pieceX - x - 1][pieceY - x - 1] != '_':
#                             print("INVALID MOVE")
#                             return
#                     board[pieceX][pieceY] = '_'
#                     board[targetX][targetY] = buffer
#                 else:
#                     for x in range(pieceX - targetX - 1):
#                         if board[pieceX - x - 1][pieceY + x + 1] != '_':
#                             print("INVALID MOVE")
#                             return
#                     board[pieceX][pieceY] = '_'
#                     board[targetX][targetY] = buffer
#             else:
#                 if targetY < pieceY:
#                     for x in range(targetX - pieceX - 1):
#                         if board[pieceX + x + 1][pieceY - x - 1] != '_':
#                             print("INVALID MOVE")
#                             return
#                     board[pieceX][pieceY] = '_'
#                     board[targetX][targetY] = buffer
#                 else:
#                     for x in range(targetX - pieceX - 1):
#                         if board[pieceX + x + 1][pieceY + x + 1] != '_':
#                             print("INVALID MOVE")
#                             return
#                     board[pieceX][pieceY] = '_'
#                     board[targetX][targetY] = buffer
#         else:
#             if board[pieceX][pieceY] == attackingPieces[3]:
#                 if targetX == pieceX:
#                     if targetY - pieceY >= 0:
#                         for i in range(abs(targetY - pieceY) - 1):
#                             if board[pieceX][pieceY + i + 1] != '_':
#                                 print("INVALID MOVE")
#                                 return
#                         board[pieceX][pieceY] = '_'
#                         board[targetX][targetY] = attackingPieces[3]
#                     else:
#                         for i in range(abs(targetY - pieceY) - 1):
#                             if board[targetX][targetY + i + 1] != '_':
#                                 print("INVALID MOVE")
#                                 return
#                         board[pieceX][pieceY] = '_'
#                         board[targetX][targetY] = attackingPieces[3]
#                 elif targetY == pieceY:
#                     if targetX - pieceX >= 0:
#                         for i in range(abs(targetX - pieceX) - 1):
#                             if board[pieceX + i + 1][pieceY] != '_':
#                                 print("INVALID MOVE")
#                                 return
#                         board[pieceX][pieceY] = '_'
#                         board[targetX][targetY] = attackingPieces[3]
#                     else:
#                         for i in range(abs(targetX - pieceX) - 1):
#                             if board[targetX + i + 1][targetY] != '_':
#                                 print("INVALID MOVE")
#                                 return
#                         board[pieceX][pieceY] = '_'
#                         board[targetX][targetY] = attackingPieces[3]
#                 else:
#                     print("INVALID MOVE")
#             else:
#                 print("INVALID MOVE")
#
#     elif board[pieceX][pieceY] == attackingPieces[4]:
#         if (targetY == pieceY - 1 or targetY == pieceY + 1) and (targetX == pieceX - 2 or targetX == pieceX + 2):
#             board[pieceX][pieceY] = '_'
#             board[targetX][targetY] = attackingPieces[4]
#         elif (targetY == pieceY - 2 or targetY == pieceY + 2) and (targetX == pieceX - 1 or targetX == pieceX + 1):
#             board[pieceX][pieceY] = '_'
#             board[targetX][targetY] = attackingPieces[4]
#         else:
#             print("INVALID MOVE")


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
