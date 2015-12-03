import matplotlib.pyplot as plt
import math
import re

fin = open("note_info_clean.txt")
line = fin.readlines()
fin.close()

info = []
raw_freqs = []

# reads note info from textfile to info list 
# for every list in the list: 0 - name of note, 1 - freq, 2 - wave length
for i, l in enumerate(line):
    info.append(re.split(' ', re.sub('\n', '', l)))
    raw_freqs.append(info[i][1])

# calculate factor used to produce note frequencies
a = math.pow(2, float(1)/12)
split_factor = math.pow(2, float(1)/24)

freqs = [float(raw_freqs[0])] # holds frequencies for notes
splits = [float(raw_freqs[0]) * split_factor] # separations for different notes

for i in range(len(raw_freqs) - 1):
    freqs.append(freqs[i] * a)
    splits.append(splits[i] * a)

# add lower and upper boundaries
splits = [splits[0] / a] + splits + [splits[-1] * a]