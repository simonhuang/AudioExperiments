import matplotlib.pyplot as plt
import math
import re

fin = open("note_info_clean.txt")
line = fin.readlines()
fin.close()

info = []
raw_freqs = []

for i, l in enumerate(line):
    info.append(re.split(' ', re.sub('\n', '', l)))
    raw_freqs.append(info[i][1])
    
a = math.pow(2, float(1)/12)
split_factor = math.pow(2, float(1)/24)

freqs = [float(raw_freqs[0])]
splits = [float(raw_freqs[0]) * split_factor]
for i in range(len(raw_freqs) - 1):
    freqs.append(freqs[i] * a)
    splits.append(splits[i] * a)
    
splits = [float(splits[0]) / a] + splits + [splits[-1] * a]
print len(splits)