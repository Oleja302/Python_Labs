import os
import hashlib
import itertools

dirs = os.walk("directory2")
hashNameFiles = [[None]]

for dir, folders, files in dirs:
    for i in range(0, len(files)):
        hash = hashlib.md5(str(files[i]).encode())
        hashNameFiles.append([hash.hexdigest(), files[i]])

for i in range(0, len(hashNameFiles)):
    if list(itertools.chain.from_iterable(hashNameFiles)).count(hashNameFiles[i][0]) > 1:
        print(hashNameFiles[i][1])
