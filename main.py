from lib2to3.pgen2.token import GREATER
from msilib.schema import SelfReg
from queue import Empty
from sre_constants import RANGE
import time

INFINITY = 50000
maxnodes = 1

def board_state (state):
    i = 0
    temp = [([0] * 3) for j in range(3)]
    for row in range(3):
        for col in range(3):
            temp[row][col] = state[i]
            i+=1
    return temp

def display_board(state):
    print("-------------")
    print("| ", state[0], "| ", state[1], "| ", state[2])
    print("-------------")
    print("| ", state[3], "| ", state[4], "| ", state[5])
    print("-------------")
    print("| ", state[6], "| ", state[7], "| ", state[8])
    print("-------------")

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

def create_node(state, parent, operator, depth, cost):
    return Node(state, parent, operator, depth, cost)
def expand_node (node):
    expanded_nodes = []
    expanded_nodes.append(create_node(move_up(node.state), node, "U", node.depth + 1, 0))
    expanded_nodes.append(create_node(move_down(node.state), node, "D", node.depth + 1, 0))
    expanded_nodes.append(create_node(move_left(node.state), node, "L", node.depth + 1, 0))
    expanded_nodes.append(create_node(move_right(node.state), node, "R", node.depth + 1, 0))

    #Filter list remove impossile momves
    expanded_nodes = [node for node in expanded_nodes if node.state != None]
    return expanded_nodes

def bfs (start, goal):
    nodes = []
    nodes.append(create_node(start, None, None, 0, 0))
    count = 0
    explored = []
    while nodes:
        node = nodes.pop(0)
        count += 1
        print ("Trying state", node.state, " and move: ", node.operator)
        explored.append(node.getState())
        if node.state == goal:
            print ("done")
            print ("The number of nodes visited ", count)
            print ("States of moves are as follows:")
            return node.pathFromStart()
        else:
            expanded_nodes = expand_node(node)
            for item in expanded_nodes:
                state = item.getState()
                if state not in explored:
                    nodes.append(item)
#depth first search
def dfs (start, goal):
    nodes = []
    #Create queue with root node in it
    nodes.append(create_node(start, None, None, 0, 0))
    count = 0
    explored = []
    while nodes:
        node = nodes.pop(0)
        count += 1
        print("Trying state", node.state, " and move: ", node.operator)
        explored.append(node.getState())
        if node.state == goal:
            print ("done")
            print ("The number of nodes visited", count)
            print ("States of moves are as follows: ")
            return node.pathFromStart()
        else:
            expanded_nodes = expand_node(node)
            for item in expanded_nodes:
                state = item.getState()
                if state not in explored:
                    nodes.insert(0, item)

#depth limit search
def dls (start, goal, depth = 20):
    #performs depth limit search
    depth_limit = depth

    #Use list as stack
    nodes = []

    #Create queue with root node
    nodes.append(create_node (start, None, None, 0, 0))
    count = 0
    explored = []
    while nodes:
        node = nodes.pop(0)
        count += 1
        explored.append(node.getState())
        print("Trying state", node.state, " and move: ", node.operator)
        if node.state == goal:
            print("done")
            print("The number of nodes visisted ", count)
            print("States of moves are as follows:")
            return node.pathFromStart()
        if node.depth < depth_limit:
            expanded_nodes = expand_node(node)
            for item in expanded_nodes:
                state = item.getState()
                if state not in explored:
                    nodes.insert(0,item)

#iterative depth first search
def ids (start, goal, depth = 50):
    for i in range(depth):
        result = dls (start, goal, i)
        if result != None:
            return result

def a_star (start, goal):
    nodes = []
    s_node = create_node(start, None, None, 0, 0)
    #change this funciton from f1 to f2 or vice versa to use different heuristics
    f2(s_node)
    nodes.append(s_node)
    explored = []
    count = 0
    while nodes:
        nodes.sort()
        node = nodes.pop(0)
        explored.append(node.getState())
        count += 1

        print("Trying state", node.state, " and move: ", node.operator)
        if node.state == goal:
            print("done")
            print("The number of nodes visited", count)
            print("States of moves are as follows:")
            return node.pathFromStart()
        else:
            expanded_nodes = expand_node(node)
            for item in expanded_nodes:
                state = item.getState()
                if state not in explored:
                    #change this function from f1 to f2 or vice versa to use different heuristics
                    f2(item)
                    nodes.append(item)


