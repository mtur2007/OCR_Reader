import time
from SET_datas import SET_list

a = [[0,3],[0,0],[2],[3],[4],[2,0]]
print(sorted(a))

a = [[[0,0,0,1,0,0,0,[10,10,[100,100],10],0],[0,0,0,0,[0,0,0,0],0,0,0,0],[0,0,0,0,0,0,0,0,0]]],[[[0,0,0,11,0,10,0],[0,0,0,111,0,0,0]]],[[[0,0,0,1,0,0,0],[0,0,0,1,0,0,0]]]


start = time.time()

set_border_list = SET_list(a,guide=True,keep_start=2,keeplen=10)

finish = time.time()
print(f'time: {finish - start}')


with open("Remake_SET.txt","w") as f:
    for line in set_border_list:
        f.write(f"{line}")

print(type([]))