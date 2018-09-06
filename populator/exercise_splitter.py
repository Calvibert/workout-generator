# Upper-lower splitter for the exercise list

import sys
import exercise_populator_config as conf

print('Enter the file name: ')
filename = sys.stdin.readline()
filename = filename[0:len(filename)-1]

f = open(filename, 'r')
upper = conf.CONST_MUSCLES['upper']
lower = conf.CONST_MUSCLES['lower']

uex = []
lex = []

for ex in f:
    i = ex.find(',')
    t = ex[i+2:].rstrip()
    
    if t in upper:
        uex.append(ex.rstrip())
        continue
    lex.append(ex.rstrip())


upper_filename = 'upper.txt'
lower_filename = 'lower.txt'
o_stdout = sys.stdout
f = open(upper_filename, 'w+')
sys.stdout = f

for i in uex:
    print(i)

f.close()
f = open(lower_filename, 'w+')
sys.stdout = f

for i in lex:
    print(i)

sys.stdout = o_stdout
f.close()
