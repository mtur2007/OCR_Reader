# txt = ' > :   90.0                 :  [21, 46]  :  [ 54,   0] ▶ :    0.0                 :  [21, 52]  :  [  0,   6]   :   -8.13010235415598    :  [22, 59]  :  [ -1,   7]   :  -18.43494882292201    :  [23, 62]  :  [ -1,   3]   :  -45.0                 :  [27, 66]  :  [ -4,   4]   :  -71.56505117707799    :  [30, 67]  :  [ -3,   1]   :  -80.53767779197439    :  [36, 68]  :  [ -6,   1]   :  -90.0                 :  [43, 68]  :  [ -7,   0]'

# list_txt = []

# print(len(txt)/54)
# for i in range(int(len(txt)/54)):
#     list_txt.append(txt[54 * i:54 * (i+1)])

# for i in range(len(list_txt)):
#     print(list_txt[-(i+1)])

# import math

# print(math.degrees(math.atan2(7,0)))

# print(math.degrees(math.atan2(6,-1)))
# print(math.degrees(math.atan2(3,-1)))
# print(math.degrees(math.atan2(4,-4)))
# print(math.degrees(math.atan2(1,-3)))
# print(math.degrees(math.atan2(1,-7)))
# print(math.degrees(math.atan2(0,-6)))



# txts = []
# with open('/Users/matsuurakenshin/WorkSpace/development/txtreader/txtreader3_rinkaku/search2.txt', 'r') as f:
#     for line in f:
#         txts.append(line)

# import numpy as np
# txts = np.array(txts)
# C_data = txts[7:15]
# e_data = txts[23:30]

# for C_line in C_data:
#     print(C_line[50:-2])
# for e_line in e_data:
#     print(e_line[46:-2])
import numpy as np
from SET_datas import SET_list
import pickle
import cv2

with open('/Users/matsuurakenshin/WorkSpace/development/txtreader/txtreader3_rinkaku/pickle_file/keep_datas.pickle',mode='br') as fi:
    keep_contourslist = pickle.load(fi)

datas = []
for line in keep_contourslist:
    datas.append(line[2][:,3,0])

for line in datas:
    print(line)
    print()

a = datas[0]
print(a[0])
print(type(a[0]))
b = datas[1]

set_list = []
for i in range(len(a)):
    set_list.append([[a[i]],[]])


searchline = 0
for i in range(len(b)):
    diff = abs(a - b[i])
    set_list[np.where(diff == np.min(diff))[0][0]][1].append(b[i])
    #print(np.min(diff))

answer = SET_list(set_list,guide=False,keep_start=False,keeplen=10)
with open('/Users/matsuurakenshin/WorkSpace/development/txtreader/txtreader3_rinkaku/Make_txtfile/search_atan2.txt','w') as f:

    for line in answer:
        f.write(line)


cv2.imwrite('/Users/matsuurakenshin/WorkSpace/development/txtreader/txtreader3_rinkaku/Make_picture/keep_data1.jpg', keep_contourslist[0][0])
cv2.imwrite('/Users/matsuurakenshin/WorkSpace/development/txtreader/txtreader3_rinkaku/Make_picture/keep_data2.jpg', keep_contourslist[1][0])