def dfs_contour(node, goal, f_limit):
    global maxnodes
    f1(node, goal)
    if node.h_cost > f_limit:
        return node, node.h_cost
    if node.state == goal:
        return node, node.h_cost
    minimum = INFINITY

    expanded_nodes = expand_node(node)
    maxnodes += 1
    for item in expanded_nodes:
        f1(item, goal)
        print ("Trying state", item.state, " and move: ", item.operator)
        newnode, newlimit = dfs_contour(item, goal, f_limit)
        if newnode.state == goal:
            return newnode, newnode.h_cost
        if newlimit < minimum:
            minimum = newlimit
    return node, minimum


def ida_star(start, goal):
    #Iterative deepening a* search with heuristics
    nodes = []
    nodes.append(create_node(start, None, None, 0, 0))
    node = nodes.pop(0)
    f_limit = ofp(node.state, goal)
    loops = 0
    while f_limit < INFINITY:
        loops += 1
        tmp_node, tmp_limit = dfs_contour(node, goal, f_limit)
        f_limit = tmp_limit + 1
        if tmp_node.state == goal:
            print("done")
            print("Max nodes ", tmp_node.depth, " loops ", loops)
            print("States of moves are as follows:")
            return tmp_node.pathFromStart()
        


def ofp (state, goal):
    #Heuristic, out of place
    cost = 0
    for i in range (len (state)):
        if state[i] != goal[i]:
            cost += 1
    return cost

def mh (state):
    #must change when testing other final position
    finalposition = [(1, 1), (0, 0), (1, 0), (2, 0), (2, 1), (2, 2), (1, 2), (0, 2),(0, 1)]
    cost = 0
    temp = board_state(state)
    for y in range(3):
        for x in range(3):
            t = temp[y][x]
            xf, yf = finalposition[t]
            cost += abs(xf - x) + abs (yf-y)
    return cost

def f1(node, goal):
    node.h_cost = node.depth + ofp(node.state, goal)

def f2(node):
    node.h_cost = node.depth + mh(node.state)



class Node:
    def __init__(self, state, parent, operator, depth, cost):
        #Contains the state of the node
        self.state = state
        #Contains the node that generated this node
        self.parent = parent
        #Contains the operation or action that genertaed this node from the parent
        self.operator = operator
        #Contains the depth of this node
        self.depth = depth
        #Contains the path cost of this node from depth 0.
        self.cost = cost
        #f-cost for IDA_star search
        self.f_cost = 0
        #heuristic cost
        self.h_cost = 0
    
    def getState(self):
        return self.state
    def getParent(self):
        return self.parent
    def getMoves(self):
        return self.operator
    def getCost(self):
        return self.cost
    def pathFromStart(self):
        stateList = []
        movesList = []
        currNode = self
        while currNode.getMoves() is not None:
            stateList.append(currNode.getState())
            movesList.append(currNode.getMoves())
            currNode = currNode.parent
        movesList.reverse()
        stateList.reverse()
        for state in stateList:
            display_board(state)
        return movesList

    def __lt__(self, other):
        return (self.h_cost < other.h_cost)

def main():
    #567408321
    print("Enter the start and goal state(respectively)")
    s_state = input()
    g_state = input()
    start_state = list(s_state)
    goal_state = list(g_state)  
    start = time.process_time()
    result = bfs(start_state, goal_state)
    totaltime = start
    if result == None:
        print ("No solution found")
    elif result == [None]:
        print ("Start node was the goal")
    else:
        print (result)
        print (len(result), " moves")
    print("Total searching time: %.5f seconds" % (totaltime))

if __name__ == "__main__":
    main()