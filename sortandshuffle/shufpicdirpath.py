import random

oldfilenames = 'filenames.txt'
newfilenames = 'randompic.txt'
of_dir = open(oldfilenames,'r')
nf_dir = open(newfilenames,'a')


with of_dir as f:
    arr = f.readlines()
    random.shuffle(arr)
    while arr:
        nf_dir.write(arr.pop())
    
    nf_dir.close() 
of_dir.close()

