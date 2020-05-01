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

def bytes_to_int(bytes):
    result = 0
    for b in bytes:
        result = result * 256 + int(b)
    return result

def swap_bytes(byte_input):
    byte_input = bytes_to_int((byte_input[::-1]))

    return byte_input

def write_anim(animation_0):

    with open(os.path.join(os.path.dirname(__file__), animation_0), 'rb') as anim:

        anim.seek(7)                                                              #get_file_size
        file_size = anim.read(1)

        if file_size == b'\x00':
            anim.seek(8)
            file_size = anim.read(3)
            file_size = swap_bytes(file_size)
            print()
            print("File Size:",file_size)

        else:
            anim.seek(7)
            file_size = anim.read(4)
            file_size = swap_bytes(file_size)
            print("File Size:", file_size)
        
        anim.seek(12)                                                              #get_blocks
        block_count = anim.read(1)
        block_count = bytes_to_int(block_count)
        print("Animation Blocks:",block_count)

        anim.seek(20)                                                              #get_id
        animation_id = anim.read(4)
        print("Animation ID:", bytes_to_int(animation_id))

    n = 0
    total = 0
    list2 = []

    def write_blocks():

        with open(os.path.join(os.path.dirname(__file__), animation_0), 'rb') as anim1:

            total = 0
            a = 0

            if n == 0 :
                a = 0

            if n > 0 :
                list1 = open("animation_list").readlines()

                for i in list1:
                    i     = int(i)
                    list2.append(i)

                for ele in range(0, len(list2)): 
                    ele = int(ele)
                    total = total + list2[ele]

                a = total

            anim1.seek(32 + a + 7)
            block_size = anim1.read(1)

            if block_size == b'\x00':
                anim1.seek(32 + a + 8)
                block_size = anim1.read(3)
                block_size = swap_bytes(block_size)
                print("Block Size:",block_size)

            else:
                anim1.seek(32 + a + 7)
                block_size = anim1.read(4)
                block_size = swap_bytes(block_size)
                print("Block Size:", block_size)
            
            anim1.seek(32 + a)
            block = anim1.read(block_size)

            if n == (block_count - 3):
                with open((str(z) + "_" + "data_list_block"), "wb") as output:
                    output.write(block)

            else:

                if n == (block_count - 2):
                    with open((str(z) + "_" + "col_list_block"), "wb") as output:
                        output.write(block)

                else:

                    if n == (block_count - 1):
                        with open((str(z) + "_" + "bone_list_block"), "wb") as output:
                            output.write(block)

                    else:
                        with open((str(z) + "_" + "animation_block" + str(n)), "wb") as output:
                            output.write(block)



            with open(("animation_list"), "w") as output1:
                block_size = str(block_size)
                block_0 = block_size + " " + "\n"
                output1.write(block_0)

    n = 0
    write_blocks()

    for _ in itertools.repeat(None, block_count - 1):
        n = n + 1
        write_blocks()

    os.remove("animation_list")
  
def int_to_bytes(value, length):
    result = []
    for i in range(0, length):
        result.append(value >> (i * 8) & 0xff)
    result.reverse()
    return result

os.chdir(sys.path[0])

merge_count = 2
animation_a = "hair_ycl.bin"
animation_b = "shoe_ycl.pac"

z = 0
write_anim(animation_a)

z = 1
write_anim(animation_b)

os.chdir(sys.path[0])


