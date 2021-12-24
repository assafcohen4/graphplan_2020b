

import util
from action import Action
from actionLayer import ActionLayer
from util import Pair
from proposition import Proposition
from propositionLayer import PropositionLayer

class PlanGraphLevel(object):
  """
  A class for representing a level in the plan graph.
  For each level i, the PlanGraphLevel consists of the actionLayer and propositionLayer at this level in this order!
  """
  independentActions = []  # updated to the independentActions of the propblem GraphPlan.py line 31 
  actions = []             # updated to the actions of the problem GraphPlan.py line 32 and planningProblem.py line 25
  props = []               # updated to the propositions of the problem GraphPlan.py line 33 and planningProblem.py line 26
  
  @staticmethod
  def setIndependentActions(independentActions):
    PlanGraphLevel.independentActions = independentActions
  
  @staticmethod  
  def setActions(actions):
    PlanGraphLevel.actions = actions
  
  @staticmethod    
  def setProps(props):
    PlanGraphLevel.props = props   
  
  def __init__(self):
    """
    Constructor
    """
    self.actionLayer = ActionLayer()    		    # see actionLayer.py
    self.propositionLayer = PropositionLayer()	# see propositionLayer.py
  
  def getPropositionLayer(self):
  # returns the proposition layer
    return self.propositionLayer
  
  def setPropositionLayer(self, propLayer):
  # sets the proposition layer
    self.propositionLayer = propLayer  
  
  def getActionLayer(self):
  # returns the action layer
    return self.actionLayer
    
  def setActionLayer(self, actionLayer):
  # sets the action layer
    self.actionLayer = actionLayer

  def updateActionLayer(self, previousPropositionLayer):
    # type: (PropositionLayer) -> None
    """ 
    Updates the action layer given the previous proposition layer (see propositionLayer.py)
    You should add an action to the layer if its preconditions are in the previous propositions layer,
    and the preconditions are not pairwise mutex. 
    allAction is the list of all the action (include noOp) in the domain
    You might want to use those functions:
    previousPropositionLayer.isMutex(prop1, prop2) returns true if prop1 and prop2 are mutex at the previous propositions layer
    previousPropositionLayer.allPrecondsInLayer(action) returns true if all the preconditions of action are in the previous propositions layer
    self.actionLayer.addAction(action) adds action to the current action layer
    """ 
    allActions = PlanGraphLevel.actions  # type: List[Action]
    #TODO autograde
    "*** YOUR CODE HERE ***"
    for a in allActions:
      should_add_a = False
      if previousPropositionLayer.allPrecondsInLayer(a):
        should_add_a = True
        for p1 in a.getPre():
          for p2 in a.getPre():
            if p2 in previousPropositionLayer.getPropositions() and \
                    previousPropositionLayer.isMutex(p1, p2):
              should_add_a = False
      if should_add_a:
        self.actionLayer.addAction(a)


    
  def updateMutexActions(self, previousLayerMutexProposition):
    # type: (list[Pair(Proposition,Proposition)]) -> None #TODO param annotation is probably incorrect
    """
    Updates the mutex list in self.actionLayer,
    given the mutex proposition from the previous layer.
    currentLayerActions are the actions in the current action layer
    You might want to use this function:
    self.actionLayer.addMutexActions(action1, action2)
    adds the pair (action1, action2) to the mutex list in the current action layer
    Note that action is *not* mutex with itself
    """

    currentLayerActions = self.actionLayer.getActions()
    # TODO was twice now changed check index
    "*** YOUR CODE HERE ***"
    for i in range(0,len(currentLayerActions)):
      for j in range (i, len(currentLayerActions)):
        if mutexActions(currentLayerActions[i],currentLayerActions[j],previousLayerMutexProposition):
          self.actionLayer.addMutexActions(currentLayerActions[i],currentLayerActions[j])

    #for a1 in currentLayerActions:
     # for a2 in currentLayerActions:
       # if mutexActions(a1, a2, previousLayerMutexProposition):
         # self.actionLayer.addMutexActions(a1, a2)
    
  def updatePropositionLayer(self):
    """
    Updates the propositions in the current proposition layer,
    given the current action layer.
    don't forget to update the producers list!
    Note that same proposition in different layers might have different producers lists,
    hence you should create two different instances.
    currentLayerActions is the list of all the actions in the current layer.
    You might want to use those functions:
    dict() creates a new dictionary that might help to keep track on the propositions that you've
           already added to the layer
    self.propositionLayer.addProposition(prop) adds the proposition prop to the current layer       
    
    """
    currentLayerActions = self.actionLayer.getActions()  # type: List[Action]
    "*** YOUR CODE HERE ***"
    already_added = {}  # type: Dict[Proposition, List[Action]]
    #add propositions and their producers to already_added
    for a in currentLayerActions:
      for p in a.getAdd():
        if p not in already_added:
          already_added[p] = [a]
        else:
          already_added[p].append(a)

    #add already_added to the proposition layer
    for key in already_added:
      new_prop = Proposition(key.getName())
      for a in already_added[key]:
        new_prop.addProducer(a)
      self.propositionLayer.addProposition(new_prop)


    
  def updateMutexProposition(self):
    """
    updates the mutex propositions in the current proposition layer
    You might want to use those functions:
    mutexPropositions(prop1, prop2, currentLayerMutexActions) returns true if prop1 and prop2 are mutex in the current layer
    self.propositionLayer.addMutexProp(prop1, prop2) adds the pair (prop1, prop2) to the mutex list of the current layer
    """
    currentLayerPropositions = self.propositionLayer.getPropositions()
    currentLayerMutexActions =  self.actionLayer.getMutexActions()

    "*** YOUR CODE HERE ***"
    #TODO was twice now changed check index
    #for p1 in currentLayerPropositions:
      #for p2 in currentLayerPropositions:
        #if mutexPropositions(p1,p2,currentLayerMutexActions):
          #self.propositionLayer.addMutexProp(p1,p2)

    for i in range(0,len(currentLayerPropositions)):
      for j in range(i, len(currentLayerPropositions)):
        if mutexPropositions(currentLayerPropositions[i],currentLayerPropositions[j],currentLayerMutexActions):
          self.propositionLayer.addMutexProp(currentLayerPropositions[i],currentLayerPropositions[j],currentLayerMutexActions)


    
  def expand(self, previousLayer):
    """
    Your algorithm should work as follows:
    First, given the propositions and the list of mutex propositions from the previous layer,
    set the actions in the action layer. 
    Then, set the mutex action in the action layer.
    Finally, given all the actions in the current layer,
    set the propositions and their mutex relations in the proposition layer.   
    """
    previousPropositionLayer = previousLayer.getPropositionLayer()
    previousLayerMutexProposition = previousPropositionLayer.getMutexProps()


    "*** YOUR CODE HERE ***"

    self.updateActionLayer(previousPropositionLayer)
    self.updateMutexActions(previousLayerMutexProposition)
    self.updatePropositionLayer()
    self.updateMutexProposition()




            
  def expandWithoutMutex(self, previousLayer):
    """
    Questions 11 and 12
    You don't have to use this function
    """
    previousPropositionLayer = previousLayer.getPropositionLayer()
    previousLayerMutexProposition = previousPropositionLayer.getMutexProps()
    "*** YOUR CODE HERE ***"
    self.updateActionLayer(previousPropositionLayer)
    self.updatePropositionLayer()
		
