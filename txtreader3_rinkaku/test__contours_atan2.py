import pickle
import math

from SET_datas import SET_list

with open('/Users/matsuurakenshin/WorkSpace/development/txtreader/txtreader3_rinkaku/pickle_file/NEW_contours.picke', mode='br') as fi:
    NEW_contours = pickle.load(fi)

contours_degrees = []
for linenum in range(len(NEW_contours)):
    contour0 = NEW_contours[linenum-1]
    contour1 = NEW_contours[linenum]

    d = contour1 - contour0
    # print(d)

    contours_degrees.append(math.degrees(math.atan2((d[0] * -1),d[1])))

answer = SET_list(contours_degrees,guide=True,keep_start=False,keeplen=0)
with open('/Users/matsuurakenshin/WorkSpace/development/txtreader/txtreader3_rinkaku/Make_txtfile/contours_degrees.txt','w')as f:
    for line in answer:
        f.write(line)