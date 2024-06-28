
def Myint(num): #数値の int部分を確実に表示させる様にする自作関数
    for line in range(len(str(num))):
        if str(num)[line] == ".":
            return int(str(num)[:line])
    return num


#数値の整列を行う関数

import copy
import numpy as np


def SET_txt(txtslist,mode,position):

    if mode == 0:
        Max = 0
        len_list = []

        for line in txtslist:
            len_list.append(len(line))
            if len(line) > Max:
                Max = len(line)

        New_list = []
        Line_list = []
        for nouse in range(Max):
            New_list.append("")

        for line in txtslist:
            Set_list = copy.deepcopy(New_list)

            for number in range(len(line)):
                Set_list[number] = line[number]
            
            Line_list.append(Set_list)
        
        Line_list = np.array(Line_list)

        search_list = []
        for num in range(np.shape(Line_list)[1]):
            search_list.append(Line_list[:,num])

        search_list = np.array(SET_txt(search_list,1,position))

        Line_list = []
        
        for num in range(np.shape(search_list)[1]):
            Line_list.append(search_list[:,num])
        
        returndata = []

        for line in range (np.shape(Line_list)[0]):
            cut = len_list[line]
            listline = Line_list[line].tolist()
            returndata.append(listline[:cut])

        return returndata

    
    elif mode == 1:

        for line in range(len(txtslist)):
            Maxtxtlen = 0

            for num in txtslist[line]:

                if len(str(num)) > Maxtxtlen:
                    Maxtxtlen = len(str(num))

            Maxlen = Maxtxtlen

            for nowread in range(len(txtslist[line])):
                txt = txtslist[line][nowread]
                Air = Maxlen - len(str(txt))

                if position == 0:

                    txtslist[line][nowread] = str(txt) + (Air * " ")
                elif position == 1:
                    txtslist[line][nowread] = (Air//2 * " ") + str(txt) + ((Air//2 + Air%2) * " ")
                elif position == 2:
                    txtslist[line][nowread] = (Air * " ") + str(txt)


        return txtslist#[:-1]


def SET_txts(txtslist,mode,position):

    if isinstance(txtslist[0], list) == False:
        txtslist = [txtslist]
        print(f"SET修正: {txtslist}")
        mode = 1

    if position == "left":
        position = 0
    if position == "center":
        position = 1
    if position == "right":
        position = 2

    txtslist = SET_txt(txtslist,mode,position)

    return txtslist



def SET_number(numberslist,mode):

    if mode == 0:
        Max = 0
        len_list = []

        for line in numberslist:
            len_list.append(len(line))
            if len(line) > Max:
                Max = len(line)
        
        New_list = []
        Line_list = []
        for nouse in range(Max):
            New_list.append("")

        for line in numberslist:
            Set_list = copy.deepcopy(New_list)

            for number in range(len(line)):
                Set_list[number] = line[number]
            
            Line_list.append(Set_list)
        
        Line_list = np.array(Line_list)

        search_list = []
        for num in range(np.shape(Line_list)[1]):
            search_list.append(Line_list[:,num])

        search_list = np.array(SET_number(search_list,1))

        Line_list = []
        
        for num in range(np.shape(search_list)[1]):
            Line_list.append(search_list[:,num])
        
        returndata = []

        for line in range (np.shape(Line_list)[0]):
            cut = len_list[line]
            listline = Line_list[line].tolist()
            returndata.append(listline[:cut])

        return returndata

    
    elif mode == 1:

        for line in range(len(numberslist)):
            Maxintlen,Maxfloatlen = 0,0

            for num in numberslist[line]:

                if len(str(Myint(num))) > Maxintlen:
                    Maxintlen = len(str(Myint(num)))

                if len(str(num)) - len(str(Myint(num))) > Maxfloatlen:
                    Maxfloatlen = len(str(num)) - len(str(Myint(num)))

            Maxlen = Maxintlen + Maxfloatlen

            for nowread in range(len(numberslist[line])):
                num = numberslist[line][nowread]
                Air0 = Maxintlen - len(str(Myint(num)))
                Air1 = Maxlen - (Air0 + len(str(num)))

                numberslist[line][nowread] = (Air0 * " ") + str(num) + (Air1 * " ")

        return numberslist#[:-1]

def SET_numbers(numberslist,mode):

    if isinstance(numberslist[0], list) == False:
        numberslist = [numberslist]
        print(f"SET修正: {numberslist}")
        mode = 1

    numberslist = SET_number(numberslist,mode)

    return numberslist


def data_print(data,print_on_off):
    printlist = []
    for line in data:
        printtxt = " ["
        for txt in line:
            printtxt = printtxt + str(txt) + " "
        
        printtxt = printtxt[:-1] + "]"
    
        printlist.append(printtxt)

    printlist[0] = "[" + printlist[0][1:]
    printlist[-1] = printlist[-1] + "]"

    if print_on_off == 1:
        for line in printlist:
            print(line)
        
    return printlist


def SET_data(datas):

    Allprint_txt = []
    Lineslist = []
    for line in datas:
        # [[],[],[]]
        #  ^  ^  ^
        max= 0
        for data in line:
            # [ [ [],[] ], [ [],[] ] ,[ [],[] ] ]
            #      ^  ^       ^  ^       ^  ^

            if len(data) > max:
                max = len(data)

        printline = []
        for nouse in range(max):
            printline.append([])
        for data in line:
            for dataline in range(len(data)):
                printline[dataline].append(data[dataline])

            for num in range((max-1 - dataline)):
                printline[dataline + num+1].append('')

        for line in printline:
            Allprint_txt.append(line)
        
        Lineslist.append(len(Allprint_txt)-1)
    
    #return Allprint_txt

    set_datas = SET_txts(Allprint_txt,0,0)

    set_shape = []
    start = 0
    finish = Lineslist[0] + 1
    set_shape.append(set_datas[start:finish])


    for linenum in range(len(Lineslist)-1):
        linenum += 1

        start = Lineslist[linenum-1] + 1
        finish = Lineslist[linenum] + 1
        set_shape.append(set_datas[start:finish])

    return set_shape

def data_border_print(set_data,file_name):
    printlist = []
    linelen0 = 0

    for linenum in range(len(set_data)):
        dataline = set_data[linenum]
        if len(dataline) != 0:
            writeline = []
            for line in dataline:
                printline = ""
                for txt in line:
                    printline = printline + "  |  " + txt
                printline = printline[2:] + "  |"

                writeline.append(printline)
        
            linelen1 = len(printline)

            if linelen0 > linelen1:
                printlist.append(f"{'-'*linelen0}\n\n")
            else:
                printlist.append(f"{'-'*linelen1}\n\n")
            
            linelen0 = linelen1

            for line in writeline:
                printlist.append(f"{line}\n")
            printlist.append("\n")
        
        else:
            printlist.append(f"{'-'*linelen0}\n\n")
            if linenum != len(set_data)-1:
                printlist.append(f" >> Xx_None_data_xX\n\n")
            else:
                printlist.append(f" >> Xx_None_data_xX")
            linelen0 = 0

    if len(set_data[-1]) != 0:
        printlist.append(f"{'-'*linelen1}")

    return printlist




import random

def Myrandom(lennum, a,b, numtype):

    numberslist = []
    for i in range(lennum):
        if numtype == 0:
            randomnum = random.randint(a, b)
        elif numtype == 1:
            randomnum = random.uniform(a, b)
        elif numtype == 2:
            if random.randint(0, 1) == 0:
                randomnum = random.randint(a, b)
            else:
                randomnum = random.uniform(a, b)

        lownum = 1
        if randomnum % 1 > 0:
            lownum = len(str(Myint(randomnum))) +2
        elif randomnum < 0:
            lownum = 2
        stop = random.randint(lownum,len(str(randomnum)))

        numberslist.append(str(randomnum)[:stop])

    return numberslist

def list_random_del(datalist):
    count = 0

    for line in range(len(datalist)):
        cut_line = random.randint(1, len(datalist[line]))

        datalist[line] = datalist[line][0:cut_line]

        if cut_line == 1:
            count += 1
    
    if count == len(datalist):
        New_datalist = []
        for line in range(len(datalist)):
            New_datalist.append(datalist[line][0])
        datalist = New_datalist
        print(f"\n\nここだーーーーーーーー !!!! \n\n")

    return datalist

#------------------------------------------------------------------------------------------------------------------------

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

    if print_on_off == 1:
        for line in printlist:
            print(line)
        
    return printlist

#========================================================================================================================


def area_search(sample_txtdata,centerYX,search_area_XY):

    shape = np.shape(sample_txtdata)
    radius = search_area_XY // 2

    count = 0

    for line in range(np.shape(centerYX)[1]):
        set_y,set_x = centerYX[0][line],centerYX[1][line]

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


        search = np.array(sample_txtdata[start_y:finish_y, start_x:finish_x])
        center = np.array([radius + (Ssay), radius + (Ssax)])

        #-----------------------------------------------------------------------

        
        center = np.array([radius + (Ssay), radius + (Ssax)])

        where_search0 = np.where(search == 0)

        sa = np.abs(where_search0 - center.reshape(2, 1))
        sa = sa[0] ** 2 + sa[1] ** 2
        #sa = np.sqrt(sa)
        if np.shape(sa)[0] != 0:
            min = np.min(sa)
            #print(f"MIN: {min}")
            count += min

        else:

            where_sample0 = np.where(sample_txtdata == 0)

            center = np.array((set_y,set_x)).reshape(2, 1)
            sa = np.abs(where_sample0 - center)
            sa = sa[0] ** 2 + sa[1] ** 2
            #sa = np.sqrt(sa)

            if np.shape(sa)[0] != 0:
                min = np.min(sa)
                #print(f"MIN: ？{min}")
                count += min

            else:
                print("は？")


    return count


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

#========================================================================================================================

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
    S_shape = np.array(search_txtdata[1])
    P_shape = np.shape(txtimage)

    P_XYwariai = P_shape[1] / P_shape[0]

    #if abs(P_shape[0]-S_shape[0])/P_shape[0] < abs(P_shape[1]-S_shape[1])/P_shape[1]:
    if P_XYwariai < search_txtdata[0]:
        hiritu = S_shape[0]/P_shape[0]
        set_image = cv2.resize(txtimage,None,fx=hiritu,fy=hiritu)
    
    else:
        hiritu = S_shape[1]/P_shape[1]
        set_image = cv2.resize(txtimage,None,fx=hiritu,fy=hiritu)
    
    set_image = removal_background(set_image,rgb,kyoyoucolor)
    
    P_resize = np.shape(set_image)
    sa = S_shape - P_resize

    s_one = np.ones(S_shape,dtype="i1")
    start_Y = 0+sa[0]//2
    start_X = 0+sa[1]//2
    
    s_one[start_Y:start_Y+P_resize[0],start_X:start_X+P_resize[1]] = set_image
    set_image = s_one

    print(set_image)
    print("set_image; ",np.shape(set_image))
    #set_image = removal_background(cv2.resize(txtimage,dsize=(S_shape[1],S_shape[0])),rgb,kyoyoucolor)
    "|c|"
    "|C|"

    search_data = np.ones(S_shape,dtype='i1')
    search_data[search_txtdata[2]] = np.array(0)
    print(search_data)

    False_position = np.where(set_image != search_data)
    False0_FalsePosition = np.where(search_data[False_position] == 0)
    false0_ImagePosition = (False_position[0][False0_FalsePosition],False_position[1][False0_FalsePosition])

    False1_FalsePosition = np.where(search_data[False_position] == 1)
    false1_ImagePosition = (False_position[0][False1_FalsePosition],False_position[1][False1_FalsePosition])
    #print(f"\nwhere_false0:\n{where_false0}\n")

    return [set_image,false0_ImagePosition],[search_data, false1_ImagePosition]


#------------------------------------------------------------------------------------------------------------------------

import cv2
import matplotlib.pyplot as plt
import numpy as np

import pickle

### pickleで保存したファイルを読み込み
normal = '/Users/matsuurakenshin/WorkSpace/development/sample_txtdata.pickle'
set = "/Users/matsuurakenshin/WorkSpace/development/txtreader/SET_sample_txtdata.pickle"

with open(set, mode='br') as fi:
    S_dataslist,insert_txtdatas,seach_textdatas = pickle.load(fi)

with open('/Users/matsuurakenshin/WorkSpace/development/txtreader/picture_datas.pickle', mode='br') as fi:
    P_dataslist = pickle.load(fi)



def keys_print():
    print(f"\ndataslist_keys:")
    for info_key in P_dataslist:
        print(f">> {info_key}")
    print()

#keys_print()

def TEST_area_search(txtimage,search_txtdata,mode,dataslist):

    Alltxtimages = dataslist["Alltxtimages"]

    import copy

    txtimage_copy = copy.copy(txtimage)
    search_txtdata_copy = copy.copy(search_txtdata)

    if mode == 0:
        txtimage = Alltxtimages[txtimage[0]][txtimage[1]]
    else:
        Alltxtimages = Alltxtimages[0]
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

    #------------------------------------------------------------------------------------------------------------------------

    anser1,anser2 = NEW_search(txtimage,search_txtdata,dataslist)

    M_printlist,P_printlist = "",""

    if np.shape(anser1[1])[1] != 0:
        M_count = area_search(anser1[0],anser1[1],5)
    else:
        M_count = 0

    if np.shape(anser2[1])[1] != 0:
        P_count = area_search(anser2[0],anser2[1],5)
    else:
        P_count = 0

    return [[np.shape(anser1[1])[1],M_count],[np.shape(anser2[1])[1],P_count]]
    
    """
    import pickle

    ### pickleで保存（書き出し
    with open('search_area_anser.pickle', mode='wb') as fo:
        pickle.dump((M_printlist,P_printlist,printlist), fo)

    import pickle

    ### pickleで保存したファイルを読み込み
    with open('/Users/matsuurakenshin/WorkSpace/development/txtreader/search_area_anser.pickle', mode='br') as fi:
        M_printlist,P_printlist,printlist = pickle.load(fi)
    """


import time


linelen = 110

loop = 0

sampledatas = []
mode = 0
modetype = "picture & sample"
modetype0 = "sample  & sample"
example = "indent(Y X)"
example0 = "    txt    "
needdatanum0 = 1
needdatanum = 2

while loop == 0:


    search = list(input(f"\n{'='*linelen}\n\n → 調べたい文字を入力  {example}\n   [ 現サーチタイプ: '{modetype}', 必要要素数: '{needdatanum}', 入力情報: '{example}' ]" + f'\n   [ 他サーチタイプ: "{modetype0}", 必要要素数: "{needdatanum0}", 入力情報: "{example0}" ]\n ▶ 調査終了(END)\n回答: ').split())
    anser0 = search[0]

    if len(anser0) >= 3 and ((anser0[0] == "E" or anser0[0] == "e") and (anser0[1] == "N" or anser0[1] == "n") and (anser0[2] == "D" or anser0[2] == "d" )):
        flag = True
        break

    elif len(search) != needdatanum:
        #mode = int(input(f"\n{'- '*(linelen//2)}\n\n >> サーチタイプの指定 / 0: picture & sample\n    　　　　　　　　　   1: sample  & sample\n回答: "))
        modetype0 = modetype
        example0 = example
        needdatanum0 = needdatanum

        if mode == 0:
            mode = 1
            modetype = "sample  & sample"
            example = "    txt    "
            needdatanum = 1

        else:
            mode = 0
            modetype = "picture & sample"
            example = "indent(Y X)"
            needdatanum = 2


        print(f"\n{'- '*(linelen//2)}\n\nサーチタイプを変更しました。\n[ '{modetype0}' > '{example}' ]")


    if mode == 0:
        position = [int(search[0]),int(search[1])]
    else:
        position = anser0


    print(f"\n{'-'*linelen}")
    search2 = input(f"\n → 比較したい文字を入力、なければ''と入力\n ▶ 調査終了(END)\n回答: ")
    if len(search2) >= 3 and ((search2[0] == "E" or search2[0] == "e") and (search2[1] == "N" or search2[1] == "n") and (search2[2] == "D" or search2[2] == "d" )):
        break

    print(f"\n{'='*linelen}\n")




    if mode == 0:
        dataslist = P_dataslist
    else:
        dataslist = S_dataslist



    start = time.time()  # 現在時刻（処理開始前）を取得

    print(TEST_area_search(position,search2,mode,dataslist))

    end = time.time()  # 現在時刻（処理完了後）を取得

    time_diff = end - start  # 処理完了後の時刻から処理開始前の時刻を減算する
    print(f"\ntime: {time_diff}")  # 処理にかかった時間データを使用


"""
import pickle

with open('sample_datas.pickle', mode='wb') as fo:
    pickle.dump((sampledatas), fo)
"""

print(f"\n{'='*linelen}\n\n終了します。\n")
