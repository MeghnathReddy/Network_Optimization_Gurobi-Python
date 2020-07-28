#!/usr/bin/env python
# coding: utf-8

# In[13]:


#coefficients and parameters
Warehouse=["W1","W2"]
Retailer=["R1","R2","R3","R4","R5"]
Cost={
    ("W1","R1"):2,
    ("W1","R2"):4,
    ("W1","R3"):5,
    ("W1","R4"):2,
    ("W1","R5"):1,    #cost from warehouse to retailer
    ("W2","R1"):3,
    ("W2","R2"):1,
    ("W2","R3"):3,
    ("W2","R4"):2,
    ("W2","R5"):3,
    }

supply={}
supply["W1"]=2000    #that can be produced at warehouse
supply["W2"]=3000

demand={}
demand["R1"] = 500
demand["R2"] = 800
demand["R3"] = 1800  #demand at retailer
demand["R4"] = 300
demand["R5"] = 700

#Defining decision variables
#vtype: Variable type for new variable (GRB.CONTINUOUS, GRB.BINARY, GRB.INTEGER) 
from gurobipy import * 
model = Model("Warehouse Model")
    
X={}

for i in Warehouse: 
    for j in Retailer:
        X[i,j] = model.addVar(vtype=GRB.INTEGER,lb=0,ub=GRB.INFINITY)
model.modelSense = GRB.MINIMIZE                  
model.update()

#Constraints
#demand constraints
for m in Retailer:
    model.addConstr(quicksum(X[i,m] for i in Warehouse)==demand[m])
    
# maximum capacity 
for i in Warehouse:    
    model.addConstr(quicksum(X[i,j] for j in Retailer) <= supply[i] )  

#objective function
objective = quicksum(Cost[i,j]*X[i,j] for i in Warehouse for j in Retailer )
model.setObjective(objective)
model.optimize()

#Printing outputs
if model.status==GRB.OPTIMAL:
    print ("Optimal value:", model.objVal)
    print ("--- Quantity (Warehouse to customers)---")
    for i in Warehouse: 
        for m in Retailer:
            print ( i, m, X[i,m].x)
  

