import math
a=float(input('Enter a= '))
b=float(input('Enter b= '))
c=float(input('Enter c= '))
if a==0:
    print('Incorrect input')
else:
    D=b*b-4*a*c
    if D==0:
        x=-b/2/a
        print('x1=x2=',x, sep='')
   
    elif D>0:
        x1=(-b-math.sqrt(D))/2/a
        x2=(-b+math.sqrt(D))/2/a
        print(f'x1={x1}, x2={x2}',sep='')
   
    else:
        print ('Equation has no solution')
