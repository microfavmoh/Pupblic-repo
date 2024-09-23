import hashlib
import os
import time
from tkinter.filedialog import askdirectory

directory=askdirectory()
hashes=set()
non_hashable_files=[]

def dup_remover(directory):
    for filename in os.listdir(directory):
        path=os.path.join(directory, filename)
        try:
            hash=hashlib.sha512(open(path,'rb').read()).digest()
            if hash not in hashes:
                hashes.append(hash)
            else:
                os.remove(path)
        except Exception as e:
            non_hashable_files.append(filename)
        if os.path.isdir(path):
            dup_remover(path)

    if len(non_hashable_files)==0:
        print("the operation was completed sucessfuly")
        pass
    else:
        time.sleep(2)
        print("files that may still be duplicates:")
        time.sleep(2)
        for index_list in range(len(non_hashable_files)):
            print(non_hashable_files[index_list])
            time.sleep(1)

while not directory:
    directory=askdirectory()
else:
    dup_remover(directory)     