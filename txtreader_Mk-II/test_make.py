import cv2
import matplotlib.pyplot as plt
import numpy as np

import pickle

# seach_textdatas
with open('/Users/matsuurakenshin/WorkSpace/development/txtreader/txtreader_Mk-II/Save_retest.pickle', mode='br') as fi:
    seach_textdatas,retest = pickle.load(fi)

seach_textdatas

#------------------------------------------------------------------------------------------------------------------------

line = 0

sample_txtdata = seach_textdatas[line][2]

shape = seach_textdatas[line][1]

seach_data = np.ones(shape,dtype='i1')
seach_data[seach_textdatas[line][2]] = np.array(0)

print(seach_data)

test_txtdata = seach_data.copy()

set_x = 0
set_y = 17

search_area_XY = 5

radius = search_area_XY // 2

'''

<seach_area_XY>

seach_area_XY = 3  |  search_area_XY = 5  |
                   |    *  *  *  *  *     |
     *  *  *       |    *  *  *  *  *     |
     *  *  *       |    *  *  *  *  *     |   ・・・
     *  *  *       |    *  *  *  *  *     |
                   |    *  *  *  *  *     |
radius == 1        |  radius == 2         |


<radius>

       . <   +
       . < radius
 .  .  *  .  .
 ^  ^  .
radius .

'''

start_x = set_x - radius
start_y = set_y - radius

finish_x = set_x + radius + 1
finish_y = set_y + radius + 1

if start_x < 0:
    start_x = 0
if start_y < 0:
    start_y = 0

if finish_x > (shape[1]):
    finish_x = shape[1]
if finish_y > (shape[0]):
    finish_y = shape[0]


def data_print(data):
    printlist = []
    for line in data:
        printtxt = " ["
        for txt in line:
            printtxt = printtxt + txt + " "
        
        printtxt = printtxt[:-1] + "]"
    
        printlist.append(printtxt)

    printlist[0] = "[" + printlist[0][1:]
    printlist[-1] = printlist[-1] + "]"


    for line in printlist:
        print(line)

print()

data_copy = np.array(seach_data.copy(),dtype=str)
data_copy[set_y,set_x] = "+"

search = np.array(data_copy[start_y:finish_y, start_x:finish_x],dtype=str)

search[np.where(search == "0")] = "･"
search[np.where(search == "1")] = " "

data_copy[start_y:finish_y, start_x:finish_x] = search

print(f"center / X: {set_x}, Y: {set_y}")
print(f"start  / X:{start_x}, Y{start_y}")
print(f"finish / X:{finish_x}, Y{finish_y}\n")

data_print(data_copy)

print()

data_print(search)

print()

