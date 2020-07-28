#!/usr/bin/env python
# coding: utf-8

# In[75]:


from gurobipy import * 
model=Model("Metalco company")

#decision variables one for each alloy
A = model.addVar(vtype=GRB.CONTINUOUS,lb=0,ub=GRB.INFINITY)
B = model.addVar(vtype=GRB.CONTINUOUS,lb=0,ub=GRB.INFINITY)
C = model.addVar(vtype=GRB.CONTINUOUS,lb=0,ub=GRB.INFINITY)
D = model.addVar(vtype=GRB.CONTINUOUS,lb=0,ub=GRB.INFINITY)
E = model.addVar(vtype=GRB.CONTINUOUS,lb=0,ub=GRB.INFINITY)
model.modelSense = GRB.MINIMIZE                   
model.update()

#constraints
model.addConstr(60*A+25*B+45*C+30*D+50*E==35) #Tin limit
model.addConstr(20*A+15*B+45*C+40*D+40*E==35) #Zinc limit
model.addConstr(20*A+60*B+10*C+30*D+10*E==30) #Lead limit
model.addConstr(A+B+C+D+E==1)

#objective function
objective=22*A+26*B+25*C+21*D+27*E #minimize cost
model.setObjective(objective)
model.optimize()
    


# In[76]:


#printing output
if model.status==GRB.OPTIMAL:
    print ("Optimal value:", model.objVal)
    print("Proportion of alloy1 used:",A)
    print("Proportion of alloy2 used:",B)
    print("Proportion of alloy3 used:",C)
    print("Proportion of alloy4 used:",D)
    print("Proportion of alloy5 used:",E)


# In[ ]:


#Tried the same problem using Network flow but could not get the same result


# In[68]:


#coefficients and parameters
Warehouse=["Alloy1","Alloy2","Alloy3","Alloy4","Alloy5"]
Customer=["Tin","Lead","Zinc"]

demand={}
demand["Tin"]=35
demand["Lead"]=30
demand["Zinc"]=35

capacity_1={
    ("Alloy1","Tin"):60,
    ("Alloy1","Lead"):20, #for alloy1
    ("Alloy1","Zinc"):20,
}

capacity_2={
    ("Alloy2","Tin"):25,
    ("Alloy2","Lead"):60, #for alloy2
    ("Alloy2","Zinc"):15,
}

capacity_3={
    ("Alloy3","Tin"):45,
    ("Alloy3","Lead"):10, #for alloy3
    ("Alloy3","Zinc"):45,
}

capacity_4={
    ("Alloy4","Tin"):30,
    ("Alloy4","Lead"):30, #for alloy4
    ("Alloy4","Zinc"):40,
}

capacity_5={
    ("Alloy5","Tin"):50,
    ("Alloy5","Lead"):10, #for alloy5
    ("Alloy5","Zinc"):40,
    
}

cost={
    ("Alloy1","Tin"):22,
    ("Alloy1","Lead"):22,
    ("Alloy1","Zinc"):22,
    
    ("Alloy2","Tin"):26,
    ("Alloy2","Lead"):26,
    ("Alloy2","Zinc"):26,
                            #cost for each alloy type
    ("Alloy3","Tin"):25,
    ("Alloy3","Lead"):25,
    ("Alloy3","Zinc"):25,
    
    ("Alloy4","Tin"):21,
    ("Alloy4","Lead"):21,
    ("Alloy4","Zinc"):21,
    
    ("Alloy5","Tin"):27,
    ("Alloy5","Lead"):27,
    ("Alloy5","Zinc"):27,
}


# In[72]:


from gurobipy import * 
model=Model("Metalco company")
#decision variable
X={}
for i in Warehouse: 
    for j in Customer:
        X[i,j] = model.addVar(vtype=GRB.CONTINUOUS,lb=0,ub=GRB.INFINITY)
model.modelSense = GRB.MINIMIZE                   
model.update()


# In[73]:


#demand constraint
for m in Customer:
    model.addConstr(quicksum(X[i,m] for i in Warehouse)== demand[m]) 

#maximum flow constraint
for Alloy1 in Warehouse:
    for j in Customer:
        model.addConstr(X["Alloy1",j] <= capacity_1["Alloy1",j]) 
        
for Alloy2 in Warehouse:
    for j in Customer:
        model.addConstr(X["Alloy2",j] <= capacity_2["Alloy2",j]) 
        
for Alloy3 in Warehouse:
    for j in Customer:
        model.addConstr(X["Alloy3",j] <= capacity_3["Alloy3",j]) 
        
for Alloy4 in Warehouse:
    for j in Customer:
        model.addConstr(X["Alloy4",j] <= capacity_4["Alloy4",j]) 
        
for Alloy5 in Warehouse:
    for j in Customer:
        model.addConstr(X["Alloy5",j] <= capacity_5["Alloy5",j]) 
        
objective = quicksum(cost[i,j]*X[i,j] for j in Customer for i in Warehouse)
model.setObjective(objective)
model.optimize()
    


# In[74]:


#Printing outputs
if model.status==GRB.OPTIMAL:
    print ("Optimal value:", model.objVal)
    print ("--- Quantity (Warehouse to customers)---")
    for i in Warehouse: 
        for j in Customer:
            print ( i, j, X[i,j].x)

