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


import random
import math

import util
from game import Agent, Directions  # noqa
from util import manhattanDistance  # noqa


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
        chosenIndex = random.choice(bestIndices)  # Pick randomly among the best

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

        "*** YOUR CODE HERE ***"

        food = newFood.asList()
        oldFoodNum = len(currentGameState.getFood().asList())
        # prioritize states that eat food
        score = min([manhattanDistance(newPos, f) for f in food]) if len(food) == oldFoodNum else 0

        gDist = [manhattanDistance(newPos, g) for g in [g.getPosition() for g in newGhostStates] if manhattanDistance(newPos, g) < 2]
        # ghosts get scarier the closer they are 👻
        score += math.inf if gDist and min(gDist) == 0 else sum([25.0 / d for d in gDist])
        score -= 2 * sum([g.scaredTimer for g in newGhostStates])
        # subtract scores instead of adding reciprocal values
        return successorGameState.getScore() - score


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

    PACMAN = 0

    def __init__(self, evalFn="scoreEvaluationFunction", depth="2"):
        self.index = 0  # Pacman is always agent index 0
        self.evaluationFunction = util.lookup(evalFn, globals())
        self.depth = int(depth)

    def isTerminalState(self, state):
        return state.isWin() or state.isLose()


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
        "*** YOUR CODE HERE ***"

        return self.maxAgent(gameState, 0)

    def maxAgent(self, state, depth):
        # Pacman's turn: get the state with the max score, it will be a ghost's turn next
        return state.getScore() if self.isTerminalState(state) else (
            max([(self.minAgent(state.generateSuccessor(self.PACMAN, a), depth, 1), a)
                 for a in state.getLegalActions(self.PACMAN)])[1] if depth == 0 else
            max([(self.minAgent(state.generateSuccessor(self.PACMAN, a), depth, 1), a)
                 for a in state.getLegalActions(self.PACMAN)])[0])

    def minAgent(self, state, depth, ghost):
        # Ghost #ghost's turn: get the state with the min score
        # It could be another ghost's turn next, or Pacman's turn next
        # Depth is only incremented after the last ghost moves,
        # so check the depth bound to decide the next step
        return state.getScore() if self.isTerminalState(state) else \
            min([(self.evaluationFunction(state.generateSuccessor(ghost, a))
                  if depth + 1 == self.depth else self.maxAgent(state.generateSuccessor(ghost, a), depth + 1))
                 if ghost + 1 == state.getNumAgents() else
                 self.minAgent(state.generateSuccessor(ghost, a), depth, ghost + 1)
                 for a in state.getLegalActions(ghost)])


class AlphaBetaAgent(MultiAgentSearchAgent):
    """
      Your minimax agent with alpha-beta pruning (question 3)
    """

    def getAction(self, gameState):
        """
          Returns the minimax action using self.depth and self.evaluationFunction
        """
        "*** YOUR CODE HERE ***"
        # Expanded versions of the minimax list comprehensions above to accomodate pruning
        return self.maxAgent(gameState, 0, -math.inf, math.inf)

    def maxAgent(self, state, depth, alpha, beta):
        if self.isTerminalState(state):
            return state.getScore()

        maxScore = -math.inf
        maxAction = Directions.STOP
        for a in state.getLegalActions(self.PACMAN):
            curr = self.minAgent(state.generateSuccessor(self.PACMAN, a), depth, 1, alpha, beta)

            if curr > maxScore:
                maxAction = a
                maxScore = curr
            if maxScore > alpha:
                alpha = maxScore
            if alpha >= beta:
                return alpha

        return maxAction if depth == 0 else maxScore

    def minAgent(self, state, depth, ghost, alpha, beta):
        if self.isTerminalState(state):
            return state.getScore()

        minScore = math.inf
        for a in state.getLegalActions(ghost):
            curr = (self.evaluationFunction(state.generateSuccessor(ghost, a)) if depth + 1 == self.depth else
                self.maxAgent(state.generateSuccessor(ghost, a), depth + 1, alpha, beta)) if ghost + 1 == state.getNumAgents() else \
                self.minAgent(state.generateSuccessor(ghost, a), depth, ghost + 1, alpha, beta)

            if curr < minScore:
                minScore = curr
            if minScore < beta:
                beta = minScore
            if alpha >= beta:
                return beta

        return minScore


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
        "*** YOUR CODE HERE ***"

        return self.maxAgent(gameState, 0)

    def maxAgent(self, state, depth):
        return self.evaluationFunction(state) if self.isTerminalState(state) else (
            max([(self.chanceAgent(state.generateSuccessor(self.PACMAN, a), depth, 1), a)
                 for a in state.getLegalActions(self.PACMAN)])[1] if depth == 0 else
            max([(self.chanceAgent(state.generateSuccessor(self.PACMAN, a), depth, 1), a)
                 for a in state.getLegalActions(self.PACMAN)])[0])

    def chanceAgent(self, state, depth, ghost):
        # return of the 1 liner list comprehensions, this time with some addition and division!
        return self.evaluationFunction(state) if self.isTerminalState(state) else \
            sum([((self.evaluationFunction(state.generateSuccessor(ghost, a))
                   if depth + 1 == self.depth else
                     self.maxAgent(state.generateSuccessor(ghost, a), depth + 1,))
                   if ghost + 1 == state.getNumAgents() else
                     self.chanceAgent(state.generateSuccessor(ghost, a), depth, ghost + 1)) /
                     len(state.getLegalActions(ghost))
                 for a in state.getLegalActions(ghost)])


def betterEvaluationFunction(currentGameState):
    """
      Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
      evaluation function (question 5).

      DESCRIPTION: The idea is to prioritize states with higher current game score and those states
      with more potential as determined by the features. As a side note, trying to prioritize
      power pellets directly seems to be a bad idea unfortunately.

      "Optimal" coefficients for the following features were found through trial and error.

      Features used:
      Current game score
        - Used as a baseline
      Inverse of total food distance
        - Used to prioritize states where Pacman is closer to food
        - Because total distance is used, sometimes Pacman will first ignore a
          small amount of food in favor of a large amount of food that is far away
      Distance from ghosts only if they are very close
        - 👻 Ghosts are only scary when they are close after all 👻
        - Used to make Pacman wait next to a power pellet to ensure a kill on a nearby ghost
            - Though sometimes Pacman will spare the ghost in favor of food
        - Also used to make Pacman run away from ghosts when they're not scared
      Total time that ghosts are scared for
        - Used to incentivise grabbing power pellets so ghosts can be treated as food
    """
    "*** YOUR CODE HERE ***"

    pos = currentGameState.getPacmanState().getPosition()
    ghosts = currentGameState.getGhostStates()

    foodScore = sum([1.0 / f for f in [manhattanDistance(pos, f) for f in currentGameState.getFood().asList()]])
    gDist = [manhattanDistance(pos, g) for g in [g.getPosition() for g in ghosts] if manhattanDistance(pos, g) < 2]
    gDistScore = math.inf if gDist and min(gDist) == 0 else sum([25.0 / d for d in gDist])
    scaredTime = 2 * sum([g.scaredTimer for g in ghosts])

    return currentGameState.getScore() + foodScore - gDistScore + scaredTime


# Abbreviation
better = betterEvaluationFunction
