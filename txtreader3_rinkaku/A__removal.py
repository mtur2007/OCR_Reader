
"""
画像処理 [背景色抜き(removal)] 関連のファイル
"""

import cv2
import matplotlib.pyplot as plt
import numpy as np
import os

#-----------------------------------------------------------------------------------------------------------

def removal_background(color_image,RGB,kyoyou): #写真のNumPy配列を渡すと戻り値として背景を１とし、それ以外を0に置き換えた配列が戻ってくる。
    background_color = np.array(RGB)

    code0list = np.ones((color_image.shape[0]*color_image.shape[1],1), dtype='i1') #一旦0で埋める

    sa = np.abs(background_color - color_image)
    sa = sa.reshape(color_image.shape[0]*color_image.shape[1],3) #1ピクセル毎に背景色RGBと写真のRGBの差の絶対値の集合値を算出する為、配列を縦一列、列数３にする。
    text = np.array(np.where((np.sum(sa,axis=1)) > kyoyou)[0]) #背景色判定の許容値を超えた場合文字判定。

    code0list[text, 0] = np.array(0) #code0listに文字判定の場所を再代入。
    code0list = code0list.reshape(color_image.shape[0],color_image.shape[1]) #写真の比率にリサイズ。

    return code0list

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


    # with open("coode0list_printfile.txt","w") as f:
    #     for y in range(code0list.shape[0]):
    #         txt = ""
    #         for x in range(code0list.shape[1]):
    #             txt = txt + str(code0list[y,x])
    #         f.write(txt + "\n")

    dataslist["code0list"] = code0list

    return dataslist
