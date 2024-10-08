from hashlib import sha256
import os
from tkinter.filedialog import askdirectory

hashes:set=set()

def dup_remover(directory):
    for filename in os.listdir(directory):
        path:str=os.path.join(directory, filename)
        if os.path.isdir(path):
            dup_remover(path)
            continue
        hash=sha256(open(path,'rb').read()).digest()
        if hash not in hashes:
            hashes.add(hash)
        else:
            os.remove(path)

directory:str=askdirectory()
if directory:
    dup_remover(directory)
print("the operation was completed sucessfuly")     