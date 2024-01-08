from board import Board
from player import Player
from gamestate import GameState
from copy import deepcopy
import random

transpositionTable = {}
prunes = 0

valueBoardList = []

INFINITY = 99999999
NEG_INFINITY = -99999999

alpha_beta = False
heuristic = False
debugging = False




def main():
    global alpha_beta
    global heuristic
    global debugging

    part = input("Run part A or B or C? (A/B/C): ")
    part = part.upper()
    if (part == "A"):
        alpha_beta = False
    elif (part == "B"):
        alpha_beta = True
    elif (part == "C"):
        alpha_beta = True
        heuristic = True
    else:
        print("Invalid input")
        return
    
    debug = input("Include debugging info? (y/n)")
    if (debug == "y"):
        debugging = True
    elif (debug == "n"):
        debugging = False
    else:
        print("Invalid input")
        return
    
    noOfRows = int(input("Enter rows: "))
    noOfCols = int(input("Enter columns: "))
    noTowin = int(input("Enter number in a row to win: "))

    depth = 0

    if (heuristic):
        depth = int(input("Number of moves to look ahead (depth): "))


    board = Board(noOfRows, noOfCols, noTowin)
    valueBoard(board, noTowin)

    certainWin = [False, ""]

    
    
    
    # return

    

    if (not heuristic):
        value, move = minimax(board, NEG_INFINITY, INFINITY, depth)
        if (value < 0):
            certainWin[0] = True
            certainWin[1] = "Second player"
        elif (value > 0):
            certainWin[0] = True
            certainWin[1] = "First player"
        else:
            certainWin[0] = False
            certainWin[1] = "Neither player"

    if not heuristic:

        print(f"Transposition table has {len(transpositionTable)} states.")
        if (alpha_beta):
            print(f"The tree was pruned {prunes} times.")

    if (certainWin[0]):
        print(f"{certainWin[1]} has a guaranteed win with perfect play.")

    if debugging and not heuristic:

        keys = []
        for i in transpositionTable:
            keys += [f"{i} -> MinimaxInfo[value={transpositionTable[i][0]}, action={transpositionTable[i][1]}]"]
        keys.sort()
        print("\n".join(keys))
        
    
    
    turn = input("Who plays first? 1=human, 2=computer: ")
    playerTurn = "MAX"
    
    while True:
        print()
        print(board.to_2d_string())
        state = (board.__str__())

        if (alpha_beta):
            if (state not in transpositionTable):
                minimax(board, NEG_INFINITY, INFINITY, depth)
        
        

        print(f"It is {playerTurn}'s turn")   
        if (turn == "1"):
            print(f"Minimax value for this state: {transpositionTable[state][0]}, optimal move: {transpositionTable[state][1]}")
            playerMove = input("Enter your move: ")
            turn = "2"
           
        else:

            hvalue, playerMove = minimax(board, NEG_INFINITY, INFINITY, depth)
            if heuristic:
                print(f"Minimax value for this state: {hvalue}, optimal move: {playerMove}")
            else:
                print(f"Minimax value for this state: {transpositionTable[state][0]}, optimal move: {transpositionTable[state][1]}")

            print(f"Computer chooses move: {playerMove}") 
            turn = "1"
        
        playerTurn = "MAX" if playerTurn == "MIN" else "MIN"
        
        board = board.make_move(int(playerMove))

        if (board.get_game_state() != GameState.IN_PROGRESS):
            print()
            print(board.to_2d_string())
            if (board.has_winner()):
                print(f"Winner is {board.get_winner()}")
            else:
                print("It is a tie")
            return
        
        
# This function returns a list of all the possible actions that can be made on the board
def actions(board):
    result = []
    for i in range(board.get_cols()):
        if (board.is_column_full(i) == False):
            result += [i]
    return result


def minimax(board, alpha, beta, depth):
    global transpositionTable
    global heuristic

    if heuristic:
        transpositionTable = {}
        
    if (board.get_player_to_move_next() == Player.MAX):
        value, move  = max_value(deepcopy(board), alpha, beta, depth)
    else:
        value, move = min_value(deepcopy(board), alpha, beta, depth)

    if heuristic:
        print(f"Transposition table has {len(transpositionTable)} states.")
    
    return value, move

