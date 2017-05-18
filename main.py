import sys

piecesDict = {"ROOK": "R", "KNIGHT": "K", "BISHOP": "B", "QUEEN": "Q", "KING": "KI", "PAWN": "P"}

for k in piecesDict:
    print(k, piecesDict[k])

counter = 0
board = []
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


def play():
    while(True): # Implement while(boardCheck()) where boardCheck() checks if game has ended
        global counter
        if counter % 2 == 0:
            print("PLAYER 1s TURN (WHITE)")
            flag = 1
        else:
            print("PLAYER 2s TURN (BLACK)")
            flag = 2

        # GET USER INPUT - piece coordinates and the target coordinates - b7b5
        stringVal = str(input())
        piecePosy = ord(stringVal[0]) - ord('a')
        piecePosx = int(stringVal[1]) - 1
        targetPosy = ord(stringVal[2]) - ord('a')
        targetPosx = int(stringVal[3]) - 1
        # CHECK IF POSITIONS DEFINED ARE VALID

        if board[piecePosx][piecePosy] != '_' and flag == 1:
            if board[piecePosx][piecePosy].islower():
                # Logic for moving to target pos (new func)
                if board[targetPosx][targetPosy].islower() and board[targetPosx][targetPosy] != '_':
                    print("CAN NOT MOVE PIECE TO SPECIFIED COORDINATES (PREOCCUPIED BY YOUR PIECE)")
                else:
                    validateAndMove(piecePosx, piecePosy, targetPosx, targetPosy, flag)
            else:
                print("YOU CAN NOT MOVE YOUR OPPONENTS PIECE")

        elif board[piecePosx][piecePosy] != '_' and flag == 2:
            if board[piecePosx][piecePosy].isupper():
                # Logic for moving to target pos (new func)
                if board[targetPosx][targetPosy].isupper():
                    print("CAN NOT MOVE PIECE TO SPECIFIED COORDINATES (PREOCCUPIED BY YOUR PIECE)")
                else:
                    validateAndMove(piecePosx, piecePosy, targetPosx, targetPosy, flag)
            else:
                print("YOU CAN NOT MOVE YOUR OPPONENTS PIECE")

        else:
            print("NO PIECE PRESENT AT THE POSITION SPECIFIED")

        counter += 1
        print("X", end=" ")
        pos = ["a", "b", "c", "d", "e", "f", "g", "h"]
        print(pos, "\n")

        for i in range(8):
            print(i + 1, end=" ")
            print(board[i])


