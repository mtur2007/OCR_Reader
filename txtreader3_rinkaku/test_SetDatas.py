
from SET_datas import SET_list as SET_list



samplelist =  [
                [1000,[[1111]],1000,1000,[1111]],
                [2000,2000,2000,2000,[2222,2222],2000],
                [3000,3000,3000,3000,[3333,[3333,3333],3333,3333],3000],
                [4000,4000,4000,4000]
               ]
              
'''
samplelist =  [
                [1000,[[1111]],1000,1000,[1111]],
                [2000,2000,2000,2000,[2222,2222],2000],
                [3000,3000,3000,3000,[3333,[3333,3333],3333,3333],3000],
                [4000,4000,4000,4000]
               ]
'''              



answer = SET_list(samplelist,guide=True,keep_start=1,keeplen=3)

with open("/Users/matsuurakenshin/WorkSpace/development/txtreader/txtreader3_rinkaku/Make_txtfile/test_SET.txt","w") as f:
    for line in answer:
        f.write(f"{line}")
