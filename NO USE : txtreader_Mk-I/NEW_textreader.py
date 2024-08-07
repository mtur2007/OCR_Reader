#  inpirt / PIL, matplorlib, numpy

from PIL import Image
import matplotlib.pyplot as plt
import numpy as np


'''
-----------------------------------------------------------------------------------------------------------------
写真加工関数⬇️
'''

# function / 'set_image'
# (イメージ更新プログラム)

def set_image(image,wariai):

    image = Image.open(image)
    color_image = np.array(image)

    image = image.resize((int(color_image.shape[1]*wariai), int(color_image.shape[0]*wariai)))
    color_image = np.array(image)

    return color_image



# function / 'removal_background'
# 背景くり抜きプログラム

def zettai(num): #絶対値
    if num >= 0:
        return num
    if num < 0:
        return num * -1

def removal_background(color_image,RGB,kyoyou):
    Red, Green, Blue = RGB[0], RGB[1], RGB[2] #背景の色

    code1list = np.ones((color_image.shape[0], color_image.shape[1]), dtype='i1') #一旦0で埋める
    #code1list = np.array([],dtype="i1")


    for y in range(color_image.shape[0]):
        for x in range(color_image.shape[1]):
            if zettai(Red - color_image[y, x][0]) + zettai(Green - color_image[y, x][1]) + zettai(Blue - color_image[y, x][2]) > kyoyou:
                code1list[y,x] = np.array(0)

            #if zettai(Red - color_image[y, x][0]) > kyoyou:
            #    if zettai(Green - color_image[y, x][1]) > kyoyou:
            #        if zettai(Blue - color_image[y, x][2]) > kyoyou:
            #            code1list.itemset((y,x),0)
                #code1list[y,x] = np.array(0)
                #code1list = np.append(code1list,1) #背景色と類似(許容(kyoyou)範囲内)なら1で書き換え、そうでなければ0のまま
            #else:
            #    code1list = np.append(code1list,0)

    #code1list.reshape(color_image.shape[0],color_image.shape[1])

    with open("test.txt","w") as f:
        for y in range(code1list.shape[0]):
            txt = ""
            for x in range(code1list.shape[1]):
                txt = txt + str(code1list[y,x])
            f.write(txt + "\n")
        else:
            print(code1list.shape)

    print("gogo")

    return code1list




# function / 'CUT'
# ブロック可視化プログラム


def sisyagonyu(num):
    if num - int(num) <= 0.5:
        return int(num - (num - int(num)))
    else:
        return int(num) + 1

