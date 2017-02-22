# search.py
# ---------
# Licensing Information:  You are free to use or extend these projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to UC Berkeley, including a link to http://ai.berkeley.edu.
# 
# Attribution Information: The Pacman AI projects were developed at UC Berkeley.
# The core projects and autograders were primarily created by John DeNero
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and
# Pieter Abbeel (pabbeel@cs.berkeley.edu).


"""
In search.py, you will implement generic search algorithms which are called by
Pacman agents (in searchAgents.py).
"""

import util

class SearchProblem:
    """
    This class outlines the structure of a search problem, but doesn't implement
    any of the methods (in object-oriented terminology: an abstract class).

    You do not need to change anything in this class, ever.
    """

    def getStartState(self):
        """
        Returns the start state for the search problem.
        """
        util.raiseNotDefined()

    def isGoalState(self, state):
        """
          state: Search state

        Returns True if and only if the state is a valid goal state.
        """
        util.raiseNotDefined()

    def getSuccessors(self, state):
        """
          state: Search state

        For a given state, this should return a list of triples, (successor,
        action, stepCost), where 'successor' is a successor to the current
        state, 'action' is the action required to get there, and 'stepCost' is
        the incremental cost of expanding to that successor.
        """
        util.raiseNotDefined()

    def getCostOfActions(self, actions):
        """
         actions: A list of actions to take

        This method returns the total cost of a particular sequence of actions.
        The sequence must be composed of legal moves.
        """
        util.raiseNotDefined()

class Node:

    def __init__(self, state, parent=None, action=None, path_cost=0):
        self.state = state
        self.parent = parent
        self.action = action
        self.path_cost = path_cost
        self.depth = 0
        self.ChildList=[] #lista pou krataei tous successors
        self.Actions=[]#lista pou krataei tis energeies
        if parent:
            self.depth = parent.depth + 1

    def __repr__(self):
        return self.action

    def __lt__(self, node):
        return self.state < node.state

    def expand(self, problem): #h expand xrhsimopoiei thn getSuccessors kai apo8ikeuei tous komvous sthn ChildList

        if(len(self.ChildList)==0):
            for n in problem.getSuccessors(self.state):
                node = Node(n[0],self,n[1],len(self.Actions))#dhmiourgia twn komvwn paidiwn,to costos einai to mege8os ths listas Actions
                node.Actions = self.Actions + [node.action]          
                self.ChildList.append(node)

        return self.ChildList


    def solution(self):
        return self.Actions



    def __eq__(self, other):
        return isinstance(other, Node) and self.state == other.state

    def __hash__(self):
        return hash(self.state)


def tinyMazeSearch(problem):
    """
    Returns a sequence of moves that solves tinyMaze.  For any other maze, the
    sequence of moves will be incorrect, so only use this for tinyMaze.
    """
    from game import Directions
    s = Directions.SOUTH
    w = Directions.WEST
    return  [s, s, w, s, w, w, s, w]

def depthFirstSearch(problem):

    stack = util.Stack()
    visited=[]

    cur_node = Node(problem.getStartState() ,None,None,0)
    
    stack.push(cur_node)
    while(not stack.isEmpty()):
        cur_node = stack.pop()
               
        if(problem.isGoalState(cur_node.state)):
            break 

        if(cur_node.state in visited):
            continue 

        visited.append(cur_node.state)        

        for n in cur_node.expand(problem):
            stack.push(n)    
        
   
    return cur_node.solution()

    util.raiseNotDefined()

def breadthFirstSearch(problem):

    queue = util.Queue()
    visited=[]
    ActionList=[]
    cur_node = Node(problem.getStartState() ,None,None,0)
    
    queue.push(cur_node)
    while(not queue.isEmpty()):
        cur_node = queue.pop()
               
        if(problem.isGoalState(cur_node.state)):
            break 

        if(cur_node in visited):
            continue 

        visited.append(cur_node)        

        for n in cur_node.expand(problem):
            queue.push(n)    
  
    return cur_node.solution()

    util.raiseNotDefined()


def uniformCostSearch(problem):

    pqueue = util.PriorityQueue()
    visited=[]
    Inpqueue={}
    cur_node = Node(problem.getStartState() ,None,None,0)

    pqueue.push(cur_node,0)

    while(not pqueue.isEmpty()):
        cur_node = pqueue.pop()
        if(cur_node in visited):
            continue

        if(problem.isGoalState(cur_node.state)):
            break 


        for n in cur_node.expand(problem):
            pqueue.update(n,problem.getCostOfActions(n.solution()))
        

        visited.append(cur_node)           
    return cur_node.solution()


    util.raiseNotDefined()

def nullHeuristic(state, problem=None):
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """
    return 0

def aStarSearch(problem, heuristic=nullHeuristic):

    pqueue = util.PriorityQueue()
    visited=[]

    cur_node = Node(problem.getStartState() ,None,None,0)

    pqueue.push(cur_node,0)

    while(not pqueue.isEmpty()):
        cur_node = pqueue.pop()
        if(cur_node in visited):
            continue

        if(problem.isGoalState(cur_node.state)):
            break 


        for n in cur_node.expand(problem):
            pqueue.update(n,problem.getCostOfActions(n.solution())+heuristic(n.state, problem))
          
        visited.append(cur_node)           
    return cur_node.solution()


    util.raiseNotDefined()


# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch
