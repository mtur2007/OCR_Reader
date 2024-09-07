import time

testlist = []

for i in range(100000):
    testlist.append(0)


indexnum = 0
start = time.time()
testlist[indexnum]
testlist[indexnum]
finish = time.time()

print(f'[0] time:',finish - start)
print()

indexnum = 10000
start = time.time()
testlist[indexnum]
testlist[indexnum]
finish = time.time()

print(f'[{indexnum}] time:',finish - start)