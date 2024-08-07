
"""
輪郭関連 [ 輪郭検出 / 輪郭右回りソート ] のファイル
"""

import time
import math
import numpy as np


#輪郭でまとめる処理---------------------------------------------------------------------------------------------------------------------
"""
斜辺の長さから近いものを調べ、まとめる 
"""

def search_rinkaku(code0list,start_position):

  start = time.time()
  now_t_Y = start_position[0]
  now_t_X = start_position[1]

  search_area = code0list[now_t_Y-1:now_t_Y+2,now_t_X-1:now_t_X+2]
  if search_area[0,1] == 1:
    now_b_Y = now_t_Y-1
    now_b_X = now_t_X

  NG_data = (np.array((0,1,2,1)),np.array((1,2,1,0)))

  # code0list の座標から area への座標変換の仕方
  # area[y] = code0list[y] - (center_code0list[y] +1 )
  # area[x] = code0list[x] - (center_code0list[x] +1 )

  # area の座標から code0list への座標変換の仕方
  # code0list[y] = center_code0list[y) + (area[y] -1 )
  # code0list[x] = center_code0list[x] + (area[y] -1 )

  print()
  
  search_area = code0list[now_t_Y-1:now_t_Y+2,now_t_X-1:now_t_X+2]
  area0_index = np.where(search_area == 0) #del_senterのインデックス
  print(area0_index[0])
  print(np.shape(area0_index)[1])
  print(np.reshape(area0_index,(np.shape(area0_index)[1],2)))
  
  #previous

  print()
  # for i in range(1):
  #   search_area = code0list[now_t_Y-1:now_t_Y+2,now_t_X-1:now_t_X+2]
  #   area0_index = np.where(search_area[del_senter] == 0)[0] #del_senterのインデックス
  #   area0_index = (del_senter[0][area0_index],del_senter[1][area0_index])
  #   for y,x in zip(area0_index[0],area0_index[1]):
  #     print(y,x)
    

  finish = time.time()

  print()
  print(f'time: {finish-start}')
  print()
#一括でコメントする方法(cmd + /)


#輪郭でまとめる処理---------------------------------------------------------------------------------------------------------------------