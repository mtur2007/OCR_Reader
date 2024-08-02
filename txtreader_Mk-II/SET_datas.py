
def Myint(num): #数値の int部分を確実に表示させる様にする自作関数
    for line in range(len(str(num))):
        if str(num)[line] == ".":
            return int(str(num)[:line])
    return num


#数値の整列を行う関数

import copy
import numpy as np
import time


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


def SET_data(datas,mode):

    if isinstance(datas[0][0], list) == False:
        datas = [datas]
        mode = 1

    Allprint_txt = []
    Lineslist = []

    #リストの２次元配列ごとに, 3次元配列同士の要素を縦方向毎になる様に入れ変える
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
            if len(data) == 0:
                data.append("")
            for dataline in range(len(data)):
                printline[dataline].append(data[dataline])

            for num in range((max-1 - dataline)):
                printline[dataline + num+1].append('')

        for line in printline:
            Allprint_txt.append(line)
        
        Lineslist.append(len(Allprint_txt)-1)
    
    #return Allprint_txt
    '''
    print("\nSET_data(datas) ソート結果\n")
    for line in Allprint_txt:
        print(line[:10])
    '''
    set_datas = SET_txts(Allprint_txt,mode,0)

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

def data_border_print(set_data,guide,indeximage):

    start = time.time()

    printlist = []
    linelen0 = 0

    if guide == True:
        max_leny = len(str(len(set_data)-1))+2
        sample_guide = f" {max_leny * ' '} |  "
    else:
        sample_guide = "|  "

    list_index = []
    for linenum in range(len(set_data)):
        dataline = set_data[linenum]
        if len(dataline) != 0:
            writeline = []

            #それぞれのラインに横枠をつける
            list_index.append(dataline[0])
            for linenum in range(len(dataline)-1):
                line = dataline[linenum+1]
                printline = sample_guide
                for txt in line:
                    printline +=  txt + "  |  "
                printline = printline[:-2]

                writeline.append(printline)

            
            linelen1 = len(printline)

            #横枠の作成...表示文字列列の以前の長さと現在の長さによって長さの基準を変える
            if linelen0 > linelen1:
                printlist.append(f"{'='*linelen0}\n")
                printlist.append('\n')
            else:
                printlist.append(f"{'='*linelen1}\n")
                printlist.append('\n')

            linelen0 = linelen1

            for line in writeline:
                printlist.append(f"{line}\n")

            printlist.append('\n') #※0
        
        else:
            printlist.append(f"{'='*linelen0}\n")
            printlist.append('\n')
            if linenum != len(set_data)-1:
                printlist.append(f" >> Xx__No_data__xX\n")
                printlist.append('\n')
            else:
                printlist.append(f" >> Xx__No_data__xX\n")
            linelen0 = 0

    if len(set_data[-1]) != 0:
        printlist.append(f"{'='*linelen1}\n")

    finish = time.time()
    print(f'[SET_border, border] time: {finish - start}')

    #ガイド(index)を追加する場合の処理
    if guide == True:
        start = time.time()

        sample_guide = f" {max_leny * ' '} "
        set_index = 1
        for linenum in range(len(set_data)):
            line = set_data[linenum]
            indexline = list_index[linenum]

            if len(line) != 0:
                if linenum != 0:
                    #txt = str(indeximage[linenum]) + '\n {' + str(linenum-1) + '}'
                    txt = '{' + str(linenum-1) + '}'
                    air = (max_leny - len(txt)) * ' '
                    guidex0 = ' ' + air + str(txt) + ' |  '
                else:
                    guidex0 = sample_guide+ '|  '
                guidex1 = sample_guide + '|--'
                guidex2 = sample_guide + ':  '

                for txtnum in range(len(line[0])):
                    txt_index = indexline[txtnum]

                    guidex0 += str(txt_index) + "  |  "
                    guidex1 += len(line[0][txtnum]) * "-" + "--|--"
                    guidex2 += len(line[0][txtnum]) * " " + "  :  "

                printlist.insert(set_index,guidex0[:-2]+'\n')
                printlist.insert(set_index+1,guidex1[:-2]+'\n')

                #ボーダー作成時に追加した空白部分(※0)はガイドをつける場合、いらないので情報を書き換える。
                printlist[set_index+2] = guidex2[:-2] + '\n'

                set_index += len(line)+2 + 2

            else: #データがない時は1文で表示される為、例外処理
                set_index += 1 +3

        finish = time.time()
        print(f'[SET_border, guide ] time: {finish - start}')

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


