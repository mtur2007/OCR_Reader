import numpy as np
import pickle
import math
import cv2
import matplotlib.pyplot as plt

from SET_datas import SET_numbers

from pynput import keyboard



def search_anser_contours(contours,minus):
    global square_size,square
    contours = np.array(contours) * square_size

    squareY = []
    squareX = []
    guideY = []
    guideX = []
    for linenum in range((np.shape(contours)[0])-minus):
        linenum += minus

        index0 = contours[linenum-1]
        index1 = contours[linenum]
        sY = square[0] + index1[0]
        sX = square[1] + index1[1]

        squareY.append(sY)
        squareX.append(sX)


        dy = index1[0]-index0[0]
        dx = index1[1]-index0[1]


        if dy >= 0:
            Y_type = 1
        else:
            Y_type = -1

        if dx >= 0:
            X_type = 1
        else:
            X_type = -1

        if abs(dy) > abs(dx):
            x = ( abs(dx)/abs(dy) )
            for i in range(abs(dy)):
                guideY.append(int(index0[0]+(i*Y_type)) + center)
                guideX.append(int(index0[1]+(( x* i ) * X_type)) + center)
                #print(index1[0]+(i*Y_type),index1[1]+(( x* ( abs(dy)-i ) ) * X_type))
                #print(int(index0[0]+(i*Y_type)), int(index0[1]+(( x* ( abs(dy)-i ) ) * X_type)))
                
                #guide.append[i*Y_type, ( x* ( abs(dy)-i ) ) * X_type]
                            #               ^   逆演算   ^
        else:
            y = ( abs(dy)/abs(dx) )
            for i in range(abs(dx)):
                #guide.append[ (y*i)*Y_type, i*X_type]
                #guide = [int(index1[0]+((y*i)*Y_type)), int(index1[1]+(i*X_type))]
                #print (index1[0]+((y*i)*Y_type), index1[1]+(i*X_type))
                guideY.append(int(index0[0]+((y*i)*Y_type)) + center)
                guideX.append((index0[1]+(i*X_type)) + center)
                
                #print(guide)


    square_guide = (np.array(squareY), np.array(squareX))
    atan2_guide = (np.array(guideY),np.array(guideX))

    return square_guide,atan2_guide


