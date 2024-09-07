
from SET_datas import SET_list as SET_list

from SET_datas import SET_numbers

import numpy as np


test_list = np.array([  -5,  -1])
print(test_list)
print(test_list.tolist())

test_list = np.array([[-5,-1],[-271,0],[71,292090000],[-5,-1]])
#test_list = [[5,1],[271,0],[71,29209],[5,1]]
#test_list = [['-5','-1'],['-271','0']]
#test_list = [[5,1,27,0]]

answer = SET_numbers(test_list,mode=0)
for line in answer:
    print(line)

# samplelist =  [
#                 [1000,1000,1000,1000],
#                 [2000,2000,2000,2000],
#                 [3000,[3000,3000],3000,3000,3000],
#                 [4000,4000,4000]
#                ]
              
# '''
# samplelist =  [
#                 [1000,[[1111]],1000,1000,[1111]],
#                 [2000,2000,2000,2000,[2222,2222],2000],
#                 [3000,3000,3000,3000,[3333,[3333,3333],3333,3333],3000],
#                 [4000,4000,4000,4000]
#                ]
# '''              



# answer = SET_list(samplelist,guide=True,keep_start=1,keeplen=20)

# with open("/Users/matsuurakenshin/WorkSpace/development/txtreader/txtreader3_rinkaku/Make_txtfile/test_SET.txt","w") as f:
#     for line in answer:
#         f.write(f"{line}")
