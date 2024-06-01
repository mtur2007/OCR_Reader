import cv2
import matplotlib.pyplot as plt
import numpy as np

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

    dataslist = {}
    dataslist["image"] = image
    dataslist["RGB"] = RGB
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


#-----------------------------------------------------------------------------------------------------------

import copy

def seach_txtposition(dataslist, Airauto):
    code0list = dataslist["code0list"]
    xlen = code0list.shape[1]

    seach = "background"
    txt_sfy = []

    for y in range(int(code0list.shape[0])):

        if np.sum(code0list[y,:]) != xlen:
            if seach == "background":
                seach = "txt"
                txt_sfy.append([y, ""])

        else:
            if seach == "txt":
                seach = "background"
                txt_sfy[-1][1] = y-1

    seach = "background"
    linetxts_sfyx = []
    Airlist = []
    Airnum,Aircount,txtlen = 0,0,0
    #Aircount,deviation = 1,0

    for line in range(len(txt_sfy)):
        txt_sfyx = []

        for x in range(int(code0list.shape[1])):

            if np.sum(code0list[txt_sfy[line][0]:txt_sfy[line][1],x]) != txt_sfy[line][1]-txt_sfy[line][0]:
                if seach == "background":
                    seach = "txt"
                    txt_sfyx.append( [x , ""] )

            else:
                if seach == "txt":
                    seach = "background"
                    txt_sfyx[-1][1] = x-1

                    if Airauto == "auto":
                        if len(txt_sfyx) >= 2:
                            if abs(Airnum - (txt_sfyx[-1][0] - txt_sfyx[-2][1])) <= 1:
                                if Aircount >= 3:
                                    Airlist.append(txtlen)
                                Aircount += 1
                            else:
                                Airnum = txt_sfyx[-1][0] - txt_sfyx[-2][1]
                                txtlen = txt_sfyx[-1][1] - txt_sfyx[-2][1]
                                Aircount,deviation = 1,0


        linetxts_sfyx.append([txt_sfy[line],txt_sfyx])

    Airlinetxts_sfyx = copy.deepcopy(linetxts_sfyx)

    if Airauto == "auto":
        Airlen = int(sum(Airlist)/len(Airlist))
        print(Airlist,Airlen)
    else:
        Airlen = Airauto

    for line in range(len(linetxts_sfyx)):
        count = 0
        for txtline in range(len(linetxts_sfyx[line][1])-1):
            if linetxts_sfyx[line][1][txtline+1][0] - linetxts_sfyx[line][1][txtline][1] > Airlen:

                Airlinetxts_sfyx[line][1].insert(txtline + count + 1,"Air")
                count += 1

    dataslist["linetxts_sfyx"] = Airlinetxts_sfyx
    return dataslist


#-----------------------------------------------------------------------------------------------------------

def readtxt_imshow(dataslist):
    color_image = np.array(dataslist['image'])
    linetxts_sfyx = dataslist["linetxts_sfyx"]

    for line in linetxts_sfyx:
        a = line[0][0]
        b = line[0][1]
        color_image[a,:] = np.array([0,150,150])
        color_image[b,:] = np.array([0,150,150])
        for txt in range(len(line[1])):
            if line[1][txt] != "Air":
                color_image[a:b,line[1][txt][1]] = np.array([0,150,0])
                color_image[a:b,line[1][txt][0]] = np.array([0,150,0])
            else:
                color_image[a:b,line[1][txt-1][1]+5] = np.array([255,0,0])
                color_image[a:b,line[1][txt+1][0]-5] = np.array([255,0,0])

    return color_image


#-----------------------------------------------------------------------------------------------------------