def get_data_list_blocks():

    with open(os.path.join(os.path.dirname(__file__), ((str(n)) + "_data_list_block")), 'rb') as data_block:  #segments_datalist

        header_data   = data_block.read(64)

        with open(((str(n)) + "_header_datal_block"), "wb") as output1:
            output1.write(header_data)

        data_block.seek(64)
        header_data_2 = data_block.read(32)

        with open(((str(n)) + "_header2_datal_block"), "wb") as output1:
            output1.write(header_data_2)

        with open(((str(n)) + "_header2_datal_block"), "rb") as output1:
            output1.seek(12)
            data_block_count = bytes_to_int((output1.read(1)))
            print(data_block_count)

        data_block.seek(96)
        header_data_3 = data_block.read(data_block_count * 112)

        with open(((str(n)) + "_header3_datal_block"), "wb") as output1:
            output1.write(header_data_3)



        data_block.seek(96 + (data_block_count * 112))
        header_data_4 = data_block.read(32)

        with open(((str(n)) + "_header4_datal_block"), "wb") as output1:
            output1.write(header_data_4)

        with open(((str(n)) + "_header4_datal_block"), "rb") as output1:
            output1.seek(12)
            data_block_count2 = bytes_to_int((output1.read(1)))
            print(data_block_count2)

        data_block.seek((96 + (data_block_count * 112)) + 32)
        header_data_5 = data_block.read(data_block_count2 * 96)

        with open(((str(n)) + "_header5_datal_block"), "wb") as output1:
            output1.write(header_data_5)

n = 0
get_data_list_blocks()

n = 1 
get_data_list_blocks()


with open((str(merge_count - 2) + "_header3_datal_block"), "rb") as output1:
    input_0 = output1.read()

with open((str(merge_count - 1) + "_header3_datal_block"), "rb") as output1:
    input_1 = output1.read()

with open(("merged_datablock3"), "ab") as output1:
    output1.write(input_0)
    output1.write(input_1)

a = os.path.getsize(os.path.join(os.path.dirname(__file__), "merged_datablock3"))

new_data3_size    = 32 + a
data3_block_count = int((a / 112))
new_data3_size    = new_data3_size.to_bytes(4, byteorder = 'little')
data3_block_count = bytes([data3_block_count])

with open(("0_header2_datal_block"), "r+b") as output1:
    output1.seek(12)
    output1.write(data3_block_count)
    output1.seek(8)
    output1.write(new_data3_size)

#---------------------------------------------------------------------header4

with open((str(merge_count - 2) + "_header5_datal_block"), "rb") as output1:
    input_0 = output1.read()

with open((str(merge_count - 1) + "_header5_datal_block"), "rb") as output1:
    input_1 = output1.read()

with open(("merged_datablock4"), "ab") as output1:
    output1.write(input_0)
    output1.write(input_1)

a = os.path.getsize(os.path.join(os.path.dirname(__file__), "merged_datablock4"))

new_data3_size    = 32 + a
data3_block_count = int((a / 96))
new_data3_size    = new_data3_size.to_bytes(4, byteorder = 'little')
data3_block_count = bytes([data3_block_count])

with open(("0_header4_datal_block"), "r+b") as output1:
    output1.seek(12)
    output1.write(data3_block_count)
    output1.seek(8)
    output1.write(new_data3_size)

my_dir = os.getcwd()

with open(("datablock"), "wb") as output1:

    with open(("0_header_datal_block"), "rb") as output2:
        file_0 = output2.read()
    with open(("0_header2_datal_block"), "rb") as output2:
        file_1 = output2.read()
    with open(("merged_datablock3"), "rb") as output2:
        file_2 = output2.read()
    with open(("0_header4_datal_block"), "rb") as output2:
        file_4 = output2.read()
    with open(("merged_datablock4"), "rb") as output2:
        file_5 = output2.read()
    with open(("0_data_list_block"), "rb") as output2:
        file_6 = output2.read()

    output1.write(file_0)
    output1.write(file_1)
    output1.write(file_2)
    output1.write(file_4)
    output1.write(file_5)
    output1.write(file_6)

with open(("datablock"), "r+b") as output1:
    a = os.path.getsize(os.path.join(os.path.dirname(__file__), "datablock"))
    a = a.to_bytes(4, byteorder = 'little')
    output1.seek(8)
    output1.write(a)

