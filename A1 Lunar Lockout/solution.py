# Look for #IMPLEMENT tags in this file. These tags indicate what has
# to be implemented to complete the LunarLockout  domain.

#   You may add only standard python imports---i.e., ones that are automatically
#   available on TEACH.CS
#   You may not remove any imports.
#   You may not import or otherwise source any of your own files

# import os for time functions
from search import *  # for search engines
from lunarlockout import LunarLockoutState, Direction, \
  lockout_goal_state  # for LunarLockout specific classes and problems
import math

# LunarLockout HEURISTICS
def heur_trivial(state):
  '''trivial admissible LunarLockout heuristic'''
  '''INPUT: a LunarLockout state'''
  '''OUTPUT: a numeric value that serves as an estimate of the distance of the state to the goal.'''
  return 0


def heur_manhattan_distance(state):
  '''Manhattan distance LunarLockout heuristic'''
  '''INPUT: a lunar lockout state'''
  '''OUTPUT: a numeric value that serves as an estimate of the distance of the state to the goal.'''
  # Write a heuristic function that uses Manhattan distance to estimate distance between the current state and the goal.
  # Your function should return a sum of the Manhattan distances between each xanadu and the escape hatch.
  mid = state.width // 2
  return sum([abs(mid - x[0]) + abs(mid - x[1]) for x in state.xanadus])


def heur_L_distance(state):
  '''L distance LunarLockout heuristic'''
  '''INPUT: a lunar lockout state'''
  '''OUTPUT: a numeric value that serves as an estimate of the distance of the state to the goal.'''
  # Write a heuristic function that uses mahnattan distance to estimate distance between the current state and the goal.
  # Your function should return a sum of the L distances between each xanadu and the escape hatch.
  mid = state.width // 2
  return sum([min(abs(mid - x[0]), 1) + min(abs(mid - x[1]), 1) for x in state.xanadus])


def heur_alternate(state):
  '''a better lunar lockout heuristic'''
  '''INPUT: a lunar lockout state'''
  '''OUTPUT: a numeric value that serves as an estimate of the distance of the state to the goal.'''
  # Your function should return a numeric value for the estimate of the distance to the goal.

  '''
  Uses L-distance as a base and deprioritizes certain undesirable states:
  states which have helper robots on none of the squares adjacent to the exit, or
  states which have helper robots on all 4 of the squares adjacent to the exit,
  both of which indicates there is no immediate path to the exit.
  Possibly because L-distance is trinary (and so has a really hard time distinguishing between 2 states [*]),
  using infinity as the hval for those states gave the best results.
  
  It seems that increasing the complexity of the hval calculatation even a little bit more
  results in a lot more failed searches, likely due to the 2 sec timebound as the hval is
  calculated for every state before it can even get put in the frontier (priority queue).
  
  For me, it seems that calculating whether or not every xanadu has a move in the state is too
  computationally expensive and ends up with more failed cases. Similarly with computing whether
  or not there is a helper on the exit, although in that case it could be because of [*] above.
  '''
  mid = state.width // 2
  r = 0
  robots = state.robots + state.xanadus

  for d in ((mid+1, mid), (mid, mid+1), (mid-1, mid), (mid, mid-1)):
    if d in robots:
      r += 1

  return math.inf if r == 0 or r == 4 else sum([min(abs(mid - x[0]), 1) + min(abs(mid - x[1]), 1) for x in state.xanadus])



def fval_function(sN, weight):
  """
  Provide a custom formula for f-value computation for Anytime Weighted A star.
  Returns the fval of the state contained in the sNode.

  @param sNode sN: A search node (containing a LunarLockoutState)
  @param float weight: Weight given by Anytime Weighted A star
  @rtype: float
  """

  # Many searches will explore nodes (or states) that are ordered by their f-value.
  # For UCS, the fvalue is the same as the gval of the state. For best-first search, the fvalue is the hval of the state.
  # You can use this function to create an alternate f-value for states; this must be a function of the state and the weight.
  # The function must return a numeric f-value.
  # The value will determine your state's position on the Frontier list during a 'custom' search.
  # You must initialize your search engine object as a 'custom' search engine if you supply a custom fval function.
  return sN.gval + weight * sN.hval


