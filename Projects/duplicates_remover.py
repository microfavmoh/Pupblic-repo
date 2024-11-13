from hashlib import sha256
from os import remove,listdir
from os.path import isdir,join
from tkinter.filedialog import askdirectory

hashes:set=set()

def dup_remover(directory):
    for filename in listdir(directory):
        path:str=join(directory, filename)
        if isdir(path):
            dup_remover(path)
            continue
        hash:str=sha256(open(path,'rb').read()).digest()
        if hash not in hashes:
            hashes.add(hash)
        else:
            remove(path)

directory:str=askdirectory()
if directory:
    dup_remover(directory)
print("the operation was completed sucessfuly")