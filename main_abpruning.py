from board import Board
from player import Player
from gamestate import GameState
from copy import deepcopy

transpositionTable = {}
prunes = 0

INFINITY = 99999999
NEG_INFINITY = -99999999




def main():

    # part = input("Run part A or B or C? (A/B/C): ")
    part = "A"
    debug = True
    noOfRows = 3
    noOfCols = 3
    noTowin = 3

    board = Board(noOfRows, noOfCols, noTowin)
    
    value, move = minimax(board, NEG_INFINITY, INFINITY)
    
    
    print(f"States {len(transpositionTable)}")
    print(f"Prunes {prunes}")

    keys = []
    for i in transpositionTable:
        keys += [f"{i} -> MinimaxInfo[value={transpositionTable[i][0]}, action={transpositionTable[i][1]}]"]
    keys.sort()
    # print("\n".join(keys[:1000]))
    # print(keys)
    # return
    turn = input("Who goes first? (MAX/MIN): ")
    playerTurn = "MAX"
    
    while True:
        print()
        print(board.to_2d_string())
        state = (board.__str__(), board.get_player_to_move_next())
        if (state not in transpositionTable):
            minimax(board, NEG_INFINITY, INFINITY)
        print(f"Minimax value for this state: {transpositionTable[state][0]}, optimal move: {transpositionTable[state][1]}")

        print(f"It is {playerTurn}'s turn")   
        if (turn == "1"):
            playerMove = input("Enter your move: ")
            turn = "2"
           
        else:
            playerMove = transpositionTable[state][1]
            print(f"Ciomputer move: {playerMove}") 
            turn = "1"
        
        playerTurn = "MAX" if playerTurn == "MIN" else "MIN"
        
        board = board.make_move(int(playerMove))

        if (board.get_game_state() != GameState.IN_PROGRESS):
            if (board.has_winner()):
                print(f"Winner is {board.get_winner()}")
            else:
                print("It is a tie")
            return
        
        

def actions(board):
    result = []
    for i in range(board.get_cols()):
        if (board.is_column_full(i) == False):
            result += [i]
    return result


def minimax(board, alpha, beta):
    if (board.get_player_to_move_next() == Player.MAX):
        value, move  = max_value(deepcopy(board), alpha, beta)
    else:
        value, move = min_value(deepcopy(board), alpha, beta)
    
    return value, move

def max_value(board, alpha, beta):
    global transpositionTable
    global prunes
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

    v = -99999999

    if state in transpositionTable:
        # print("found")
        return transpositionTable[state][0], transpositionTable[state][1]
    for action in actions(board):
        v2, a2 = min_value(deepcopy(board).make_move(action), alpha, beta)
        # print(v2)
        if (v2 > v):
            v = v2
            a = action
            alpha = max(alpha, v)
        
        if (v >= beta):
            prunes += 1
            if (v == -1):
                v *= -1
            # transpositionTable[state] = [v, a]
            return v, a
            
        
        
    
   



    if (v == -1):
        v *= -1

    transpositionTable[state] = [v, a]
    return v, a



def min_value(board, alpha, beta):
    global transpositionTable
    global prunes
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

    if (state in transpositionTable):
        # print("found")
        return transpositionTable[state][0], transpositionTable[state][1]

    v = 99999999

    for action in actions(board):
        v2, a2 = max_value(deepcopy(board).make_move(action), alpha, beta)
        # print(v2)
        if (v2 < v):
            v = v2
            a = action
            beta = min(beta, v)
    
        if (v <= alpha):
            prunes += 1
            if (v == -1):
                v *= -1
            # transpositionTable[state] = [v, a]
            return v, a
        
    if (v == -1):
        v *= -1
    
    

    transpositionTable[state] = [v, a]
    return v, a

main()