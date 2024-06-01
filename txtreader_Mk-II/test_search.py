import cv2
import matplotlib.pyplot as plt
import numpy as np

import pickle

# seach_textdatas
with open('/Users/matsuurakenshin/WorkSpace/development/txtreader/txtreader_Mk-II/Save_retest.pickle', mode='br') as fi:
    seach_textdatas,retest = pickle.load(fi)

search_line = []

for linenum in range(len(seach_textdatas)):

    line = seach_textdatas[linenum]

    Sa_xy = line[1][0] * line[1][1]

    wariai = (len(line[2][0]) / Sa_xy) * 100

    if wariai > 90:
        
        search_line.append(linenum)
        print(f"\n対象: {line[3]}\nデータ比率: {(len(line[2][0]) / Sa_xy) * 100}%\n")
    #print(np.shape(line[2]))

printtxt = ""
count = 0
for line in search_line:
    printtxt = printtxt + f"{count}: {linenum} / {seach_textdatas[line][3]}\n"
    count += 1


NEW_retest = []

for line in range(len(retest)):
    insertlist = []
    for num in range(len(retest[line])):
        for search in search_line:
            if retest[line][num] != search:
                insertlist.append(retest[line][num])
    NEW_retest.append(insertlist)
                
        


"""
for line in retest:
    print(line)
"""