def txtdatas_insert(dataslist):
    color_image = np.array(dataslist["image"])
    code0list = dataslist["code0list"]

    #plt.imshow(color_image[:100,:100])
    linetxts_sfyx = dataslist["linetxts_sfyx"]
    Alltxtimages,txtimages = [],[]
    Alltxtdatas,txtdatas = [],[]


    for line in range(len(linetxts_sfyx)):
        placey = linetxts_sfyx[line][0]
        for txt in range(len(linetxts_sfyx[line][1])):
            if linetxts_sfyx[line][1][txt] != "Air":

                placex = linetxts_sfyx[line][1][txt]
                leny = placey[1] - placey[0]
                lenx = placex[1] - placex[0]

                txtimage = color_image[placey[0]:placey[1],placex[0]:placex[1]]
                txtdata = code0list[placey[0]:placey[1],placex[0]:placex[1]]

                for top in range(leny):
                    if np.sum(txtdata[top,:]) != lenx:
                        txtimage = txtimage[top:,:]
                        txtdata = txtdata[top:,:]
                        break

                resizeleny = np.shape(txtdata)[0]

                for lower in range(resizeleny):
                    if np.sum(txtdata[resizeleny-lower -1 ,:]) != lenx:
                        txtimage = txtimage[:resizeleny-lower,:]
                        txtdata = txtdata[:resizeleny-lower,:]
                        break

            else:
                txtimage = ""
                txtdata = ""

            txtimages.append(txtimage)
            txtdatas.append(txtdata)

        Alltxtimages.append(txtimages)
        Alltxtdatas.append(txtdatas)

        txtimages = []
        txtdatas = []

    dataslist["Alltxtimages"] = Alltxtimages
    dataslist["Alltxtdatas"] = Alltxtdatas
    return dataslist


#-----------------------------------------------------------------------------------------------------------

def print_textdatas(dataslist,writefilename):
    txtdatas = dataslist["Alltxtdatas"]
    lineMaxlenx,lineMaxleny = [],[]

