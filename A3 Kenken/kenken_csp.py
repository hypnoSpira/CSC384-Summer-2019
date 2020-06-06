#Look for #IMPLEMENT tags in this file.
'''
All models need to return a CSP object, and a list of lists of Variable objects 
representing the board. The returned list of lists is used to access the 
solution. 

For example, after these three lines of code

    csp, var_array = kenken_csp_model(board)
    solver = BT(csp)
    solver.bt_search(prop_FC, var_ord)

var_array[0][0].get_assigned_value() should be the correct value in the top left
cell of the KenKen puzzle.

The grid-only models do not need to encode the cage constraints.

1. binary_ne_grid (worth 10/100 marks)
    - A model of a KenKen grid (without cage constraints) built using only 
      binary not-equal constraints for both the row and column constraints.

2. nary_ad_grid (worth 10/100 marks)
    - A model of a KenKen grid (without cage constraints) built using only n-ary 
      all-different constraints for both the row and column constraints. 

3. kenken_csp_model (worth 20/100 marks) 
    - A model built using your choice of (1) binary binary not-equal, or (2) 
      n-ary all-different constraints for the grid.
    - Together with KenKen cage constraints.

'''
from cspbase import *
import itertools
from functools import reduce

def setup(kenken_grid):
    # shared setup between all models
    csp = CSP('KenKen')
    n = kenken_grid[0][0]
    dom = [i + 1 for i in range(n)]
    var = [[Variable('V{}{}'.format(i, j), dom) for j in dom] for i in dom]

    return n, dom, var, csp


def binary_ne_grid(kenken_grid):
    #IMPLEMENT
    n, dom, var, csp = setup(kenken_grid)
    good_tups = [t for t in itertools.product(dom, dom) if t[0] != t[1]]

    for vs in var:
        for v in vs:
            csp.add_var(v)

    for i in range(n):
        for j in range(n):
            for k in range(n):
                if j < k:
                    row = Constraint('C(V{}{},V{}{})'.format(i + 1, j + 1, i + 1, k + 1), [var[i][j], var[i][k]])
                    row.add_satisfying_tuples(good_tups)
                    csp.add_constraint(row)
                if i < k:
                    col = Constraint('C(V{}{},V{}{})'.format(i + 1, j + 1, k + 1, j + 1), [var[i][j], var[k][j]])
                    col.add_satisfying_tuples(good_tups)
                    csp.add_constraint(col)

    return csp, var

def nary_ad_grid(kenken_grid):
    #IMPLEMENT
    n, dom, var, csp = setup(kenken_grid)
    good_tups = [t for t in itertools.product(dom, dom) if t[0] != t[1]]

    for vs in var:
        for v in vs:
            csp.add_var(v)

    for i in range(n):
        for j in range(n):
            for k in range(n):
                row = Constraint('C(V{}{},V{}{})'.format(i + 1, j + 1, i + 1, k + 1), [var[i][j], var[i][k]])
                col = Constraint('C(V{}{},V{}{})'.format(i + 1, j + 1, k + 1, j + 1), [var[i][j], var[k][j]])

                row.add_satisfying_tuples(good_tups)
                col.add_satisfying_tuples(good_tups)

                csp.add_constraint(row)
                csp.add_constraint(col)

    return csp, var

def kenken_csp_model(kenken_grid):
    #IMPLEMENT
    n, dom, var, csp = setup(kenken_grid)
    cs = []

    for cage in kenken_grid[1 : ]:
        if len(cage) == 2:
            i = int(str(cage[0])[0]) - 1
            j = int(str(cage[0])[1]) - 1
            var[i][j] = Variable('V{}{}'.format(i, j), [cage[1]])
        else:
            op = cage[-1]
            target = cage[-2]
            vCage = []
            for c in cage[: -2]:
                i = int(str(c)[0]) - 1
                j = int(str(c)[1]) - 1
                vCage.append(var[i][j])

            c = Constraint("C(C{})".format(cage), vCage)
            good_tups = []

            for t in itertools.product(*([dom] * len(vCage))):
                if op == 0 and sum(t) == target or op == 3 and reduce(lambda x, y: x * y, t) == target:
                    good_tups.append(t)

                elif op == 1:
                    for p in itertools.permutations(t):
                        if reduce(lambda x, y: x - y, p) == target:
                            good_tups.append(t)
                            break

                elif op == 2:
                    for p in itertools.permutations(t):
                        if reduce(lambda x, y: x // y, p) == target:
                            good_tups.append(t)
                            break

            c.add_satisfying_tuples(good_tups)
            cs.append(c)

    for vs in var:
        for v in vs:
            csp.add_var(v)

    for c in cs:
        csp.add_constraint(c)

    add_binary_constraints(n, dom, var, csp)

    return csp, var

def add_binary_constraints(n, dom, var, csp):
    good_tups = [t for t in itertools.product(dom, dom) if t[0] != t[1]]

    for i in range(n):
        for j in range(n):
            for k in range(n):
                if j < k:
                    row = Constraint('C(V{}{},V{}{})'.format(i + 1, j + 1, i + 1, k + 1), [var[i][j], var[i][k]])
                    row.add_satisfying_tuples(good_tups)
                    csp.add_constraint(row)
                if i < k:
                    col = Constraint('C(V{}{},V{}{})'.format(i + 1, j + 1, k + 1, j + 1), [var[i][j], var[k][j]])
                    col.add_satisfying_tuples(good_tups)
                    csp.add_constraint(col)