def anytime_weighted_astar(initial_state, heur_fn, weight=4., timebound=2):
  '''Provides an implementation of anytime weighted a-star, as described in the HW1 handout'''
  '''INPUT: a lunar lockout state that represents the start state and a timebound (number of seconds)'''
  '''OUTPUT: A goal state (if a goal is found), else False'''
  '''implementation of weighted astar algorithm'''
  se = SearchEngine('custom')
  start = os.times()[0]
  stop = start + timebound
  while os.times()[0] <= stop and weight >= 0:
    se.init_search(initial_state, lockout_goal_state, heur_fn, lambda sN : fval_function(sN, weight))
    final = se.search(timebound)
    weight -= 1
  return final


def anytime_gbfs(initial_state, heur_fn, timebound=2):
  # OPTIONAL
  '''Provides an implementation of anytime greedy best-first search.  This iteratively uses greedy best first search,'''
  '''At each iteration, however, a cost bound is enforced.  At each iteration the cost of the current "best" solution'''
  '''is used to set the cost bound for the next iteration.  Only paths within the cost bound are considered at each iteration.'''
  '''INPUT: a lunar lockout state that represents the start state and a timebound (number of seconds)'''
  '''OUTPUT: A goal state (if a goal is found), else False'''
  return 0


PROBLEMS = (
  # 5x5 boards: all are solveable
  LunarLockoutState("START", 0, None, 5, ((0, 0), (1, 0), (2, 2), (4, 2), (0, 4), (4, 4)), ((0, 1),)),
  LunarLockoutState("START", 0, None, 5, ((0, 0), (1, 0), (2, 2), (4, 2), (0, 4), (4, 4)), ((0, 2),)),
  LunarLockoutState("START", 0, None, 5, ((0, 0), (1, 0), (2, 2), (4, 2), (0, 4), (4, 4)), ((0, 3),)),
  LunarLockoutState("START", 0, None, 5, ((0, 0), (1, 0), (2, 2), (4, 2), (0, 4), (4, 4)), ((1, 1),)),
  LunarLockoutState("START", 0, None, 5, ((0, 0), (1, 0), (2, 2), (4, 2), (0, 4), (4, 4)), ((1, 2),)),
  LunarLockoutState("START", 0, None, 5, ((0, 0), (1, 0), (2, 2), (4, 2), (0, 4), (4, 4)), ((1, 3),)),
  LunarLockoutState("START", 0, None, 5, ((0, 0), (1, 0), (2, 2), (4, 2), (0, 4), (4, 4)), ((1, 4),)),
  LunarLockoutState("START", 0, None, 5, ((0, 0), (1, 0), (2, 2), (4, 2), (0, 4), (4, 4)), ((2, 0),)),
  LunarLockoutState("START", 0, None, 5, ((0, 0), (1, 0), (2, 2), (4, 2), (0, 4), (4, 4)), ((2, 1),)),
  LunarLockoutState("START", 0, None, 5, ((0, 0), (0, 2), (0, 4), (2, 0), (4, 0)), ((4, 4),)),
  LunarLockoutState("START", 0, None, 5, ((0, 0), (1, 0), (2, 2), (4, 2), (0, 4), (4, 4)), ((4, 0),)),
  LunarLockoutState("START", 0, None, 5, ((0, 0), (1, 0), (2, 2), (4, 2), (0, 4), (4, 4)), ((4, 1),)),
  LunarLockoutState("START", 0, None, 5, ((0, 0), (1, 0), (2, 2), (4, 2), (0, 4), (4, 4)), ((4, 3),)),
  # 7x7 BOARDS: all are solveable
  LunarLockoutState("START", 0, None, 7, ((4, 2), (1, 3), (6, 3), (5, 4)), ((6, 2),)),
  LunarLockoutState("START", 0, None, 7, ((2, 1), (4, 2), (2, 6)), ((4, 6),)),
  LunarLockoutState("START", 0, None, 7, ((2, 1), (3, 1), (4, 1), (2, 6), (4, 6)), ((2, 0), (3, 0), (4, 0))),
  LunarLockoutState("START", 0, None, 7, ((1, 2), (0, 2), (2, 3), (4, 4), (2, 5)), ((2, 4), (3, 1), (4, 0))),
  LunarLockoutState("START", 0, None, 7, ((3, 2), (0, 2), (3, 3), (4, 4), (2, 5)), ((1, 2), (3, 0), (4, 0))),
  LunarLockoutState("START", 0, None, 7, ((3, 1), (0, 2), (3, 3), (4, 4), (2, 5)), ((1, 2), (3, 0), (4, 0))),
  LunarLockoutState("START", 0, None, 7, ((2, 1), (0, 2), (1, 2), (6, 4), (2, 5)), ((2, 0), (3, 0), (4, 0))),
)

