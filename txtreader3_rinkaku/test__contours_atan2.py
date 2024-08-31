import pickle
import math

with open('/Users/matsuurakenshin/WorkSpace/development/txtreader/txtreader3_rinkaku/pickle_file/NEW_contours.picke', mode='br') as fi:
    NEW_contours = pickle.load(fi)


for linenum in range(len(NEW_contours)):
    contour0 = NEW_contours[linenum-1]
    contour1 = NEW_contours[linenum]

    d = contour1 - contour0
    # print(d)

    print((math.atan2((d[0] * -1),d[1])))