from actionLayer import ActionLayer
from proposition import Proposition
from util import Pair
import copy
from propositionLayer import PropositionLayer
from planGraphLevel import PlanGraphLevel
from Parser import Parser
from action import Action

try:
  from search import SearchProblem
  from search import aStarSearch

except:
  from  search import SearchProblem
  from  search import aStarSearch

class PlanningProblem():
  def __init__(self, domain, problem):
    """
    Constructor
    """
    p = Parser(domain, problem)
    self.actions, self.propositions = p.parseActionsAndPropositions()	
                                            # list of all the actions and list of all the propositions
    self.initialState, self.goal = p.pasreProblem() 				
                                            # the initial state and the goal state are lists of propositions
    self.createNoOps() 											# creates noOps that are used to propagate existing propositions from one layer to the next
    PlanGraphLevel.setActions(self.actions)
    PlanGraphLevel.setProps(self.propositions)
    self._expanded = 0

   
    
  def getStartState(self):
    "*** YOUR CODE HERE ***"
    return self.initialState
    
  def isGoalState(self, state):
    # type: (list[Proposition]) -> bool
    """
    Hint: you might want to take a look at goalStateNotInPropLayer function
    """
    "*** YOUR CODE HERE ***"

    return not self.goalStateNotInPropLayer(state)
    
  def getSuccessors(self, state):
    # type: (list[Proposition]) -> (list[Proposition], Action, int)
    """   
    For a given state, this should return a list of triples, 
    (successor, action, stepCost), where 'successor' is a 
    successor to the current state, 'action' is the action
    required to get there, and 'stepCost' is the incremental 
    cost of expanding to that successor, 1 in our case.
    You might want to this function:
    For a list of propositions l and action a,
    a.allPrecondsInList(l) returns true if the preconditions of a are in l
    """
    self._expanded += 1
    "*** YOUR CODE HERE ***"
    successors = []  # type: list[(list[Proposition], Action, int)]

    for a in self.actions: #type: Action
      if a.allPrecondsInList(state):
        successor = ([],a,1)
        for p in state:
          if p not in successor[0]:
            successor[0].append(p)
        for p in a.getAdd():
          if p not in successor[0]:
            successor[0].append(p)
        for p in a.getDelete():
          if p in successor[0]:
            successor[0].remove(p)
        successors.append(successor)

    return successors



  def getCostOfActions(self, actions):
    return len(actions)
    
  def goalStateNotInPropLayer(self, propositions):
    """
    Helper function that returns true if all the goal propositions 
    are in propositions
    """
    for goal in self.goal:
      if goal not in propositions:
        return True
    return False

  def createNoOps(self):
    """
    Creates the noOps that are used to propagate propositions from one layer to the next
    """
    for prop in self.propositions:
      name = prop.name
      precon = []
      add = []
      precon.append(prop)
      add.append(prop)
      delete = []
      act = Action(name,precon,add,delete, True)
      self.actions.append(act)





def hasLeveledOff(Graph, level):
  if level == 0:
    return False
  return len(Graph[level].getPropositionLayer().getPropositions()) == len(Graph[level - 1].getPropositionLayer().getPropositions())


def maxLevel(state, problem): # type: (List[Proposition], PlanningProblem) -> float

  propLayerInit = PropositionLayer()
  for p in state:
    propLayerInit.addProposition(p)

  level = PlanGraphLevel()
  level.setPropositionLayer(propLayerInit)
  level_props = level.getPropositionLayer().getPropositions()

  graphPlan = []
  graphPlan.append(level)

  while not problem.isGoalState(level_props):
    if hasLeveledOff(graphPlan, len(graphPlan) - 1):
      return float('inf')

    next_level = PlanGraphLevel()
    next_level.expandWithoutMutex(level)
    level_props = next_level.getPropositionLayer().getPropositions()
    graphPlan.append(next_level)

  return len(graphPlan) - 1
  
def levelSum(state, problem):

  propLayerInit = PropositionLayer()

  for p in state:
    propLayerInit.addProposition(p)

  level = PlanGraphLevel()
  level.setPropositionLayer(propLayerInit)
  level_props = level.getPropositionLayer().getPropositions()
  graphPlan = [level]
  goals_levels = {p.getName(): None for p in problem.goal}  # type: dict[Proposition,int]

  while None in goals_levels.values():
    if hasLeveledOff(graphPlan, len(graphPlan) - 1):
      return float('inf')

    for p in problem.goal:
      if p in level_props and goals_levels[p.getName()] is None:
        goals_levels[p.getName()] = len(graphPlan) - 1

    next_level = PlanGraphLevel()
    next_level.expandWithoutMutex(level)
    level_props = next_level.getPropositionLayer().getPropositions()
    graphPlan.append(next_level)

  return sum(goals_levels.values())
  

if __name__ == '__main__':
  import sys
  import time
  if len(sys.argv) != 1 and len(sys.argv) != 4:
    print("Usage: PlanningProblem.py domainName problemName heuristicName(max, sum or zero)")
    exit()
  domain = 'dwrDomain.txt'
  problem = 'dwrProblem.txt'
  heuristic = lambda x,y: 0
  if len(sys.argv) == 4:
    domain = str(sys.argv[1])
    problem = str(sys.argv[2])
    if str(sys.argv[3]) == 'max':
      heuristic = maxLevel
    elif str(sys.argv[3]) == 'sum':
      heuristic = levelSum
    elif str(sys.argv[3]) == 'zero':
      heuristic = lambda x,y: 0
    else:
      print("Usage: PlanningProblem.py domainName problemName heuristicName(max, sum or zero)")
      exit()

  prob = PlanningProblem(domain, problem)
  start = time.clock()
  plan = aStarSearch(prob, heuristic)  
  elapsed = time.clock() - start
  if plan is not None:
    print("Plan found with %d actions in %.2f seconds" % (len(plan), elapsed))
  else:
    print("Could not find a plan in %.2f seconds" %  elapsed)
  print("Search nodes expanded: %d" % prob._expanded)
 