for fname in os.listdir(my_dir):
    if fname.endswith("datal_block"):
        os.remove(os.path.join(my_dir, fname))
    if fname.startswith("merged"):
        os.remove(os.path.join(my_dir, fname))


with open(("0_col_list_block"), "rb") as output2:
    header_block_col = output2.read(32)
    output2.seek(84)
    the_rest = output2.read()

    with open(("1_col_list_block"), "rb") as output2:
        output2.seek(32)
        header_block_col2 = output2.read(76)

    with open(("0_col_list_block"), "rb") as output2:
        output2.seek(32)
        header_block_col3 = output2.read(52)

    with open(("col_block"), "wb+") as output1:
        output1.write(header_block_col)
        output1.write(header_block_col3)
        output1.write(header_block_col2)
        output1.write(the_rest)

    with open(("col_block"), "r+b") as output1:
        output1.seek(12)
        count = output1.read(1)
        count = bytes_to_int(count)
        count = count + 3
        output1.seek(12)
        count = count.to_bytes(4, byteorder = 'little')
        output1.write(count)
        a = os.path.getsize(os.path.join(os.path.dirname(__file__), "col_block"))
        a = a.to_bytes(4, byteorder = 'little')
        output1.seek(8)
        output1.write(a)


with open(("0_bone_list_block"), "rb") as output2:
    boneheader = output2.read(32)
    output2.seek(12)
    bone_count = bytes_to_int(output2.read(1))
    output2.seek(32)
    bone_list_1 = output2.read()

    with open(("1_bone_list_block"), "rb") as output1:
        output1.seek(12)
        bone_count2 = bytes_to_int(output1.read(1))
        output1.seek(32)
        bone_list_2 = output1.read()
        new_bone_count = bone_count + bone_count2

    with open(("bonelistblock"), "wb") as output3:
        output3.write(boneheader)
        output3.write(bone_list_1)
        output3.write(bone_list_2)

    with open(("bonelistblock"), "r+b") as output3:
        a = os.path.getsize(os.path.join(os.path.dirname(__file__), "bonelistblock"))
        a = a.to_bytes(4, byteorder = 'little')
        new_bone_count = new_bone_count.to_bytes(4, byteorder = 'little')
        output3.seek(8)
        output3.write(a)
        output3.seek(12)
        output3.write(new_bone_count)
        output3.seek(16)
        output3.write(new_bone_count)


with open(("ycl_output"), "wb") as output1:

    with open((animation_a), "rb") as output:
        full_header = output.read(32)
    with open("0_animation_block0", "rb") as output:
        b = output.read()
    with open("1_animation_block0", "rb") as output:
        b0 = output.read()
    with open("1_animation_block1", "rb") as output:
        b1 = output.read()
    with open("0_animation_block1", "rb") as output:
        b2 = output.read()
    with open("datablock", "rb") as output:
        b3 = output.read()
    with open("col_block", "rb") as output:
        b4 = output.read()
    with open("bonelistblock", "rb") as output:
        b5 = output.read()
    
    output1.write(full_header)
    output1.write(b)
    output1.write(b0)
    output1.write(b1)
    output1.write(b2)
    output1.write(b3)
    output1.write(b4)
    output1.write(b5)

with open(("ycl_output"), "r+b") as output1:
    a = os.path.getsize(os.path.join(os.path.dirname(__file__), "ycl_output"))
    a = a.to_bytes(4, byteorder = 'little')
    output1.seek(8)
    output1.write(a)
    output1.seek(12)
    b = 7
    b = b.to_bytes(4, byteorder = 'little')
    output1.write(b)

for fname in os.listdir(my_dir):
    if fname.endswith("block"):
        os.remove(os.path.join(my_dir, fname))

for fname in os.listdir(my_dir):
    if fname.startswith("1_"):
        os.remove(os.path.join(my_dir, fname))
    if fname.startswith("0_"):
        os.remove(os.path.join(my_dir, fname))