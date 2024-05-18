from PIL import Image
import matplotlib.pyplot as plt
import numpy as np


#-----------------------------------------------------------------------------------------------------------

filename = "/Users/matsuurakenshin/WorkSpace/development/txtreader/txtreader_Mk-II/image_file_name.txt"
imageslist = []
import os
if os.path.exists(filename) == False:
    with open("image_file_name.txt","w") as f:
        f.write("image_file_name")

imagenamefile = "/Users/matsuurakenshin/WorkSpace/development/txtreader/txtreader_Mk-II/image_file_name.txt"
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
    image = Image.open(imagename)
    color_image = np.array(image)
    background_color = np.array(RGB)
    print(background_color)

    code0list = removal_background(color_image,RGB,kyoyou)


    with open("coode0list_printfile.txt","w") as f:
        for y in range(code0list.shape[0]):
            txt = ""
            for x in range(code0list.shape[1]):
                txt = txt + str(code0list[y,x])
            f.write(txt + "\n")
        else:
            print(code0list.shape)

    dataslist = {}
    dataslist["image"] = image
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

        
        

#-----------------------------------------------------------------------------------------------------------

for imagename in imageslist:

    dataslist = image_removal_background(imagename,[36,36,36],80)
    dataslist = seach_txtposition(dataslist,"auto")
    dataslist = txtdatas_insert(dataslist)
    
    """
    txtimage = dataslist["Alltxtimages"]
    txtidata = dataslist["Alltxtdatas"]
    #plt.imshow(readtxt_imshow(dataslist))
    plt.imshow(np.array(txtimage[0][0]))
    print(txtidata[0][0])
    print_textdatas(dataslist,"textdataslist_printfile.txt")
    """
    