def validateAndMove(pieceX, pieceY, targetX, targetY, playerNo):
    if playerNo == 1:
        if board[pieceX][pieceY] == 'p':
            if targetY == pieceY:
                if board[pieceX+1][pieceY] == '_':
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

        elif board[pieceX][pieceY] == 'ki':
            if targetY == pieceY or targetY == pieceY-1 or targetY == pieceY+1:
                if pieceX - targetX == 1:
                    board[pieceX][pieceY] = '_'
                    board[targetX][targetY] = 'ki'
                elif pieceX - targetX == 0:
                    board[pieceX][pieceY] = '_'
                    board[targetX][targetY] = 'ki'
                elif pieceX - targetX == -1:
                    board[pieceX][pieceY] = '_'
                    board[targetX][targetY] = 'ki'
                else:
                    print("INVALID MOVE")
            else:
                print("INVALID MOVE")

        elif board[pieceX][pieceY] == 'r':
            if targetX == pieceX:
                if targetY - pieceY >= 0:
                    for i in range(abs(targetY-pieceY)-1):
                        if board[pieceX][pieceY+i+1] != '_':
                            print("INVALID MOVE")
                            return
                    board[pieceX][pieceY] = '_'
                    board[targetX][targetY] = 'r'
                else:
                    for i in range(abs(targetY - pieceY) - 1):
                        if board[targetX][targetY+i+1] != '_':
                            print("INVALID MOVE")
                            return
                    board[pieceX][pieceY] = '_'
                    board[targetX][targetY] = 'r'
            elif targetY == pieceY:
                if targetX - pieceX >= 0:
                    for i in range(abs(targetX-pieceX)-1):
                        if board[pieceX+i+1][pieceY] != '_':
                            print("INVALID MOVE")
                            return
                    board[pieceX][pieceY] = '_'
                    board[targetX][targetY] = 'r'
                else:
                    for i in range(abs(targetX - pieceX) - 1):
                        if board[targetX+i+1][targetY] != '_':
                            print("INVALID MOVE")
                            return
                    board[pieceX][pieceY] = '_'
                    board[targetX][targetY] = 'r'

        elif board[pieceX][pieceY] == 'b' or board[pieceX][pieceY] == 'q':
            buffer = board[pieceX][pieceY]
            if abs(pieceX-targetX) == abs(pieceY-targetY):
                print(pieceX, targetX)
                if targetX < pieceX:
                    if targetY < pieceY:
                        for x in range(pieceX - targetX - 1):
                            if board[pieceX-x-1][pieceY-x-1] != '_':
                                print("INVALID MOVE")
                                return
                        board[pieceX][pieceY] = '_'
                        board[targetX][targetY] = buffer
                    else:
                        for x in range(pieceX - targetX - 1):
                            if board[pieceX-x-1][pieceY+x+1] != '_':
                                print("INVALID MOVE")
                                return
                        board[pieceX][pieceY] = '_'
                        board[targetX][targetY] = buffer
                else:
                    if targetY < pieceY:
                        print("YES")
                        for x in range(targetX - pieceX - 1):
                            if board[pieceX+x+1][pieceY-x-1] != '_':
                                print("INVALID MOVE")
                                return
                        board[pieceX][pieceY] = '_'
                        board[targetX][targetY] = buffer
                    else:
                        for x in range(targetX - pieceX - 1):
                            if board[pieceX+x+1][pieceY+x+1] != '_':
                                print("INVALID MOVE")
                                return
                        board[pieceX][pieceY] = '_'
                        board[targetX][targetY] = buffer
            else:
                if board[pieceX][pieceY] == 'q':
                    if targetX == pieceX:
                        if targetY - pieceY >= 0:
                            for i in range(abs(targetY - pieceY) - 1):
                                if board[pieceX][pieceY + i + 1] != '_':
                                    print("INVALID MOVE")
                                    return
                            board[pieceX][pieceY] = '_'
                            board[targetX][targetY] = 'q'
                        else:
                            for i in range(abs(targetY - pieceY) - 1):
                                if board[targetX][targetY + i + 1] != '_':
                                    print("INVALID MOVE")
                                    return
                            board[pieceX][pieceY] = '_'
                            board[targetX][targetY] = 'q'
                    elif targetY == pieceY:
                        if targetX - pieceX >= 0:
                            for i in range(abs(targetX - pieceX) - 1):
                                if board[pieceX + i + 1][pieceY] != '_':
                                    print("INVALID MOVE")
                                    return
                            board[pieceX][pieceY] = '_'
                            board[targetX][targetY] = 'q'
                        else:
                            for i in range(abs(targetX - pieceX) - 1):
                                if board[targetX + i + 1][targetY] != '_':
                                    print("INVALID MOVE")
                                    return
                            board[pieceX][pieceY] = '_'
                            board[targetX][targetY] = 'q'
                    else:
                        print("INVALID MOVE")
                else:
                    print("INVALID MOVE")

        elif board[pieceX][pieceY] == 'k':
            if (targetY == pieceY - 1 or targetY == pieceY + 1) and (targetX == pieceX - 2 or targetX == pieceX + 2):
                board[pieceX][pieceY] = '_'
                board[targetX][targetY] = 'k'
            elif (targetY == pieceY - 2 or targetY == pieceY + 2) and (targetX == pieceX - 1 or targetX == pieceX + 1):
                board[pieceX][pieceY] = '_'
                board[targetX][targetY] = 'k'
            else:
                print("INVALID MOVE")








##################################### PLAYER 2 ############################################

    else:
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

        elif board[pieceX][pieceY] == 'KI':
            if targetY == pieceY or targetY == pieceY - 1 or targetY == pieceY + 1:
                if pieceX - targetX == 1:
                    board[pieceX][pieceY] = '_'
                    board[targetX][targetY] = 'KI'
                elif pieceX - targetX == 0:
                    board[pieceX][pieceY] = '_'
                    board[targetX][targetY] = 'KI'
                elif pieceX - targetX == -1:
                    board[pieceX][pieceY] = '_'
                    board[targetX][targetY] = 'KI'
                else:
                    print("INVALID MOVE")
            else:
                print("INVALID MOVE")

        elif board[pieceX][pieceY] == 'R':
            if targetX == pieceX:
                if targetY - pieceY >= 0:
                    for i in range(abs(targetY - pieceY) - 1):
                        if board[pieceX][pieceY + i + 1] != '_':
                            print("INVALID MOVE")
                            return
                    board[pieceX][pieceY] = '_'
                    board[targetX][targetY] = 'R'
                else:
                    for i in range(abs(targetY - pieceY) - 1):
                        if board[targetX][targetY + i + 1] != '_':
                            print("INVALID MOVE")
                            return
                    board[pieceX][pieceY] = '_'
                    board[targetX][targetY] = 'R'
            elif targetY == pieceY:
                if targetX - pieceX < 0:
                    for i in range(abs(targetX - pieceX) - 1):
                        if board[pieceX - i - 1][pieceY] != '_':
                            print("INVALID MOVE")
                            return
                    board[pieceX][pieceY] = '_'
                    board[targetX][targetY] = 'R'
                else:
                    for i in range(abs(targetX - pieceX) - 1):
                        if board[targetX - i - 1][targetY] != '_':
                            print("INVALID MOVE")
                            return
                    board[pieceX][pieceY] = '_'
                    board[targetX][targetY] = 'R'

        elif board[pieceX][pieceY] == 'B' or board[pieceX][pieceY] == 'Q':
            buffer = board[pieceX][pieceY]
            if abs(pieceX - targetX) == abs(pieceY - targetY):
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
                if board[pieceX][pieceY] == 'Q':
                    if targetX == pieceX:
                        if targetY - pieceY >= 0:
                            for i in range(abs(targetY - pieceY) - 1):
                                if board[pieceX][pieceY + i + 1] != '_':
                                    print("INVALID MOVE")
                                    return
                            board[pieceX][pieceY] = '_'
                            board[targetX][targetY] = 'Q'
                        else:
                            for i in range(abs(targetY - pieceY) - 1):
                                if board[targetX][targetY + i + 1] != '_':
                                    print("INVALID MOVE")
                                    return
                            board[pieceX][pieceY] = '_'
                            board[targetX][targetY] = 'Q'
                    elif targetY == pieceY:
                        if targetX - pieceX < 0:
                            for i in range(abs(targetX - pieceX) - 1):
                                if board[pieceX - i - 1][pieceY] != '_':
                                    print("INVALID MOVE")
                                    return
                            board[pieceX][pieceY] = '_'
                            board[targetX][targetY] = 'Q'
                        else:
                            for i in range(abs(targetX - pieceX) - 1):
                                if board[targetX - i - 1][targetY] != '_':
                                    print("INVALID MOVE")
                                    return
                            board[pieceX][pieceY] = '_'
                            board[targetX][targetY] = 'Q'
                    else:
                        print("INVALID MOVE")
                else:
                    print("INVALID MOVE")

        elif board[pieceX][pieceY] == 'K':
            if (targetY == pieceY - 1 or targetY == pieceY + 1) and (targetX == pieceX - 2 or targetX == pieceX + 2):
                board[pieceX][pieceY] = '_'
                board[targetX][targetY] = 'K'
            elif (targetY == pieceY - 2 or targetY == pieceY + 2) and (targetX == pieceX - 1 or targetX == pieceX + 1):
                board[pieceX][pieceY] = '_'
                board[targetX][targetY] = 'K'
            else:
                print("INVALID MOVE")


if __name__ == "__main__":
    initialise()
    play()
