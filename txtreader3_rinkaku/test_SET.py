import numpy as np
from SET_datas import SET_list as SET_list



# samplelist =  [
#                 [1000,1000,1000,1000,1000,1000],
#                 [2000,2000,2000,2000],
#                 [3000,3000,3000,3000,3000,3000,3000],
#                 [4000,4000,4000]
#                ]

# for line in samplelist:
#     print(line)
# [ R,G,B ]
test_array = np.zeros((40,15,3),dtype='i8')


test_array = test_array.tolist()
bug = 'bug'
test_array[5][1][0] = [bug,bug,bug]

test_array[8][1][0] = [bug,bug,bug]

test_array[9][3]  = bug
test_array[15][3] = bug
test_array[30][3] = bug

test_array[10][5][0] = [bug,[bug,bug]]
test_array[15][5][1] = [bug,[bug,bug]]
test_array[20][5][2] = [bug,bug,bug]
test_array[21][5][0] = [bug,bug,bug]


# test_array[5][14][0] = [bug,bug,bug]
# test_array[8][9][0] = [bug,bug,bug]

# test_array[10][8][0] = [bug,bug,bug]
# test_array[15][7][0] = [bug,bug,bug]
# test_array[20][12][0] = [bug,bug,bug]
# test_array[21][10][0] = [bug,bug,bug]


for line in test_array:
    print(line)


anser = SET_list(test_array,guide=True,keep_start=1,keeplen=100)

with open('/Users/matsuurakenshin/WorkSpace/development/txtreader/txtreader3_rinkaku/Make_txtfile/test_SET.txt','w') as f:
    for line in anser:
        f.write(line)