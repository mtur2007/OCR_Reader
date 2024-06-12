
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
        
    #return Allprint_txt
    return SET_txts(Allprint_txt,0,0)



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

#------------------------------------------------------------------------------------------------------------------------

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


        data_copy = np.array(sample_txtdata.copy())
        search = np.array(data_copy[start_y:finish_y, start_x:finish_x])

        #data_copy[start_y:finish_y, start_x:finish_x] = search

        center = np.array([radius + (Ssay), radius + (Ssax)])
        #data_copy[set_y,set_x] = "+"

        sa = np.abs(np.where(search == 0) - center.reshape(2, 1))
        sa = sa[0] ** 2 + sa[1] ** 2
        #sa = np.sqrt(sa)
        if np.shape(sa)[0] != 0:
            min = np.min(sa)
            #print(f"MIN: {min}")
            count += min
        else:
            center = np.array((set_y,set_x)).reshape(2, 1)
            sa = np.abs(np.where(sample_txtdata == 0) - center)
            sa = sa[0] ** 2 + sa[1] ** 2
            #sa = np.sqrt(sa)

            if np.shape(sa)[0] != 0:
                min = np.min(sa)
                #print(f"MIN: ？{min}")
                count += min
            else:
                print("は？")

    print(count)


def print_area_search(sample_txtdata,centerYX,search_area_XY):

    printlist = []

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

        printline = []

        search_copy = np.array(search,dtype=str)
        search_copy[search == 0] = "."
        search_copy[search == 1] = " "
        search_copy[center[0],center[1]] = "+"

        data_copy = np.array(sample_txtdata,dtype=str)
        data_copy[start_y:finish_y, start_x:finish_x] = search_copy

        for line in data_print(data_copy,0):
            printline.append(line)

        
        printline.append("")

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

            where_min = np.where(sa == min)
            where_min = np.array((where_search0[0][where_min],where_search0[1][where_min]))

            search_copy[where_min[0],where_min[1]] = "#"

            for line in data_print(search_copy,0):
                printline.append(line)
            

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

                where_min = np.where(sa == min)
                where_min = np.array((where_sample0[0][where_min],where_sample0[1][where_min]))

                data_copy[data_copy == "0"] = "."
                data_copy[data_copy == "1"] = " "
                data_copy[where_min[0],where_min[1]] = "#"

                for line in data_print(data_copy,0):
                    printline.append(line)

            else:
                print("は？")

        
        printline.append("")
        printline.append(f" > MIN: {np.sqrt(min)}")

        printlist.append(printline)

    return printlist,count


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

    true0_position = np.where(anser_data[search_txtdata[2]] == "0")
    false0_position = np.where(anser_data[search_txtdata[2]] == "1")

    #print(f"\nwhere_false0:\n{where_false0}\n")


    true0_position = (search_txtdata[2][0][true0_position],search_txtdata[2][1][true0_position])
    false0_position = (search_txtdata[2][0][false0_position],search_txtdata[2][1][false0_position])
        
    #print(f"\nfalse0:\n{where_false0}\n")

    anser_data[true0_position] = "."
    anser_data[false0_position] = "\\"
    anser_data[anser_data == "1"] = " "

    rest0_position = np.where(anser_data == "0")
    anser_data[rest0_position] = '+'

    anser_data = data_print(anser_data,0)


    seach_data = np.ones(shape,dtype='i1')
    seach_data[search_txtdata[2]] = np.array(0)

    printlist = []

    printlist.append(f"\n<picture>{((np.shape(set_image)[1])*2 + 1 - 9 + 5)*' '}<search>{((np.shape(set_image)[1])*2 + 1 - 8 + 5)*' '}<anser>\n")
    #print(f"\n<picture>{((np.shape(set_image)[1])*2 + 1 - 9 + 5)*' '}<search>{((np.shape(set_image)[1])*2 + 1 - 8 + 5)*' '}<anser>")

    for i in range(np.shape(set_image)[0]):
        if i+1 == np.shape(set_image)[0] // 2:
            printlist.append(f'{set_image[i]} --- {seach_data[i]} === {anser_data[i]}\n')
            #print(f'{set_image[i]} --- {seach_data[i]} === {anser_data[i]}')
        else:
            printlist.append(f'{set_image[i]}     {seach_data[i]}     {anser_data[i]}\n')
            #print(f'{set_image[i]}     {seach_data[i]}     {anser_data[i]}')

    printlist.append(f"\n{(((np.shape(set_image)[1])*2 + 1 + 5)*' ')*2} ▶ [  \\ :無し ][  + :多い ]\n\n")
    printlist.append(f"{(((np.shape(set_image)[1])*2 + 1 + 5)*' ')*2} > [  . : 文字判定一致 ]\n")
    printlist.append(f"{(((np.shape(set_image)[1])*2 + 1 + 5)*' ')*2} > [ ' ': 背景判定一致 ]\n")
    #print(f"\n{(((np.shape(set_image)[1])*2 + 1 + 5)*' ')*2} ▶ [  \\ :無し ][  + :多い ]\n")
    #print(f"{(((np.shape(set_image)[1])*2 + 1 + 5)*' ')*2} > [  . : 文字判定一致 ]")
    #print(f"{(((np.shape(set_image)[1])*2 + 1 + 5)*' ')*2} > [ ' ': 背景判定一致 ]")

    return [set_image,false0_position],[seach_data,rest0_position],printlist


