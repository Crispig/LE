import os
import re
import random
from shutil import copyfile

raw_path="/home/inspur/Xu/ASC_DL/albert/ELE"

def Pasting(raw_path):

    dir=os.path.join(raw_path,"train")
    allfiles=os.listdir(dir)
    random.shuffle(allfiles)
    print(allfiles)
 
    cnt=0
    for file in allfiles:
        src=os.path.join(dir,file)
        # 
        dst=os.path.join(raw_path,"train5")
        dst="{}/{}".format(dst,file)
        if   cnt < 3500:
            copyfile(src,dst)
        cnt+=1

Pasting("/home/inspur/Xu/ASC_DL/albert/ELE")

dir=os.path.join(raw_path,"train5")
allfiles=os.listdir(dir)
print(len(allfiles))

