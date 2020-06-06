#Look for #IMPLEMENT tags in this file. These tags indicate what has
#to be implemented.

import random
'''
This file will contain different variable ordering heuristics to be used within
bt_search.

var_ordering == a function with the following template
    var_ordering(csp)
        ==> returns Variable 

    csp is a CSP object---the heuristic can use this to get access to the
    variables and constraints of the problem. The assigned variables can be
    accessed via methods, the values assigned can also be accessed.

    var_ordering returns the next Variable to be assigned, as per the definition
    of the heuristic it implements.

val_ordering == a function with the following template
    val_ordering(csp,var)
        ==> returns [Value, Value, Value...]
    
    csp is a CSP object, var is a Variable object; the heuristic can use csp to access the constraints of the problem, and use var to access var's potential values. 

    val_ordering returns a list of all var's potential values, ordered from best value choice to worst value choice according to the heuristic.

'''

def ord_mrv(csp):
    #IMPLEMENT
    mrv = min([(v.cur_domain_size(), v) for v in csp.get_all_unasgn_vars()]) if csp.get_all_unasgn_vars() else None
    return mrv[1] if mrv else mrv


def val_lcv(csp,var):
    #IMPLEMENT
    lcv = []
    for d in var.cur_domain():
        var.assign(d)
        sups = 0
        for c in csp.get_cons_with_var(var):
            for v in c.get_unasgn_vars():
                sups = sum([-1 for s in v.cur_domain() if c.has_support(v, s)])

        lcv.append((sups, d))
        var.unassign()

    return [value for (supports, value) in sorted(lcv)]

