#斜辺調査プログラム
y = 0
x = 2
#------------------------------------------------------------

import math
import numpy as np

if y >= 0:
    senter_y = y
    point_y  = 0
    hosei_y  = y
else:
    senter_y = 0
    point_y  = abs(y)
    hosei_y  = None
    
if x >= 0:
    senter_x = 0
    point_x  = x
    hosei_x  = None
    
else:
    senter_x = abs(x)
    point_x  = 0
    hosei_x  = abs(x)


area = np.zeros((abs(y)+1,abs(x)+1),dtype=str)
area[:,:] = "."

a = abs(y)/abs(x)

for x1 in range(abs(x)):
    y1 = a*x1
    if y1%1 >= 0.6:
        y1 += (1 - y1%1)
    else:
        y1 -= y1%1
    if hosei_y != None:
        y1 = (hosei_y - y1)
    if hosei_x != None:
        x1 = (hosei_x - x1)
    area[int(y1),x1] = '+'

area[senter_y,senter_x] = '#'
area[point_y,point_x] = '*'

print()
for line in area:
    printline = ''
    for txt in line:
        printline += txt + ' '
    print(printline)

print()
airx = (len(str(x)) - 1) * ' '
airy = (len(str(y)) - 1) * ' '
print(f'"#"  y: {airy}0, x: {airx}0')
print(f'"*"  y: {y}, x: {x},')
print()
print('斜辺: ',math.sqrt(y**2 + x**2))
print()