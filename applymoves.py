def move_up(state):
    #moves blank tile up on the board
    new_state = state[:]
    index = new_state.index('0')

    if index not in [0,1,2]:
        #Swap values
        temp = new_state[index - 3]
        new_state[index - 3] = new_state[index]
        new_state[index] = temp
        return new_state
    else:
        #Can't move
        return None

def move_down(state):
    #Moves blank tile down on the board
    new_state = state[:]
    index = new_state.index('0')

    if index not in [6,7,8]:
        #Swap values
        temp = new_state[index + 3]
        new_state[index + 3] = new_state[index]
        new_state[index] = temp
        return new_state
    else:
        #Can't move
        return None

def move_left(state):
    #Moves blank tile left on the board
    new_state = state[:]
    index = new_state.index('0')

    if index not in [0,3,6]:
        #Swap values
        temp = new_state[index - 1]
        new_state[index - 1] = new_state[index]
        new_state[index] = temp
        return new_state
    else:
        #Can't move
        return None

def move_right(state):
    new_state = state[:]
    index = new_state.index('0')

    if index not in [2,5,8]:
        #Swap values
        temp = new_state[index + 1]
        new_state[index + 1] = new_state[index]
        new_state[index] = temp
        return new_state
    else:
        #Can't move
        return None

def apply(state, moves):
    new_state = []
    for move in moves:
        if move == 'u':
            if move_up(state) == None: continue
            else: new_state = move_up(state)
        if move == 'd':
            if move_down(state) == None: continue
            else: new_state = move_down(state)
            
        if move == 'l':
            if move_left(state) == None: continue
            else: new_state = move_left(state)
        if move == 'r':
            if move_right(state) == None: continue
            else: new_state = move_right(state)
        state = new_state
    return new_state


def main():
    print("Enter a state: ")
    state = input()
    state = list(state)
    print("Enter moves for state: ")
    moves = input()
    moves = list(moves)
    new_state = apply(state, moves)
    print(new_state)

if __name__ == "__main__":
    main()