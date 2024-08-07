import numpy as np

#============================================

def search_Allrinkaku(imagedata):

    #0の文字判定をまとめたリストを作成
    where_0_Y, where_0_X = np.where( imagedata == 0)
    code0list = imagedata

    rinnkaku_Y = []
    rinnkaku_X = []

    #輪郭検出

    NG_data = (np.array((0,1,2,1)),np.array((1,2,1,0)))
    NG_data_y = np.array((0,1,2,1))
    NG_data_x = np.array((1,2,1,0))
    '''
    NG_data は 輪郭を正確に検出する為 文字判定と背景判定のベクトルが１以内に文字判定があるかを調査する為の配列

     index(1)  |   __NG__   : 周りに1があるだけだと
    [[0,1,0],  | [[0,0,1],  : 0の半径1に 1(文字判定)
     [1,0,1],  |  [0,#,0],  : があるかないかで判別。
     [0,1,0] ] |  [0,0,0] ] : 
    '''

    #y軸を順に調べていく
    for i in range(np.shape(where_0_Y)[0]):

        now0_Y = where_0_Y[i]
        now0_X = where_0_X[i]
        area = code0list[now0_Y-1:now0_Y+2, now0_X-1:now0_X+2]
        if np.count_nonzero(area[NG_data] == 1) > 0: #0の周りに1 (背景判定: 位置はNG_data) があるかで検出

            # where_1_x = np.where(area[NG_data] == 1)[0]
            # where_1_y,where_1_x = NG_data_y[where_1_x],NG_data_x[where_1_x]

            # rinnkaku_y = now0_Y + (where_1_y - 1)
            # rinnkaku_x = now0_X + (where_1_x - 1)

            # rinnkaku_Y[len(rinnkaku_Y):len(rinnkaku_Y)] = rinnkaku_y.tolist()
            # rinnkaku_X[len(rinnkaku_X):len(rinnkaku_X)] = rinnkaku_x.tolist()

            rinnkaku_Y.append(now0_Y)
            rinnkaku_X.append(now0_X)

    #輪郭をまとめる
    rinkaku = (rinnkaku_Y,rinnkaku_X)

    #結果を視覚的に表す (SET_list_noset関数を使って表示すると視覚的に輪郭がどうのように検出されたかが分かる)
    rinkaku_image = np.ones(code0list.shape,str)
    rinkaku_image[:,:] = ' '
    rinkaku_image[rinkaku] = 0

    return rinkaku,rinkaku_image


'''
printimage = dataslist["image"]
print(printimage[0,0])

print(rinkaku[0])
printimage[rinkaku] = (255, 0, 0)
    
end = time.time()  

time_diff = end - start  # 処理完了後の時刻から処理開始前の時刻を減算する
print(f"\ntime: {time_diff}")  # 処理にかかった時間データを使用

# 結果を表示
cv2.imshow('Green My Characters', printimage)
cv2.waitKey(0)
cv2.destroyAllWindows()
'''