
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

  only_data = [np.array((-1,0,1,0)),np.array((0,1,0,-1))]

  # code0list の座標から area への座標変換の仕方
  # area[y] = (code0list[y] - center_code0list[y]) +1 
  # area[x] = (code0list[x] - center_code0list[x]) +1 

  # area の座標から code0list への座標変換の仕方
  # code0list[y] = center_code0list[y) + (area[y] -1 )
  # code0list[x] = center_code0list[x] + (area[y] -1 )

  print()
  
  #サーチエリアを作り、0の場所を取得する。
  search_area = code0list[now_t_Y-1:now_t_Y+2,now_t_X-1:now_t_X+2]
  area0_index = np.where(search_area == 0) #del_senterのインデックス
  
  min_diff = 3
  count = []

  for ty,tx in zip(area0_index[0],area0_index[1]):

    #(1,1)は現在位置なので除外
    if ty != 1 or tx != 1:

      # 検出した近隣の0 を エリア_インデックス から 元リスト_インデックス へ変換し, エリア外の輪郭の候補の座標を取得する。
      # - 近隣0 のインデックス変換
      choiceTY_change = now_t_Y + (ty -1)
      choiceTX_change = now_t_X + (tx -1)
        
      rinkaku_choice = only_data.copy()
      rinkaku_choice[0] = rinkaku_choice[0] + choiceTY_change
      rinkaku_choice[1] = rinkaku_choice[1] + choiceTX_change
      #                   ^    候補範囲    ^  
    
      #取得した座標の候補位置に 1(背景判定)があるインデックスを取得し、現在の輪郭との差分を取得。
      rinkaku_x = np.where(code0list[rinkaku_choice[0],rinkaku_choice[1]] == 1)
      rinkaku_y = rinkaku_choice[0][rinkaku_x]
      rinkaku_x = rinkaku_choice[1][rinkaku_x]

      rinkaku_y -= now_b_Y
      rinkaku_x -= now_b_X


      #現在の輪郭と輪郭の候補位置の斜辺が最小だったものを調べる。
      for by,bx in zip(rinkaku_y,rinkaku_x):
        diff = math.sqrt(by**2 + bx**2)

        if diff <= min_diff:
          choiceRY_change = by+now_b_Y
          choiceRX_change = bx+now_b_X

          if diff == min_diff:
            #2回目以降
            count.append([[choiceTY_change, choiceTX_change],[choiceRY_change, choiceRX_change]])
          else:
            #新しいデータ
            count = [[[choiceTY_change, choiceTX_change],[choiceRY_change, choiceRX_change]]]
            min_diff = diff
  
  for index in count:
    if now_b_X > index[1][1]:
      print(now_t_Y,index[0][0])
      previous_t = [index[0][0] - now_t_Y +1, index[0][1] - now_t_X +1]
      previous_b = index[1]

  print()
  print(min_diff)
  print(count)
  print('previous_t: ',previous_t)

  print(now_t_Y,now_t_X)
  print(now_b_Y,now_b_X)
  

  print()

  for i in range(10):

    #サーチエリアを作り、0の場所を取得する。
    search_area = code0list[now_t_Y-1:now_t_Y+2,now_t_X-1:now_t_X+2]
    area0_index = np.where(search_area == 0) #del_senterのインデックス
    
    min_diff = 3
    count = []

    for ty,tx in zip(area0_index[0],area0_index[1]):

      #(1,1)は現在位置なので除外
      if (ty != 1 or tx != 1) and (ty != previous_t[0] or tx != previous_t[1]):

        # 検出した近隣の0 を エリア_インデックス から 元リスト_インデックス へ変換し, エリア外の輪郭の候補の座標を取得する。
        # - 近隣0 のインデックス変換
        choiceTY_change = now_t_Y + (ty -1)
        choiceTX_change = now_t_X + (tx -1)

        #print(f'search_index: {choiceTY_change,choiceTX_change}')
          
        rinkaku_choice = only_data.copy()
        rinkaku_choice[0] = rinkaku_choice[0] + choiceTY_change
        rinkaku_choice[1] = rinkaku_choice[1] + choiceTX_change
        #                   ^    候補範囲    ^  
      
        #取得した座標の候補位置に 1(背景判定)があるインデックスを取得し、現在の輪郭との差分を取得。
        rinkaku_x = np.where(code0list[rinkaku_choice[0],rinkaku_choice[1]] == 1)
        rinkaku_y = rinkaku_choice[0][rinkaku_x]
        rinkaku_x = rinkaku_choice[1][rinkaku_x]

        print(rinkaku_y,now_b_Y)
        print(rinkaku_x,now_b_X)
        rinkaku_y -= now_b_Y
        rinkaku_x -= now_b_X

        #現在の輪郭と輪郭の候補位置の斜辺が最小だったものを調べる。
        for by,bx in zip(rinkaku_y,rinkaku_x):
          diff = math.sqrt(by**2 + bx**2)
          print(diff,by,bx)

          if diff <= min_diff:
            choiceRY_change = by+now_b_Y
            choiceRX_change = bx+now_b_X

            if diff == min_diff:
              #2回目以降
              count.append([[choiceTY_change, choiceTX_change],[choiceRY_change, choiceRX_change]])
            else:
              #新しいデータ
              count = [[[choiceTY_change, choiceTX_change],[choiceRY_change, choiceRX_change]]]
              min_diff = diff

    if len(count) == 1:
      previous_t = (now_t_Y,now_t_X)
      previous_b = (now_b_Y,now_b_X)

      count = count[0]

      now_t_Y,now_t_X = count[0][0],count[0][1]
      now_b_Y,now_b_X = count[1][0],count[1][1]

      previous_t = (1+(previous_t[0] - now_t_Y),1+(previous_t[1] - now_t_X))

      now_t_X - (previous_t[1] +1)

      print()
      print(min_diff)
      print(now_t_Y,now_t_X)
      print('-'*60)
      
  finish = time.time()

  print()
  print(f'time: {finish-start}')
  print()
#一括でコメントする方法(cmd + /)


#輪郭でまとめる処理---------------------------------------------------------------------------------------------------------------------