line = input()

sample = "abcdefghijklmnopqrstuvwxyz"
sample2 = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"

small_position = []

for txtline in range(len(line)):
  txt = line[txtline]
  for sampleline in range (len(sample)):
    sampletxt = sample[sampleline]
    if txt == sampletxt:
       small_position.append([txtline,sampleline])

oomoji = (len(line)-len(small_position))
if oomoji > len(line)-oomoji:
  set_sample = sample2
else:
  set_sample = sample

anser = []
for txt in line:
  anser.append(txt)

for linedata in small_position:
  anser[linedata[0]] = set_sample[linedata[1]]

anser2 = ""
for txt in anser:
  anser2 = anser2+txt
print(anser2)

  
         
