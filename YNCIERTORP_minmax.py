import pygame
import sys
from pygame.locals import *
import math
import copy

size = 3

# ------------------------ Splash Screen ------------------------
def splashScreen(): # returns the user's choice of player
    pygame.init()
    screen = pygame.display.set_mode((400, 300))
    pygame.display.set_caption('Tic Tac Toe')

    font_large = pygame.font.Font('freesansbold.ttf', 32)
    font_small = pygame.font.Font('freesansbold.ttf', 20)

    text_tic_tac_toe = font_large.render('Tic Tac Toe', True, (0, 0, 0))
    textRect_tic_tac_toe = text_tic_tac_toe.get_rect()
    textRect_tic_tac_toe.center = (200, 50)

    text_choose_player = font_small.render('Choose Player', True, (0, 0, 0))
    textRect_choose_player = text_choose_player.get_rect()
    textRect_choose_player.center = (200, 100)

    text_x = font_small.render('X', True, (0, 0, 0))
    textRect_x = text_x.get_rect()
    textRect_x.center = (150, 150)

    text_o = font_small.render('O', True, (0, 0, 0))
    textRect_o = text_o.get_rect()
    textRect_o.center = (250, 150)

    text_start = font_small.render('Start', True, (0, 0, 0))
    textRect_start = text_start.get_rect()
    textRect_start.center = (200, 200)

    user_choice = None
    error_message = None

    while True:                                    # main game loop
      # reset colors to black
      text_x = font_small.render('X', True, (0, 0, 0))
      text_o = font_small.render('O', True, (0, 0, 0))
      text_start = font_small.render('Start', True, (0, 0, 0))

      for event in pygame.event.get():            # event handling loop
        if event.type == MOUSEBUTTONDOWN:         # user clicked on something
          x, y = event.pos                        # get the mouse position
          if textRect_x.collidepoint(x, y):       # check if the mouse position is on the button
            user_choice = 'X'
            error_message = None                  # reset error message
            print("Player chose X")
          elif textRect_o.collidepoint(x, y):
            user_choice = 'O'
            error_message = None
            print("Player chose O")
          elif textRect_start.collidepoint(x, y):
            if user_choice is None:               # check if the player has chosen
              error_message = font_small.render('Please choose a player', True, (255, 0, 0))  # display error message
              print("Please choose a player")
            else:
              return user_choice

      # Check if the cursor is over the text and change color if true
      if textRect_x.collidepoint(pygame.mouse.get_pos()):
          text_x = font_small.render('X', True, (255, 0, 0))          # change color to red
      elif textRect_o.collidepoint(pygame.mouse.get_pos()):
          text_o = font_small.render('O', True, (255, 0, 0))          # change color to red
      elif textRect_start.collidepoint(pygame.mouse.get_pos()):
          text_start = font_small.render('Start', True, (0, 255, 0))  # change color to green

      screen.fill((255, 255, 255))                                # clear the screen
      screen.blit(text_tic_tac_toe, textRect_tic_tac_toe)         # draw the text onto the screen
      screen.blit(text_choose_player, textRect_choose_player)     
      screen.blit(text_x, textRect_x)                             
      screen.blit(text_o, textRect_o)
      screen.blit(text_start, textRect_start)

      if error_message:                                           # display error message if there is one
          screen.blit(error_message, (200 - error_message.get_width() // 2, 250))

      pygame.display.update()   # update the screen

def drawBoard(screen, board):
    screen_width, screen_height = screen.get_size()
    
    # Draw the grid lines
    cell_width = screen_width // 3
    cell_height = screen_height // 3
    pygame.draw.line(screen, (0, 0, 0), (cell_width, 0), (cell_width, screen_height), 5)
    pygame.draw.line(screen, (0, 0, 0), (cell_width * 2, 0), (cell_width * 2, screen_height), 5)
    pygame.draw.line(screen, (0, 0, 0), (0, cell_height), (screen_width, cell_height), 5)
    pygame.draw.line(screen, (0, 0, 0), (0, cell_height * 2), (screen_width, cell_height * 2), 5)

    # Draw the X's and O's
    for i in range(3):
        for j in range(3):
            if board[i][j] == 'X':
                # Calculate the coordinates and size based on the screen size
                x1 = j * cell_width + cell_width // 6
                y1 = i * cell_height + cell_height // 6
                x2 = (j + 1) * cell_width - cell_width // 6
                y2 = (i + 1) * cell_height - cell_height // 6

                pygame.draw.line(screen, (0, 0, 0), (x1, y1), (x2, y2), 5)
                pygame.draw.line(screen, (0, 0, 0), (x2, y1), (x1, y2), 5)
            elif board[i][j] == 'O':
                # Calculate the coordinates and size based on the screen size
                center_x = j * cell_width + cell_width // 2
                center_y = i * cell_height + cell_height // 2
                radius = min(cell_width, cell_height) // 3

                pygame.draw.circle(screen, (0, 0, 0), (center_x, center_y), radius, 5)

# ------------------------ Min-Max Algorithm ------------------------
def checkWin(state):
    for i in range(size):
        if state[i][0] == state[i][1] == state[i][2] != ' ':  # check horizontal win
            return 1 if state[i][0] == 'X' else -1
        if state[0][i] == state[1][i] == state[2][i] != ' ':  # check vertical win
            return 1 if state[0][i] == 'X' else -1

    if state[0][0] == state[1][1] == state[2][2] != ' ' or state[0][2] == state[1][1] == state[2][0] != ' ':  # check diagonal win
        return 1 if state[1][1] == 'X' else -1

    if all(cell != ' ' for row in state for cell in row):  # check if game is a draw
        return 0

    return None  # game is not over yet

def getSuccessors(state, isPlayerX):
    successors = []                    

    for i in range(size):
        for j in range(size):
            if state[i][j] == ' ': 
                newState = copy.deepcopy(state)   # create a copy of the current state
                if (isPlayerX == 1):                # if user is X         
                    newState[i][j] = 'O' 
                else:                               # if user is O 
                    newState[i][j] = 'X'
                successors.append(newState)      # append new state to successors 
    return successors

def minMax(state, isPlayerX, alpha, beta, depth):
    u = checkWin(state)  # check if game is over
    if u == 1:                      # X wins 
        return 1, state
    elif u == (-1):                 # O wins
        return -1, state
    elif u == 0:                    # draw
        return 0, state

    successors = getSuccessors(state, isPlayerX) # generate possible moves

    # maximize score if the current player is 'O' (attack)
    if isPlayerX == 0:              
        m = -math.inf 
        currState = state               # keep track of current state              

        for i in range(len(successors)):  # for each successor
            sVal, currentState = minMax(successors[i], 1, alpha, beta, depth + 1)  # compute the score for the successor
            if (sVal > m):                # update the current state if the successor has a higher score
                currState = successors[i]
            m = max(sVal, m)
            # perform alpha-beta pruning 
            if sVal >= beta: # if the score is greater than or equal to beta, break because the opponent will not choose this node since it is worse than beta          
                break                 
            alpha = max(m, alpha)        
        return m, currState

    # minimize score if the current player is 'X' (defense)
    else:                            
        m = math.inf 
        currState = state     

        for i in range(len(successors)):
            sVal, currentState = minMax(successors[i], 0, alpha, beta, depth + 1) # compute the score for the successor
            if(sVal < m):  # # Update the current state if the successor has a lower score                   
                currState = successors[i]      
            m = min(sVal, m)   
            # perform alpha-beta pruning                
            if sVal <= alpha:                 
                break                           
            beta = min(m, beta)                 
        return m, currState

# ------------------------ Main Game ------------------------
def mainGame(screen, user_choice):
    font = pygame.font.Font('freesansbold.ttf', 32)

    text_x = font.render('X', True, (0, 0, 0))
    text_o = font.render('O', True, (0, 0, 0))
    text_tie = font.render('Tie', True, (0, 0, 0))

    textRect_x = text_x.get_rect()
    textRect_o = text_o.get_rect()
    textRect_tie = text_tie.get_rect()

    textRect_x.center = (150, 150)
    textRect_o.center = (150, 150)
    textRect_tie.center = (200, 150)

    global board
    board = [[' ', ' ', ' '], [' ', ' ', ' '], [' ', ' ', ' ']]

    # determine the initial player based on user_choice
    isPlayerX = 1 if user_choice == 'X' else 0
    playerFirst = isPlayerX
    
    # main game loop
    while True:
        print("Player's turn" if isPlayerX == 1 else "AI's turn")

        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == MOUSEBUTTONDOWN and isPlayerX == 1:
                x, y = event.pos
                col = x // (screen.get_width() // 3)
                row = y // (screen.get_height() // 3)

                if board[row][col] == ' ':
                    board[row][col] = user_choice
                    isPlayerX = 0

        drawBoard(screen, board)
        pygame.display.flip()

        print("Player's turn" if isPlayerX == 1 else "AI's turn")

        # check for game over
        result = checkWin(board)
        if result == 1:
            pygame.time.wait(1000)
            screen.fill((255, 255, 255))
            if user_choice == 'X':
                screen.blit(font.render('Player wins', True, (0, 0, 0)), textRect_x)
            else:
                screen.blit(font.render('AI wins', True, (0, 0, 0)), textRect_x)
            pygame.display.flip()
            pygame.time.wait(2000)
            pygame.quit()
            sys.exit()
        elif result == -1:
            pygame.time.wait(1000)
            screen.fill((255, 255, 255))
            if user_choice == 'O':
                screen.blit(font.render('Player wins', True, (0, 0, 0)), textRect_o)
            else:
                screen.blit(font.render('AI wins', True, (0, 0, 0)), textRect_o)
            pygame.display.flip()
            pygame.time.wait(2000)
            pygame.quit()
            sys.exit()
        elif result == 0:
            pygame.time.wait(1000)
            screen.fill((255, 255, 255))
            screen.blit(text_tie, textRect_tie)
            pygame.display.flip()
            pygame.time.wait(2000)
            pygame.quit()
            sys.exit()

        # AI's turn
        if isPlayerX == 0:
            best_sValue, best_move = minMax(board, playerFirst, -math.inf, math.inf, 0)
            board = best_move
            isPlayerX = 1

        drawBoard(screen, board)
        pygame.display.flip()


def main():
    pygame.init()
    screen = pygame.display.set_mode((300, 300))
    pygame.display.set_caption('Tic Tac Toe')

    user_choice = splashScreen()
    screen.fill((255, 255, 255))
    mainGame(screen, user_choice)

if __name__ == '__main__':
    main()