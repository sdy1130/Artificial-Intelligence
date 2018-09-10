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
import cspbase
import itertools

def binary_ne_grid(kenken_grid):
    
    #initialize
    binaryCSP = cspbase.CSP("Binary NE Grid", [])   
    gridSize = kenken_grid[0][0]
    domain = []
    satisfyingTuples = []
    varArray = []
    
    #compute domain values
    for i in range(gridSize):
        domain.append(i+1)

    #comptue satisfying tuples
    for i in range(gridSize):
        for j in range(gridSize):
            if i+1 != j+1:
                satisfyingTuples.append((i+1,j+1))
    
    #create variables
    for i in range(gridSize):
        #for each row
        varArray.append([])
        for j in range(gridSize):
            #create new variable - each coordinate
            newVar = cspbase.Variable( "%d%d" % (i+1,j+1) , domain)
            #add a row element
            varArray[i].append(newVar)
            #add the variable to CSP
            binaryCSP.add_var(newVar)
            
    checked = []
    for i in range(gridSize):

        for j in range(gridSize):
            for k in range(gridSize):
                if j != k:
                    #to prevent double counting
                    #2^a * 3^b * 5^c - results a unique number using two numbers: a, b, and c
                    if (2**j)*(3**k)*(5**i) not in checked:
                        #row
                        #create a constraint
                        newConstraint = cspbase.Constraint("%d%d not equal %d%d" % (i+1,j+1,i+1,k+1), [varArray[i][j], varArray[i][k]])
                        #add satisfying tuples
                        newConstraint.add_satisfying_tuples(satisfyingTuples)
                        #add constraint to csp
                        binaryCSP.add_constraint(newConstraint)

                        #column
                        #create a constraint
                        newConstraint = cspbase.Constraint("%d%d not equal %d%d" % (j+1,i+1,k+1,i+1), [varArray[j][i], varArray[k][i]])
                        #add satisfying tuples
                        newConstraint.add_satisfying_tuples(satisfyingTuples)
                        #add constraint to csp
                        binaryCSP.add_constraint(newConstraint)
                        #mark as checked - add one for when j and k are switched to prevent double counting
                        checked.append((2**j)*(3**k)*(5**i))
                        checked.append((2**k)*(3**j)*(5**i))
    
    return binaryCSP, varArray
    

def nary_ad_grid(kenken_grid):
    #initialize
    naryCSP = cspbase.CSP("nary Grid", [])
    gridSize = kenken_grid[0][0]
    domain = []
    
    #compute domain values
    for i in range(gridSize):
        domain.append(i+1)
        
    #comptue satisfying tuples
    satisfyingTuples = [permutation for permutation in itertools.permutations(range(1, gridSize+1))]

    #create an array of variables
    varArray = []
    
    #create variables
    for i in range(gridSize):
        #for each row
        varArray.append([])
        for j in range(gridSize):
            #create new variable - each coordinate
            newVar = cspbase.Variable( "%d%d" % (i+1,j+1), domain)
            #add a row element
            varArray[i].append(newVar)
            #add the variable to CSP
            naryCSP.add_var(newVar)
            
    #create row and column constraints
    #initialize
    rowConstraintDict = {}
    colConstraintDict = {}
    for i in range(gridSize):
        rowConstraintDict[i] = []
        colConstraintDict[i] = []
 
    #compute scope
    for i in range(gridSize):
        for j in range(gridSize):
            rowConstraintDict[i].append(varArray[i][j])
            colConstraintDict[i].append(varArray[j][i])

    #create constraints
    for i in range(gridSize):
        rowConstraint = cspbase.Constraint("row %d" % i, rowConstraintDict[i])
        colConstraint = cspbase.Constraint("col %d" % i, colConstraintDict[i])
        #add satisfying tuples
        rowConstraint.add_satisfying_tuples(satisfyingTuples)
        colConstraint.add_satisfying_tuples(satisfyingTuples)
        #add to CSP
        naryCSP.add_constraint(rowConstraint)
        naryCSP.add_constraint(colConstraint)
    
    return naryCSP, varArray

def kenken_csp_model(kenken_grid):
    #initialize
    kenCSP = cspbase.CSP("kenken Grid", [])
    gridSize = kenken_grid[0][0]
    domain = []
    satisfyingTuples = []
    varArray = []
    
    #compute domain values
    for i in range(gridSize):
        domain.append(i+1)

    #comptue satisfying tuples
    for i in range(gridSize):
        for j in range(gridSize):
            if i+1 != j+1:
                satisfyingTuples.append((i+1,j+1))
    
    #create variables
    for i in range(gridSize):
        #for each row
        varArray.append([])
        for j in range(gridSize):
            #create new variable - each coordinate
            newVar = cspbase.Variable( "%d%d" % (i+1,j+1) , domain)
            #add a row element
            varArray[i].append(newVar)
            #add the variable to CSP
            kenCSP.add_var(newVar)
            
    checked = []
    for i in range(gridSize):

        for j in range(gridSize):
            for k in range(gridSize):
                if j != k:
                    #to prevent double counting
                    #2^a * 3^b * 5^c - results a unique number using two numbers: a, b, and c
                    if (2**j)*(3**k)*(5**i) not in checked:
                        #row
                        #create a constraint
                        newConstraint = cspbase.Constraint("%d%d not equal %d%d" % (i+1,j+1,i+1,k+1), [varArray[i][j], varArray[i][k]])
                        #add satisfying tuples
                        newConstraint.add_satisfying_tuples(satisfyingTuples)
                        #add constraint to csp
                        kenCSP.add_constraint(newConstraint)

                        #column
                        #create a constraint
                        newConstraint = cspbase.Constraint("%d%d not equal %d%d" % (j+1,i+1,k+1,i+1), [varArray[j][i], varArray[k][i]])
                        #add satisfying tuples
                        newConstraint.add_satisfying_tuples(satisfyingTuples)
                        #add constraint to csp
                        kenCSP.add_constraint(newConstraint)
                        #mark as checked - add one for when j and k are switched to prevent double counting
                        checked.append((2**j)*(3**k)*(5**i))
                        checked.append((2**k)*(3**j)*(5**i))
     
    #cage constraints
    cageConstraints = kenken_grid[1:]
    #cage constaints dictionary
    cageConstraintsDict = {}
    
    for i in range(len(cageConstraints)):
        #if cage size is 1
        if len(cageConstraints[i]) == 2:
            varArray[int(str(cageConstraints[i][0])[0])-1][int(str(cageConstraints[i][0])[1])-1].assign(cageConstraints[i][1])
        else:
            target = cageConstraints[i][-2]
            operation = cageConstraints[i][-1]
            cageSize = len(cageConstraints[i])-2

            satisfyingTuplesCage = []
            cageDomain = []

            for k in range(cageSize):
                cageDomain.append(domain)
            
            if cageSize not in cageConstraintsDict:
                #all possible values of cage values
                for possibles in itertools.product(*cageDomain):
                    satisfyingTuplesCage.append(possibles)
                cageConstraintsDict[cageSize] = satisfyingTuplesCage
            else:
                satisfyingTuplesCage = cageConstraintsDict[cageSize]

            #find all possible values for cage variables
            kenkenTuples = []
            #add    
            if operation == 0:
                for item in satisfyingTuplesCage:
                    sumItem = 0
                    for j in range(len(item)):
                        sumItem += int(item[j])
                    if sumItem == target:
                        kenkenTuples.append(item)
            #subtract
            elif operation == 1: 
                for item in satisfyingTuplesCage:
                    #prevent double checking
                    if item not in kenkenTuples:
                        subItem = int(item[0])
                        for j in range(1,len(item)):
                            subItem -= int(item[j])
                        if subItem == target:
                            #need consider all permutations
                            subAll = [permutation for permutation in itertools.permutations(item, len(item))]    
                            while len(subAll) > 0:  
                                kenkenTuples.append(subAll.pop(0))
            #multiply
            elif operation == 3:
                for item in satisfyingTuplesCage:
                    multItem = int(item[0])
                    for j in range(1,len(item)):
                        multItem *= int(item[j])
                    if multItem == target:
                        kenkenTuples.append(item)
            #divide
            else:
                for item in satisfyingTuplesCage:
                    #prevent double checking
                    if item not in kenkenTuples:
                        perms = itertools.permutations(item)
                        for p in perms:
                            product = 1
                            for i in p[1:]:
                                product = i*product
                            if p[0]/product == target:
                                divAll = [permutation for permutation in perms]    
                                while len(divAll) > 0:  
                                    kenkenTuples.append(divAll.pop(0))
    
            if len(kenkenTuples) == 0:
                print ("NO SOLUTION FOUND!!!")

            scope = []
            for item in cageConstraints[i][:-2]:
                scope.append(varArray[int(str(item)[0])-1][int(str(item)[1])-1])
            
            #add new cage constraint
            newConstraint = cspbase.Constraint("Cage %d" % (i), scope)
            newConstraint.add_satisfying_tuples(kenkenTuples)
            kenCSP.add_constraint(newConstraint)
    
    return kenCSP, varArray