def mutexActions(a1, a2, mutexProps):
  """
  This function returns true if a1 and a2 are mutex actions.
  We first check whether a1 and a2 are in PlanGraphLevel.independentActions,
  this is the list of all the independent pair of actions (according to your implementation in question 1).
  If not, we check whether a1 and a2 have competing needs
  """ 
  if Pair(a1,a2) not in PlanGraphLevel.independentActions:
    return True    
  return haveCompetingNeeds(a1, a2, mutexProps)

def haveCompetingNeeds(a1, a2, mutexProps):
  # type: (Action, Action, list[Pair(Proposition,Proposition)]) -> bool
  """
  Complete code for deciding whether actions a1 and a2 have competing needs,
  given the mutex proposition from previous level (list of pairs of propositions).
  Hint: for propositions p  and q, the command  "Pair(p, q) in mutexProps"
        returns true if p and q are mutex in the previous level
  """
  "*** YOUR CODE HERE ***"
  #TODO autograder
  for pair in mutexProps:  # type: Pair
    if pair.a in a1.getPre() and pair.b in a2.getPre() or\
            pair.a in a2.getPre() and pair.b in a1.getPre():
      return False
  return True

		
def mutexPropositions(prop1, prop2, mutexActions):
  # type: (Proposition, Proposition, list[Pair(Action,Action)]) -> bool
  """
  complete code for deciding whether two propositions are mutex,
  given the mutex action from the current level (list of pairs of actions).
  Your updateMutexProposition function should call this function
  You might want to use this function:
  prop1.getProducers() returns the list of all the possible actions in the layer that have prop1 on their add list
  """
  # TODO autograder
  "*** YOUR CODE HERE ***"
  for action1 in prop1.getProducers():
    for action2 in prop2.getProducers():
      if Pair(action1,action2) in mutexActions:
        return False
  return True

