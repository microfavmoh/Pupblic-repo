import hashlib
import os
import time

directory=input("please enter the folder you want to delete the duplicates in")
hashes=set()
index=1
non_hashable_files=[]

for filename in os.listdir(directory):
    print(f"{index}-{filename}")
    index+=1
    try:
        path=os.path.join(directory, filename)
        digest=hashlib.sha512(open(path,'rb').read()).digest()
        if digest not in hashes:
            hashes.add(digest)
        else:
            os.remove(path)
    except Exception as e:
        non_hashable_files.append(filename)

if len(non_hashable_files)==0:
    print("the operation was completed sucessfuly")
    pass
else:
    time.sleep(2)
    print("folders that may still contain duplicates:")
    time.sleep(2)
    for index_list in range(len(non_hashable_files)):
        print(non_hashable_files[index_list])
        time.sleep(1)