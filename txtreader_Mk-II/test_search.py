import cv2
import matplotlib.pyplot as plt
import numpy as np

import pickle

# seach_textdatas
with open('/Users/matsuurakenshin/WorkSpace/development/txtreader/txtreader_Mk-II/Save_retest.pickle', mode='br') as fi:
    seach_textdatas,retest = pickle.load(fi)

for line in seach_textdatas:

    Sa_xy = line[1][0] * line[1][1]
    print(Sa_xy)

    #print(np.shape(line[2]))