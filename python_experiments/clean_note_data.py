import re

fin = open("note_info.txt")
line = fin.readlines()
fin.close()

info = []

for l in line:
    info.append(re.split(r'\t', re.sub('(\n| )', '', l)))

print info

fout = open('note_info_clean.txt', 'w+')
for note in info:
    print note[0]
    fout.write(note[0] + ' ' + note[1] + ' ' + note[2] + '\n')
fout.close()