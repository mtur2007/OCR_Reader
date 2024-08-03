import cv2
import matplotlib.pyplot as plt
import numpy as np
import os
import time
from SET_datas import SET_list
import pickle

#-----------------------------------------------------------------------------------------------------------
filename = "/Users/matsuurakenshin/WorkSpace/development/image_file_name.txt"
imageslist = []

if os.path.exists(filename) == False:
    with open("image_file_name.txt","w") as f:
        f.write("image_file_name")

imagenamefile = filename
if os.path.exists(imagenamefile) == True:
    with open(imagenamefile,"r") as f:
        for line in f:
            line = line.strip()
            if line != "image_file_name":
                if os.path.exists(line) == True:
                    imageslist.append(str(line.strip()))
                else:
                    print(f'image_file : "{line}" は存在しません。')


#-----------------------------------------------------------------------------------------------------------

# 輪郭 関連のファイル
def removal_background(color_image,RGB,kyoyou): #写真のNumPy配列を渡すと戻り値として背景を１とし、それ以外を0に置き換えた配列が戻ってくる。
    background_color = np.array(RGB)

    code0list = np.ones((color_image.shape[0]*color_image.shape[1],1), dtype='i1') #一旦0で埋める

    sa = np.abs(background_color - color_image)
    sa = sa.reshape(color_image.shape[0]*color_image.shape[1],3) #1ピクセル毎に背景色RGBと写真のRGBの差の絶対値の集合値を算出する為、配列を縦一列、列数３にする。
    text = np.array(np.where((np.sum(sa,axis=1)) > kyoyou)[0]) #背景色判定の許容値を超えた場合文字判定。

    code0list[text, 0] = np.array(0) #code0listに文字判定の場所を再代入。
    code0list = code0list.reshape(color_image.shape[0],color_image.shape[1]) #写真の比率にリサイズ。

    return code0list

# 画像処理 関連のファイル
def image_removal_background(imagename,RGB,kyoyou):
    #image = Image.open(imagename)
    image = cv2.cvtColor(cv2.imread(imagename),cv2.COLOR_BGR2RGB)
    color_image = np.array(image)


    if RGB == "auto":

        #自動背景検出機能

        shape = np.shape(image)
        a = image.reshape(shape[0] * shape[1],3)
        u, indices, inverse, counts = np.unique(a, axis=0, return_index=True, return_inverse=True, return_counts=True)
        #print(u)
        # [[ 0  0 10 30]
        #  [20 20 10 10]]

        print()

        #print(indices)
        # [1 0]

        #print(a[indices])
        # [[ 0  0 10 30]
        #  [20 20 10 10]]

        Max = np.amax(counts)
        print(Max)
        posishon = np.where(counts == Max)[0]
        
        RGB = u[posishon][0].tolist()

        #RGB = [31,31,31]

        #print(f"背景色自動検出: {RGB}")
    #else:
        #print(f"背景色指定: {RGB}")


    dataslist = {}
    dataslist["image"] = image
    dataslist["background_color"] = RGB
    dataslist["kyoyou"] = kyoyou

    code0list = removal_background(color_image,RGB,kyoyou)


    with open("coode0list_printfile.txt","w") as f:
        for y in range(code0list.shape[0]):
            txt = ""
            for x in range(code0list.shape[1]):
                txt = txt + str(code0list[y,x])
            f.write(txt + "\n")

    dataslist["code0list"] = code0list

    return dataslist


imagename = "/Users/matsuurakenshin/WorkSpace/development/POCARI.png"

dataslist = image_removal_background(imagename,'auto',1)


start = time.time()

where_0_Y, where_0_X = np.where(dataslist["code0list"] == 0)
code0list = dataslist["code0list"]
rinnkaku_Y = []
rinnkaku_X = []

for i in range(np.shape(where_0_Y)[0]):
    if np.count_nonzero(code0list[where_0_Y[i]-1:where_0_Y[i]+2, where_0_X[i]-1:where_0_X[i]+2] == 1) > 0:
        rinnkaku_Y.append(where_0_Y[i])
        rinnkaku_X.append(where_0_X[i])

rinkaku = (np.array(rinnkaku_Y), np.array(rinnkaku_X))
#sample = np.where(dataslist["code0list"] == 0)


### pickleで保存（書き出し）
with open('data.pickle', mode='wb') as fo:
  pickle.dump([rinnkaku_X,rinnkaku_Y], fo)



"""
with open("Remake_SET.txt","w") as f:
    for line in anser:
        f.write(f"{line}")
"""
"""
# 結果を表示
cv2.imshow('Green My Characters', printimage)
cv2.waitKey(0)
cv2.destroyAllWindows()
"""