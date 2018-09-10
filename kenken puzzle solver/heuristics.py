'''
This file will contain different variable ordering heuristics to be used within
bt_search.

1. ord_dh(csp)
    - Takes in a CSP object (csp).
    - Returns the next Variable to be assigned as per the DH heuristic.
2. ord_mrv(csp)
    - Takes in a CSP object (csp).
    - Returns the next Variable to be assigned as per the MRV heuristic.
3. val_lcv(csp, var)
    - Takes in a CSP object (csp), and a Variable object (var)
    - Returns a list of all of var's potential values, ordered from best value 
      choice to worst value choice according to the LCV heuristic.

The heuristics can use the csp argument (CSP object) to get access to the 
variables and constraints of the problem. The assigned variables and values can 
be accessed via methods.
'''

import random
from copy import deepcopy
import propagators

def ord_dh(csp):
    '''
    Determine the variable with a largest number of 
    unassigned variables in constraints with the variable
    '''
    maxDegree = -1
    maxVar = None

    for var in csp.get_all_unasgn_vars():

        degree = 0
        #add up the number of other unassigned variables
        for c in csp.get_cons_with_var(var):
            degree = degree + c.get_n_unasgn() - 1
        
        if maxDegree < 0:
            maxDegree = degree
            maxVar = var
        if maxDegree < degree:
            maxDegree = degree
            maxVar = var

    return maxVar


def ord_mrv(csp):
    '''
    Determine an unassigned variable with the smallest number of leftover values
    '''

    minDomainSize = -1
    minVar = None

    for var in csp.get_all_unasgn_vars():
        #initialize
        if minDomainSize < 0:
            minDomainSize = var.cur_domain_size()
            minVar = var

        elif var.cur_domain_size() < minDomainSize:
            minDomainSize = var.cur_domain_size()
            minVar = var

    return minVar   

def val_lcv(csp, var):
    '''
    Assign a value (from the variable's domain) to the given variable
    then leverage FC propagation to determine how many values are being pruned
    due to the assignment. Return a sorted (according to the number of pruned values)
    list of values.
    '''

    domain = var.cur_domain()
    returnList = []
    dictionary = {}
    
    for value in domain:

        var.assign(value)

        garbage, prunedList = propagators.prop_FC(csp, var)
        dictionary[value] = len(prunedList)

        #reset
        for variable, val in prunedList:
            variable.unprune_value(val)

        var.unassign()

    #sort the dictionary according to the number of the pruned values
    dictionarySorted = sorted(dictionary.items(), key=lambda x: x[1])
    for key in dictionarySorted:
        returnList.append(int(key[0]))

    return returnList