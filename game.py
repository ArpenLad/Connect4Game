from circle import Circle
from Player import Player
import pygame as pg
import math

# Constants
RADIUS = 40
COL = 7
ROW = 6
SCREENWIDTH = 760
SCREENHEIGHT = 700
USERCIRCLESTARTX = 80
USERCIRCLEY = 50
USERCIRCLEXGAP = 100

# pygame initial config
pg.init()
gameScreen = pg.display.set_mode((SCREENWIDTH, SCREENHEIGHT))
pg.display.set_caption("Connect 4")
pgRunning = True
# text
font32 = pg.font.SysFont("arialunicode", 32)
font24 = pg.font.SysFont("arialunicode", 24)


# generate the circles for user checkers
def getClickableCircle():
    x = USERCIRCLESTARTX
    y = USERCIRCLEY
    color = "darkgray"
    circles = []
    for i in range(COL):
        x1 = x + i * 100
        circles.append(Circle(x1, y, RADIUS, shift=0, color=color))

    return circles


# Display the footer board
def displayFooterBar(player1, player2):
    # player's color
    pg.draw.rect(gameScreen, color="black", rect=pg.Rect(0, 760, 760, 100))
    playerText1 = font24.render(f'Player 1: {player1.color}', True, player1.color)
    playerText2 = font24.render(f'Player 2: {player2.color}', True, player2.color)
    pTextRect1 = playerText1.get_rect()
    pTextRect2 = playerText2.get_rect()

    pTextRect1.top = 772
    pTextRect2.top = 812
    pTextRect1.left = pTextRect2.left = 20

    gameScreen.blit(playerText1, pTextRect1)
    gameScreen.blit(playerText2, pTextRect2)


# Display the game board
def display_board(board, player1, player2, clickableCircle, gameOver, text=None):
    pg.draw.rect(gameScreen, color="blue", rect=pg.Rect(0, 100, 760, 660))

    if not gameOver:
        for c in clickableCircle:
            c.display_circle(gameScreen, doShift=False)

    for c in board:
        c.display_circle(gameScreen, doShift=True)

    if gameOver:
        for c in clickableCircle:
            c.display_circle(gameScreen, doShift=False)
        textRect = text.get_rect()
        textRect.center = (SCREENWIDTH / 2, 50)
        gameScreen.blit(text, textRect)

    # status bar display player's color and stuff
    displayFooterBar(player1, player2)


# Get all circles at give column(X)
def getAllCirclesFromX(clickedX, board):
    circles = []
    for c in board:
        if c.x == clickedX and not c.hasCheker:
            circles.append(c)
    return circles


# Adding checkers to the available position of the board
def getCircleFromXANDY(x, y, board):
    for c in board:
        if c.x == x and c.y == y:
            return c
    return None


def checkForResult(circle, board):
    response = {
        "gameOver": False,
        "msg": None
    }
    gameOver = False
    draw = False
    matched = False
    allCirclesCovered = True

    # Draw condition
    for c in board:
        if not c.hasCheker:
            allCirclesCovered = False
            break

    if allCirclesCovered:
        response["gameOver"] = True
        response["msg"] = "Drawn"
        return response

    # check the horizontal
    if (circle.x + 3) < COL:
        matched = circle.color == getCircleFromXANDY(circle.x + 1, circle.y, board).color and \
                  getCircleFromXANDY(circle.x + 1, circle.y, board).color == getCircleFromXANDY(circle.x + 2, circle.y,
                                                                                                board).color and \
                  getCircleFromXANDY(circle.x + 2, circle.y, board).color == getCircleFromXANDY(circle.x + 3, circle.y,
                                                                                                board).color

    if not matched and (circle.x - 3) >= 0:
        matched = circle.color == getCircleFromXANDY(circle.x - 1, circle.y, board).color and \
                  getCircleFromXANDY(circle.x - 1, circle.y, board).color == getCircleFromXANDY(circle.x - 2, circle.y,
                                                                                                board).color and \
                  getCircleFromXANDY(circle.x - 2, circle.y, board).color == getCircleFromXANDY(circle.x - 3, circle.y,
                                                                                                board).color

    if matched:
        response["gameOver"] = True
        response["msg"] = "Win"
        return response

    # check the vertical
    if (circle.y + 3) < ROW:
        matched = circle.color == getCircleFromXANDY(circle.x, circle.y + 1, board).color and \
                  getCircleFromXANDY(circle.x, circle.y + 1, board).color == getCircleFromXANDY(circle.x, circle.y + 2,
                                                                                                board).color and \
                  getCircleFromXANDY(circle.x, circle.y + 2, board).color == getCircleFromXANDY(circle.x, circle.y + 3,
                                                                                                board).color

    if not matched and (circle.y - 3) >= 0:
        matched = circle.color == getCircleFromXANDY(circle.x, circle.y - 1, board).color and \
                  getCircleFromXANDY(circle.x, circle.y - 1, board).color == getCircleFromXANDY(circle.x, circle.y - 2,
                                                                                                board).color and \
                  getCircleFromXANDY(circle.x, circle.y - 2, board).color == getCircleFromXANDY(circle.x, circle.y - 3,
                                                                                                board).color

    if matched:
        response["gameOver"] = True
        response["msg"] = "Win"
        return response

    # check diagonally
    if circle.x - 3 >= 0 and circle.y - 3 >= 0:
        matched = circle.color == getCircleFromXANDY(circle.x - 1, circle.y - 1, board).color and \
                  getCircleFromXANDY(circle.x - 1, circle.y - 1, board).color == getCircleFromXANDY(circle.x - 2,
                                                                                                    circle.y - 2,
                                                                                                    board).color and \
                  getCircleFromXANDY(circle.x - 2, circle.y - 2, board).color == getCircleFromXANDY(circle.x - 3,
                                                                                                    circle.y - 3,
                                                                                                    board).color

    if not matched and circle.x + 3 < COL and circle.y + 3 < ROW:
        matched = circle.color == getCircleFromXANDY(circle.x + 1, circle.y + 1, board).color and \
                  getCircleFromXANDY(circle.x + 1, circle.y + 1, board).color == getCircleFromXANDY(circle.x + 2,
                                                                                                    circle.y + 2,
                                                                                                    board).color and \
                  getCircleFromXANDY(circle.x + 2, circle.y + 2, board).color == getCircleFromXANDY(circle.x + 3,
                                                                                                    circle.y + 3,
                                                                                                    board).color

    if not matched and circle.x + 3 < COL and circle.y - 3 >= 0:
        matched = circle.color == getCircleFromXANDY(circle.x + 1, circle.y - 1, board).color and \
                  getCircleFromXANDY(circle.x + 1, circle.y - 1, board).color == getCircleFromXANDY(circle.x + 2,
                                                                                                    circle.y - 2,
                                                                                                    board).color and \
                  getCircleFromXANDY(circle.x + 2, circle.y - 2, board).color == getCircleFromXANDY(circle.x + 3,
                                                                                                    circle.y - 3,
                                                                                                    board).color

    if not matched and circle.x - 3 >= 0 and circle.y + 3 < ROW:
        matched = circle.color == getCircleFromXANDY(circle.x - 1, circle.y + 1, board).color and \
                  getCircleFromXANDY(circle.x - 1, circle.y + 1, board).color == getCircleFromXANDY(circle.x - 2,
                                                                                                    circle.y + 2,
                                                                                                    board).color and \
                  getCircleFromXANDY(circle.x - 2, circle.y + 2, board).color == getCircleFromXANDY(circle.x - 3,
                                                                                                    circle.y + 3,
                                                                                                    board).color
    if matched:
        response["gameOver"] = True
        response["msg"] = "Win"
        return response

    return response