#    with open(writefilename,"w") as f:

    Maxlenx = 0
    for line in range(len(txtdatas)):
        lineMaxleny.append(0)
        if len(txtdatas[line]) > Maxlenx:
            Maxlenx = len(txtdatas[line])
        txtline = txtdatas[line]
        for txt in range(len(txtline)):
            if len(txtline[txt]) != 0:
                if np.shape(txtline[txt])[0] > lineMaxleny[line]:
                    lineMaxleny[line] = np.shape(txtline[txt])[0]


    for nouse in range(Maxlenx):
        lineMaxlenx.append(0)

    for line in range(len(txtdatas)):
        txtline = txtdatas[line]
        for txt in range(len(txtline)):
            if len(txtline[txt]) != 0:
                if np.shape(txtline[txt])[1] > lineMaxlenx[txt]:
                    lineMaxlenx[txt] = np.shape(txtline[txt])[1]


    with open(writefilename,"w") as f:
        for line in range(len(txtdatas)):
            printlist = []
            txtline = txtdatas[line]
            thislineMaxY = lineMaxleny[line]

            for nouse in range(thislineMaxY):
                printlist.append("")

            for txt in range(len(txtline)):
                thislineMaxX = lineMaxlenx[txt]

                Textlen = thislineMaxX *2 +1

                if len(txtline[txt]) != 0:
                    ylen,xlen = np.shape(txtline[txt])
                    Airy = thislineMaxY - ylen
                    Airx = (thislineMaxX - xlen)*2

                    y = 0

                    for nouse in range(Airy//2 + Airy%2):
                        printlist[y] = (f"{printlist[y]}{Textlen * ' '} | ")
                        y += 1

                    for txty in txtline[txt]:
                        printlist[y] = (f"{printlist[y]}{(Airx//2 + Airx%2)*' '}{txty}{(Airx//2)*' '} | ")
                        y += 1
                    for nouse in range(Airy//2):
                        printlist[y] = (f"{printlist[y]}{Textlen * ' '} | ")
                        y += 1


                else:
                    y = 0
                    for nouse in range(thislineMaxY):
                        printlist[y] = (f"{printlist[y]}{Textlen * ' '} | ")
                        y += 1

            printlen = len(printlist[0][:894])

            if line != 0:
                b = printlen
                if a > b:
                    f.write(f"\n{a*'-'}\n\n")
                else:
                    f.write(f"\n{b*'-'}\n\n")
                a = printlen

            else:
                f.write(f"{printlen*'-'}\n\n")
                a = printlen
            

            for printline in printlist:
                f.write("| "+printline[:894]+ "\n")

        f.write(f"\n{len(printline[:894])*'-'}")


#===========================================================================================================


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


#===========================================================================================================


seach_textdatas = []
set_txttype = ""
set_wariai = ""
seach_shape = [0,0]
set_txtdata = []
textdata = ""
seach_num = 0

with open("/Users/matsuurakenshin/WorkSpace/development/txtreader/txtreader_Mk-II/Seave_Txtdatas.txt","r") as f:
    for line in f:
        line = line.strip()
        if len(line) == 5 and line[-2:] == " ]":
            #print(line)
            set_txtdata = np.array(set_txtdata).reshape(seach_shape)
            seach_textdatas.append([set_wariai,seach_shape,np.where(set_txtdata==0),set_txttype])
            textdata = textdata + set_txttype
            set_txtdata = []
            set_txttype = line[2]
            seach_num = 1
        elif seach_num == 1:
            set_wariai = float(line)
            seach_num = 2
        elif seach_num == 2:
            for txt in range(len(line)):
                if line[txt] == ",":
                    seach_shape = [int(line[1:txt]),int(line[txt+2:-1])]
            seach_num = 3
        elif seach_num == 3:
            for txt in range(len(line)):
                if line[txt] == "0" or line[txt] == "1":
                    set_txtdata.append(int(line[txt]))

    set_txtdata = np.array(set_txtdata).reshape(seach_shape)
    seach_textdatas.append([set_wariai,np.shape(set_txtdata),np.where(set_txtdata==0),set_txttype])
    textdata = textdata + set_txttype

seach_textdatas = seach_textdatas[1:]

'''
testdata        が 文字
seach_textdatas が 文字コード
'''

#識字用のコード配列が合っているかの確認

for i in range(len(seach_textdatas)):
    if seach_textdatas[i][3] != textdata[i]:
        print(i)



#---------------------------------------------------------------------------------------------------------------

#類似・重なる字の調査用プログラム

def test_seach_txt(txtimage,seach_textdatas,kyoyou,dataslist,txt):
    #for txt in seach_textdatas[3]:
    resembletxt = []
    rgb = dataslist["RGB"]
    kyoyoucolor = dataslist["kyoyou"]
    hiritu = np.shape(txtimage)[1]/np.shape(txtimage)[0]
    for line in range(len(seach_textdatas)):

        if abs(seach_textdatas[line][0] - hiritu) < kyoyou:
            set_image = removal_background(cv2.resize(txtimage,dsize=(seach_textdatas[line][1][1],seach_textdatas[line][1][0])),rgb,kyoyoucolor)
            #print(set_image)
            syougouritu = np.count_nonzero(set_image[seach_textdatas[line][2]] == 0) / np.shape(seach_textdatas[line][2])[1]

            if txt != "None" and seach_textdatas[line][3] == txt:
                #print(set_image)

                print(f"\n ▶️ {txt} :{str(syougouritu * 100)}%\n")

            if syougouritu > 0.85:

                resembletxt.append(line)
                #resembletxt.append(seach_textdatas[line][3])
                
    return resembletxt


#===========================================================================================================

def Saerch_retest():
    seach_txtimage = txtimage[0]

    txtimages = []
    line = 0

    with open("testanser_printfile.txt", "w")as f:

        
        a = 0
        Truecount = 0
        Falsecount = 0

        retest = [[[]],[]]
        num = []
        txtnum = []


        for txt in range(len(seach_textdatas)):
            num.append(txt)
            txtnum.append([])
        
        retest[0][0] = num
        retest[1] = txtnum

        for txtnum in range(len(seach_txtimage)):
            anser = test_seach_txt(seach_txtimage[txtnum],seach_textdatas,0.15,dataslist,"None")
            
            for txt in anser:
                retest[1][txt].append(txtnum)

                if txtnum == txt:
                    count = 1


        txts = []
        count = 0

        for line in range(len(retest[1])):
            txtlist = []
            Err = 1
            for txt in retest[1][line]:
                txtlist.append(seach_textdatas[txt][3])
                if line == txt:
                    Err = 0
            
            if Err == 1:
                print(f"\n無: {seach_textdatas[line][3]}\ntxtnum: {line}\n")
                count += 1

            txts.append(txtlist)

        if Err != 0:
            print(f"正しく識字されていない文字があります。")
    
        
        retest[0] = SET_numbertxt(retest[0],1)
        retest_copy = SET_numbertxt(retest[1],0)

        numdata = ""
        txtdata = ""

        for num in range(len(retest[0][0])):
            printlist = []
            for txt in retest_copy[num]:
                printlist.append(txt)
                
            if len(printlist) >= 2:
                numdata = numdata + f"{retest[0][0][num]}: {printlist}\n"
                txtdata = txtdata + f"{seach_textdatas[num][3]}: {txts[num]}\n"

        f.write(f"\n\n登録字数 : {len(seach_textdatas)}\n登録情報 : {textdata}\n検証を開始...\n\nErr ({count})\n\n")

        f.write(txtdata)
        f.write(f"\n\nNumber.Ver (機械用データ)\n\n{numdata}")

    return retest


"""
            if len(anser) >= 2:
                f.write(f"▶️{textdata[i]}:{anser}\n")

            if textdata[i] != anser:
                Falsecount += 1
                print (f"▶️結果が違う {textdata[i]} → {anser}")
            else:
                Truecount += 1
"""

    #print(f"\n検証結果[合致数{Truecount}, 誤検知数{Falsecount}]\n")


#===========================================================================================================


def seach_txt(txtimage,seach_textdatas,kyoyou,dataslist,txt):
    rgb = dataslist["RGB"]
    kyoyoucolor = dataslist["kyoyou"]
    hiritu = np.shape(txtimage)[1]/np.shape(txtimage)[0]        
    Max = 0
    anserline = ""
    for line in range(len(seach_textdatas)):

        if abs(seach_textdatas[line][0] - hiritu) < kyoyou:
            set_image = removal_background(cv2.resize(txtimage,dsize=(seach_textdatas[line][1][1],seach_textdatas[line][1][0])),rgb,kyoyoucolor)
            #print(set_image)
            syougouritu = np.count_nonzero(set_image[seach_textdatas[line][2]] == 0) / np.shape(seach_textdatas[line][2])[1]
            
            if syougouritu > Max:
                if syougouritu > 0.9:
                    anserline = line
                    break
                Max = syougouritu
                anserline = line


    #print(f'▶️▶️ {anserline} :{str(Max * 100)}%')
    Max = 0
    Min = 1

    if anserline == "":
        return "</?/>"

    for line in retest[1][anserline]:

        set_image = removal_background(cv2.resize(txtimage,dsize=(seach_textdatas[line][1][1],seach_textdatas[line][1][0])),rgb,kyoyoucolor)

        syougouritu = np.count_nonzero(set_image[seach_textdatas[line][2]] == 0) / np.shape(seach_textdatas[line][2])[1]

        Pi0 = np.count_nonzero(set_image == 0)
        Sa0 = np.shape(seach_textdatas[line][2])[1]
        Tr = np.count_nonzero(set_image[seach_textdatas[line][2]] == 0)

        #False0num = Pi0 - Tr + Sa0 - Tr
        Tr_xy = Tr / (seach_textdatas[line][1][1] * seach_textdatas[line][1][0])
        Sa_xy = Sa0 / (seach_textdatas[line][1][1] * seach_textdatas[line][1][0])

        #sougouritu = Tr_xy + (Tr_xy - Sa_xy)
        #sougouritu = Tr_xy / Sa_xy
        sougouritu = Tr / Sa0
        #a = (Sa_xy + Tr_xy) / 2
        #sougouritu = Tr_xy / Sa_xy # 合致割合にすると全体割合が無視されてしまう為全体の割合で計算する。

        #sougouritu = False0num / a

        if txt != "None" and seach_textdatas[line][3] == txt:

            #サンプル
            #print(f" ▶️ 称号割合 :{a * 100}%")
            if txt == "'":
                print(f' ▶️ ["{seach_textdatas[line][3]}"] 重複率: {syougouritu}%')
            else:
                print(f" ▶️ ['{seach_textdatas[line][3]}'] 重複率: {syougouritu}%")

            print(f" > 比較要素数 :{Sa0}")
            print(f" > 合致数     :{Tr}")
            print(f" >> 合致率  :{(sougouritu) * 100}%")
            #print(f" ▶️ 不合致割合 :{a * 100}%")

            seach_data = np.ones(np.shape(set_image),dtype='i1')
            seach_data[seach_textdatas[line][2]] = np.array(0)

            print(f"\n<picture>{((np.shape(set_image)[1])*2 + 1 - 9 + 5)*' '}<search>")

            for i in range(np.shape(set_image)[0]):
                if i+1 == np.shape(set_image)[0] // 2:
                    print(f'{set_image[i]} =?= {seach_data[i]}')
                else:
                    print(f'{set_image[i]}     {seach_data[i]}')

            print()
        
        if sougouritu > Max:
            Max = sougouritu
            anserline = line
        """
        if sougouritu < Min:
            Min = sougouritu
            anserline = line
        """




    return seach_textdatas[anserline][3]


#===========================================================================================================


dataimage = "/Users/matsuurakenshin/WorkSpace/development/txtreader/txtreader_Mk-II/textdata.jpeg"

dataslist = image_removal_background(dataimage,[31,31,31],180)

image = dataslist['image']
imageshape = np.shape(image)
a = image.reshape(imageshape[0] * imageshape[1],3)

#-----------------------------------------------------------------------------------------------------------

#print(a)

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
print(u[posishon])

#-----------------------------------------------------------------------------------------------------------
    
dataslist = seach_txtposition(dataslist,100)
dataslist = txtdatas_insert(dataslist)

print_textdatas(dataslist,"Alltextimages.text")
txtimage = dataslist["Alltxtimages"]
txtdata = dataslist["Alltxtdatas"]
#plt.imshow(readtxt_imshow(dataslist))
#plt.imshow(cv2.resize(txtimage[0][0],dsize=(10,30)))
print(len(txtdata[0][72][0]))
print_textdatas(dataslist,"Serach_textdataslist_printfile.txt")

#-----------------------------------------------------------------------------------------------------------


retest = Saerch_retest()

import pickle

### pickleで保存（書き出し）
with open('Save_retest.pickle', mode='wb') as fo:
  pickle.dump((seach_textdatas,retest[1]), fo)



line,lennum = 0,92
Falselist = []
#txt = textdata[lennum]
txt = ""

true = 0
false = 0

for lennum in range(len(textdata)):
    if len(txtimage[line][lennum]) != 0:
        fainalanser = seach_txt(txtimage[line][lennum],seach_textdatas,0.15,dataslist,txt)
        if fainalanser != textdata[lennum]:
            Falselist.append(f"▶️結果が違う {textdata[lennum]} → {fainalanser}")
            false += 1
        else:
            true += 1

        #print(f"文字は ' {seach_txt(txtimage[line][lennum],seach_textdatas,0.15,dataslist,txt)} ' ですか？")
        #print(textdata[num])
        #plt.imshow(txtimage[line][lennum])

print(f"\n登録字数 : {len(seach_textdatas)}\n登録情報 : {textdata}\n検証を開始...\n\nErr ({len(Falselist)})\n")

if false == 0:
    print("--------")
for line in Falselist:
    print(line)

print()
print(f"検証結果[合致数{true}, 誤検知{false}]\n")


#===========================================================================================================


def get_anser(anser):
    anserreturn = anser

    for a in range(len(anser)):
        if anser[a] == "=":
            start = a+1
            for b in range(len[anser]- (start+1)):
                if anser[b] != " ":
                    start = b+1
                    for c in range(len[anser]- (start+1)):
                        if anser[c] != " ":
                            anserreturn = anserreturn + anser[c]                                
            else:
                return anserreturn
    else:
        return anserreturn

linelen = 100

if01 = 0
while if01 == 0:

    search = input(f"\n{'='*linelen}⬇️\n\n ➡️ 調べたい文字を入力\n ➡️ 行数を指定する場合は(lennum = 行数)\n ▶️ 調査終了(END)\n回答: ")
    if (search[0] == "E" or search[0] == "e") and (search[1] == "N" or search[1] == "n") and (search[2] == "D" or search[2] == "d" ): #片方は自分のタイプミスに対応する為のものです。笑
        break
    print(f"\n{'-'*linelen}")
    search2 = input(f"\n ➡️ 比較したい文字を入力、なければ''と入力\n ▶️ 調査終了(END)\n回答: ")
    if (search2[0] == "E" or search2[0] == "e") and (search2[1] == "N" or search2[1] == "n") and (search2[2] == "D" or search2[2] == "d" ):
        break
    print(f"\n{'='*linelen}⬆️\n")

    search = get_anser(search)


    if search[:7] == "lennum":
        lennum = search

    line = 0

    if search2 != "":
        for searchline in range(len(seach_textdatas)):
            if seach_textdatas[searchline][3] == search2:
                txt = seach_textdatas[searchline][3]
                break
        else:
            print("比較対象が登録されていない為、比較をOFFにします。")
            search2 = ""

    
    if search != "":
        for searchline in range(len(seach_textdatas)):
            if seach_textdatas[searchline][3] == search:
                lennum = searchline

                if len(txtimage[line][lennum]) != 0:
                    print(f"文字は ' {seach_txt(txtimage[line][lennum],seach_textdatas,0.15,dataslist,txt)} ' ですか？")
                    #print(textdata[num])
                    #plt.imshow(txtimage[line][lennum])

                else:
                    print(f"文字は Air判定 です。")
                
                break

        else:
            print("調査対象が登録されていない為、調査をパスします。")
            search2 = ""

print(f"\n終了します。\n\n{'='*linelen}⬆️\n")