def max_value(board, alpha, beta, depth):
    global transpositionTable
    global prunes
    global alpha_beta
    global heuristic

    state = (board.__str__())
    if (board.get_game_state() != GameState.IN_PROGRESS):
        
        if (board.has_winner()):
            v = int(10000*board.get_cols() * board.get_rows() / board.get_number_of_moves())
            transpositionTable[state] = [v, None]

            if (board.get_winner() == Player.MAX):
                return v, None
            transpositionTable[state] = [-1*v, None]
            
            return -1*v, None
        transpositionTable[state] = [0, None]
        return 0, None
    
    if heuristic:
        if depth == 0:
            return evaluate(board, board.consec_to_win), None

    v = NEG_INFINITY

    if state in transpositionTable:
        return transpositionTable[state][0], transpositionTable[state][1]
    
    for action in actions(board):
        v2, a2 = min_value(deepcopy(board).make_move(action), alpha, beta, depth - 1)
        if (v2 > v):
            v = v2
            a = action
            alpha = max(alpha, v)

        
        if alpha_beta:
            if (v >= beta):
                prunes += 1
                if (v == -1):
                    v *= -1
                return v, a
            
    if (v == -1):
        v *= -1

    transpositionTable[state] = [v, a]
    return v, a



def min_value(board, alpha, beta, depth):
    global transpositionTable
    global prunes
    global alpha_beta
    global heuristic

    state = (board.__str__())
    if (board.get_game_state() != GameState.IN_PROGRESS):
        
        if (board.has_winner()):
            v = int(10000*board.get_cols() * board.get_rows() / board.get_number_of_moves())
            transpositionTable[state] = [v, None]

            if (board.get_winner() == Player.MAX):
                return v, None
            transpositionTable[state] = [-1*v, None]
            
            return -1*v, None
        transpositionTable[state] = [0, None]
        return 0, None
    
    if heuristic:
        if depth == 0:
            return evaluate(board, board.consec_to_win), None

    if (state in transpositionTable):
        return transpositionTable[state][0], transpositionTable[state][1]

    v = INFINITY

    for action in actions(board):
        v2, a2 = max_value(deepcopy(board).make_move(action), alpha, beta, depth - 1)
        if (v2 < v):
            v = v2
            a = action
            beta = min(beta, v)

        if alpha_beta:
            if (v <= alpha):
                prunes += 1
                if (v == -1):
                    v *= -1
                return v, a
        
    if (v == -1):
        v *= -1
    
    

    transpositionTable[state] = [v, a]
    return v, a


