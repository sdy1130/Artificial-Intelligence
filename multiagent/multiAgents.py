# multiAgents.py
# --------------
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


from util import manhattanDistance
from game import Directions
import random, util
import sys

from game import Agent

def manhattanHeuristicMod(position1, position2, info={}):
    "The Manhattan distance heuristic for a PositionSearchProblem"
    xy1 = position1
    xy2 = position2
    return abs(xy1[0] - xy2[0]) + abs(xy1[1] - xy2[1])

def euclideanHeuristicMod(position1, position2, info={}):
    "The Euclidean distance heuristic for a PositionSearchProblem"
    xy1 = position1
    xy2 = position2
    return ( (xy1[0] - xy2[0]) ** 2 + (xy1[1] - xy2[1]) ** 2 ) ** 0.5

class ReflexAgent(Agent):
    """
      A reflex agent chooses an action at each choice point by examining
      its alternatives via a state evaluation function.

      The code below is provided as a guide.  You are welcome to change
      it in any way you see fit, so long as you don't touch our method
      headers.
    """


    def getAction(self, gameState):
        """
        You do not need to change this method, but you're welcome to.

        getAction chooses among the best options according to the evaluation function.

        Just like in the previous project, getAction takes a GameState and returns
        some Directions.X for some X in the set {North, South, West, East, Stop}
        """
        # Collect legal moves and successor states
        legalMoves = gameState.getLegalActions()

        # Choose one of the best actions
        scores = [self.evaluationFunction(gameState, action) for action in legalMoves]
        bestScore = max(scores)
        bestIndices = [index for index in range(len(scores)) if scores[index] == bestScore]
        chosenIndex = random.choice(bestIndices) # Pick randomly among the best

        "Add more of your code here if you want to"

        return legalMoves[chosenIndex]

    def evaluationFunction(self, currentGameState, action):
        """
        Design a better evaluation function here.

        The evaluation function takes in the current and proposed successor
        GameStates (pacman.py) and returns a number, where higher numbers are better.

        The code below extracts some useful information from the state, like the
        remaining food (newFood) and Pacman position after moving (newPos).
        newScaredTimes holds the number of moves that each ghost will remain
        scared because of Pacman having eaten a power pellet.

        Print out these variables to see what you're getting, then combine them
        to create a masterful evaluation function.
        """
        # Useful information you can extract from a GameState (pacman.py)
        successorGameState = currentGameState.generatePacmanSuccessor(action)
        newPos = successorGameState.getPacmanPosition()
        newFood = successorGameState.getFood()
        newGhostStates = successorGameState.getGhostStates()
        newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]
        
        score = 0
        maxInt = sys.maxint
        #keep moving buddy!
        if action == Directions.STOP:
          score = -50
        #if the given action leads to win or lose
        if(successorGameState.isWin()):
          return maxInt

        #consider distance to food
        minDistanceToFood = maxInt
        for food in newFood.asList():
          nextDistanceToFood = manhattanHeuristicMod(food, newPos)
          if(nextDistanceToFood < minDistanceToFood):
            minDistanceToFood = nextDistanceToFood
        #give lower score if distance is greater
        score += 200 / (minDistanceToFood)

        #consider eating food
        if(currentGameState.getNumFood() > successorGameState.getNumFood()):
          score += 200

        #consider capsules
        successorCapsules = successorGameState.getCapsules()
        minDistanceToCapsule = maxInt
        for capsule in successorCapsules:
          nextDistanceToCap = manhattanHeuristicMod(capsule, newPos)
          if(nextDistanceToCap < minDistanceToCapsule):
            minDistanceToCapsule = nextDistanceToCap
        #give lower score if distance is greater
        score += 300 /(minDistanceToCapsule)

        #consider change in amount of capsules
        currentCapsules = currentGameState.getCapsules()
        if(len(currentCapsules) > len(successorCapsules)):
          score += 300

        #consider distance to ghosts
        ghostsPos = currentGameState.getGhostPositions()
        minDistanceToGhost = maxInt
        i = 0
        for ghost in ghostsPos:
          nextDistanceToGhost = manhattanHeuristicMod(ghost, newPos)
          #give lower score if distance is greater (go eat the ghost!)
          if newScaredTimes[i] > nextDistanceToGhost:
            score += newScaredTimes[i] / (nextDistanceToGhost + 1)
          #give higher score if distance is greater
          else:
            #game over bro
            if nextDistanceToGhost < 3:
              score = -maxInt
            score += nextDistanceToGhost / 5
          i += 1
          
        return score

