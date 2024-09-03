import numpy as np
import pickle
import math
import cv2
import matplotlib.pyplot as plt

from SET_datas import SET_list

from pynput import keyboard


def search_anser_contours(contours,square_size):
    contours = np.array(contours) * square_size

    squareY = []
    squareX = []
    guideY = []
    guideX = []
    for linenum in range(np.shape(contours)[0]):

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

### pickleで保存したファイルを読み込み
with open('/Users/matsuurakenshin/WorkSpace/development/txtreader/txtreader3_rinkaku/pickle_file/TEST_rinkaku.pickle', mode='br') as fi:
    image,contours,now_binary = pickle.load(fi)

Back_Color = [0,0,0]
Square_Color = np.array((0,255,0))
Guide_Colror = [0,0,255]
mathme_Color = [100,30,30]

square_size = 15
frame = 3
image=cv2.resize(image,None,fx=square_size,fy=square_size,interpolation=cv2.INTER_NEAREST)

center = square_size//2 + square_size%2

maxnum = np.amax(contours,axis=0)+1

height = square_size*maxnum[0]
width  = square_size*maxnum[1]


square = np.tile(1, square_size**2).reshape((square_size,square_size))
square[frame:square_size-frame,frame:square_size-frame] = 0

square = np.where(square == 1)


square_guide,atan2_guide = search_anser_contours(contours,square_size)


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
        
            insert_index = index1
            #内側と外側はベクトルが反転する為、同条件のifの結果が異なることで判別し、内側と外側に沿って加工することができる。
            if (d[0] == 1) and (d[1] == 1):
                insert_index = index0
            if (d[0] == -1) and (d[1] == -1):
                insert_index = index0
            NEW_contours[-1] = insert_index
        else:
            insert_index = index0

            if (d[0] == 1) and (d[1] == 1):
                insert_index = index1
            if (d[0] == -1) and (d[1] == -1):
                insert_index = index1
            NEW_contours[-1] = insert_index



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
            insert_index = index0
            if (d2[0] > 0) and (d2[1] > 0):
                insert_index = index1
            if (d2[0] < 0) and (d2[1] < 0):
                insert_index = index1
        else:
            insert_index = index1
            if (d2[0] > 0) and (d2[1] > 0):
                insert_index = index0
            if (d2[0] < 0) and (d2[1] < 0):
                insert_index = index0
        
        NEW_contours[-1] = insert_index

        # d3 = index1 - contours[linenum-3]
        # if (abs(d3[0]) - abs(d3[1])) == 0:
        #     #NEW_contours[-2] = contours[linenum-3]
        #     NEW_contours[-1] = index1
        # else:
        #     direction = contours[linenum-2] - contours[linenum-3]
        #     if str(abs(direction)) == str(abs(d)):
        #         print(abs(direction),abs(d))
        #         if (direction == [0,1]).all() or (direction == [-1,0]).all():
        #             NEW_contours[-1] = index1
    else:
        NEW_contours.append(index1)


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

NEW_guide,NEW_atan2_guide = search_anser_contours(NEW_contours,square_size)



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


contours_image = image.copy()
Black_image = np.zeros((height, width, 3))
#Black_image += #[255,255,255]


image_print   = True
square_print  = False
atan2_print   = False
math_print    = False
square2_print = False
atan22_print  = False

print('[:] ximage')
print('[.] contours')
print('[/] guide')
print('[#] boarder')

print('{_} break')


def Make_ContoursImage(image_print,atan2_print,square_print,math_print,atan22_print,square2_print,image,atan2_guide,square_guide,mathme,NEW_atan2_guide,NEW_guide):
    contours_image = image.copy()

    if image_print == True:
        Square_Color = [0,0,255]
        Square2_Color =[255,0,0]
        Guide_Colror = [0,0,200]
        Guide2_Colror =[0,200,0]
        mathme_Color = [80,10,10]
    else:
        contours_image[:,:] = Back_Color.copy()
        #contours_image = Black_image
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

    global image_print,square_print,atan2_print,math_print,square2_print,atan22_print,image,atan2_guide,square_guide,mathme,NEW_atan2_guide,NEW_guide
    
    try:
        if key.char == '.':  #'輪郭の表示'
            square_print = not square_print

        elif key.char == '/': #'角度の表示'
            atan2_print = not atan2_print
        
        elif key.char == '3': #'3[#の代用](マス目の表示))_'
            math_print = not math_print

        elif key.char == '@': #'*(元の情報の表示)'
            image_print = not image_print
        
        elif key.char == ';':
            square2_print = not square2_print
        elif key.char == ':':
            atan22_print = not atan22_print
        pass
        
            
        contours_image = Make_ContoursImage(image_print,atan2_print,square_print,math_print,atan22_print,square2_print,image,atan2_guide,square_guide,mathme,NEW_atan2_guide,NEW_guide)
        cv2.imwrite('/Users/matsuurakenshin/WorkSpace/development/txtreader/txtreader3_rinkaku/Make_picture/__Controllable__contours_image.jpg', contours_image)
    
    except AttributeError:

        if key == keyboard.Key.esc:
            # ESC キーが押された場合に終了
            return False
        pass

contours_image = Make_ContoursImage(image_print,atan2_print,square_print,math_print,atan22_print,square2_print,image,atan2_guide,square_guide,mathme,NEW_atan2_guide,NEW_guide)
cv2.imwrite('/Users/matsuurakenshin/WorkSpace/development/txtreader/txtreader3_rinkaku/Make_picture/__Controllable__contours_image.jpg', contours_image)
    
# キーボードのリスナーを開始
with keyboard.Listener(on_press=on_press) as listener:
    listener.join()

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


contours_image = Make_ContoursImage(image_print,atan2_print,square_print,math_print,atan22_print,square2_print,image,atan2_guide,square_guide,mathme,NEW_atan2_guide,NEW_guide)
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

with open('/Users/matsuurakenshin/WorkSpace/development/txtreader/txtreader3_rinkaku/pickle_file/NEW_contours.picke',mode='wb') as fo:
    pickle.dump(NEW_contours, fo)


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