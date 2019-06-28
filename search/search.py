# search.py
# ---------
# Licensing Information: Please do not distribute or publish solutions to this
# project. You are free to use and extend these projects for educational
# purposes. The Pacman AI projects were developed at UC Berkeley, primarily by
# John DeNero (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# For more info, see http://inst.eecs.berkeley.edu/~cs188/sp09/pacman.html

"""
In search.py, you will implement generic search algorithms which are called
by Pacman agents (in searchAgents.py).
"""

import util
from Queue import Queue, PriorityQueue

class SearchProblem:
    """
    This class outlines the structure of a search problem, but doesn't implement
    any of the methods (in object-oriented terminology: an abstract class).

    You do not need to change anything in this class, ever.
    """

    def getStartState(self):
        """
        Returns the start state for the search problem
        """
        util.raiseNotDefined()

    def isGoalState(self, state):
        """
          state: Search state

        Returns True if and only if the state is a valid goal state
        """
        util.raiseNotDefined()

    def getSuccessors(self, state):
        """
          state: Search state

        For a given state, this should return a list of triples,
        (successor, action, stepCost), where 'successor' is a
        successor to the current state, 'action' is the action
        required to get there, and 'stepCost' is the incremental
        cost of expanding to that successor
        """
        util.raiseNotDefined()

    def getCostOfActions(self, actions):
        """
         actions: A list of actions to take

        This method returns the total cost of a particular sequence of actions.  The sequence must
        be composed of legal moves
        """
        util.raiseNotDefined()


def tinyMazeSearch(problem):
    """
    Returns a sequence of moves that solves tinyMaze.  For any other
    maze, the sequence of moves will be incorrect, so only use this for tinyMaze
    """
    from game import Directions
    s = Directions.SOUTH
    w = Directions.WEST
    return  [s,s,w,s,w,w,s,w]

def search(problem, fringe):
    initial_state = problem.getStartState()
    initial_actions = []
    initial_candidate = (initial_state, initial_actions)
    fringe.push(initial_candidate)
    closed_set = set()
    while not fringe.isEmpty():
        candidate = fringe.pop()
        state, actions = candidate
        if problem.isGoalState(state):
            return actions
        if state not in closed_set:
            closed_set.add(state)
            candidate_successors = problem.getSuccessors(state)
            candidate_successors = filter(lambda x: x[0] not in closed_set, candidate_successors)
            candidate_successors = map(lambda x: (x[0], actions + [x[1]]), candidate_successors)
            for candidate in candidate_successors:
                fringe.push(candidate)

def depthFirstSearch(problem):
    """
    Search the deepest nodes in the search tree first

    Your search algorithm needs to return a list of actions that reaches
    the goal.  Make sure to implement a graph search algorithm

    To get started, you might want to try some of these simple commands to
    understand the search problem that is being passed in:

    print "Start:", problem.getStartState()
    print "Is the start a goal?", problem.isGoalState(problem.getStartState())
    print "Start's successors:", problem.getSuccessors(problem.getStartState())
    """

    parent = {}
    parent_move = {}
    Q = []

    Q.append(problem.getStartState())
    while len(Q) > 0:
        v = Q.pop()
        if problem.isGoalState(v):
            solution = []
            while v != problem.getStartState():
                solution.append(parent_move[v])
                v = parent[v]
            solution.reverse()
            return solution

        for (w, d, c) in problem.getSuccessors(v):
            if w not in parent:
                parent[w] = v
                parent_move[w] = d
                Q.append(w)
    raise Exception("oh no")

def breadthFirstSearch(problem):
    """
    Search the shallowest nodes in the search tree first.
    """
    parent = {}
    parent_move = {}
    Q = Queue()

    Q.put(problem.getStartState())
    while not Q.empty():
        v = Q.get()
        if problem.isGoalState(v):
            solution = []
            while v != problem.getStartState():
                solution.append(parent_move[v])
                v = parent[v]
            solution.reverse()
            return solution

        for (w, d, c) in problem.getSuccessors(v):
            if w not in parent:
                parent[w] = v
                parent_move[w] = d
                Q.put(w)
    raise Exception("oh no")

def uniformCostSearch(problem):
    "Search the node of least total cost first."
    parent = {}
    parent_move = {}
    distance = {}
    Q = PriorityQueue()

    Q.put((0, problem.getStartState()))
    distance[problem.getStartState()] = 0
    while not Q.empty():
        (d, v) = Q.get()
        if problem.isGoalState(v):
            solution = []
            while v != problem.getStartState():
                solution.append(parent_move[v])
                v = parent[v]
            solution.reverse()
            return solution

        for (w, direction, c) in problem.getSuccessors(v):
            if w not in parent or distance[w] > c+d :
                parent[w] = v
                parent_move[w] = direction
                distance[w] = c+d
                Q.put((c+d, w))

    raise Exception("oh no")

def nullHeuristic(state, problem=None):
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """
    return 0

def aStarSearch(problem, heuristic=nullHeuristic):
    "Search the node that has the lowest combined cost and heuristic first."
    heur = lambda x, problem=problem: 4 * heuristic(x, problem)
    parent = {}
    parent_move = {}
    distance = {}
    Q = PriorityQueue()
    raiz = problem.getStartState()
    Q.put((heur(raiz), 0, raiz))
    distance[raiz] = 0
    while not Q.empty():
        (h, d, v) = Q.get()
        if problem.isGoalState(v):
            solution = []
            while v != raiz:
                solution.append(parent_move[v])
                v = parent[v]
            solution.reverse()
            return solution

        for (w, direction, c) in problem.getSuccessors(v):
            if w not in parent or distance[w] > c+d :
                parent[w] = v
                parent_move[w] = direction
                distance[w] = c+d
                Q.put((heur(w)+c+d, c+d, w))

    raise Exception("oh no")

# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch
