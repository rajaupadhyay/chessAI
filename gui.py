# THIS IS A GUI IMPLEMENTATION OF A CHESS BOARD DONE BY Steve Osborne - I have modified a bit
import pygame
import os
import sys
from pygame.locals import *
from ScrollingTextBox import ScrollingTextBox
import math
import main


class ChessGUI_pygame:
    def __init__(self, graphicStyle=1):
        os.environ['SDL_VIDEO_CENTERED'] = '1'  # should center pygame window on the screen
        pygame.init()
        pygame.display.init()
        self.screen = pygame.display.set_mode((850, 500))
        self.boardStart_x = 50
        self.boardStart_y = 50
        pygame.display.set_caption('Python Chess')
        self.textBox = ScrollingTextBox(self.screen, 525, 825, 50, 450)
        self.LoadImages(graphicStyle)
        # pygame.font.init() - should be already called by pygame.init()
        self.fontDefault = pygame.font.Font(None, 20)
        self.PrintMessage("WHITE STARTS")

    def LoadImages(self, graphicStyle):
        if graphicStyle == 0:
            self.square_size = 50  # all images must be images 50 x 50 pixels
            self.white_square = pygame.image.load(os.path.join("images", "white_square.png")).convert()
            self.brown_square = pygame.image.load(os.path.join("images", "brown_square.png")).convert()
            self.cyan_square = pygame.image.load(os.path.join("images", "cyan_square.png")).convert()
            # "convert()" is supposed to help pygame display the images faster.  It seems to mess up transparency - makes it all black!
            # And, for this chess program, the images don't need to change that fast.
            self.black_pawn = pygame.image.load(os.path.join("images", "blackPawn.png"))
            self.black_rook = pygame.image.load(os.path.join("images", "blackRook.png"))
            self.black_knight = pygame.image.load(os.path.join("images", "blackKnight.png"))
            self.black_bishop = pygame.image.load(os.path.join("images", "blackBishop.png"))
            self.black_king = pygame.image.load(os.path.join("images", "blackKing.png"))
            self.black_queen = pygame.image.load(os.path.join("images", "blackQueen.png"))
            self.white_pawn = pygame.image.load(os.path.join("images", "whitePawn.png"))
            self.white_rook = pygame.image.load(os.path.join("images", "whiteRook.png"))
            self.white_knight = pygame.image.load(os.path.join("images", "whiteKnight.png"))
            self.white_bishop = pygame.image.load(os.path.join("images", "whiteBishop.png"))
            self.white_king = pygame.image.load(os.path.join("images", "whiteKing.png"))
            self.white_queen = pygame.image.load(os.path.join("images", "whiteQueen.png"))
        elif graphicStyle == 1:
            self.square_size = 50
            self.white_square = pygame.image.load(os.path.join("images", "white_square.png")).convert()
            self.brown_square = pygame.image.load(os.path.join("images", "brown_square.png")).convert()
            self.cyan_square = pygame.image.load(os.path.join("images", "cyan_square.png")).convert()

            self.black_pawn = pygame.image.load(os.path.join("images", "Chess_tile_pd.png")).convert()
            self.black_pawn = pygame.transform.scale(self.black_pawn, (self.square_size, self.square_size))
            self.black_rook = pygame.image.load(os.path.join("images", "Chess_tile_rd.png")).convert()
            self.black_rook = pygame.transform.scale(self.black_rook, (self.square_size, self.square_size))
            self.black_knight = pygame.image.load(os.path.join("images", "Chess_tile_nd.png")).convert()
            self.black_knight = pygame.transform.scale(self.black_knight, (self.square_size, self.square_size))
            self.black_bishop = pygame.image.load(os.path.join("images", "Chess_tile_bd.png")).convert()
            self.black_bishop = pygame.transform.scale(self.black_bishop, (self.square_size, self.square_size))
            self.black_king = pygame.image.load(os.path.join("images", "Chess_tile_kd.png")).convert()
            self.black_king = pygame.transform.scale(self.black_king, (self.square_size, self.square_size))
            self.black_queen = pygame.image.load(os.path.join("images", "Chess_tile_qd.png")).convert()
            self.black_queen = pygame.transform.scale(self.black_queen, (self.square_size, self.square_size))

            self.white_pawn = pygame.image.load(os.path.join("images", "Chess_tile_pl.png")).convert()
            self.white_pawn = pygame.transform.scale(self.white_pawn, (self.square_size, self.square_size))
            self.white_rook = pygame.image.load(os.path.join("images", "Chess_tile_rl.png")).convert()
            self.white_rook = pygame.transform.scale(self.white_rook, (self.square_size, self.square_size))
            self.white_knight = pygame.image.load(os.path.join("images", "Chess_tile_nl.png")).convert()
            self.white_knight = pygame.transform.scale(self.white_knight, (self.square_size, self.square_size))
            self.white_bishop = pygame.image.load(os.path.join("images", "Chess_tile_bl.png")).convert()
            self.white_bishop = pygame.transform.scale(self.white_bishop, (self.square_size, self.square_size))
            self.white_king = pygame.image.load(os.path.join("images", "Chess_tile_kl.png")).convert()
            self.white_king = pygame.transform.scale(self.white_king, (self.square_size, self.square_size))
            self.white_queen = pygame.image.load(os.path.join("images", "Chess_tile_ql.png")).convert()
            self.white_queen = pygame.transform.scale(self.white_queen, (self.square_size, self.square_size))

    def PrintMessage(self, message):
        # prints a string to the area to the right of the board
        self.textBox.Add(message)
        self.textBox.Draw()

    def ConvertToScreenCoords(self, chessSquareTuple):
        # converts a (row,col) chessSquare into the pixel location of the upper-left corner of the square
        (row, col) = chessSquareTuple
        screenX = self.boardStart_x + col * self.square_size
        screenY = self.boardStart_y + row * self.square_size
        return (screenX, screenY)

    def ConvertToChessCoords(self, screenPositionTuple):
        # converts a screen pixel location (X,Y) into a chessSquare tuple (row,col)
        # x is horizontal, y is vertical
        # (x=0,y=0) is upper-left corner of the screen
        (X, Y) = screenPositionTuple
        row = (Y - self.boardStart_y) / self.square_size
        col = (X - self.boardStart_x) / self.square_size
        return (row, col)

    def Draw(self, board):
        self.screen.fill((0, 0, 0))
        self.textBox.Draw()
        boardSize = len(board)

        # draw blank board
        current_square = 0
        for r in range(boardSize):
            for c in range(boardSize):
                (screenX, screenY) = self.ConvertToScreenCoords((r, c))
                if current_square:
                    self.screen.blit(self.brown_square, (screenX, screenY))

                else:
                    self.screen.blit(self.white_square, (screenX, screenY))

                current_square = (current_square + 1) % 2

            current_square = (current_square + 1) % 2

        # draw row/column labels around the edge of the board
        # chessboard_obj = ChessBoard(0)  # need a dummy object to access some of ChessBoard's methods....
        color = (255, 255, 255)  # white
        antialias = 1

        # top and bottom - display cols
        for c in range(boardSize):
            for r in [-1, boardSize]:
                (screenX, screenY) = self.ConvertToScreenCoords((r, c))
                screenX = screenX + self.square_size / 2
                screenY = screenY + self.square_size / 2
                # notation = chessboard_obj.ConvertToAlgebraicNotation_col(c)
                # renderedLine = self.fontDefault.render(notation, antialias, color)
                # self.screen.blit(renderedLine, (screenX, screenY))

        # left and right - display rows
        for r in range(boardSize):
            for c in [-1, boardSize]:
                (screenX, screenY) = self.ConvertToScreenCoords((r, c))
                screenX = screenX + self.square_size / 2
                screenY = screenY + self.square_size / 2
                # notation = chessboard_obj.ConvertToAlgebraicNotation_row(r)
                # renderedLine = self.fontDefault.render(notation, antialias, color)
                # self.screen.blit(renderedLine, (screenX, screenY))

        # highlight squares if specified
        # for square in highlightSquares:
        #     (screenX, screenY) = self.ConvertToScreenCoords(square)
        #     self.screen.blit(self.cyan_square, (screenX, screenY))

        # draw pieces
        for r in range(boardSize):
            for c in range(boardSize):
                (screenX, screenY) = self.ConvertToScreenCoords((r, c))
                if board[r][c] == 'P':
                    self.screen.blit(self.black_pawn, (screenX, screenY))
                if board[r][c] == 'R':
                    self.screen.blit(self.black_rook, (screenX, screenY))
                if board[r][c] == 'K':
                    self.screen.blit(self.black_knight, (screenX, screenY))
                if board[r][c] == 'B':
                    self.screen.blit(self.black_bishop, (screenX, screenY))
                if board[r][c] == 'Q':
                    self.screen.blit(self.black_queen, (screenX, screenY))
                if board[r][c] == 'KI':
                    self.screen.blit(self.black_king, (screenX, screenY))
                if board[r][c] == 'p':
                    self.screen.blit(self.white_pawn, (screenX, screenY))
                if board[r][c] == 'r':
                    self.screen.blit(self.white_rook, (screenX, screenY))
                if board[r][c] == 'k':
                    self.screen.blit(self.white_knight, (screenX, screenY))
                if board[r][c] == 'b':
                    self.screen.blit(self.white_bishop, (screenX, screenY))
                if board[r][c] == 'q':
                    self.screen.blit(self.white_queen, (screenX, screenY))
                if board[r][c] == 'ki':
                    self.screen.blit(self.white_king, (screenX, screenY))

        pygame.display.flip()


    def GetClickedSquare(self, mouseX, mouseY):
        # test function
        # print
        # "User clicked screen position x =", mouseX, "y =", mouseY
        (row, col) = self.ConvertToChessCoords((mouseX, mouseY))
        if col < 8 and col >= 0 and row < 8 and row >= 0:
            print("  Chess board units row =", math.floor(row), "col =", math.floor(col))
            return row, col
        else:
            return -1, -1


if __name__ == "__main__":
    # try out some development / testing stuff if this file is run directly
    testBoard = [['R', 'K', 'B', 'Q', 'KI', 'B', 'K', 'R'], \
                 ['P', 'P', 'P', 'P', 'P', 'P', 'P', 'P'], \
                 ['e', 'e', 'e', 'e', 'e', 'e', 'e', 'e'], \
                 ['e', 'e', 'e', 'e', 'e', 'e', 'e', 'e'], \
                 ['e', 'e', 'e', 'e', 'e', 'e', 'e', 'e'], \
                 ['e', 'e', 'e', 'e', 'e', 'e', 'e', 'e'], \
                 ['p', 'p', 'p', 'p', 'p', 'p', 'p', 'p'], \
                 ['r', 'k', 'b', 'q', 'ki', 'b', 'k', 'r']]

    game = ChessGUI_pygame()

    # main.play()
    game.Draw(testBoard)
    # game.TestRoutine()
