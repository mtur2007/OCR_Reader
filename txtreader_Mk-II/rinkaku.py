import pickle
import time
import math
import numpy as np

with open('data.pickle', mode='br') as fi:
  rinnkaku_Y,rinnkaku_X = pickle.load(fi)

rinnkaku_X = np.array(rinnkaku_X)
rinnkaku_Y = np.array(rinnkaku_Y)

#輪郭でまとめる処理---------------------------------------------------------------------------------------------------------------------
"""
斜辺の長さから近いものを調べ、まとめる 
"""
#anser = SET_list(rinnkaku_Y,guide=True,keep_start=1,keeplen=1)

start = time.time()

count = 0

search_Y = 0
searcj_X = 0
y = rinnkaku_Y[search_Y]
x = rinnkaku_X[searcj_X]

print(y,x)
print(f'最長: {math.sqrt((1 ** 2) + (1 ** 2))}')

count = 0

diff = np.abs(y - rinnkaku_Y) + np.abs(x - rinnkaku_X)
index0 = np.where(diff == 0)
diff = np.delete(diff,index0)

mindiff = np.min(diff)
print('min',mindiff)
diff = np.where(diff==mindiff)
print('where',diff)

# for nowy,nowx in zip(rinnkaku_Y,rinnkaku_X):

#     say = y - nowy
#     sax = x - nowx
    
#     answer = math.sqrt(say**2+sax**2)
#     if answer <= 1.42:
#         if answer != 0:
#             print(nowy,nowx,answer)

finish = time.time()

print()
print(f'time: {finish-start}')
print()
#一括でコメントする方法(cmd + /)