"""
numberslist = []

for i in range(50):
    numberslist.append(Myrandom(8, -2000,2000, 2))

#numberslist = list_random_del(numberslist)


print(f"\n\nnormal_print\n")

for line in numberslist:
    print(line)


set_txts    = 1
set_numbers = 1

print()

if set_txts == 1:
    print(f"\nSET_txts()_print\n>> position[left--]\n")

    txtslist = SET_txts(numberslist,0,0)
    #txtslist = []

    for line in txtslist:
        print(line)
    print()


if set_txts == 1:
    print(f"\nSET_txts()_print\n>> position[-center-]\n")

    txtslist = SET_txts(numberslist,0,1)
    #txtslist = []

    for line in txtslist:
        print(line)
    print()


if set_txts == 1:
    print(f"\nSET_txts()_print\n>> position[--right]\n")

    txtslist = SET_txts(numberslist,0,2 )
    #txtslist = []

    for line in txtslist:
        print(line)
    print()

if set_numbers == 1:
    print(f"\nSET_numbers()_print\n")

    set_number = SET_numbers(numberslist,0)

    for line in set_number:
        print(line)
    print()

"""


#========================================================================================================================
'''
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
'''
"""
import pickle

### pickleで保存したファイルを読み込み
with open('/Users/matsuurakenshin/WorkSpace/development/txtreader/sample_datas.pickle', mode='br') as fi:
    sample_datas = pickle.load(fi)
"""
#------------------------------------------------------------------------------------------------------------------------
"""
def data_print(set_data):
        
    print(f"\n\n配列の縦表示\n")

    txtlen0 = 0

    for data in set_data:
        printlist = []
        Max = 0
        for line in data:
            printlist.append(f" '{line}'")
            if len(printlist[-1]) > Max:
                Max = len(printlist[-1])

        printlist.insert(0,"[")
        printlist.append("]")
        
        txtlen1 = (Max + 2) * 2 + 1
        if txtlen0 > txtlen1:
            print(txtlen0*"-")
        else:
            print(txtlen1*"-")

        for linenum in range(len(printlist)):
            line = printlist[linenum]
            if linenum != 0 and linenum != len(printlist)-1:
                print(f"{line}{(Max - len(line))*' '}  |  {(len(line)-3)*'*'}{(Max - len(line))*'.'}  |")
            else:
                print(f"{line}{(Max - len(line))*' '}  |  {(Max-1)*' '}|")
        txtlen0 = txtlen1
            
    print(txtlen0*"-")
"""
#------------------------------------------------------------------------------------------------------------------------

def data_print(datas):
    print('\n\n\n'+25*'-/-\\'+'\n')
    print("配列状態:")

    for linenum in range(len(datas)):
        txtlen0 = 0
        if txtlen0 != 0:
            print(f"{txtlen0*'-'}\n")
        print(f"\n{100*'='}")
        linetxt = f" line: {linenum+1} "
        print(f"[{linetxt}]\n")
        datasline = datas[linenum]
        for line in datasline:
            printdata = []
            Max = 0
            for txt in line:
                printdata.append("|  " + txt)
                if len(printdata[-1]) > Max:
                    Max = len(printdata[-1])
            txtlen1 = (Max + 2) * 2 + 1
            if txtlen0 > txtlen1:
                print(txtlen0*"-")
            else:
                print(txtlen1*"-")
            for line in printdata:
                print(f"{line}{(Max - len(line))*' '}  |  {(len(line)-3)*'*'}{(Max - len(line))*'.'}  |")
            txtlen0 = txtlen1
        
        if len(datasline) == 0:
            print(" >> Xx_No_data_xX")
            txtlen0 = 0
        else:
            print(txtlen0*"-")
    
    print(f"\n{100*'='}")

#------------------------------------------------------------------------------------------------------------------------

def SET_data_print(datas):

    print('\n\n\n'+25*'-/-\\'+'\n')

    TEST_datas = SET_data(datas,0)

    print("\nSET_data(datas) ソート結果\n")
    for dataline in TEST_datas:
        print(f"\n{100*'='}\n")
        if len(dataline) == 0:
            print('\n'+">> Xx_No_data_xX"+'\n')
        for line in dataline:
            print(line[:10])


#========================================================================================================================

