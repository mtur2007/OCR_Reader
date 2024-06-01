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

retest[0] = SET_numbertxt(retest[0],1)
retest_copy = SET_numbertxt(retest)

numdata = ""
txtdata = ""

for num in range(len(retest)):
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
