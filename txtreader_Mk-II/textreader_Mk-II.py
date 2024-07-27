import cv2
import matplotlib.pyplot as plt
import numpy as np


#-----------------------------------------------------------------------------------------------------------
filename = "/Users/matsuurakenshin/WorkSpace/development/image_file_name.txt"
imageslist = []
import os
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

        print(f"背景色自動検出: {RGB}")
    else:
        print(f"背景色指定: {RGB}")


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
                # Air判定の場合は何も入れない。
                txtimage = [""]
                txtdata = [""]

            txtimages.append(txtimage)
            '''
            #表示内容状strに変換
            a = []
            for dataline in txtdata:
                b = ''
                for data in dataline:
                    b += str(data) + ' '
                a.append(b[:-1])
            txtdatas.append(a)
            '''
            txtdatas.append(txtdata)

        Alltxtimages.append(txtimages)
        Alltxtdatas.append(txtdatas)

        txtimages = []
        txtdatas = []

    dataslist["Alltxtimages"] = Alltxtimages
    dataslist["Alltxtdatas"] = Alltxtdatas
    return dataslist


#-----------------------------------------------------------------------------------------------------------

def print_textdatas(dataslist,writefilename,linestart,linefinish):
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

        Allprintlist = []
        guide_X = "| "
        for linenum in range(len(lineMaxlenx)):
            linelen = (lineMaxlenx[linenum])*2+1
            Air0 = ( (linelen//2) - len(str(linenum)) ) * " "
            Air1 = ( (linelen//2) + (linelen%2) )*" "
            
            guide_X += Air0 + str(linenum) + Air1 +  " | "
            #guide_X += Air0 + str(linenum) + Air1 + " | "
        guide_X = guide_X[:-3]
        Allprintlist.append(guide_X)
        Allprintlist.append("")
        
        #f.write(f"{guide_X[:890]}\n\n")
        
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
            
            printlen = len(printlist[0].replace('\n', ''))

            if line != 0:
                b = printlen
                if a > b:
                    Allprintlist.append("")
                    Allprintlist.append(a*'-')
                    Allprintlist.append("")
                    #f.write(f"\n{a*'-'}\n\n")
                else:
                    Allprintlist.append("")
                    Allprintlist.append(b*'-')
                    Allprintlist.append("")
                    #f.write(f"\n{b*'-'}\n\n")
                a = printlen

            else:
                Allprintlist.append(printlen*'-')
                Allprintlist.append("")
                #f.write(f"{printlen*'-'}\n\n")
                a = printlen
            

            for printline in printlist:
                Allprintlist.append(printline)
                #f.write("| "+printline[:890]+ "\n")

        Allprintlist.append("")
        Allprintlist.append(len(printline)*'-')
        Allprintlist.append("")

        nowline = 3
        linefinish = linefinish - (len(str(len(lineMaxleny)-1)) + 5)

        for line in range (len(Allprintlist)):
            Allprintlist[line] = Allprintlist[line][linestart:linefinish]
        
        Air = len(str(len(lineMaxleny)-1))

        txt1 = Air*" "
        txt2 = Air*"-"
        Allprintlist[0] = "   " + txt1 + Allprintlist[0]
        Allprintlist[1] = "  " + txt1 + " | " + Allprintlist[1]
        Allprintlist[2] = "  " + txt2 + " + " + Allprintlist[2]
        Allprintlist[3] = "  " + txt1 + " | " + Allprintlist[3]
        
        for linenum in range(len(lineMaxleny)-0):
            linelen = lineMaxleny[linenum]

            half = nowline + linelen//2

            for i in range(linelen):
                i += nowline + 1

                if i == half:
                    saAir = Air-len(str(linenum))
                    Allprintlist[i] = " " + ((saAir)*" ") + str(linenum) + " " + " | " + Allprintlist[i]
                else:
                    Allprintlist[i] = "  " + (Air*" ") + " | " + Allprintlist[i]

            Allprintlist[i+1] = "  " + txt1 + " | " + Allprintlist[i+1]
            Allprintlist[i+2] = "  " + txt2 + " + " + Allprintlist[i+2]
            if linenum != len(lineMaxleny)-1:
                Allprintlist[i+3] = "   " + txt1 + guide_X[linestart:linestart+len(Allprintlist[i+5])+1]
            
            nowline += linelen + 3
            #print(nowline)


        for line in Allprintlist:
            f.write(line.replace('\n', '')  + "\n")
        

        #f.write(f"\n{len(printline[:890])*'-'}")


#===========================================================================================================

import pickle

# seach_textdatas
with open('/Users/matsuurakenshin/WorkSpace/development/txtreader/txtreader_Mk-II/Save_retest.pickle', mode='br') as fi:
  seach_textdatas,retest = pickle.load(fi)


#===========================================================================================================


def seach_txt(txtimage,seach_textdatas,kyoyou,dataslist,txt):
    rgb = dataslist["background_color"]
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

    if anserline == "":
        return "</?/>"

    for line in retest[anserline]:

        set_image = removal_background(cv2.resize(txtimage,dsize=(seach_textdatas[line][1][1],seach_textdatas[line][1][0])),rgb,kyoyoucolor)

        syougouritu = np.count_nonzero(set_image[seach_textdatas[line][2]] == 0) / np.shape(seach_textdatas[line][2])[1]

        Pi0 = np.count_nonzero(set_image == 0)
        Sa0 = np.shape(seach_textdatas[line][2])[1]
        Tr = np.count_nonzero(set_image[seach_textdatas[line][2]] == 0)

        #False0num = Pi0 - Tr + Sa0 - Tr
        Tr_xy = Tr / (seach_textdatas[line][1][1] * seach_textdatas[line][1][0])
        Sa_xy = Sa0 / (seach_textdatas[line][1][1] * seach_textdatas[line][1][0])

        sougouritu = Tr_xy + (Tr_xy - Sa_xy)


        if txt != "":
            print(f"{seach_textdatas[line][3]}: Pi0 {Pi0}, Sa0 {Sa0} , Tr {Tr}")
        
        if txt != "None" and seach_textdatas[line][3] == txt:
            print(f"\n ▶️ {txt} :{syougouritu * 100}%\n ▶️ 全体合致率 :{sougouritu}")

        if sougouritu < Max:
            Max = sougouritu
            anserline = line

    return seach_textdatas[anserline][3]


#===========================================================================================================


import pickle

for imagename in imageslist:

    if imageslist[0] == "/Users/matsuurakenshin/WorkSpace/development/txtreader/txtreader_Mk-II/textdata.jpeg":
        dataslist = image_removal_background(imagename,[36,36,36],180)
    else:
        dataslist = image_removal_background(imagename,'auto',100)
        
    dataslist = seach_txtposition(dataslist,'auto')
    dataslist = txtdatas_insert(dataslist)

    #print_textdatas(dataslist,"Alltextimages.text")
    txtimage = dataslist["Alltxtimages"]
    txtdata = dataslist["Alltxtdatas"]
    #plt.imshow(readtxt_imshow(dataslist))
    #plt.imshow(cv2.resize(txtimage[0][0],dsize=(10,30)))
    #print(txtdata[0][1])

    #-----------------------------------------------------------------------------------------------------------


    ### pickleで保存（書き出し
    with open('picture_datas.pickle', mode='wb') as fo:
        pickle.dump(dataslist, fo)
    
    #-----------------------------------------------------------------------------------------------------------
    '''
    linestart = int(input("データ表示の開始位置\n>"))
    linefinish = linestart + int(input(f"データ表示の開始位置: {linestart} から表示する長さ\nfinish = strat + 'anser\n>"))
    print_textdatas(dataslist,"picture_Alltxtdatas.txt",linestart,linefinish)
    '''
#-----------------------------------------------------------------------------------------------------------


#-----------------------------------------------------------------------------------------------------------
"""
line,lennum = 0,4
#txt = textdata[lennum]

txt = ""

print(len(txtimage[line][lennum]))

if len(txtimage[line][lennum]) != 0:
    print(f"文字は ' {seach_txt(txtimage[line][lennum],seach_textdatas,0.15,dataslist,txt)} ' ですか？")
    #print(textdata[num])
    plt.imshow(txtimage[line][lennum])

else:
    print(f"文字は Air判定 です。")
"""
#-----------------------------------------------------------------------------------------------------------
import time
from SET_datas import SET_list

#a = [[[[0,0,0,1,0,0,0],[0,0,0,1,0,0,0]],[],[[0,0,0,1,0,0,0],[0,0,0,1,0,0,0]]],[[[0,0,0,1,0,0,0],[0,0,0,1,0,0,0]]]]

y,x = 0,1
listdata = dataslist["Alltxtdatas"][:2]
#listdata = dataslist["Alltxtimages"][:1]

start = time.time()
set_border_list = SET_list(listdata,guide=True,keep=2)
finish = time.time()
print(f'time: {finish - start}')

with open("Remake_SET.txt","w") as f:
    for line in set_border_list:
        f.write(f"{line}")

print(type([]))