import numpy as np
import time
from SET_datas import SET_list_noset as SET_list

from A__removal        import image_removal_background
from B__search_rinkaku import search_Allrinkaku
from C__sort_rinkaku   import search_rinkaku

import pickle

#-----------------------------------------------------------------------------------------------------------

imagename = "/Users/matsuurakenshin/WorkSpace/development/txtreader/picture_file/newsample.jpeg"

dataslist = image_removal_background(imagename,'auto',160)

code0list_str = np.array(dataslist["code0list"],dtype=str)
where0 = np.where(code0list_str == '0')
code0list_str[:,:] = ' '
code0list_str[where0] = '0'


answer = SET_list([code0list_str],guide=True,keep_start=1,keeplen=10)

with open("/Users/matsuurakenshin/WorkSpace/development/txtreader/txtreader3_rinkaku/Make_txtfile/code0list.txt","w") as f:
    for line in answer:
        f.write(f"{line}")

#-----------------------------------------------------------------------------------------------------------


start = time.time()

imagedata = dataslist['code0list']
rinkaku,rinkaku_image = search_Allrinkaku(imagedata)

finish = time.time()
print('[search rinkaku] time :' + str(finish-start))

answer = SET_list([rinkaku_image],guide=True,keep_start=1,keeplen=10)

with open("/Users/matsuurakenshin/WorkSpace/development/txtreader/txtreader3_rinkaku/Make_txtfile/rinkaku_image.txt","w") as f:
    for line in answer:
        f.write(f"{line}")
#sample = np.where(dataslist["code0list"] == 0)

# ### pickleで保存（書き出し）
# with open('data.pickle', mode='wb') as fo:
#   pickle.dump([rinnkaku_X,rinnkaku_Y], fo)


#-----------------------------------------------------------------------------------------------------------
code0list = dataslist['code0list']
index0_y,index0_x = np.where(code0list == 0)
print(index0_y[0],index0_x[0])
search_rinkaku(code0list,[9,14])

"""
with open("Remake_SET.txt","w") as f:
    for line in anser:
        f.write(f"{line}")
"""
"""
# 結果を表示
cv2.imshow('Green My Characters', printimage)
cv2.waitKey(0)
cv2.destroyAllWindows()
"""