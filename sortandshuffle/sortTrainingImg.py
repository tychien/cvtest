import os, random 


def add_root(root,filename):
    while names:
        current_names=root+'/'+filename.pop()
        new_names.append(current_names)
    return new_names


#####os.walk###############

dirPath = '/home/tychien/Desktop/Original photo'
filenames = 'filenames.txt'
f_dir = open(filenames, 'a')

files = os.walk(dirPath)
#random.shuffle(files)

for root, dirs, files in os.walk('/home/tychien/Desktop/Original photo'):
    print(root)
#    print(dirs)
    print(files)
    new_names = []
    names = files 
    new_names = add_root(root,names)
    print(new_names)
    while new_names:
        f_dir.write(new_names.pop()+'\n')
f_dir.close()


