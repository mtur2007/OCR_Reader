import cv2
import matplotlib.pyplot as plt
import numpy as np

import pickle

# seach_textdatas
with open('/Users/matsuurakenshin/WorkSpace/development/txtreader/txtreader_Mk-II/Save_retest.pickle', mode='br') as fi:
    seach_textdatas,retest = pickle.load(fi)

search_line = []
wariai = []

for linenum in range(len(seach_textdatas)):

    line = seach_textdatas[linenum]

    Sa_xy = line[1][0] * line[1][1]

    wariai.append((len(line[2][0]) / Sa_xy) * 100)

NEW_retest = []
for retestline in retest:
    insertlist = []
    insertwariai = []
    for num in range(len(retestline)):
        slices_numdata = retestline[num]
        for listline in range(len(insertlist)):
            if wariai[slices_numdata] > insertwariai[listline]:
                insertlist.insert(listline,retestline[num])
                insertwariai.insert(listline,wariai[slices_numdata])
                break
        else:
            insertlist.append(retestline[num])
            insertwariai.append(wariai[slices_numdata])

    NEW_retest.append(insertlist)


retest = NEW_retest



import copy

def Myint(num): #数値の int部分を確実に表示させる様にする自作関数
    for line in range(len(str(num))):
        if str(num)[line] == ".":
            return int(str(num)[:line])
    return num


#数値の整列を行う関数

def SET_numbertxt(numberslist,mode):
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

        search_list = np.array(SET_numbertxt(search_list,1))
        Line_list = []

        for num in range(np.shape(search_list)[1]):
            Line_list.append(search_list[:,num])

        returndata = []
        for line in range (np.shape(Line_list)[0]):
            cut = len_list[line]
            returndata.append(Line_list[line][:cut])

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

#-----------------------------------------------------------------------------------------------------------

retest_copy = copy.deepcopy(retest)
retest_copy = SET_numbertxt(retest_copy,0)

txtsample = ""
linelist = [[]]
for i in range(len(retest)):
    txtsample = txtsample + seach_textdatas[i][3]
    linelist[0].append(i)
linelist = SET_numbertxt(linelist,1)[0]


numdata = ""
txtdata = ""

for num in range(len(retest)):
    printlist_num = []
    printlist_txt = []

    for txt in retest_copy[num]:
        printlist_num.append(txt)
    
    for txt in retest[num]:
        printlist_txt.append(seach_textdatas[txt][3])

    if len(retest[num]) >= 2:
        numdata = numdata + f"{linelist[num]}: {printlist_num}\n"
        txtdata = txtdata + f"{seach_textdatas[num][3]}: {printlist_txt}\n"

with open ("remake_retest.txt", "w") as f:
    f.write(f"\n\n登録字数 : {len(seach_textdatas)}\n登録情報 : {txtsample}\n検証を開始...\n\n")

    f.write(txtdata)
    f.write(f"\n\nNumber.Ver (機械用データ)\n\n{numdata}")