def search_index(datas,deep,keep_start,keep_finish,index,now_index,line_txts,keep_linetxts,keep_index,MAX_indexlen):
    deep += 1 #deepはインデックスの次元測定

    txt_index = ''
    for i in now_index:
        txt_index += '['+str(i)+']'
    #txtline = [txt_index]
    txtline = []
    insert_index = len(line_txts)-1

    if keep_start == deep:
        keep = 1
        line_txts.append('')
        insert_index = len(line_txts)-1

        for linenum in range(len(datas)):
            keep_index = []
            line = datas[linenum]
            if linenum == 0:
                now_index.append(linenum)

            else:
                now_index[-1] = linenum

            datatype = type(line)

            if datatype == list or datatype == np.ndarray:
                keep_linetxts = []
                # < MAX_indexlen > インデックス別整列をする為、linenumの値は使わず、リストの階層だげを調べる。
                index,now_index,line_txts,keep_linetxts,keep_index,MAX_indexlen = search_index(line,deep,keep_start,keep_finish,index,now_index,line_txts,keep_linetxts,keep_index,MAX_indexlen)
                #keep_linetxts = '['+keep_linetxts[:-1]+']'
                #keep_linetxts = keep_linetxts[:-1]
                txtline.append(keep_linetxts)
            else:
                #txtline.append(str(line))
                #リストの最下層の場合の処理
                index += '.'
        print('\n'+('-'*84)+'\n'+txt_index)
        del MAX_indexlen['[]']
        print(MAX_indexlen)

        linenum = 0
        printlist = []

        for keep_linenum in range(len(txtline)):
            keep_line = txtline[keep_linenum]
            printlist.append([''])
            keep_linetxts = ''

            for k, v in MAX_indexlen.items():
                #print(k,v)
                for keep_txtnum in range(len(keep_line)):
                    keep_txts = keep_line[keep_txtnum]

                    if k == keep_txts[0]:
                        air = (v - len(keep_txts[1])) * ' ' + ' '
                        keep_linetxts += air + str(keep_txts[1])
                        if v != len(keep_txts[1]):
                            printlist.append(['[ len  ]','index: '+ k , 'len: ' + str(v) ,' txtlen: '+str(len(keep_txts))])
                        #print(keep_txts[0])
                        break
                else:
                    keep_linetxts += v*' ' + ' '
                    printlist.append(['[ None ]','index: '+ k , 'len: ' + str(v)])
            
            print(keep_linetxts)
        
        if len(printlist) != 0:
            anser = SET_txts(printlist,0,0)
            for a in anser:
                txt = ''
                for b in a:
                    txt += b+' '
                print(txt)

        MAX_indexlen = {}


        #中身のリスト作成
        #line_txts[insert_index] = txtline
        line_txts[insert_index] = [('! - NOW_MAKE - '*4)+('!')]
    

    elif keep_start < deep <= keep_finish:

        #リストが出てきた場合、順番がおかしくならないよう、仮置きとして0を代入する。
        key = str(keep_index)
        if (key in MAX_indexlen) == False:
            MAX_indexlen[key] = 0

        keep_index.append('')

        for linenum in range(len(datas)):
            keep_index[-1] = linenum
            line = datas[linenum]
            if linenum == 0:
                #print()
                now_index.append(linenum)

            else:
                now_index[-1] = linenum

            #print(txt)
            datatype = type(line)
            if datatype == list or datatype == np.ndarray:
                #print(search_index(line))
                #keep_linetxts += f'[ '
                index,now_index,line_txts,keep_linetxts,keep_index,MAX_indexlen = search_index(line,deep,keep_start,keep_finish,index,now_index,line_txts,keep_linetxts,keep_index,MAX_indexlen) 
                #keep_linetxts += '] '
            else:
                key = str(keep_index)
                keep_linetxts.append([key,str(line)])
                #key = f'{deep},{linenum}'

                #テキストの場合、中身の長さを入れる。
                if (key in MAX_indexlen) == False:
                    MAX_indexlen[key] = len(str(line))
                elif MAX_indexlen[key] < len(str(line)):
                    MAX_indexlen[key] = len(str(line))


                #リストの最下層の場合の処理
                index += '.'

        del keep_index[-1]
    
    else:
        keep = 0

        line_txts.append('')
        insert_index = len(line_txts)-1

        for linenum in range(len(datas)):
            line = datas[linenum]
            if linenum == 0:
                #print()
                now_index.append(linenum)

            else:
                now_index[-1] = linenum

            txt = ""
            for i in now_index:
                txt += "[" + str(i) + "]"
            #print(txt)
            datatype = type(line)
            if datatype == list or datatype == np.ndarray:
                #print(search_index(line))
                index,now_index,line_txts,keep_linetxts,keep_index,MAX_indexlen = search_index(line,deep,keep_start,keep_finish,index,now_index,line_txts,keep_linetxts,keep_index,MAX_indexlen)
                txtline.append(f'data_type: {datatype}')
            else:
                txtline.append(str(line))
                #リストの最下層の場合の処理
                index += '.'
            
        #中身のリスト作成
        line_txts[insert_index] = txtline

    #インデックス簡易表現作成
    if len(datas) != 0:
        #print(index[-len(datas):])

        txt = ''
        for data in index[-len(datas):]:
            #if data != ".":
            txt += data
        
        txt = f" [ {txt} :{len(datas)} ] "
        index = index[:-len(datas)]

        del now_index[-1] #インデックスの調査が終わったら戻す

    else:
        txt = " [ nodata :0 ]"
        print(f"list index: {now_index} / data: {txt}\nデータがありません。※修正は任意\n")
    index.append(txt)

    return index,now_index,line_txts,keep_linetxts,keep_index,MAX_indexlen