if __name__ == "__main__":

  # TEST CODE
  solved = 0;
  unsolved = [];
  counter = 0;
  percent = 0;
  timebound = 2;  # 2 second time limit for each problem
  print("*************************************")
  print("Running A-star")

  for i in range(len(
      PROBLEMS)):  # note that there are 40 problems in the set that has been provided.  We just run through 10 here for illustration.

    print("*************************************")
    print("PROBLEM {}".format(i))

    s0 = PROBLEMS[i]  # Problems will get harder as i gets bigger

    print("*******RUNNING A STAR*******")
    se = SearchEngine('astar', 'full')
    se.init_search(s0, lockout_goal_state, heur_alternate)
    final = se.search(timebound)

    if final:
      final.print_path()
      solved += 1
    else:
      unsolved.append(i)
    counter += 1

  if counter > 0:
    percent = (solved / counter) * 100

  print("*************************************")
  print("{} of {} problems ({} %) solved in less than {} seconds.".format(solved, counter, percent, timebound))
  print("Problems that remain unsolved in the set are Problems: {}".format(unsolved))
  print("*************************************")

  solved = 0;
  unsolved = [];
  counter = 0;
  percent = 0;
  print("Running Anytime Weighted A-star")

  for i in range(len(PROBLEMS)):
    print("*************************************")
    print("PROBLEM {}".format(i))

    s0 = PROBLEMS[i]
    weight = 4
    final = anytime_weighted_astar(s0, heur_alternate, weight, timebound)

    if final:
      final.print_path()
      solved += 1
    else:
      unsolved.append(i)
    counter += 1

  if counter > 0:
    percent = (solved / counter) * 100

  print("*************************************")
  print("{} of {} problems ({} %) solved in less than {} seconds.".format(solved, counter, percent, timebound))
  print("Problems that remain unsolved in the set are Problems: {}".format(unsolved))
  print("*************************************")

  # solved = 0;
  # unsolved = [];
  # counter = 0;
  # percent = 0;
  # print("Running Anytime GBFS")
  #
  # for i in range(len(PROBLEMS)):
  #   print("*************************************")
  #   print("PROBLEM {}".format(i))
  #
  #   s0 = PROBLEMS[i]
  #   final = anytime_gbfs(s0, heur_alternate, timebound)
  #
  #   if final:
  #     final.print_path()
  #     solved += 1
  #   else:
  #     unsolved.append(i)
  #   counter += 1
  #
  # if counter > 0:
  #   percent = (solved / counter) * 100
  #
  # print("*************************************")
  # print("{} of {} problems ({} %) solved in less than {} seconds.".format(solved, counter, percent, timebound))
  # print("Problems that remain unsolved in the set are Problems: {}".format(unsolved))
  # print("*************************************")
