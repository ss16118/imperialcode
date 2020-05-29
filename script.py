import os, sys
import re

path = 'static'

files = []
# r=root, d=directories, f = files
for r, d, f in os.walk(path):
    for file in f:
        if '.js' in file:
            files.append(os.path.join(r, file))


#print (len(files))

# for f in files:
#     file_opened = open(f,"rw")
#     content = file_opened.read()
#     n = re.sub("\".js\"",)


