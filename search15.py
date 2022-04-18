from lib2to3.pgen2.token import GREATER
from msilib.schema import SelfReg
from queue import Empty
from sre_constants import RANGE
import time

INFINITY = 50000
maxnodes = 1
max_search_depth = 0
costs = set()

def board_state (state):
    i = 0
    temp = [([0] * 4) for j in range(4)]
    for row in range(4):
        for col in range(4):
            temp[row][col] = state[i]
            i+=1
    return temp

def display_board(state):
    print("------------------------------------------------------------------------------")
    print("| ", state[0], "| ", state[1], "| ", state[2], "| ", state[3])
    print("------------------------------------------------------------------------------")
    print("| ", state[4], "| ", state[5], "| ", state[6], "| ", state[7])
    print("------------------------------------------------------------------------------")
    print("| ", state[8], "| ", state[9], "| ", state[10], "| ", state[11])
    print("------------------------------------------------------------------------------")
    print("| ", state[12], "| ", state[13], "| ", state[14], "| ", state[15])
    print("------------------------------------------------------------------------------")

def move_up(state):
    #moves blank tile up on the board
    new_state = state[:]
    index = new_state.index('0')

    if index not in [0,1,2,3]:
        #Swap values
        temp = new_state[index - 4]
        new_state[index - 4] = new_state[index]
        new_state[index] = temp
        return new_state
    else:
        #Can't move
        return None

def move_down(state):
    #Moves blank tile down on the board
    new_state = state[:]
    index = new_state.index('0')

    if index not in [12,13,14,15]:
        #Swap values
        temp = new_state[index + 4]
        new_state[index + 4] = new_state[index]
        new_state[index] = temp
        return new_state
    else:
        #Can't move
        return None

def move_left(state):
    #Moves blank tile left on the board
    new_state = state[:]
    index = new_state.index('0')

    if index not in [0,4,8,12]:
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

    if index not in [3,7,11,15]:
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
    explored = {''.join(nodes[0].getState()):True}
    while nodes:
        node = nodes.pop(0)
        count += 1
        print ("Trying state", node.state, " and move: ", node.operator)
        if count > 2000000:
            break
        expanded_nodes = expand_node(node)
        for item in expanded_nodes:
            state = ''.join(item.getState())
            if item.state == goal:
                print ("done")
                print ("The number of nodes visited ", count)
                print ("States of moves are as follows:")
                return item.pathFromStart()
            if not state in explored:
                explored[state] = True
                nodes.append(item)
#depth first search
def dfs (start, goal):
    nodes = []
    nodes.append(create_node(start, None, None, 0, 0))
    count = 0
    explored = {''.join(nodes[0].getState()):True}
    while nodes:
        node = nodes.pop(0)
        count += 1
        print ("Trying state", node.state, " and move: ", node.operator)
        if count > 2000000:
            break
        expanded_nodes = expand_node(node)
        for item in expanded_nodes:
            state = ''.join(item.getState())
            if item.state == goal:
                print ("done")
                print ("The number of nodes visited ", count)
                print ("States of moves are as follows:")
                return item.pathFromStart()
            if not state in explored:
                explored[state] = True
                nodes.insert(0,item)

#depth limit search
def dls (start, goal, depth = 20):
    #performs depth limit search
    depth_limit = depth

    #Use list as stack
    nodes = []

    #Create queue with root node
    nodes.append(create_node (start, None, None, 0, 0))
    count = 0
    explored = {''.join(nodes[0].getState()):True}
    while nodes:
        node = nodes.pop(0)
        count += 1
        print("Trying state", node.state, " and move: ", node.operator)
        if node.depth < depth_limit:
            expanded_nodes = expand_node(node)
            for item in expanded_nodes:
                state = ''.join(item.getState())
                if item.state == goal:
                    print("done")
                    print("The number of nodes visisted ", count)
                    print("States of moves are as follows:")
                    #tofile(start, goal, count, item.pathFromStart())
                    return item.pathFromStart()
                if not state in explored:
                    explored[state] = True
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
    f1(s_node, goal)
    nodes.append(s_node)
    explored = {''.join(nodes[0].getState()):True}
    count = 0
    while nodes:
        nodes.sort()
        node = nodes.pop(0)
        count += 1
        print("Trying state", node.state, " and move: ", node.operator)
        expanded_nodes = expand_node(node)
        for item in expanded_nodes:
            state = ''.join(item.getState())
            if item.state == goal:
                print("done")
                print("The number of nodes visited", count)
                print("States of moves are as follows:")
                return item.pathFromStart()            
            if not state in explored:
                #change this function from f1 to f2 or vice versa to use different heuristics
                explored[state] = True
                f1(item, goal)
                nodes.append(item)


def a_star_mh (start, goal):
    nodes = []
    s_node = create_node(start, None, None, 0, 0)
    #change this funciton from f1 to f2 or vice versa to use different heuristics
    f2(s_node, goal)
    nodes.append(s_node)
    print(goal)
    explored = {''.join(nodes[0].getState()):True}
    count = 0
    while nodes:
        nodes.sort()
        node = nodes.pop(0)
        count += 1
        print("Trying state", node.state, " and move: ", node.operator)
        expanded_nodes = expand_node(node)
        for item in expanded_nodes:
            state = ''.join(item.getState())
            if item.state == goal:
                print("done")
                print("The number of nodes visited", count)
                print("States of moves are as follows:")
                tofile(start,goal,count,item.pathFromStart())
                return item.pathFromStart()            
            if not state in explored:
                #change this function from f1 to f2 or vice versa to use different heuristics
                explored[state] = True
                f2(item, goal)
                nodes.append(item)



