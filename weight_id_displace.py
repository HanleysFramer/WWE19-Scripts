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

weights_file  = input("Enter Weights File: ")
displace      = input("Enter Displacements: ") 
displace      = int(displace)

with open(os.path.join(os.path.dirname(__file__), weights_file), 'r') as f:            
    read_weights = f.read()
    nlines = read_weights.count('\n')

    print("Model vertices:", nlines)

    fo = open(weights_file, "r")                                                          
    file_read = fo.readlines()

    def write_paletted_weights(curr_line):
        weight_bone_ID = curr_line.split()     
        weight_bone_ID2 = weight_bone_ID[::2]
        weight_bone_ID3 = weight_bone_ID[1::2]

        newlist  = []
        newerlist= []

        for i in weight_bone_ID2:
            i = int(i) + displace
            i = str(i)
            newlist.append(i)
        
        for i,b in zip(newlist,weight_bone_ID3):
            newerlist.append(i)
            newerlist.append(b)
        
        newerlist = " ".join(newerlist)
        newerlist = newerlist + " " + "\n"
        
        with open(("displaced_")+(weights_file), "a") as output:
            output.write(str(newerlist))


curr_line = file_read[0]
n = 0
write_paletted_weights(curr_line)

for _ in itertools.repeat(None, nlines - 1):
    n = n + 1
    curr_line = file_read[n] 
    write_paletted_weights(curr_line)

input("Displaced All Weights. Press enter to exit, fucker." )