#------------------------------------------------------------------------------------------------------------------------

#keys_print()
Alltxtimages = dataslist["Alltxtimages"][0]

def TEST_area_search(txtimage,search_txtdata):

    import copy

    txtimage_copy = copy.copy(txtimage)
    search_txtdata_copy = copy.copy(search_txtdata)

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

    anser1,anser2,printlist = NEW_search(txtimage,search_txtdata,dataslist)


    printlist.insert(0,f"\n{txtimage_copy} > 比率調整 ▶ {search_txtdata_copy}\n")

    if np.shape(anser1[1])[1] != 0:
        M_printlist,M_count = print_area_search(anser1[0],anser1[1],5)
    else:
        M_count = 0

    if np.shape(anser2[1])[1] != 0:
        P_printlist,P_count = print_area_search(anser2[0],anser2[1],5)
    else:
        P_count = 0

    #anser_area_search = [M_printlist,P_printlist]

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

    with open("area_search_printfilea.txt","w")as f:
        for line in printlist:
            f.write(line)
        f.write(f"( \\ : - )\n{M_count}\n\n")
        f.write(f"( + )\n{P_count}\n\n\n")

        if M_count != 0: 
            M_printlist = [M_printlist]
            M_printlist = SET_data(M_printlist)

            for line in M_printlist:
                f.write(f"{line}\n")
                #print(line[:4])
        if P_count != 0:
            P_printlist = [P_printlist]
            P_printlist = SET_data(P_printlist)

            for line in P_printlist:
                f.write(F"\n{line}")

linelen = 110

if01 = 0
while if01 == 0:

    search = input(f"\n⬇ {'='*(linelen-2)}\n\n ➡️ 調べたい文字を入力\n ▶️ 調査終了(END)\n回答: ")
    if len(search) >= 3 and ((search[0] == "E" or search[0] == "e") and (search[1] == "N" or search[1] == "n") and (search[2] == "D" or search[2] == "d" )): #片方は自分のタイプミスに対応する為のものです。笑
        break
    print(f"\n{'-'*linelen}")
    search2 = input(f"\n ➡️ 比較したい文字を入力、なければ''と入力\n ▶️ 調査終了(END)\n回答: ")
    if len(search2) >= 3 and ((search2[0] == "E" or search2[0] == "e") and (search2[1] == "N" or search2[1] == "n") and (search2[2] == "D" or search2[2] == "d" )):
        break

    print(f"\n⬆ {'='*(linelen-2)}\n")





    TEST_area_search(search,search2)




            
print(f"\n終了します。\n\n⬆ {'='*(linelen-2)}\n")