def dfs_contour(start, node, goal, f_limit):
    global max_search_depth
    nodes = []
    nodes.append(create_node(node, None, None, 0, 0))
    nodes[0].key = f_limit
    explored = {''.join(nodes[0].getState()):True}
    count = 0
    while nodes:
        node = nodes.pop(0)
        count += 1
        print("Trying state", node.state, " and move: ", node.operator)
        if node.state == goal:
            tofile(start, goal, count, node.pathFromStart())
            return node.pathFromStart()
        if node.key > f_limit:
            costs.add(node.key)
        if node.depth < f_limit:
            neighbors = expand_node(node)
            for neighbor in neighbors:
                state = ''.join(neighbor.getState())
                if not state in explored:
                    neighbor.key = neighbor.cost + mh(neighbor.state, goal)
                    nodes.append(neighbor)
                    explored[state] = True
                    if neighbor.depth > max_search_depth:
                        max_search_depth +=1
    return min(costs)


def ida_star(start, goal):
    #Iterative deepening a* search with heuristics
    global costs
    threshold = mh(start, goal)
    while True:
        response = dfs_contour(start, start, goal, threshold)
        if type(response) is list:
            return response
        
        threshold = response
        costs = set()
        


def ofp (state, goal):
    #Heuristic, out of place
    cost = 0
    for i in range (len (state)):
        if state[i] != goal[i]:
            cost += 1
    return cost

def mh (state, goal):
    s_state = list(state)
    g_state = list(goal)
    cost = 0
    for i in range(len(s_state)):
        if s_state[i] == 'A':
            s_state[i] = 10
        elif s_state[i] == 'B':
            s_state[i] = 11
        elif s_state[i] == 'C':
            s_state[i] = 12
        elif s_state[i] == 'D':
            s_state[i] = 13
        elif s_state[i] == 'E':
            s_state[i] = 14
        elif s_state[i] == 'F':
            s_state[i] = 15
        else:
            s_state[i] = int(s_state[i])
    for i in range(len(g_state)):
        if g_state[i] == 'A':
            g_state[i] = 10
        elif g_state[i] == 'B':
            g_state[i] = 11
        elif g_state[i] == 'C':
            g_state[i] = 12
        elif g_state[i] == 'D':
            g_state[i] = 13
        elif g_state[i] == 'E':
            g_state[i] = 14
        elif g_state[i] == 'F':
            g_state[i] = 15
        else:
            g_state[i] = int(g_state[i])
    #must change when testing other final position
    #cost = sum(abs((s_state.index(i)%4 - g_state.index(i)%4)) + abs (s_state.index(i)//4 - g_state.index(i)//4))
    cost = sum(abs(val1%4 - val2%4) + abs(val1//4 - val2//4) for val1, val2 in zip(s_state, g_state))
    return cost

def f1(node, goal):
    node.h_cost = node.depth + ofp(node.state, goal)

def f2(node, goal):
    node.h_cost = node.depth + mh(node.state, goal)

def cmp(x):
    return x.h_cost

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


def tofile(start, goal, nodes, moves ):
    file1 = open("IDASTAR_MH_15Puzzle.txt", "a")
    file1.write("Start: " + ''.join(start) + "\n")
    file1.write("Goal: " + ''.join(goal) + "\n")
    file1.write("Nodes expanded: " + str(nodes) + "\n")
    file1.write("Moves: " + ''.join(moves) + "\n")
    file1.write("\n")
    file1.close()


def main():
    #567408321
    print("Enter Search Algorithm: \n bfs \n dfs \n ids \n a_star \n ida_star \n")
    search_algo = input()
    print("Enter the start state: ")
    s_state = input()
    start_state = list(s_state)
    goal_state = "123456789ABCDEF0"
    # f = open("tests.txt", "r")
    # for state in f:
    if search_algo == "bfs":
        start = time.process_time()
        result = bfs(start_state, goal_state)
        stop = time.process_time()
    elif search_algo == "dfs":
        start = time.process_time()
        result = dfs(start_state, goal_state)
        stop = time.process_time()
    elif search_algo == "ids":
        start = time.process_time()
        result = ids(start_state, goal_state)
        stop = time.process_time()
    elif search_algo == "a_star":
        start = time.process_time()
        result = a_star(start_state, goal_state)
        stop = time.process_time()
    elif search_algo == "ida_star":
        start = time.process_time()
        result = ida_star(start_state, goal_state)
        stop = time.process_time()
    totaltime = stop - start

    if result == None:
        print("No solution found")
    elif result == [None]:
        print("Start node was the goal")
    else:
        print(result)
        print(len(result), " moves")
    print("Total searching time: %.5f seconds" % (totaltime))

if __name__ == "__main__":
    main()
