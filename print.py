with open("/Users/matsuurakenshin/WorkSpace/development/txtreader/test.txt","r") as f:
    printtxt = "["
    for line in f:
        printtxt = printtxt + line
        printtxt = printtxt + " "
    
    printtxt = printtxt + "\n]"

print(printtxt)
