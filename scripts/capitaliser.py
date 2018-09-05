# Capitalize a file.
# Used for our exercises.

import sys


print('Enter the file name: ')
filename = sys.stdin.readline()
filename = filename[0:len(filename)-1]

f = open(filename, 'r')

exl = []

for ex in f:
    count = 0
    space = True
    l = list(ex)
    for i in l:
        if space:
            l[count] = i.upper()
            space = False
        if i == ' ':
            space = True
        count = count+1
        
    exl.append("".join(l).rstrip())


print(exl)
output_filename = 'sorted-' + filename
o_stdout = sys.stdout
f = open(output_filename, 'w')
sys.stdout = f

for i in exl:
    print(i)

sys.stdout = o_stdout
f.close()
