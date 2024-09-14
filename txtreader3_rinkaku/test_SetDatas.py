
from SET_datas import SET_list
import numpy as np


samplelist =  [
                ['00','01','02','03','04'],
                ['10','11','12','13'],
                ['20','21','22','23','24','25'],
                ['30','31','32']
               ]

# samplelist =  [
#                 ['00',['010','011',['0120','0121'],'013'],'02','03','04'],
#                 ['10','11','12',['130','131']],
#                 ['20',['210','211',[['21200'],['21210','21211']]],'22','23','24','25'],
#                 ['30','31','32']
#                ]


answer = SET_list(samplelist,guide=True,keep_start=1,keeplen=20)

with open("/Users/matsuurakenshin/WorkSpace/development/txtreader/txtreader3_rinkaku/Make_txtfile/test_SET.txt","w") as f:
    for line in answer:
        f.write(f"{line}")

