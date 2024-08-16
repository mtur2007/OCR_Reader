
from SET_datas import SET_list as SET_list



samplelist = [
               [
                 [1000,['d',1111],1000,1000,[11111]],
                 [10000,100000,100000,100,[11111,11111],0],
                 [10000,100,1000,10,[11111,[22222,22222],11111,111111],100]
                ]
              ]




answer = SET_list(samplelist,guide=True,keep_start=1,keeplen=3)

with open("/Users/matsuurakenshin/WorkSpace/development/txtreader/txtreader3_rinkaku/Make_txtfile/test_SET.txt","w") as f:
    for line in answer:
        f.write(f"{line}")
