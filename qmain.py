import random
import copy

gamma = 0.9
qtable = {}



start_state = tuple(map(int,input("Enter the starting state of the piles (Eg: 1 2 3): ").split()))
numberofgames = int(input("Enter the number of games to be simulated: "))


def game_over(state):
    # print(state)
    # print(" STATE")
    if (all(x == 0 for x in state)):
        return True
    return False

def play():
    state = (start_state, True)

    while not game_over(state[0]):

        turn = state[1]
        random_action = get_random_action(state)
        next_state = make_action(state, random_action)
        reward = get_reward(next_state)

       


        if turn == 1:
            qtable[(state, random_action)] = reward + gamma * min_a(next_state)
        else:
            qtable[(state, random_action)] = reward + gamma * max_a(next_state)

        state = next_state
    #     print(state)
    #     print("NEw state")
    # print(qtable)

def play_more(n):
    for i in range(n):
       
        play()
    print(qtable)







def max_a(state):
    actions = get_actions(state[0])
    if len(actions) == 0:
        return 0
    max_value = -100000
    for action in actions:
        value = getQvalue(state, action)
        if value > max_value:
            max_value = value
            
    return max_value

def min_a(state):
    actions = get_actions(state[0])
    min_value = 100000
    if len(actions) == 0:
        return 0
    for action in actions:
        value = getQvalue(state, action)
        if value < min_value:
            min_value = value
    return min_value

def get_actions(state):
    actions = []
    for i in range(len(state)):
        for j in range(1,state[i]+1):
            actions.append((i, j))
    return actions

def get_reward(state):
    if game_over(state[0]):
        if (state[1]):
            return 1000
        else:
            return -1000
    return 0

def getQvalue(state, action):
    if (state, action) not in qtable:
        qtable[(state, action)] = 0
    return qtable[(state, action)]



            

def get_random_action(state):
    all_actions = get_actions(state[0])
    # print(all_actions)
    rand = random.choice(all_actions)
    return rand


def make_action(state, action):
    newstate = list(state[0])
   
    newstate[action[0]] -= action[1]
    
    newstate = (tuple(newstate), not state[1])
    return newstate



# # training phase

# for i in range(numberofgames):
#     play()

def main():



    play_more(100000)
    print("Final Q-values:")
    print()
    for key in qtable:
        player = "A"
        if not key[0][1]:
            player = "B"
        
        print(f"Q[{player}{key[0][0][0]}{key[0][0][1]}{key[0][0][2]}, {key[1][0]}{key[1][1]}] = {qtable[key]}")

    
    while True:
        turn = input("Who moves first, (1) User or (2) Computer? ")
        current_player = "user"
        turn_count = "A"

        if (turn == "2"):
            current_player = "computer"
        
        curr_state = (start_state, True)

        while not game_over(curr_state[0]):
            print(f"Player {turn_count} ({current_player})'s turn; board is {curr_state[0]}.")
            if (current_player == "computer"):
                best = -10000
                bestaction = None
                for action in get_actions(curr_state[0]):
                    val = getQvalue(curr_state, action)
                    if val > best:
                        best = val
                        bestaction = action
                print(f"Computer chooses pile {bestaction[0]} and removes {bestaction[1]}.")
                curr_state = make_action(curr_state, bestaction)
            else:
                pilecol = int(input("What pile? "))
                noremove = int(input("How many? "))
                action = (pilecol, noremove)
                curr_state = make_action(curr_state, action)
            
            turn_count = "B" if turn_count == "A" else "A"
            current_player = "computer" if current_player == "user" else "user"

        print(f"Game over. Winner is {turn_count} ({current_player}).")

        continue_playing = input("Play again? (1) Yes (2) No: ") 
        if continue_playing == "2":
            break
       

main()

