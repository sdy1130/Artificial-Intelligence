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
    """
    Search the deepest nodes in the search tree first.

    Your search algorithm needs to return a list of actions that reaches the
    goal. Make sure to implement a graph search algorithm.

    To get started, you might want to try some of these simple commands to
    understand the search problem that is being passed in:

    print "Start:", problem.getStartState()
    print "Is the start a goal?", problem.isGoalState(problem.getStartState())
    print "Start's successors:", problem.getSuccessors(problem.getStartState())
    """

    #stack for frontier in format: [node, path taken, ancestor nodes]
    stack = util.Stack()
    start = problem.getStartState()
    stack.push((start, [], []))

    while not stack.isEmpty():
        #pop a node and a path to it
        node, path, path_checker = stack.pop()
        #get successors
        if problem.isGoalState(node):
            return path
        successors = problem.getSuccessors(node)
        for i in range(len(successors)):
            #node has not been visited by ancestors
            if successors[i][0] not in path_checker:
                #push into frontier
                stack.push((successors[i][0], path + [successors[i][1]], path_checker + [successors[i][0]]))

    #no path found, return empty path
    return []

def breadthFirstSearch(problem):
    """Search the shallowest nodes in the search tree first."""
    #queue for frontier in format: [node, path taken]
    queue = util.Queue()
    #full cycle checker
    visited = []

    start = problem.getStartState()

    queue.push((start, []))

    while not queue.isEmpty():
        #pop a node and a path to it
        node, path = queue.pop()
        if node not in visited:
            #mark as visited
            visited.append(node)
           #check if goal state
            if problem.isGoalState(node):
                return path
             #get successors
            successors = problem.getSuccessors(node)
            for i in range(len(successors)):
                #node has not been visited
                if successors[i][0] not in visited:
                    #push into frontier
                    queue.push((successors[i][0], path + [successors[i][1]]))

    #no path found, return empty path
    return []
    util.raiseNotDefined()

def uniformCostSearch(problem):
    """Search the node of least total cost first."""
    #priority queue for frontier in format: [(current node, path, cost), cost]
    frontier = util.PriorityQueue()
    #full cycle checker
    visited = []
    start = problem.getStartState()
    frontier.push((start, [], 0), 0)

    while not frontier.isEmpty():
        #pop a node and a path to it
        node, path, cost = frontier.pop()
        if node not in visited:
            #mark as visited
            visited.append(node)
            #check if node is goal
            if problem.isGoalState(node):
                return path
            #get successors
            successors = problem.getSuccessors(node)
            for i in range(len(successors)):
                #node has not been visited
                if successors[i][0] not in visited:
                    #push into frontier
                    frontier.push((successors[i][0], path + [successors[i][1]], successors[i][2] + cost), successors[i][2] + cost)

    #no path found, return empty path
    return []

def nullHeuristic(state, problem=None):
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """
    return 0

def aStarSearch(problem, heuristic=nullHeuristic):
    """Search the node that has the lowest combined cost and heuristic first."""
    #priority queue for frontier in format: [(current node, path, cost), cost]
    frontier = util.PriorityQueue()
    #full cycle checker
    visited = []
    start = problem.getStartState()
    frontier.push((start, [], 0), 0)

    while not frontier.isEmpty():
        #pop a node and a path to it
        node, path, cost = frontier.pop()
        if node not in visited:
            #mark as visited
            visited.append(node)
            #check if node is goal
            if problem.isGoalState(node):
                return path
            #get successors
            successors = problem.getSuccessors(node)
            for i in range(len(successors)):
                #node has not been visited
                if successors[i][0] not in visited:
                    #push into frontier
                    f = successors[i][2] + cost + heuristic(successors[i][0], problem)
                    frontier.push((successors[i][0], path + [successors[i][1]], successors[i][2] + cost), f)

    #no path found, return empty path
    return []

# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch
