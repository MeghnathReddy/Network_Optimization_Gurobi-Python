#!/usr/bin/env python
# coding: utf-8

# In[34]:


#coefficients and parameters
Production=["Factory1","Factory2"]
Distribution=["C"]
Warehouse=["W1","W2"]

#demand for Factory
demand_p={}
demand_p["Factory1"]=80
demand_p["Factory2"]=70

#demand for warehouse
demand={}
demand["W1"]=60
demand["W2"]=90

#cost from Factory to warehouse
cost_p={
    ("Factory1","W1"):6,
    ("Factory1","W2"):0,
    ("Factory2","W1"):0,
    ("Factory2","W2"):9,
    ("Factory1","C"):2,
    ("Factory2","C"):4,
}

#capacity of distribution centre
capacity_p={
    ("Factory1","C"):50,
    ("Factory2","C"):50,
    
}

#capacity of unused factory
capacity_x={
    ("Factory1","W2"):0,
    ("Factory2","W1"):0,
}

#capacity of distribution centre
capacity_w={
    ("C","W1"):50,
    ("C","W2"):50,
}

#cost from Distribution to warehouse
cost_d={
    ("C","W1"):3,
    ("C","W2"):4,
}


# In[35]:


from gurobipy import * 
model = Model("Company")

#decision variables
X={}
Y={}
Z={}

for i in Production: 
    for j in Distribution:
        X[i,j] = model.addVar(vtype=GRB.INTEGER,lb=0,ub=GRB.INFINITY)

for i in Production: 
    for j in Warehouse:
        Y[i,j] = model.addVar(vtype=GRB.INTEGER,lb=0,ub=GRB.INFINITY)

for i in Distribution: 
    for j in Warehouse:
        Z[i,j] = model.addVar(vtype=GRB.INTEGER,lb=0,ub=GRB.INFINITY)
        
model.modelSense = GRB.MINIMIZE                   
model.update()


# In[38]:


#demand constraints
#for factory
for i in Production:    
    model.addConstr ( quicksum(X[i,j] for j in Distribution)+ quicksum(Y[i,j] for j in Warehouse)== demand_p[i])  
#for warehouse
for j in Warehouse:    
    model.addConstr ( quicksum(Y[i,j] for i in Production) + quicksum(Z[i,j] for i in Distribution)== demand[j]) 
    
#maximum flow contraints
#from factory to centre
for i in Production:
    for j in Distribution:
        model.addConstr(X[i,j] <= capacity_p[i,j]) 

#from factory1 to centre
for Factory1 in Production:
    for W2 in Warehouse:
        model.addConstr(Y["Factory1","W2"] <= capacity_x["Factory1","W2"])
        
#from factory2 to centre       
for Factory2 in Production:
    for W2 in Warehouse:
        model.addConstr(Y["Factory2","W1"] <= capacity_x["Factory2","W1"])  
        
#from centre to warehouse    
for i in Distribution:
    for j in Warehouse:
        model.addConstr(Z[i,j] <= capacity_w[i,j]) 
        
# Equilibrium 

for j in Distribution:
    model.addConstr(quicksum(X[i,j] for i in Production) - quicksum(Z[j,m] for m in Warehouse) == 0) 

#objective function
objective = quicksum(cost_p[i,j]*X[i,j] for j in Distribution for i in Production)+ quicksum(cost_p[i,j]*Y[i,j] for j in Warehouse for i in Production) +quicksum(cost_d[j,m]*Z[j,m] for m in Warehouse for j in Distribution)

model.setObjective(objective)
model.optimize()


# In[39]:


#Printing outputs
if model.status==GRB.OPTIMAL:
    print ("Optimal value:", model.objVal)
    print ("--- Quantity (Production to Distribution)---")
    for j in Production: 
        for m in Distribution:
            print ( j, m, X[j,m].x)
    
    print ("--- Quantity (Production to Warehouse)---")
    for i in Production: 
        for j in Warehouse:
            print (i, j, Y[i,j].x)
    
    print ("--- Quantity (Distribution to Warehouse)---")
    for i in Distribution: 
        for j in Warehouse:
            print (i, j, Z[i,j].x)

