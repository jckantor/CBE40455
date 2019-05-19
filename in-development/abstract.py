from __future__ import division
from coopr import pyomo

# define an abstract model
model = pyomo.AbstractModel()

# add number of linear constraints as attribute 
model.m = pyomo.Param(within=pyomo.NonNegativeIntegers)
model.n = pyomo.Param(within=pyomo.NonNegativeIntegers)

# although not required, it is convenient to define index sets
model.I = pyomo.RangeSet(1, model.m)
model.J = pyomo.RangeSet(1, model.n)

# now we define the coefficients (which are themselves defined over index sets!)
model.a = pyomo.Param(model.I, model.J)
model.b = pyomo.Param(model.I)
model.c = pyomo.Param(model.J)

# the next line declares a variable indexed by the set J
model.x = pyomo.Var(model.J, domain=pyomo.NonNegativeReals)

def objective(model):
    """Abstract representation of our model objective.""" 
    obj = pyomo.summation(model.c, model.x)
    return obj

# add the objective function to the model object as an attribute (OBJ can be arbitrary!)
model.OBJ = pyomo.Objective(rule=objective)

def constraints(model, i):
    """Abstract representation of model constraints."""
    # return the expression for the constraint for i
    return sum(model.a[i,j] * model.x[j] for j in model.J) >= model.b[i]

# the next line creates one constraint for each member of the set model.I (CONS can be arbitrary!)
model.CONS = pyomo.Constraint(model.I, rule=constraints)