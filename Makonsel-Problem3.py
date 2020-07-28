#!/usr/bin/env python
# coding: utf-8

# In[21]:


#coefficients and parameters
Production=["Plant1","Plant2"]
Warehouse=["W1","W2"]
Customer=["R1","R2","R3"]

#demand for plant
demand_w={}
demand_w["Plant1"]=225
demand_w["Plant2"]=300

#final demand of retailer
demand={}
demand["R1"]=175
demand["R2"]=200
demand["R3"]=150

#transportation cost from plant to warehouse
cost_w={
    ("Plant1","W1"):450,
    ("Plant1","W2"):560,
    ("Plant2","W1"):510,
    ("Plant2","W2"):600,
}

#capacity for warehouse
capacity_p={
    ("Plant1","W1"):125,
    ("Plant1","W2"):150,
    ("Plant2","W1"):175,
    ("Plant2","W2"):200,
}

#transportation cost from warehouse to retailer
cost_r={
    ("W1","R1"):470,
    ("W1","R2"):505,
    ("W1","R3"):495,
    
    ("W2","R1"):390,
    ("W2","R2"):415,
    ("W2","R3"):440,
}

#capacity for retailer
capacity_w={
    ("W1","R1"):100,
    ("W1","R2"):150,
    ("W1","R3"):100,
    
    ("W2","R1"):125,
    ("W2","R2"):150,
    ("W2","R3"):75,
}


# In[22]:


from gurobipy import * 
model = Model("Makonsel")

#decision variable
X={}
Y={}

for i in Production:
    for j in Warehouse:
        X[i,j] = model.addVar(vtype=GRB.INTEGER,lb=0,ub=GRB.INFINITY)
        
for i in Warehouse:
    for j in Customer:
         Y[i,j] = model.addVar(vtype=GRB.INTEGER,lb=0,ub=GRB.INFINITY)
            
model.modelSense = GRB.MINIMIZE                   
model.update()


# In[24]:


#demand constraints
#for plant
for i in Production:    
    model.addConstr(quicksum(X[i,j] for j in Warehouse)== demand_w[i])  

#for customer
for j in Customer:    
    model.addConstr(quicksum(Y[i,j] for i in Warehouse)== demand[j])  
    
#maximum flow contraints
#for warehouse
for i in Production:
    for j in Warehouse:
        model.addConstr(X[i,j] <= capacity_p[i,j]) 
#for customer
for i in Warehouse:
    for j in Customer:
        model.addConstr(Y[i,j] <= capacity_w[i,j]) 
    
# Equilibrium 
for j in Warehouse:
    model.addConstr(quicksum(X[i,j] for i in Production) - quicksum(Y[j,m] for m in Customer) == 0) 

#objective function
objective = quicksum(cost_w[i,j]*X[i,j] for j in Warehouse for i in Production)+ quicksum(cost_r[i,m]*Y[i,m] for m in Customer for i in Warehouse)

model.setObjective(objective)
model.optimize()


# In[25]:


#Printing outputs
if model.status==GRB.OPTIMAL:
    print ("Optimal value:", model.objVal)
    print ("--- Quantity (Production to Warehouse)---")
    for i in Production: 
        for j in Warehouse:
            print ( i, j, X[i,j].x)
    
    print ("--- Quantity (Warehouse to Customers)---")
    for i in Warehouse: 
        for j in Customer:
            print (i, j, Y[i,j].x)

