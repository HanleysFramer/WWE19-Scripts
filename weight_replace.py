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

weights_file  = input("Enter Weight File: ")

def operation():
        
    swap_file1    = input("Enter Original Value: ")
    swap_file2    = input("Enter New Value: ")

    with open(os.path.join(os.path.dirname(__file__), weights_file), 'r') as f:            
        read_weights = f.read()
        nlines = read_weights.count('\n')

    fo = open(weights_file, "r")                                                          
    file_read = fo.readlines()

    file1_boneid = swap_file1
    file2_boneid = swap_file2

    def id_swap():
        weight_bone_ID = curr_line.split()     
        weight_bone_ID2 = weight_bone_ID[::2]

        affected_bones = [file1_boneid,file2_boneid]

        for item in affected_bones:
            if item in weight_bone_ID2:
                if file1_boneid in weight_bone_ID2:
                    for n, i in enumerate(weight_bone_ID2):
                        if i == file1_boneid:
                            weight_bone_ID2[n] = file2_boneid

        weight_bone_ID3 = weight_bone_ID[1::2]


        newerlist = []

        for i,b in zip(weight_bone_ID2,weight_bone_ID3):
            newerlist.append(i)
            newerlist.append(b)

        print(weight_bone_ID)
        print(newerlist)


        newerlist = " ".join(newerlist)
        newerlist = newerlist + " " + "\n"

        with open(("r_")+(weights_file), "a") as output:
            output.write(str(newerlist))

    curr_line = file_read[0]
    id_swap()
    n = 0

    for _ in itertools.repeat(None, nlines - 1):
        n = n + 1
        curr_line = file_read[n] 
        id_swap()

operation()

print()
print("Operation Complete.")
op_ivy = input("Run again?(y/n): ")

if op_ivy == "y":
    weights_file = ("r_")+(weights_file)
    operation()
else:
    input("\nID's replaced. Press enter to exit.")
