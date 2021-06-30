import math    
for x in range(2,11):
    print("For X =",x,"the possible 'ans' values are:")
    print(list(range(2,math.floor(20/x)+1)))