def SET_list(datas,guide,keep_start,keeplen):
    if keep_start == False:
        keep_start = 0
        keep_finish = 0
    else:
        keep_start += 1
        keep_finish = keep_start + keeplen

    start = time.time()

    deep,index,now_index,line_txts,keep_linetxts,keep_index,MAX_indexlen = 0,[],[],[],[],[],{}
    deep += 1 #deepはインデックスの次元測定

    txtline = ['[]']
    list_txts = []
    indexline = []
    for linenum in range(len(datas)):
        line_txts = []
        line = datas[linenum]
        now_index = [linenum]
        #print(txt)
        datatype = type(line)
        if  datatype == list or datatype == np.ndarray:
            #print(search_index(line))
            index,now_index,line_txts,keep_linetxts,keep_index,MAX_indexlen = search_index(line,deep,keep_start,keep_finish,index,now_index,line_txts,keep_linetxts,keep_index,MAX_indexlen)
            list_txts.append(line_txts)
            txtline.append(f'data_type: {datatype}')
            indexline.append(index)
        else:
            txtline.append(str(line))
            #リストの最下層の場合の処理
            indexline.append('.')
            linedeep = deep
        index = []
    
    print(('-'*84))
    
    indexline.insert(0,'')
        
    list_txts.insert(0,[txtline])

    finish = time.time()
    print()
    print(f'[search_index] time: {finish - start}')

    #データを縦方向に合わせて整列し、結果をファイルに書き込む。
    start = time.time()
    set_list = SET_data(list_txts,0)
    finish = time.time()
    print(f'[SET_data]     time: {finish - start}')
    print()

    start = time.time()
    set_border_list = data_border_print(set_list,guide,indexline)
    finish = time.time()
    print(f'[SET_border, All ]   time: {finish - start}')
    print()

    return set_border_list

#------------------------------------------------------------------------------------------------------------------------
'''
#サンプルのデータ
data_GC_G = sample_datas[0][0]
data_GC_C = sample_datas[0][1]
data_B3_B = sample_datas[1][0]
data_B3_3 = sample_datas[1][1]
data_Il_I = sample_datas[2][0]
data_Il_l = sample_datas[2][1]
data_xa_x = sample_datas[3][0]
data_xa_a = sample_datas[3][1]


#サンプルデータの表示
datas = [data_B3_3[:4],"",data_xa_x[:4]]
datas = data_xa_x[:4]
datas = data_Il_l[:5]

#datas = [[data_B3_B[0]],data_B3_3[:2]]
#datas = [data_B3_B[0]]
#datas = [["a","a",["a","a",["ab","ab"]]],["ab","ab"],['a','a'],['a','a'],['a','a'],['a','a'],['a','a'],['a','a'],['a','a'],['a','a'],['a','a'],['a','a']]

#datas = [["a","a","a","a"],["b","b"],["c","c","c"]]
#datas = [["a","a","a","a"],["b","b"],[["c","c","c"]]]
#datas = [["a","a",["a","a",["a","a"],"a"],"a","a",["a","a"]],[["c","c",["c","c","c"],"c"]]]

datas = [data_B3_3[:2],[data_xa_x[2]],data_Il_l[:3],data_xa_x[:5]]
#リストの最適化

#print("\nリスト構造... 配列に誤りがある場合マーキングされます。")
#print(f"\n配列例:) [ 1行目[a,a,a], 2行目[b,b], ３行目[c,c,c]]\n\n")
print()

import time
start = time.time()

set_border_list = SET_list(datas,True)

for a in list_txts[1]:
#    for b in a:
    for c in a:
        print(c)
for a in datas[3]:
    for c in a:
        print(c)
#index = search_index(datas,[])[0]
#print(index)


#配列の状態をプリントするプログラム
#data_print(datas)

#列毎にリスト分けした結果
#SET_data_print(datas)

#データを縦方向に合わせて整列し、結果をファイルに書き込む。


with open("Remake_SET.txt","w") as f:
    for line in set_border_list:
        f.write(f"{line}")

finish = time.time()

print(f'time: {finish-start}')

"""
for i in line_txts:
    for a in i:
        print(a)
"""
print('\n\n\n'+25*'-/-\\'+'\n')
'''