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

#------------------------------------------------------------------------------------------------------------------------

line = 0

sample_txtdata = seach_textdatas[line][2]

shape = seach_textdatas[line][1]

seach_data = np.ones(shape,dtype='i1')
seach_data[seach_textdatas[line][2]] = np.array(0)

print(seach_data)

test_txtdata = seach_data.copy()

set_x = 12
set_y = 10

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

Ssax = 0
Ssay = 0

finish_x = set_x + radius + 1
finish_y = set_y + radius + 1

Fsax = finish_x
Fsay = finish_y

if start_x < 0:
    Ssax = start_x
    start_x = 0

if start_y < 0:
    Ssay = start_y
    start_y = 0

if finish_x > (shape[1]):
    finish_x = shape[1]
if finish_y > (shape[0]):
    finish_y = shape[0]

Fsax = finish_x - Fsax
Fsay = finish_y - Fsay


def data_print(data,print_on_off):
    printlist = []
    for line in data:
        printtxt = " ["
        for txt in line:
            printtxt = printtxt + txt + " "
        
        printtxt = printtxt[:-1] + "]"
    
        printlist.append(printtxt)

    printlist[0] = "[" + printlist[0][1:]
    printlist[-1] = printlist[-1] + "]"

    if print_on_off == "1":
        for line in printlist:
            print(line)
        
    return printlist

print()

data_copy = np.array(seach_data.copy(),dtype=str)
#data_copy[set_y,set_x] = "+"

search = np.array(data_copy[start_y:finish_y, start_x:finish_x],dtype=str)

search[np.where(search == "0")] = "･"
search[np.where(search == "1")] = " "

data_copy[start_y:finish_y, start_x:finish_x] = search

print(f"center / X: {set_x}, Y: {set_y}")
print(f"start  / X:{start_x}, Y{start_y}")
print(f"finish / X:{finish_x}, Y{finish_y}\n")
print(f"Ssa    / X:{Ssax}, Y{Ssay}")

print(f"radius / {radius}")
center = np.array([radius + (Ssay), radius + (Ssax)])
print(f"center / X:{center[1]}, Y:{center[0]}\n")

data_copy[set_y,set_x] = "+"
data_print(data_copy,1)

print()
search_copy = search.copy()
search_copy[center[1],center[0]] = "+"
data_print(search_copy,1)

print()

print(center)

print()
where = np.where(search == "･")
print(where)

print()

sa = np.abs(np.where(search == "･") - center.reshape(2, 1))
sa = sa[0] ** 2 + sa[1] ** 2
sa = np.sqrt(sa)
print(f"MIN: {np.min(sa)}")

print()

def removal_background(color_image,RGB,kyoyou): #写真のNumPy配列を渡すと戻り値として背景を１とし、それ以外を0に置き換えた配列が戻ってくる。
    background_color = np.array(RGB)

    code0list = np.ones((color_image.shape[0]*color_image.shape[1],1), dtype='i1') #一旦0で埋める

    sa = np.abs(background_color - color_image)
    sa = sa.reshape(color_image.shape[0]*color_image.shape[1],3) #1ピクセル毎に背景色RGBと写真のRGBの差の絶対値の集合値を算出する為、配列を縦一列、列数３にする。
    text = np.array(np.where((np.sum(sa,axis=1)) > kyoyou)[0]) #背景色判定の許容値を超えた場合文字判定。

    code0list[text, 0] = np.array(0) #code0listに文字判定の場所を再代入。
    code0list = code0list.reshape(color_image.shape[0],color_image.shape[1]) #写真の比率にリサイズ。

    return code0list

def NEW_search(txtimage,search_txtdata,dataslist):
    rgb = dataslist["background_color"]
    kyoyoucolor = dataslist["kyoyou"]
    shape = np.array(search_txtdata[1])

    set_image = removal_background(cv2.resize(txtimage,dsize=(shape[1],shape[0])),rgb,kyoyoucolor)

    anser_data = np.array(set_image,dtype=str)

    where_true0 = np.where(anser_data[search_txtdata[2]] == "0")
    where_false0 = np.where(anser_data[search_txtdata[2]] == "1")

    #print(f"\nwhere_false0:\n{where_false0}\n")


    where_true0 = (search_txtdata[2][0][where_true0],search_txtdata[2][1][where_true0])
    where_false0 = (search_txtdata[2][0][where_false0],search_txtdata[2][1][where_false0])
        
    #print(f"\nfalse0:\n{where_false0}\n")

    anser_data[where_true0] = "･"
    anser_data[where_false0] = "!"
    anser_data[anser_data == "1"] = " "
    anser_data[anser_data == "0"] = "#"
    anser_data = data_print(anser_data,0)


    seach_data = np.ones(shape,dtype='i1')
    seach_data[search_txtdata[2]] = np.array(0)

    print(f"\n<picture>{((np.shape(set_image)[1])*2 + 1 - 9 + 5)*' '}<search>{((np.shape(set_image)[1])*2 + 1 - 9 + 5)*' '}<anser>")

    for i in range(np.shape(set_image)[0]):
        if i+1 == np.shape(set_image)[0] // 2:
            print(f'{set_image[i]} =?= {seach_data[i]}  =  {anser_data[i]}')
        else:
            print(f'{set_image[i]}     {seach_data[i]}     {anser_data[i]}')

    print()

    return set_image



keys_print()
Alltxtimages = dataslist["Alltxtimages"][0]


txtimage = "h"
search_txtdata = "b"

print(f"{txtimage} > 比率調整 > {search_txtdata}")

for line in range (len(Alltxtimages)):
    txt = seach_textdatas[line][3]

    if txt == txtimage:
        txtimage = Alltxtimages[line]
        break

for line in range (len(seach_textdatas)):
    txt = seach_textdatas[line][3]

    if txt == search_txtdata:
        search_txtdata = seach_textdatas[line]
        break

NEW_search(txtimage,search_txtdata,dataslist)