def CUT(color_image,code0list,txtx,txty,width,hight,sahight):

    linelen = int((color_image.shape[0] - txty + sahight) // (hight + sahight))
    txtlen = int((color_image.shape[1] - txtx) // width)
    print(f"行数{linelen}, 文字数{txtlen}")

    with open("NEW_test_txtcode.txt","w") as f:
        for line in range(linelen): #行数

            for liney in range(hight):  #高さ

                txt = ""
                x = txtx

                for nouse in range(txtlen):  #文字数
                    for txtline in code0list[(liney+txty) + sisyagonyu(line*(hight+sahight)) ,sisyagonyu(x):sisyagonyu(x+width)]:
                        txt = txt + str(txtline)

                    txt = txt + "   "
                    x += width

                f.write(txt + "\n")

            f.write("\n")



# function / 'get_interval'
# 文字間隔の取得

def seach_txt(code0list,wariai,direction):
    seach = "background"
    txt_sfx_sy = []

    for x in range(int(code0list.shape[1])):
        if direction == 'Reversal':
            x = code0list.shape[1] - x -1

        for y in range(int(code0list.shape[0]*wariai)):
            if direction == 'Reversal':
                y = code0list.shape[0] - y -1

            if code0list[y, x] == 0:

                if seach == "background":
                    seach = "txt"
                    txt_sfx_sy.append([y, x, ""])

                break

        else:
            if seach == "txt":
                seach = "background"
                txt_sfx_sy[-1][2] = x-1

                if direction != "penetration":
                    return txt_sfx_sy[0]

    else: #"penetrationのみ"
        return txt_sfx_sy



def get_interval(code0list,wariai):

    block = (seach_txt(code0list, wariai, "penetration"))
    interval = []
    minimum_interval = 1000 #1000は仮置き
    for line in range(len(block)-1):
        Beforeblock = block[line][1]# + (block[line][2]-block[line][1])/2
        Afterblock = block[line+1][1]# + (block[line+1][2]-block[line+1][1])/2

        if minimum_interval > Afterblock - Beforeblock:
            minimum_interval = Afterblock - Beforeblock

        interval.append(Afterblock - Beforeblock)

    print(f"文字別間隔数:{interval}")
    print(f"最小間隔:{minimum_interval}")

    txtlen = 0
    word_count = 1
    for line in interval:
        word_count += line // minimum_interval
        txtlen += line

    print(f"総間隔{txtlen}, 総字数{word_count}")
    return (txtlen+16)/word_count

    #print(f"枠 : 縦[ {hight} + (描画範囲外:{sahight}) ]  *  幅[{width}]\nブロックの大きさ(1)に対し写真側は({width/(count/txtlen)} ※これはあくまでも目安です。)")



# function / 'insertlist'

def insertlist(color_image,code0list,txtx,txty,width,hight,sahight):

    linelen = int((color_image.shape[0] - txty + sahight) // (hight + sahight))
    txtlen = int((color_image.shape[1] - txtx) // width)
    print(f"行数{linelen}, 文字数{txtlen}")


    Max = 0 #最大データ量調べ
    x = txtx
    for nouse in range(txtlen):
        if Max < (sisyagonyu(x + width) - sisyagonyu(x)):
            Max = (sisyagonyu(x + width) - sisyagonyu(x))
        x += width

    txtcode = np.array([], dtype='i1')

    with open("txtcode.txt", "w") as f:

        for line in range(linelen): #行数
            x = txtx
            for nouse in range(txtlen):  #文字数

                for liney in range(hight):  #高さ

                    txtdata = (code0list[(liney+txty) + sisyagonyu(line*(hight+sahight)) ,sisyagonyu(x):sisyagonyu(x+width)])

                    if zettai(20 - len(txtdata)) != 0:
                        for nouse in range(zettai(20 - len(txtdata))):
                            txtdata = np.insert(txtdata,0,np.array(1))

                    txtcode = np.append(txtcode, txtdata)

                x += width

        txtcode = txtcode.reshape(linelen ,txtlen, hight, Max)


        for line in range(txtcode.shape[0]):
            for txtline in range(txtcode.shape[1]):
                for txthight in range(txtcode.shape[2]):
                    f.write(f"{(txtcode[line][txtline][txthight])}\n")
                f.write("\n")


    return txtcode,linelen,txtlen,hight,Max


def seach (txtcode,Unicode):
    Max = 0
    for serch in range(len(Unicode)):
        Truecount = np.count_nonzero(txtcode == Unicode[serch])
        if Truecount > Max:
            Max = Truecount
            point = serch
            if Max > 650:
                return point
    
    else:
        return point


#調整が終わったら起動していくプログラム
def seach_strat(color_image,code0list,txtx,txty,width,hight,sahight):
    txtcode,linelen,txtlen,hight,Max = insertlist(color_image,code0list,txtx,txty,width,hight,sahight)
    #print(f"\ntxtcode.shape{txtcode.shape}\n{txtcode}\n----------------------------")


    txt = ""
    for i in range(linelen):
        txt = ""
        for a in range(txtlen):
            textnum = seach(txtcode[i,a],Unicode)
            txt = txt + guide[textnum]

        print(txt)

    return txtcode

'''
-----------------------------------------------------------------------------------------------------------------
識字元の定義関数⬇️
'''


# function / txtcode_selection / [解読用リストの作成 兼 復旧用プログラム] / (保存ファイル名) / return 指標リスト, 文字コード, サンプルリスト

def txtcode_selection(filename):
    seach_code_test = np.array([],dtype='i8')
    seach_type_test = []
    onetxt = np.array([0])
    seach = "None"
    txttype, sample_txtdata = "",[]
    Nonetype = []

    with open(filename,"r") as f:
        for line in f:
            line = line.strip()

            if len(line) == 3:
                if seach == "txtdata":
                    seach_code_test = np.append(seach_code_test,onetxt)
                    for i in range(4):
                        seach_type_test.append(txttype)
                    sample_txtdata.append([txt,onetxt.reshape(36,20)])
                txttype = line[1]

                txt = line[1]
                onetxt = np.array([],dtype='i8')

            elif line == "None":
                seach = "None"
                sample_txtdata.append([txt,"none"])
                Nonetype.append(txttype)

            elif line != "":
                seach = "txtdata"
                for txtline in line:
                    if txtline == "0":
                        onetxt = np.append(onetxt,0)

                    elif txtline == "1":
                        onetxt = np.append(onetxt,1)

    linelen = seach_code_test.shape[0]/(36*20)
    seach_code_test = seach_code_test.reshape(int(linelen),36,20)

    print(Nonetype)
    for i in range(int((len(seach_type_test))/4)):

        " ↑ → "
        copy = seach_code_test[i*4].copy()
        copy[:,1:] = copy[:,:-1]
        copy[:,0] = np.array(1)
        seach_code_test = np.insert(seach_code_test,i*4+1,copy,axis=0)

        " ↓ ← "
        copy = seach_code_test[i*4].copy()
        copy[1:,:] = copy[:-1,:]
        copy[0,:] = np.array(1)
        seach_code_test = np.insert(seach_code_test,i*4+2,copy,axis=0)

        " ↓ → "
        copy = seach_code_test[i*4].copy()
        copy[1:,1:] = copy[:-1,:-1]
        copy[0,:] = np.array(1)
        copy[:,0] = np.array(1)
        seach_code_test = np.insert(seach_code_test,i*4+3,copy,axis=0)


    return seach_type_test, seach_code_test, sample_txtdata

#　function / save_txtcode_data　/ [解読用テキストデータの保存] / (保存ファイル名) / return "セーブ完了"

def save_txtcode_data(sample_txtdata,filename):

    with open(filename,"w") as f:
        for line in range(len(sample_txtdata)):
            f.write(f"'{sample_txtdata[line][0]}'\n")

            if len(sample_txtdata[line][1]) == 36:

                for y in range(len(sample_txtdata[line][1])):

                    txt = "[ "
                    for x in range(len(sample_txtdata[line][1][y])-1):
                        txt = txt + f"{sample_txtdata[line][1][y][x]}, "
                    txt = f"{txt}{sample_txtdata[line][1][y][-1]} ]"
                    f.write(txt + "\n")
            else:
                f.write("None" + "\n")

            f.write("\n")

        f.write("END")

    return("セーブ完了")



#識字コードの定義
backupfile_name = "/Users/matsuurakenshin/WorkSpace/development/test_seach_txtcode.txt" # このファイルに情報が入っている
guide,Unicode,seach_txttype = txtcode_selection(backupfile_name)


"""
============================================================================================================================================
"""


# マニュアル操作
imagename = "/Users/matsuurakenshin/WorkSpace/公開用/TextReader/version=1&uuid=373F890D-0E09-4AFD-A766-6EA15D4186CB&mode=compatible&noloc=0.jpeg"

wariai = 0.892

color_image = set_image(imagename,wariai) #イメージとその比率
code0list = removal_background(color_image,[36,36,36],80) #イメージ,背景色,背景色範囲

dataslist = {

    "imagename" : "",
    "siz" : 0.892,

    #変更可能 /  一番初めの文字の左上の位置を(txtx,txty)に代入する
    "txtx" : 4,
    "txty" : 11,

    #変更不可 // ブロックの幅を変えることに対応していないので(width,hight,sahight)の値は変える事はできない
    "width": 19.84,
    "hight": 36,
    "sahight": 13.4,

    #これより下のデータはプログラムを回す内に勝手に再代入されていく為、無視して大丈夫です。
    "color_image":"",
    "code0list":"",
    "txtcode":"",

    "linelen":"",
    "txtlen":"",
    "hight":"",
    "Max":"",

}


print(list(dataslist.items()))

#変更可能 /  一番初めの文字の左上の位置を(txtx,txty)に代入する
txtx = 4 #一番最初の文字の一番左の座標
txty = 11 #一番最初の文字の一番上の座標

#変更不可 // ブロックの幅を変えることに対応していないので(width,hight,sahight)の値は変える事はできない
width = 19.84   #文字の幅
hight = 36      #文字の高さ
sahight = 13.4 #余分な高さ

#CUT(color_image,code0list,txtx,txty,width,hight,sahight)
#interval = get_interval(code0list,1)
#print(interval)

#print(wariai*(width/interval))
#get_interval(code0list,0.07)

#final
#txtcode,linelen,txtlen,hight,Max = insertlist(color_image,code0list,txtx,txty,width,hight,sahight)
#txtcode = seach_strat(color_image,code0list,txtx,txty,width,hight,sahight)


#識字コードの詳細な定義
#　function / inserttxtdata　/ [解読用テキストデータへ追加、保存] / (サンプルデータ,参照元のリスト,該当文字,行数,列数,保存ファイル名) / return "セーブ完了"

def inserttxtdata(sample_txtdata,txtcode,txttype,line,txtline,filename):

    for num in range(len(sample_txtdata)):
        if sample_txtdata[num][0] == txttype:

            point = num
            print(txtcode[line,txtline])

            print((txty + ((hight+sahight)*line) - int(txty + ((hight+sahight)*line))))
            print((txtx + (width*txtline) - int(txtx + (width*txtline))))

            break

    else:
        print("該当なし")
        return

    if input(f"変更内容 [ ' {txttype} ' ] (保存:save)？") == "save":

        remake = txtcode[line,txtline].copy()

        if sisyagonyu(txty + ((hight+sahight)*line) - int(txty + ((hight+sahight)*line))) == 1:
            remake[:-1,:] = remake[1:,:]
            remake[-1,:] = np.array(1)

        if sisyagonyu(txtx + (width*txtline) - int(txtx + (width*txtline))) == 1:
            remake[:,:-1] = remake[:,1:]
            remake[:,-1] = np.array(1)

        print(remake)

        sample_txtdata[point][1] = remake
        print(save_txtcode_data(sample_txtdata,filename))

    else:
        print('No save')

filename = "/Users/matsuurakenshin/WorkSpace/development/test_seach_txtcode.txt"


#seach_type_test, seach_code_test, sample_txtdata = txtcode_selection(filename)
#inserttxtdata(sample_txtdata,txtcode,"R", 11,21,filename)
#save_txtcode_data(sample_txtdata,filename)

#backupfile_name = "thin_seach_txtcode.txt"

#set_txtcode(txtcode, seach_txtcode, inserttxt, linenum, txtlennum):
#backup_txtcode(seach_txtcode, backupfile_name)
#seach_txtcode = restoration(backupfile_name)



#np.count_nonzero(txtcode[10,48] == Unicode[41])
#txtcode[10,48]
#guide[41]

#shifxtnum = 2

#anser = Unicode[0,0]
#for y in range(Unicode[0,0].shape[0]):
#    for x in range(Unicode[0,0].shape[1]-shifxtnum):
#        anser[y,x+shifxtnum] = Unicode[0,0,y,x]

#print(anser)