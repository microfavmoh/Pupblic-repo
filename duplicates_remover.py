import hashlib
import os
import time
from tkinter.filedialog import askdirectory

directory=askdirectory()
hashes=set()
non_hashable_files=[]

def dup_remover(directory):
    global hashes
    for filename in os.listdir(directory):
        path=os.path.join(directory, filename)
        if os.path.isdir(path):
            dup_remover(path)
        hash=hashlib.sha512(open(path,'rb').read()).digest()
        if hash not in hashes:
            hashes.add(hash)
        else:
            os.remove(path)

    if not non_hashable_files:
        print("the operation was completed sucessfuly")
        pass
    else:
        time.sleep(2)
        print("files that may still be duplicates:")
        time.sleep(2)
        for file in non_hashable_files:
            print(file)
            time.sleep(1)

while not directory:
    directory=askdirectory()
dup_remover(directory)     