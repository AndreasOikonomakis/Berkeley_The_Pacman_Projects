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

from game import Agent

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
        "*** YOUR CODE HERE ***"
        score = successorGameState.getScore()
        NewFoodList = newFood.asList()
        curFoodList = currentGameState.getFood().asList()


        if(len(NewFoodList)==0):# ean den yparxei allo faghto tote o pacman nikhse
            return score+500

        
        curPos = currentGameState.getPacmanPosition()# trexousa 8esh tou pacman 
        
        for ghostState in newGhostStates:#euresh apostashs manhattan apo ka8e fantasma
            if(util.manhattanDistance(newPos, ghostState.getPosition()) < 2 and ghostState.scaredTimer == 0):#apostash asfaleias = 2
                return -500#an h apostash einai mikroterh apo 2 kai to timer einai 0 tote o pacman exase

        CurfoodDist=[]
        for food in curFoodList:#euresh apostasewn manhattan gia thn trexousa katastash faghtwn
            CurfoodDist.append(util.manhattanDistance(curPos,food))

        NewfoodDist=[]
        for food in NewFoodList:#euresh apostasewn manhattan gia thn nea katastash faghtwn
            NewfoodDist.append(util.manhattanDistance(newPos,food))

        if(min(CurfoodDist)<min(NewfoodDist)):#an h elaxisth apostash apo ena faghto ths trexousas katastashs einai mikroterh apo th nea
            score-=1#tote meiwse to score dioti o pacman apomakrun8hke apo ta faghta


       
        if(newPos == curPos):#an o pacman paramenei akinhtos meiwse to score
            score-=1


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
    

    #to depth einai to va8os kai meiwnetai, to minORmax dhlwnei poianou seira einai px minORmax = 0 shmainei pacman alliws fantasma
    def MINIMAX(self,depth,gameState,minORmax):

        from operator import itemgetter#xrisimopoih8hke gia ta3inomhsh listas pou periexei zeugh [value,action]

        if(depth == 0 or gameState.isWin() or gameState.isLose()):#edw vriskomaste se fullo
            return [self.evaluationFunction(gameState),None]#epistrofh tou score me action=None gt eimaste se fullo

        results=[]#lista pou 8a krataei zeugh [value,action]
        Actions = gameState.getLegalActions(minORmax)#oi kinhseis tou ekastote agent


        if(minORmax == 0):# o kwdikas gia ton pacman
                        
            for action in Actions:#gia ka8e legal action tou pacman
 
                newState = gameState.generateSuccessor(0,action)#h nea katastash tou pacman                   
                results.append([self.MINIMAX(depth,newState,minORmax+1)[0],action])#ektelesh tou min
                    
            return max(results,key=itemgetter(0))#epistrofh zeugous megistou value (ta3inomish ws pros value)

        else:# o kwdikas gia ta fantasmata

            for action in Actions:#gia ka8e legal action fantasmatwn

                newState = gameState.generateSuccessor(minORmax,action)#h nea katastash twn fantasmatwn 
                
                if(minORmax == gameState.getNumAgents() - 1):#seira tou pacman an exoume 3eperasei ton ari8mo twn sunolikwn agents
                    results.append([self.MINIMAX(depth-1,newState,0)[0],action])#ektelsh tou max gia ton pacman
                else:#seira epomenou fantasmatos
                    results.append([self.MINIMAX(depth,newState,minORmax+1)[0],action])#ektelesh tou min gia ka8e epomeno fantasma
               
            return min(results,key=itemgetter(0))#epistrofh zeugous elaxistou value (ta3inomish ws pros value)

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

        return self.MINIMAX(self.depth,gameState,0)[1]#edw kaleitai h minmax kai epistefei to 2o pedio apo to zeugos [score,value]