def insertChecker(clickedX, clickedY, board, clickableCircle, player):
    response = {
        "inserted": False,
        "gameOver": False,
        "msg": None
    }
    x = clickedX
    for c in clickableCircle:
        collided = c.pgCircle.collidepoint((clickedX, clickedY))
        if collided:
            x = math.floor((c.x - USERCIRCLESTARTX) / USERCIRCLEXGAP)

    eligbleCircles = getAllCirclesFromX(x, board)
    eligbleCircles.reverse()
    text = ""
    for c in eligbleCircles:
        if not c.hasCheker:
            c.hasCheker = True
            c.color = player.color
            results = checkForResult(c, board)
            gameOver = results['gameOver']
            if gameOver:
                if results['msg'] != 'Drawn':
                    text = font32.render(f'{currentPlayer.name} is Winner...', True, "green")
                else:
                    text = font32.render('Match drawn', True, "green")

            response["inserted"] = True
            response["gameOver"] = results['gameOver']
            response["msg"] = text
            return response
    return response


# changing Circle color to current player
def changeCircleColor(clickableCircle, mouseX, mouseY, player):
    for c in clickableCircle:
        collided = c.pgCircle.collidepoint((mouseX, mouseY))
        if collided:
            c.color = player.color
        else:
            c.color = "darkgray"


if __name__ == '__main__':
    board = [Circle(i, j, RADIUS, shift=100) for i in range(COL) for j in range(ROW)]
    clickableCircle = getClickableCircle()

    # screen background to white
    gameScreen.fill("darkgray")

    # Creating players
    p1 = Player("Red", "Player 1")
    p2 = Player("Yellow", "Player 2")
    currentPlayer = p1

    gameOver = False
    msg = None

    while pgRunning:

        for event in pg.event.get():
            # Close the screen
            if event.type == pg.QUIT:
                pgRunning = False
                continue

            # Show the checker on the top of board
            if not gameOver and event.type == pg.MOUSEMOTION:
                mouseX, mouseY = pg.mouse.get_pos()
                changeCircleColor(clickableCircle, mouseX, mouseY, currentPlayer)

            # Add the checker into board and check for winning
            if not gameOver and event.type == pg.MOUSEBUTTONUP:
                clickedX, clickedY = pg.mouse.get_pos()
                insertResponse = insertChecker(clickedX, clickedY, board, clickableCircle, currentPlayer)
                inserted, gameOver, msg = insertResponse["inserted"], insertResponse["gameOver"], insertResponse["msg"]
                if inserted and not gameOver:
                    currentPlayer = p2 if currentPlayer == p1 else p1
                    changeCircleColor(clickableCircle, clickedX, clickedY, currentPlayer)
                if gameOver:
                    for c in clickableCircle:
                        c.color = "darkgray"

        display_board(board, p1, p2, clickableCircle, gameOver, msg)
        pg.display.flip()

    pg.quit()