# This creates a 2d array with the same number of rows and columns as the board, assigning each cell a value based on the number of possible combinations that can be made with that cell
def valueBoard(board, toWin):
    global valueBoardList
    no_of_rows = board.get_rows()
    no_of_cols = board.get_cols()
    to_win = toWin - 1
    

    valueBoardList = [[0 for i in range(no_of_cols)] for j in range(no_of_rows)]


    # check for possible combination in each cell horizontally, vertically, and diagonally
    for row in range(no_of_rows):
        for col in range(no_of_cols):
            maximum_cell_right = min(col + to_win, no_of_cols -1)
            minimum_cell_left = max(col - to_win,0)

            maximum_cell_up = min(row + to_win, no_of_rows -1)
            minimum_cell_down = max(row - to_win,0)

            no_of_possible_combs = max(maximum_cell_right - minimum_cell_left + 1 - to_win,0)
            no_of_possible_combs += max(maximum_cell_up - minimum_cell_down + 1 - to_win, 0)

            top_right_col = min(col + to_win, no_of_cols -1)
            top_right_row = max(row - to_win,0)

            top_right_col_diff = top_right_col - col
            top_right_row_diff = row - top_right_row
            top_right_diff = min(top_right_col_diff, top_right_row_diff)

            top_right_value = (row - top_right_diff, col + top_right_diff)

            bottom_left_col = max(col - to_win,0)
            bottom_left_row = min(row + to_win, no_of_rows -1)

            bottom_left_col_diff = col - bottom_left_col
            bottom_left_row_diff = bottom_left_row - row
            bottom_left_diff = min(bottom_left_col_diff, bottom_left_row_diff)

            bottom_left_value = (row + bottom_left_diff, col - bottom_left_diff)
            
            no_of_cell_tr_diagonal = max(top_right_value[1] - bottom_left_value[1] + 1 - to_win,0)
            no_of_possible_combs += no_of_cell_tr_diagonal

            top_left_col = max(col - to_win,0)
            top_left_row = max(row - to_win,0)

            top_left_col_diff = col - top_left_col
            top_left_row_diff = row - top_left_row
            top_left_diff = min(top_left_col_diff, top_left_row_diff)

            top_left_value = (row - top_left_diff, col - top_left_diff)

            bottom_right_col = min(col + to_win, no_of_cols -1)
            bottom_right_row = min(row + to_win, no_of_rows -1)

            bottom_right_col_diff = bottom_right_col - col
            bottom_right_row_diff = bottom_right_row - row
            bottom_right_diff = min(bottom_right_col_diff, bottom_right_row_diff)

            bottom_right_value = (row + bottom_right_diff, col + bottom_right_diff)

            no_of_cell_tl_diagonal = max(bottom_right_value[1] - top_left_value[1] + 1 - to_win,0)
            no_of_possible_combs += no_of_cell_tl_diagonal



            valueBoardList[row][col] = no_of_possible_combs
    

            

# evaluates the board based on the number of possible combinations that can be made with each cell and the number of cells in a row that are occupied by the same player
def evaluate(board, toWin):   
    scorex = 0 # score for player 1
    scoreo = 0 # score for player 2

    no_of_rows = board.get_rows()
    no_of_cols = board.get_cols()

    verticalTemp = [[] for i in range(no_of_cols)]
    vertical = [] # list of all states in vertical direction
    horizontal = [] # list of all states in horizontal direction
    diagonal = [] # list of all states in diagonal direction

    for row in range(no_of_rows):
        horizontal += [[str(i) for i in board.board[row]]]
        for col in range(no_of_cols):
            verticalTemp[col] += [board.board[row][col]]

    for data in verticalTemp:
        vertical += [[str(i) for i in data]]

    for col in range(no_of_cols):
        dr = 0
        dc = col

        list_entry = []
        

        while (dr < no_of_rows and dc < no_of_cols and dr >= 0 and dc >= 0):
            cell_value = board.board[dr][dc]
            list_entry += [cell_value]
            dr += 1
            dc -= 1
        diagonal += [[str(i) for i in list_entry]]
        
        dr = 0
        dc = no_of_cols - 1 - col
        list_entry = []

        while (dr < no_of_rows and dc < no_of_cols and dr >= 0 and dc >= 0):
            cell_value = board.board[dr][dc]
            list_entry += [cell_value]
            dr += 1
            dc += 1

        diagonal += [[str(i) for i in list_entry]]

    # check for all n in a row combinations
    for num_in_row in range(1, toWin):
        valX = "1" * num_in_row
        valO = "-1" * num_in_row

        # check for all n in a row combinations in horizontal direction
        for row,entry in enumerate(horizontal):
            entry_value = 0
            for col in range(len(entry)):
                cell_value = valueBoardList[row][col]
                entry_value += cell_value * int(entry[col])
            entry = "".join(entry).replace("0", "")


            if valX in entry:
                scorex += entry_value * num_in_row * entry.count(valX)

            
            if valO in entry:
                scoreo += entry_value * num_in_row * entry.count(valO)


        # check for all n in a row combinations in vertical direction
        for col,entry in enumerate(vertical):
            entry_value = 0
            for row in range(len(entry)):
                cell_value = valueBoardList[row][col]
                entry_value += cell_value * int(entry[row])
            entry = "".join(entry).replace("0", "")

            if valX in entry:
                scorex += entry_value * num_in_row * entry.count(valX)

            if valO in entry:
                scoreo += entry_value * num_in_row * entry.count(valO)


    
    return scorex + scoreo











            


if __name__ == "__main__":
    main()