def scoreEvaluationFunction(currentGameState):
    """
      This default evaluation function just returns the score of the state.
      The score is the same one displayed in the Pacman GUI.

      This evaluation function is meant for use with adversarial search agents
      (not reflex agents).
    """
    return currentGameState.getScore()

class MultiAgentSearchAgent(Agent):
    """
      This class provides some common elements to all of your
      multi-agent searchers.  Any methods defined here will be available
      to the MinimaxPacmanAgent, AlphaBetaPacmanAgent & ExpectimaxPacmanAgent.

      You *do not* need to make any changes here, but you can if you want to
      add functionality to all your adversarial search agents.  Please do not
      remove anything, however.

      Note: this is an abstract class: one that should not be instantiated.  It's
      only partially specified, and designed to be extended.  Agent (game.py)
      is another abstract class.
    """

    def __init__(self, evalFn = 'scoreEvaluationFunction', depth = '2'):
        self.index = 0 # Pacman is always agent index 0
        self.evaluationFunction = util.lookup(evalFn, globals())
        self.depth = int(depth)

class MinimaxAgent(MultiAgentSearchAgent):
    """
      Your minimax agent (question 2)
    """

    def getAction(self, gameState):
        """
          Returns the minimax action from the current gameState using self.depth
          and self.evaluationFunction.

          Here are some method calls that might be useful when implementing minimax.

          gameState.getLegalActions(agentIndex):
            Returns a list of legal actions for an agent
            agentIndex=0 means Pacman, ghosts are >= 1

          gameState.generateSuccessor(agentIndex, action):
            Returns the successor game state after an agent takes an action

          gameState.getNumAgents():
            Returns the total number of agents in the game
        """
        agentNum = gameState.getNumAgents()
        actionsScore = []
        maxInt = sys.maxint
        minInt = -maxInt

        def miniMax(gameState, depthCount):
          agentIndex = depthCount%agentNum
          #base case
          if depthCount >= self.depth*agentNum or gameState.isWin() or gameState.isLose():
            return self.evaluationFunction(gameState) #leaves

          #1 max layer for PacMan & agentNum-1 min layer
          if agentIndex != 0: #MIN
            result = maxInt
            for action in gameState.getLegalActions(agentIndex):
              nextGameState = gameState.generateSuccessor(agentIndex, action)
              result = min(result, miniMax(nextGameState, depthCount+1))
            return result
          else: #MAX
            result = minInt
            for action in gameState.getLegalActions(agentIndex):
              nextGameState = gameState.generateSuccessor(agentIndex, action)
              result = max(result, miniMax(nextGameState, depthCount+1))
              #store each action's evaluated value
              if depthCount == 0:
                actionsScore.append(result)
            return result
          
        result = miniMax(gameState, 0)
        return gameState.getLegalActions(0)[actionsScore.index(max(actionsScore))]

class AlphaBetaAgent(MultiAgentSearchAgent):
    """
      Your minimax agent with alpha-beta pruning (question 3)
    """

    def getAction(self, gameState):
        """
          Returns the minimax action using self.depth and self.evaluationFunction
        """

        agentNum = gameState.getNumAgents()
        actionsScore = []
        maxInt = sys.maxint
        minInt = -maxInt

        def alphaBeta(gameState, depthCount, alpha, beta):
          agentIndex = depthCount%agentNum
          #base case
          if depthCount >= self.depth*agentNum or gameState.isWin() or gameState.isLose():
            return self.evaluationFunction(gameState)

          if agentIndex != 0: #MIN
            result = maxInt
            for action in gameState.getLegalActions(agentIndex):
              newGameState = gameState.generateSuccessor(agentIndex, action)
              result = min(result, alphaBeta(newGameState, depthCount+1, alpha, beta))
              beta = min(beta, result)
              if beta <= alpha:
                break
            return result
          else: #MAX
            result = minInt
            for action in gameState.getLegalActions(agentIndex):
              newGameState = gameState.generateSuccessor(agentIndex, action)
              result = max(result, alphaBeta(newGameState, depthCount+1, alpha, beta))
              alpha = max(alpha, result)
              if depthCount == 0:
                actionsScore.append(result)
              if beta <= alpha:
                break
            return result

        result = alphaBeta(gameState, 0, minInt, maxInt)
        return gameState.getLegalActions(0)[actionsScore.index(max(actionsScore))]

class ExpectimaxAgent(MultiAgentSearchAgent):
    """
      Your expectimax agent (question 4)
    """

    def getAction(self, gameState):
        """
          Returns the expectimax action using self.depth and self.evaluationFunction

          All ghosts should be modeled as choosing uniformly at random from their
          legal moves.
        """
        agentNum = gameState.getNumAgents()
        actionsScore = []
        minInt = -sys.maxint

        def expectimax(gameState, depthCount):
          agentIndex = depthCount%agentNum
          #base case
          if depthCount >= self.depth*agentNum or gameState.isWin() or gameState.isLose():
            return self.evaluationFunction(gameState) #leaves

          #1 max layer for PacMan & agentNum-1 min layer
          if agentIndex != 0: #MIN
            successorsScore = []
            for action in gameState.getLegalActions(agentIndex):
              nextGameState = gameState.generateSuccessor(agentIndex, action)
              result = expectimax(nextGameState, depthCount+1)
              successorsScore.append(result)
            #each state has equal probablity
            expectedValue = sum([float(i)/len(successorsScore) for i in successorsScore])
            return expectedValue
          else: #MAX
            result = minInt
            for action in gameState.getLegalActions(agentIndex):
              nextGameState = gameState.generateSuccessor(agentIndex, action)
              result = max(result, expectimax(nextGameState, depthCount+1))
              #store each action's evaluated value
              if depthCount == 0:
                actionsScore.append(result)
            return result
          
        result = expectimax(gameState, 0)
        return gameState.getLegalActions(0)[actionsScore.index(max(actionsScore))]

def betterEvaluationFunction(currentGameState):
  """
  Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
  evaluation function (question 5).

  DESCRIPTION: Consider the position of food, capsules, and ghosts and evaluate the states based on that
  """
  score = currentGameState.getScore()
  pacmanPos = currentGameState.getPacmanPosition()
  ghostStates = currentGameState.getGhostStates()
  foodPos = currentGameState.getFood().asList()
  capsulePos = currentGameState.getCapsules()

  #consider ghosts
  for ghost in ghostStates:
    disGhost = manhattanDistance(pacmanPos, ghost.getPosition())
    if ghost.scaredTimer > 0:
      score += pow(max(8 - disGhost, 0), 2)
    else:
      score -= pow(max(7 - disGhost, 0), 2)

  #consider foods
  disFood = []
  for food in foodPos:
    disFood.append(1.0/manhattanDistance(pacmanPos, food))
  if len(disFood)>0:
    score += max(disFood)

  #consider capsules
  disCap = []
  for capsule in capsulePos:
    disCap.append(50.0/manhattanDistance(pacmanPos, capsule))
  if len(disCap) > 0:
    score += max(disCap)

  return score

# Abbreviation
better = betterEvaluationFunction