class AlphaBetaAgent(MultiAgentSearchAgent):
    """
      Your minimax agent with alpha-beta pruning (question 3)
    """
    

    def AlphaBetaMINIMAX(self,depth,gameState,minORmax,a,b):

        from operator import itemgetter
        import sys

        if(depth == 0 or gameState.isWin() or gameState.isLose()):#vriskomaste se fullo
            return [self.evaluationFunction(gameState),None]

        Actions = gameState.getLegalActions(minORmax)
        bestAction = None
        results=[]

        if(minORmax == 0):
 
            bestValue = -sys.maxint#arxikopoihsh tou bestvalue me ton megalutero arnhtiko ari8mo
            
                       
            for action in Actions:
 
                if(a>b):#an to a einai megalutero apo to b epistrofh trexontos zeugous [bestValue,bestAction]
                    return [bestValue,bestAction]

                newState = gameState.generateSuccessor(0,action)                    
                result = self.AlphaBetaMINIMAX(depth,newState,minORmax+1,a,b)[0]#edw epistrefetai mono to value
                results.append([result,action])#eisagwgh zeugous [result,action] sthn lista

                if(a<result):#sugkrish tou result pou periexei to value
                    a=result#allagh tou a

                if(bestValue<result):#allagh twn timwn tou zeugous
                    bestValue = result
                    bestAction = action

                    
            return max(results,key=itemgetter(0))#epistrofh megistou zeugous [result,action]

        else:
        
            bestValue = sys.maxint#arxikopoihsh tou bestvalue me ton megalutero 8etiko ari8mo

            for action in Actions:

                if(a>b):#an to a einai megalutero apo to b epistrofh trexontos zeugous [bestValue,bestAction]
                    return [bestValue,bestAction]

                newState = gameState.generateSuccessor(minORmax,action) 
                
                if(minORmax == gameState.getNumAgents() - 1):#seira tou pacman
                    result = self.AlphaBetaMINIMAX(depth-1,newState,0,a,b)[0]
                else:
                    result = self.AlphaBetaMINIMAX(depth,newState,minORmax+1,a,b)[0]

                results.append([result,action])
                if(b>result):
                    b = result#allagh tou b

                if(bestValue>result):
                    bestValue = result
                    bestAction = action

        
            return min(results,key=itemgetter(0))#epistrofh elaxistou zeugous [result,action]


    def getAction(self, gameState):
        """
          Returns the minimax action using self.depth and self.evaluationFunction
        """
        "*** YOUR CODE HERE ***"
        import sys
        return self.AlphaBetaMINIMAX(self.depth,gameState,0,-sys.maxint,sys.maxint)[1]

class ExpectimaxAgent(MultiAgentSearchAgent):
    """
      Your expectimax agent (question 4)
    """
    def EXPECTIMAX(self,depth,gameState,minORmax):

        from operator import itemgetter
        import random

        if(depth == 0 or gameState.isWin() or gameState.isLose()):
            return [self.evaluationFunction(gameState),None]

        results=[]
        Actions = gameState.getLegalActions(minORmax)


        if(minORmax == 0):
                        
            for action in Actions:
 
                newState = gameState.generateSuccessor(0,action)                    
                results.append([self.EXPECTIMAX(depth,newState,minORmax+1)[0],action])
                    
            return max(results,key=itemgetter(0))

        else:

            for action in Actions:

                newState = gameState.generateSuccessor(minORmax,action) 
                
                if(minORmax == gameState.getNumAgents() - 1):
                    results.append([self.EXPECTIMAX(depth-1,newState,0)[0],action])
                else:
                    results.append([self.EXPECTIMAX(depth,newState,minORmax+1)[0],action])
               

            return [sum(result[0] for result in results)/len(results),None]#epistrofh tou mesou orou



    def getAction(self, gameState):
        """
          Returns the expectimax action using self.depth and self.evaluationFunction

          All ghosts should be modeled as choosing uniformly at random from their
          legal moves.
        """
        "*** YOUR CODE HERE ***"
        return self.EXPECTIMAX(self.depth,gameState,0)[1]

def betterEvaluationFunction(currentGameState):
    """
      Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
      evaluation function (question 5).

      DESCRIPTION: <write something here so we know what you did>
    """
    "*** YOUR CODE HERE ***"
    from operator import itemgetter

    score = currentGameState.getScore()
    
    CurPos = currentGameState.getPacmanPosition()

    GhostStates = currentGameState.getGhostStates()
    FoodList = currentGameState.getFood().asList()

   

    if(len(FoodList)==0):#an dn yparxei faghto o pacman nikhse
        return score+500

    FoodDist=[]
    for foodPos in FoodList:#upologistmos olwn twn apostasewn
        FoodDist.append(util.manhattanDistance(CurPos, foodPos))

    for ghostState in GhostStates:
        ghostDist = util.manhattanDistance(CurPos, ghostState.getPosition())

        if(ghostDist == 0 and ghostState.scaredTimer == 0):# ean dn einai tromagmeno kai to efage o pacman exase
            return -500
        elif(ghostDist < 0 and ghostState.scaredTimer != 0):# ean to fantasma einai tromagmeno kai to efage
            score+=200#bonus 200 pontoi        
  
    score-=min(FoodDist)#meiwsh tou score oso einai h elaxisth apostash apo kapoio faghto
 
    return score

# Abbreviation
better = betterEvaluationFunction

