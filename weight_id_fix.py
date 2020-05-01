import os
import os.path
import re
import itertools
from itertools import tee
import struct
import sys
import binascii
import shutil
import time
from operator import itemgetter

def replace_odd(l, v='xx'):
    return [v if not i%2 else x for i,x in enumerate(l)]

def bytes_to_int(bytes):
    result = 0
    for b in bytes:
        result = result * 256 + int(b)
    return result

os.chdir(sys.path[0])

weights_file = input("Enter Weight File: ")
model_file = input("Enter YOBJ File: ")

with open(os.path.join(os.path.dirname(__file__), weights_file), 'r') as f:             #gatherslinecount
    read_weights = f.read()
    nlines = read_weights.count('\n')
    # print(nlines)

fo = open(weights_file, "r")                                                            #printsline
file_read = fo.readlines()
curr_line = file_read[0]
print(curr_line)

with open(os.path.join(os.path.dirname(__file__), model_file), 'rb') as model:          #gathers model palette start
    model.seek(84)
    modelread = model.read(4)
    skin_palette_start = (bytes_to_int(modelread)) + 8
    skin_palette_data_start = (bytes_to_int(modelread)) + 16

    model.seek(skin_palette_start)
    modelread = model.read(4)
    skinbone_count = bytes_to_int(modelread)

    print(skin_palette_start)
    print(skinbone_count)

def id_replace():
    
    weight_bone_ID = curr_line.split()                                                      #gets id list
    weight_bone_ID2 = curr_line.split()                                                     
    weight_bone_ID = weight_bone_ID[::2]
    print()

    newlist = []

    for i in weight_bone_ID:
        i = int(i)
        new_bone_id_start = skin_palette_data_start + (i * 4)

        with open(os.path.join(os.path.dirname(__file__), model_file), 'rb') as model1:        
            model1.seek(new_bone_id_start)
            modelread1 = model1.read(4)
            new_bone_id = str(bytes_to_int(modelread1))
            newlist.append(new_bone_id)
        

    print(newlist)
    weight_bone_ID2 = weight_bone_ID2[1::2]
    print(weight_bone_ID2)

    newerlist = []

    for i,b in zip(newlist,weight_bone_ID2):
        newerlist.append(i)
        newerlist.append(b)

    print(newerlist)

    newerlist = " ".join(newerlist)
    newerlist = newerlist + " " + "\n"

    with open(("idfix_")+(weights_file), "a") as output:
        output.write(str(newerlist))

curr_line = file_read[0]
id_replace()
n = 0

for _ in itertools.repeat(None, nlines - 1):
    n = n + 1
    curr_line = file_read[n] 
    id_replace()

