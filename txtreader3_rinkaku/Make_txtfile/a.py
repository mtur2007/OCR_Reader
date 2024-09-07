# txt = ' > :   90.0                 :  [21, 46]  :  [ 54,   0] ▶ :    0.0                 :  [21, 52]  :  [  0,   6]   :   -8.13010235415598    :  [22, 59]  :  [ -1,   7]   :  -18.43494882292201    :  [23, 62]  :  [ -1,   3]   :  -45.0                 :  [27, 66]  :  [ -4,   4]   :  -71.56505117707799    :  [30, 67]  :  [ -3,   1]   :  -80.53767779197439    :  [36, 68]  :  [ -6,   1]   :  -90.0                 :  [43, 68]  :  [ -7,   0]'

# list_txt = []

# print(len(txt)/54)
# for i in range(int(len(txt)/54)):
#     list_txt.append(txt[54 * i:54 * (i+1)])

# for i in range(len(list_txt)):
#     print(list_txt[-(i+1)])

import math

print(math.degrees(math.atan2(7,0)))

print(math.degrees(math.atan2(6,-1)))
print(math.degrees(math.atan2(3,-1)))
print(math.degrees(math.atan2(4,-4)))
print(math.degrees(math.atan2(1,-3)))
print(math.degrees(math.atan2(1,-7)))
print(math.degrees(math.atan2(0,-6)))

