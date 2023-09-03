# Rosie Khurmi
# September 2, 2023

"""
Tic Tac Toe Player
"""

import math
import copy

X = "X"
O = "O"
EMPTY = None


def initial_state():
    """
    Returns starting state of the board.
    """
    return [[EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY],
            [EMPTY, EMPTY, EMPTY]]


def player(board):
    """
    Returns player who has the next turn on a board.
    """
    # Counters for each player
    x_count = 0
    o_count = 0

    # Go through each imdex of 2D array to count X and O
    for r in range(len(board)):
        for c in range(len(board)):
            if board[r][c] == X:
                x_count += 1
            elif board[r][c] == O:
                o_count += 1

    # If X = X, return X, else O
    player = X if x_count == o_count else O
    return player
        
def actions(board):
    """
    Returns set of all possible actions (i, j) available on the board.
    """
    options = set() # Hold all options in a set

    # Go through 2D array
    # If there is an empty spot, add its coordinates to the set
    for r in range(len(board)):
        for c in range(len(board)):
            if board[r][c] == EMPTY:
                options.add((r, c))

    return options # Return all possible option

def result(board, action):
    """
    Returns the board that results from making move (i, j) on the board.
    """
    # Create a deep copy of the board
    result = copy.deepcopy(board)

    r = action[0] # Row
    c = action[1] # Colum

    # If the sopt is empty, append the corresponding player
    # Else raise an exception
    if result[r][c] == EMPTY:
        result[r][c] = player(result)
        return result
    else:
        raise ValueError

def winner(board):
    """
    Returns the winner of the game, if there is one.
    """

    winner = None

    # Check if top to bottom diagonal is all the same
    if board[0][0] == board[1][1] == board[2][2]:
        # Return X or O depending who gets all the same
        winner = X if board[0][0] == X else O if board[0][0] == O else None
        
    # Check if bottom to top diagonal is all the same
    if board[0][2] == board[1][1] == board[2][0]:
        # Return X or O depending who gets all the same
        winner = X if board[0][2] == X else O if board[0][2] == O else None
        
    # Check matching in any 3 rows
    for r in board: 
        if r[0] == r[1] == r[2]:
            # Return X or O depending who gets all the same
            winner = X if r[0] == X else O if r[0] == O else None

    # Check matching in any 3 columns     
    for c in range(len(board)): 
        if board[0][c] == board[1][c] == board[2][c]:
            # Return X or O depending who gets all the same
            winner = X if board[0][c] == X else O if board[0][c] == O else None
            
    return winner

def terminal(board):
    """
    Returns True if game is over, False otherwise.
    """
    # If a winner has been declared or there are no spaces on the board
    # Return True, else False
    if (winner(board) or len(actions(board)) == 0):
        return True
    else:
        return False

def utility(board):
    """
    Returns 1 if X has won the game, -1 if O has won, 0 otherwise.
    """
    # If board has reached terminal
    if terminal(board):
        # Return 1 if X has won
        if winner(board) == X:
            return 1 
        # Return -1 if O won
        elif winner(board) == O:
            return -1
        # Return 0 if tie
        else:
            return 0 

def optimal(board, depth = 0):
    """
    Helper function for minimax
    Returns optimal value and a a set of its corresponding move
    """

    # If the board is at terminal, return the winner and no possible solution  
    if terminal(board):
        return utility(board), None
    # Else perform minimax
    else:

        move = set() # Hold best move

        if player(board) == X: # Maximizing Player
            best = float('-inf') # Optimal Value - Try to get to 1
    
            # Go through all empty spots
            for a in actions(board):
                # Perform a recursive call of the fuction with all possible spots
                temp, m = optimal(result(board, a))

                # If the result is a larger value, change best and store the move
                if temp > best:
                    best = temp
                    move = a
    
            # Return best and move
            return best, move
        
        elif player(board) == O: # Minimizing Player

            best = float('inf')  # Optimal Value - Try to get to -1

            # Go through all empty spots
            for a in actions(board):
                # Perform a recursive call of the fuction with all possible spots
                temp, m = optimal(result(board, a))

                # If the result is a smaller value, change best and store the move
                if temp < best:
                    best = temp
                    move = a

            # Return best and move
            return best, move

def minimax(board):
    """
    Returns the optimal action for the current player on the board.
    """

    # Call optimal and return the move
    value, move = optimal(board)
    return move

 









    



    











    









   


