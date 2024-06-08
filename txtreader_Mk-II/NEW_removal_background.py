
import cv2
import matplotlib.pyplot as plt
import numpy as np


import pickle

### pickleで保存したファイルを読み込み
with open('/Users/matsuurakenshin/WorkSpace/development/sample_txtdata.pickle', mode='br') as fi:
    dataslist,insert_txtdatas,seach_textdatas = pickle.load(fi)

def keys_print():
    print(f"\ndataslist_keys:")
    for info_key in dataslist:
        print(f">> {info_key}")
    print()
#keys_print()

def removal_background(color_image,RGB,kyoyou): #写真のNumPy配列を渡すと戻り値として背景を１とし、それ以外を0に置き換えた配列が戻ってくる。
    background_color = np.array(RGB)

    code0list = np.ones((color_image.shape[0]*color_image.shape[1],1), dtype='i1') #一旦0で埋める

    sa = np.abs(background_color - color_image)
    sa = sa.reshape(color_image.shape[0]*color_image.shape[1],3) #1ピクセル毎に背景色RGBと写真のRGBの差の絶対値の集合値を算出する為、配列を縦一列、列数３にする。
    text = np.array(np.where((np.sum(sa,axis=1)) > kyoyou)[0]) #背景色判定の許容値を超えた場合文字判定。

    code0list[text, 0] = np.array(0) #code0listに文字判定の場所を再代入。
    code0list = code0list.reshape(color_image.shape[0],color_image.shape[1]) #写真の比率にリサイズ。

    return code0list



Alltxtimages = dataslist["Alltxtimages"]
back_color = dataslist["background_color"]
kyoyou = dataslist["kyoyou"]

txtimage = Alltxtimages[0][1]

#print(removal_background(txtimage,back_color,kyoyou))


def NEW_removal_background(color_image,RGB,kyoyou): #写真のNumPy配列を渡すと戻り値として背景を１とし、それ以外を0に置き換えた配列が戻ってくる。
    background_color = np.array(RGB)

    reshape_image = color_image.reshape(color_image.shape[0]*color_image.shape[1],3)

    test_sa = np.sum(np.abs(background_color - reshape_image),axis=1)

    test_sa = test_sa.reshape(color_image.shape[0],color_image.shape[1])

    print(f"全体:\n{test_sa}\n最大差: {np.max(test_sa)}\n")


    code0list = np.ones((color_image.shape[0]*color_image.shape[1],1), dtype='i1') #一旦0で埋める

    sa = np.abs(background_color - color_image)
    reshape_image = color_image.reshape(color_image.shape[0]*color_image.shape[1],3)

    sa = sa.reshape(color_image.shape[0]*color_image.shape[1],3) #1ピクセル毎に背景色RGBと写真のRGBの差の絶対値の集合値を算出する為、配列を縦一列、列数３にする。
    text_where = np.array(np.where((np.sum(sa,axis=1)) > kyoyou)[0]) #背景色判定の許容値を超えた場合文字判定。
    reshape_image = color_image.reshape(color_image.shape[0]*color_image.shape[1],3)

    text_colors = reshape_image[text_where]

    for line in text_colors:
        print(line / np.max(line))

    heritu = np.max(text_colors,axis=1)
    print(heritu.shape[0])
    heritu = heritu.reshape(heritu.shape[0],1)

    print(heritu)

    print(text_colors / heritu)
    
    np.abs(background_color - color_image)

    #print(text_colors)


    code0list[text_where, 0] = np.array(0) #code0listに文字判定の場所を再代入。
    code0list = code0list.reshape(color_image.shape[0],color_image.shape[1]) #写真の比率にリサイズ。

    return code0list


NEW_removal_background(txtimage,back_color,kyoyou)
