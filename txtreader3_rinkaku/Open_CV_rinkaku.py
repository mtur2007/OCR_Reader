#解説1
import cv2
import numpy as np
import matplotlib.pyplot as plt
import pickle

from SET_datas import SET_list

#解説2
# サンプル画像
image_name = '/Users/matsuurakenshin/WorkSpace/development/txtreader/picture_file/OpenCV_image.png'
# 画像読み込む
img = cv2.imread(image_name)

#解説3
# グレースケールに変換
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
# 二値化（閾値を150に設定）
ret, binary = cv2.threshold(gray, 150, 255, cv2.THRESH_BINARY)
# answer = SET_list(binary,guide=True,keep_start=1,keeplen=3)

# with open("/Users/matsuurakenshin/WorkSpace/development/txtreader/txtreader3_rinkaku/Make_txtfile/binary.txt","w") as f:
#     for line in answer:
#         f.write(f"{line}")

#解説4
# 輪郭を検出
contours, hierarchy = cv2.findContours(binary, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

#解説5
# 全て白の画像を作成
img_blank = np.ones_like(img) * 255
# 輪郭だけを描画（黒色で描画）
#img_contour_only = cv2.drawContours(img_blank, contours, -1, (0,0,0), 3)

def remake_contours(contours):
    global img
    minnum = np.amin(contours,axis=0)
    maxnum = np.amax(contours,axis=0)
    image = img[minnum[1]:maxnum[1]+1,minnum[0]:maxnum[0]+1]
    now_binary = binary[minnum[1]:maxnum[1]+1,minnum[0]:maxnum[0]+1]


    # answer = SET_list(image,guide=True,keep_start=1,keeplen=3)

    # with open("/Users/matsuurakenshin/WorkSpace/development/txtreader/txtreader3_rinkaku/Make_txtfile/binary.txt","w") as f:
    #     for line in answer:
    #         f.write(f"{line}")


    contours[:,0] = contours[:,0] - minnum[0]
    contours[:,1] = contours[:,1] - minnum[1]

    maxnum = np.amax(contours,axis=0)
    maxnum = maxnum + 1
    testaria = np.zeros(maxnum,dtype=str)
    testaria[:,:] = ' '

    rangenum = len(contours)
    for i in range(rangenum):
        nowindex = contours[i]
        if i == rangenum-1:
            testaria[nowindex[0],nowindex[1]] = '#'
        else:
            testaria[nowindex[0],nowindex[1]] = str(i)[-1]

    with open('/Users/matsuurakenshin/WorkSpace/development/txtreader/txtreader3_rinkaku/Make_txtfile/rinkaku_test.txt','w') as f:
        for line in testaria:
            printline = ''
            for txt in line:
                printline += txt + ' '
            f.write(printline+'\n')
    ### pickleで保存（書き出し）
    #image = cv2.rotate(image, cv2.ROTATE_90_COUNTERCLOCKWISE)
    #image = cv2.rotate(image, cv2.ROTATE_90_CLOCKWISE)

    #image = cv2.flip(image, 1)

    contours_copy = contours.copy()
    contours[:,1] = contours_copy[:,0]
    contours[:,0] = contours_copy[:,1]

    return image,now_binary,contours

# (e: 3[4]),(C: 5)
pick_contours = [contours[3][:,0],contours[5][:,0]]
search_contours_list = []
for contours in pick_contours:
    image,now_binary,contours = remake_contours(contours)
    search_contours_list.append([image,now_binary,contours])

with open('/Users/matsuurakenshin/WorkSpace/development/txtreader/txtreader3_rinkaku/pickle_file/TEST_rinkaku.pickle', mode='wb') as fo:
    pickle.dump(search_contours_list, fo)