def make_search_contours_data(search_contours_set):
    global square_size,square
    image = search_contours_set[0]
    contours = search_contours_set[2]
    image=cv2.resize(image,None,fx=square_size,fy=square_size,interpolation=cv2.INTER_NEAREST)

    maxnum = np.amax(contours,axis=0)+1

    square_guide,atan2_guide = search_anser_contours(contours,0)

    #contoursの内側を沿うように情報を抽出する。
    NEW_contours = []
    for linenum in range(np.shape(contours)[0]):
        index0 = contours[linenum-1]
        index1 = contours[linenum]

        d = index1 - index0
        if (abs(d[0]) != 1) or (abs(d[1]) != 1):
            NEW_contours.append(index1)

        else:
            d2 = index1 - contours[linenum-2]
            #d2[0] = d2[0]*-1
            d2_atan2 = math.degrees(math.atan2(d2[0],d2[1]))
            if (abs(180 - abs(d2_atan2)) < 45) or (abs(d2_atan2) < 45):
            #  ^   ↙︎ ↖︎                       ^　　 ^    ↗︎ ↘︎           ^
            
                insert_index = index0
                #内側と外側はベクトルが反転する為、同条件のifの結果が異なることで判別し、内側と外側に沿って加工することができる。
                if (d[0] == 1) and (d[1] == 1):
                    insert_index = index1
                if (d[0] == -1) and (d[1] == -1):
                    insert_index = index1
                NEW_contours[-1] = insert_index
            else:
                insert_index = index1

                if (d[0] == 1) and (d[1] == 1):
                    insert_index = index0
                if (d[0] == -1) and (d[1] == -1):
                    insert_index = index0
                NEW_contours[-1] = insert_index


    #角度が45度の場合、ガタつきを直せないので特殊な加工をする。
    contours = NEW_contours
    NEW_contours = []
    for linenum in range(np.shape(contours)[0]):
        index0 = contours[linenum-1]
        index1 = contours[linenum]

        d = index1 - index0
        if(abs(d[0]) + abs(d[1])) == 1:
            
            d2 = index1 - contours[linenum-2]
            d2_atan2 = math.degrees(math.atan2(d2[0],d2[1]))
            if (abs(180 - abs(d2_atan2)) < 45) or (abs(d2_atan2) < 45):
                insert_index = index1
                if (d2[0] > 0) and (d2[1] > 0):
                    insert_index = index0
                if (d2[0] < 0) and (d2[1] < 0):
                    insert_index = index0
            else:
                insert_index = index0
                if (d2[0] > 0) and (d2[1] > 0):
                    insert_index = index1
                if (d2[0] < 0) and (d2[1] < 0):
                    insert_index = index1
            
            NEW_contours[-1] = insert_index

        else:
            NEW_contours.append(index1)


    contours = NEW_contours
    NEW_contours = []

    #連続で同じ角度が続いてるのものを除外する。
    for linenum in range(len(contours)-2):

        index_m1 = contours[linenum-1]
        index0 = contours[linenum]
        index1 = contours[linenum+1]

        diff = index0 - index_m1
        now_diff = index1 - index0
        if (diff != now_diff).any():
            NEW_contours.append(index0)

    NEW_contours.append(contours[-1])
    #[抽出前の配列: contours],[抽出後の配列: NEW_contours]


    # print('-------')
    # print(f'      |\n  . → |    {math.degrees(math.atan2(0,1))} /  {math.atan2(0,1)}\n      |\n-------')
    # print(f'    ↗ |\n  .   |   {math.degrees(math.atan2(1,1))} /  {math.atan2(1,1)}\n      |\n-------')
    # print(f'  ↑   |\n  .   |   {math.degrees(math.atan2(1,0))} /  {math.atan2(1,0)}\n      |\n-------')
    # print(f'↖     |\n  .   |  {math.degrees(math.atan2(1,-1))} /  {math.atan2(1,-1)}\n      |\n-------')
    # print(f'      |\n← .   |  {math.degrees(math.atan2(0,-1))} /  {math.atan2(0,-1)}\n      |\n-------')
    # print(f'      |\n  .   | {math.degrees(math.atan2(-1,-1))} / {math.atan2(-1,-1)}\n↙     |\n-------')
    # print(f'      |\n  .   |  {math.degrees(math.atan2(-1,0))} / {math.atan2(-1,0)}\n  ↓   |\n-------')
    # print(f'      |\n  .   |  {math.degrees(math.atan2(-1,1))} / {math.atan2(-1,1)}\n    ↘ |\n-------')


    # print(math.atan2(-1,-2))


                
    NEW_contours = np.array(NEW_contours)
    NEW_guide,NEW_atan2_guide = search_anser_contours(NEW_contours,0)
    #contoursの座標をリストインデックスの状態でテキスト化したもの(Y↓,X→)
    text_contours_list = SET_numbers(np.array(NEW_contours,dtype=str).tolist(),mode=0)

    maxnum = np.amax(NEW_contours,axis=0)
    NEW_contours_nomal = NEW_contours.copy()
    NEW_contours_nomal[:,0] = maxnum[0] - NEW_contours_nomal[:,0]
    #contoursの座標を通常の状態でテキスト化したもの(Y↑,X→)
    text_contours = SET_numbers(np.array(NEW_contours_nomal,dtype=str).tolist(),mode=0)

    contours_diff = []
    contours_degrees = []


    for linenum in range(len(NEW_contours)):
        contour0 = NEW_contours[linenum-1]
        contour1 = NEW_contours[linenum]

        d = contour1 - contour0
        contours_diff.append([(d[0] * -1),d[1]])
        contours_degrees.append(math.degrees(math.atan2((d[0] * -1),d[1])))

    #contoursの(n-(n-1))をテキスト化したもの
    text_diff = SET_numbers(np.array(contours_diff,dtype=str).tolist(),mode=0)
    #contoursの(n-(n-1))をatan2関数を使って角度したものをテキスト化したもの
    text_degrees = SET_numbers(contours_degrees.copy(),mode=1)[0]

    height = square_size*maxnum[0]
    width  = square_size*maxnum[1]
    mathmeY = []
    mathmeX = []

    mathmey = np.arange(height)
    mathmex = np.arange(width)
    if square_size > 2:
        plusnum = 0
    else:
        plusnum = 1
    for i in range(height//square_size):
        ylist = mathmex.copy()
        ylist[:] = (i*square_size)+plusnum
        mathmeY.extend(ylist)
        mathmeX.extend(mathmex)

    for i in range(width//square_size):
        mathmeY.extend(mathmey)
        xlist = mathmey.copy()
        xlist[:] = (i*square_size)+plusnum
        mathmeX.extend(xlist)

    mathme = (np.array(mathmeY),np.array(mathmeX))

    write_txt = []
    anser_data = []
    for linenum in range(len(text_degrees)):
        write_txt.append(f"   :  [{text_contours_list[linenum][0]}, {text_contours_list[linenum][1]}]  :  [{text_contours[linenum][0]}, {text_contours[linenum][1]}]  :  [{text_diff[linenum][0]}, {text_diff[linenum][1]}]  :  {text_degrees[linenum]}  ")
        anser_data.append([NEW_contours[linenum],NEW_contours_nomal[linenum],np.array(contours_diff[linenum]),np.array([contours_degrees[linenum],0])])

    anser_data = np.array(anser_data)
    return image,square_guide,atan2_guide,mathme,NEW_guide,NEW_atan2_guide,write_txt,anser_data,NEW_contours

### pickleで保存したファイルを読み込み
with open('/Users/matsuurakenshin/WorkSpace/development/txtreader/txtreader3_rinkaku/pickle_file/TEST_rinkaku.pickle', mode='br') as fi:
    search_contours_list = pickle.load(fi)

Back_Color = [0,0,0]
Square_Color = np.array((0,255,0))
Guide_Colror = [0,0,255]
mathme_Color = [100,30,30]

square_size = 15
frame = 3

square = np.tile(1, square_size**2).reshape((square_size,square_size))
square[frame:square_size-frame,frame:square_size-frame] = 0
square = np.where(square == 1)

center = square_size//2 + square_size%2

anser_contours_list = []
max_hight,max_width = 0,0
for search_contours_set in search_contours_list:
    anser_contours_list.append(make_search_contours_data(search_contours_set))


def Make_ContoursImage(image_print,atan2_print,square_print,math_print,index_print,atan22_print,square2_print,image,square_guide,atan2_guide,mathme,NEW_guide,NEW_atan2_guide,write_txt):
    contours_image = image.copy()

    if image_print == True:

        if index_print == True:
            Square_Color = [0,0,200]
            Square2_Color =[200,0,0]

            Guide_Colror = [0,0,100]
            Guide2_Colror =[0,100,0]
        else:
            Square_Color = [0,0,255]
            Square2_Color =[255,0,0]

            Guide_Colror = [0,0,200]
            Guide2_Colror =[0,200,0]

        mathme_Color = [80,10,10]
    else:
        contours_image[:,:] = Back_Color.copy()
        #contours_image = Black_image

        if index_print == True:
            Square_Color = [130,0,0]
            Square2_Color =[0,0,130]

            Guide_Colror = [5,85,80]
            Guide2_Colror =[80,85,5]
        else:
            Square_Color = [200,0,0]
            Square2_Color =[0,0,200]
                
            Guide_Colror = [10,170,160]
            Guide2_Colror =[160,170,10]

        mathme_Color = [50,50,50]

    if atan2_print == True:
        contours_image[atan2_guide] = Guide_Colror
    if square_print == True:
        contours_image[square_guide] = Square_Color

    if math_print == True:
        contours_image[mathme] = mathme_Color

    if atan22_print == True:
        contours_image[NEW_atan2_guide] = Guide2_Colror
    if square2_print == True:
        contours_image[NEW_guide] = Square2_Color

    return contours_image


def on_press(key):

    global contours_num,image_print,square_print,atan2_print,square2_print,atan22_print,math_print,index_print,now_index,anser_contours_list,keep,keep_index_S,keep_index_F,keep_side,keep_contourslist,write_txt
    try:
        key = key.char
        if key == '.':  #'輪郭の表示'
            square_print = not square_print

        elif key == '/': #'角度の表示'
            atan2_print = not atan2_print
        
        elif key == '3': #'3[#の代用](マス目の表示))'
            math_print = not math_print
        
        elif key == '1': #'現在のインデックス情報を表示'
            index_print = not index_print

        elif key == '@': #'*(元の情報の表示)'
            image_print = not image_print
        
        elif key == ';':
            square2_print = not square2_print
        elif key == ':':
            atan22_print = not atan22_print
        
        elif key == 'c':
            now_index = 0
            contours_num += 1
            contours_num = contours_num % contours_listlen
        elif key == 'z':
            now_index = 0
            contours_num -= 1
            contours_num = abs(contours_num % contours_listlen)
        
        elif key == 'd':
            now_index += 1
            now_index = now_index % len(anser_contours_list[contours_num][-1])

        elif key == 'a':
            now_index -= 1
            now_index = abs(now_index % len(anser_contours_list[contours_num][-1]))
            
        elif key == 'x':
            keep_side = not keep_side
        pass
        
        image,square_guide,atan2_guide,mathme,NEW_guide,NEW_atan2_guide,write_txt,anser_data,NEW_contours = anser_contours_list[contours_num]
        contours_image = Make_ContoursImage(image_print,atan2_print,square_print,math_print,index_print,atan22_print,square2_print,image,square_guide,atan2_guide,mathme,NEW_guide,NEW_atan2_guide,write_txt)
        
        if index_print == True:

            if keep == True:
                keep_index_F = now_index
            else:
                if now_index == 0:
                    keep_index_S = np.shape(NEW_contours)[0]-1
                else:
                    keep_index_S = now_index-1
                keep_index_F = now_index


            square_y = square[0] + NEW_contours[keep_index_S][0]*square_size
            square_x = square[1] + NEW_contours[keep_index_S][1]*square_size
            S_square = (square_y,square_x)

            square_y = square[0] + NEW_contours[keep_index_F][0]*square_size
            square_x = square[1] + NEW_contours[keep_index_F][1]*square_size
            F_square = (square_y,square_x)
            
            if keep_side == True:
                if keep_index_S < keep_index_F:
                    a = NEW_contours[keep_index_S:keep_index_F+1]
                else:
                    a = np.append(NEW_contours[keep_index_S:],NEW_contours[:keep_index_F+1],axis=0)
                contours_image[S_square] = [0,150,150]
                contours_image[F_square] = [0,255,255]
            else:
                if keep_index_S < keep_index_F:
                    a = np.append(NEW_contours[keep_index_F:],NEW_contours[:keep_index_S+1],axis=0)
                else:
                    a = NEW_contours[keep_index_F:keep_index_S+1]
                contours_image[S_square] = [0,255,255]
                contours_image[F_square] = [0,150,150]
                
            index_square, index_guide = search_anser_contours(a,1)
            
            guide_Xshape = np.shape(index_guide)[1]
            if guide_Xshape != 0:
                contours_image[index_guide] = [0,200,200]

            copy_write_txt = write_txt.copy()
            copy_write_txt[now_index-1] = ' >'+ copy_write_txt[now_index-1][2:]
            copy_write_txt[now_index] = ' ▶'+ copy_write_txt[now_index][2:]
            with open('/Users/matsuurakenshin/WorkSpace/development/txtreader/txtreader3_rinkaku/Make_txtfile/contours_degrees.txt','w') as f:
                for line in copy_write_txt:
                    f.write(line+'\n')
        cv2.imwrite('/Users/matsuurakenshin/WorkSpace/development/txtreader/txtreader3_rinkaku/Make_picture/__Controllable__contours_image.jpg', contours_image)

    except AttributeError:
        if key == keyboard.Key.shift:
            if keep == True:
                
                image,square_guide,atan2_guide,mathme,NEW_guide,NEW_atan2_guide,write_txt,anser_data,NEW_contours = anser_contours_list[contours_num]
                contours_image = Make_ContoursImage(False,False,False,False,True,True,True,image,square_guide,atan2_guide,mathme,NEW_guide,NEW_atan2_guide,write_txt)
                print(np.shape(contours_image))
                
                anser_data,NEW_contours = anser_contours_list[contours_num][-2],anser_contours_list[contours_num][-1]

                if keep_side == True:

                    square_y = square[0] + NEW_contours[keep_index_S][0]*square_size
                    square_x = square[1] + NEW_contours[keep_index_S][1]*square_size
                    S_square = (square_y,square_x)

                    square_y = square[0] + NEW_contours[keep_index_F][0]*square_size
                    square_x = square[1] + NEW_contours[keep_index_F][1]*square_size
                    F_square = (square_y,square_x)

                    if keep_index_S < keep_index_F:
                        guide = NEW_contours[keep_index_S:keep_index_F+1]
                        a = write_txt[keep_index_S:keep_index_F+1]
                        keep_anser_data = anser_data[keep_index_S:keep_index_F+1]
                    else:
                        guide = np.append(NEW_contours[keep_index_S:],NEW_contours[:keep_index_F+1],axis=0)
                        a = np.append(write_txt[keep_index_S:],write_txt[:keep_index_F+1],axis=0)
                        keep_anser_data = np.append(anser_data[keep_index_S:],anser_data[:keep_index_F+1],axis=0)

                    contours_image[S_square] = [0,150,150]
                    contours_image[F_square] = [0,255,255]

                else:
                    if keep_index_S < keep_index_F:
                        guide = np.append(NEW_contours[keep_index_F:],NEW_contours[:keep_index_S+1],axis=0)
                        a = np.append(write_txt[keep_index_F:],write_txt[:keep_index_S+1],axis=0)
                        keep_anser_data = np.append(anser_data[keep_index_F:],anser_data[:keep_index_S+1],axis=0)
                    else:
                        guide = NEW_contours[keep_index_F:keep_index_S+1]  
                        a = write_txt[keep_index_F:keep_index_S+1]
                        keep_anser_data = anser_data[keep_index_F:keep_index_S+1]
                
                    contours_image[S_square] = [0,255,255]
                    contours_image[F_square] = [0,150,150]
                
            
                index_square, guide = search_anser_contours(guide,1)
                contours_image[guide] = [0,200,200]

                a = (contours_image,(contours_num,keep_index_S,keep_index_F,keep_side),keep_anser_data,a)
                print(f'contours_number:{contours_num}, Start:{keep_index_S}, Finsh:{keep_index_F}, keep_side:{keep_side}')

                keep_contourslist.append(a)
            keep = not keep

        elif key == keyboard.Key.esc:
            # ESC キーが押された場合に終了
            return False
        
contours_num  = 0
contours_listlen  = len(search_contours_list)
image_print   = True
square_print  = False
atan2_print   = False
math_print    = False
square2_print = False
atan22_print  = False

index_print = False
now_index = 0
keep = False

NEW_contours = anser_contours_list[contours_num][-1]
keep_index_S = np.shape(NEW_contours)[0]-1
keep_index_F = now_index
keep_side = True
keep_contourslist = []

print('[:] ximage')
print('[.] contours')
print('[/] guide')
print('[#] boarder')

print('{_} break')


image,square_guide,atan2_guide,mathme,NEW_guide,NEW_atan2_guide,write_txt,nouse,nouse = anser_contours_list[contours_num]
contours_image = Make_ContoursImage(image_print,atan2_print,square_print,math_print,index_print,atan22_print,square2_print,image,atan2_guide,square_guide,mathme,NEW_atan2_guide,NEW_guide,write_txt)
cv2.imwrite('/Users/matsuurakenshin/WorkSpace/development/txtreader/txtreader3_rinkaku/Make_picture/__Controllable__contours_image.jpg', contours_image)
    
# キーボードのリスナーを開始
with keyboard.Listener(on_press=on_press) as listener:
    listener.join()

with open('/Users/matsuurakenshin/WorkSpace/development/txtreader/txtreader3_rinkaku/pickle_file/keep_datas.pickle', mode='wb') as fo:
    pickle.dump(keep_contourslist, fo)

image = anser_contours_list[contours_num][0]
C_shape = np.shape(image)
NK_image = cv2.imread('/Users/matsuurakenshin/WorkSpace/development/txtreader/picture_file/North_Korea.png')
NK_shape = np.shape(NK_image)
C_yx = C_shape[0] / C_shape[1]
NK_yx = NK_shape[0] / NK_shape[1]
if C_yx > NK_yx:
    hiritu = (C_shape[0]/NK_shape[0]) * 1
else:
    hiritu = (C_shape[1]/NK_shape[1]) * 1

NK_image = cv2.resize(NK_image,None,fx=hiritu,fy=hiritu)

C_gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
where_not0 = np.where(C_gray == 0)
not0_color = NK_image[where_not0]

image,square_guide,atan2_guide,mathme,NEW_guide,NEW_atan2_guide,write_txt,nouse,nouse = anser_contours_list[contours_num]
contours_image = Make_ContoursImage(image_print,atan2_print,square_print,math_print,index_print,atan22_print,square2_print,image,atan2_guide,square_guide,mathme,NEW_atan2_guide,NEW_guide,write_txt)

contours_image[where_not0] = not0_color
cv2.imwrite('/Users/matsuurakenshin/WorkSpace/development/txtreader/txtreader3_rinkaku/Make_picture/__Controllable__contours_image.jpg', contours_image)


# NK_gray = cv2.cvtColor(NK_image, cv2.COLOR_BGR2GRAY)
# print('SET')
# answer = SET_list(NK_gray,guide=True,keep_start=1,keeplen=3)
# print('write')
# with open("/Users/matsuurakenshin/WorkSpace/development/txtreader/txtreader3_rinkaku/Make_txtfile/NK_image.txt","w") as f:
#     for line in answer:
#         f.write(f"{line}")
print('END')
# #---------------------------------
# answer = SET_list(image,guide=True,keep_start=1,keeplen=3)

# with open("/Users/matsuurakenshin/WorkSpace/development/txtreader/txtreader3_rinkaku/Make_txtfile/now_image.txt","w") as f:
#     for line in answer:
#         f.write(f"{line}")

# answer = SET_list(now_binary,guide=True,keep_start=1,keeplen=3)

# with open("/Users/matsuurakenshin/WorkSpace/development/txtreader/txtreader3_rinkaku/Make_txtfile/now_binary.txt","w") as f:
#     for line in answer:
#         f.write(f"{line}")k
# #---------------------------------



#--------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
"""

# imagenum = 0

# image_print   = 0
# square_print  = 1
# atan2_print   = 1
# math_print    = 1
# atan22_print  = 1
# square2_print = 1
# contours_image = Make_ContoursImage(image_print,atan2_print,square_print,math_print,atan22_print,square2_print,atan2_guide,square_guide,mathme,NEW_atan2_guide,NEW_guide)
# cv2.imwrite(f'/Users/matsuurakenshin/WorkSpace/development/txtreader/txtreader3_rinkaku/Make_picture/contours_image_{imagenum}.jpg', contours_image)
# imagenum+= 1

# image_print   = 0
# square_print  = 0
# atan2_print   = 1
# math_print    = 0
# atan22_print  = 1
# square2_print = 1
# contours_image = Make_ContoursImage(image_print,atan2_print,square_print,math_print,atan22_print,square2_print,atan2_guide,square_guide,mathme,NEW_atan2_guide,NEW_guide)
# cv2.imwrite(f'/Users/matsuurakenshin/WorkSpace/development/txtreader/txtreader3_rinkaku/Make_picture/contours_image_{imagenum}.jpg', contours_image)
# imagenum+= 1

# image_print   = 1
# square_print  = 0
# atan2_print   = 0
# math_print    = 0
# atan22_print  = 1
# square2_print = 1
# contours_image = Make_ContoursImage(image_print,atan2_print,square_print,math_print,atan22_print,square2_print,atan2_guide,square_guide,mathme,NEW_atan2_guide,NEW_guide)
# cv2.imwrite(f'/Users/matsuurakenshin/WorkSpace/development/txtreader/txtreader3_rinkaku/Make_picture/contours_image_{imagenum}.jpg', contours_image)
# imagenum+= 1

# image_print   = 1
# square_print  = 1
# atan2_print   = 0
# math_print    = 0
# atan22_print  = 1
# square2_print = 1
# contours_image = Make_ContoursImage(image_print,atan2_print,square_print,math_print,atan22_print,square2_print,atan2_guide,square_guide,mathme,NEW_atan2_guide,NEW_guide)
# cv2.imwrite(f'/Users/matsuurakenshin/WorkSpace/development/txtreader/txtreader3_rinkaku/Make_picture/contours_image_{imagenum}.jpg', contours_image)
# imagenum+= 1

# image_print   = 1
# square_print  = 0
# atan2_print   = 1
# math_print    = 0
# atan22_print  = 1
# square2_print = 0
# contours_image = Make_ContoursImage(image_print,atan2_print,square_print,math_print,atan22_print,square2_print,atan2_guide,square_guide,mathme,NEW_atan2_guide,NEW_guide)
# cv2.imwrite(f'/Users/matsuurakenshin/WorkSpace/development/txtreader/txtreader3_rinkaku/Make_picture/contours_image_{imagenum}.jpg', contours_image)
# imagenum+= 1

# image_print   = 1
# square_print  = 1
# atan2_print   = 1
# math_print    = 0
# atan22_print  = 0
# square2_print = 0
# contours_image = Make_ContoursImage(image_print,atan2_print,square_print,math_print,atan22_print,square2_print,atan2_guide,square_guide,mathme,NEW_atan2_guide,NEW_guide)
# cv2.imwrite(f'/Users/matsuurakenshin/WorkSpace/development/txtreader/txtreader3_rinkaku/Make_picture/contours_image_{imagenum}.jpg', contours_image)
# imagenum+= 1

# image_print   = 1
# square_print  = 1
# atan2_print   = 1
# math_print    = 0
# atan22_print  = 0
# square2_print = 1
# contours_image = Make_ContoursImage(image_print,atan2_print,square_print,math_print,atan22_print,square2_print,atan2_guide,square_guide,mathme,NEW_atan2_guide,NEW_guide)
# cv2.imwrite(f'/Users/matsuurakenshin/WorkSpace/development/txtreader/txtreader3_rinkaku/Make_picture/contours_image_{imagenum}.jpg', contours_image)
# imagenum+= 1

# image_print   = 1
# square_print  = 1
# atan2_print   = 0
# math_print    = 0
# atan22_print  = 0
# square2_print = 1
# contours_image = Make_ContoursImage(image_print,atan2_print,square_print,math_print,atan22_print,square2_print,atan2_guide,square_guide,mathme,NEW_atan2_guide,NEW_guide)
# cv2.imwrite(f'/Users/matsuurakenshin/WorkSpace/development/txtreader/txtreader3_rinkaku/Make_picture/contours_image_{imagenum}.jpg', contours_image)
# imagenum+= 1

"""