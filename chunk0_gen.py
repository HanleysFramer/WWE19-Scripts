import os
import os.path
import re
import itertools
from itertools import tee
import struct
import sys
import binascii
from operator import itemgetter

os.chdir(sys.path[0])

input_file = "chunk_extract.bin"

arch_1 = "chunk_1.temp"
arch_2 = "chunk_2.temp"
arch_3 = "chunk_3.temp"
arch_4 = "chunk_4.temp"

byte_pad     = b'\x00'
byte_block   = b'\x00\x00\x00\x00'*8 
part_header  = b'\x04\x02\x00\x08'
def_header   = b'\x04\x02\x00\x00'
byte_block_2 = b'\xFF\xFF\xFF\xFF'

chunk_2_buffer = b'\xDA\x07\x00\x00'

def int_to_bytes_LE(input):
    input = struct.pack('<I', input)
    return input

def swap32(x):
    x = struct.unpack('<L', x)
    x = int(''.join(map(str, x))) 
    return x

def bytes_to_int(bytes):
    result = 0
    for b in bytes:
        result = result * 256 + int(b)
    return result

def find_chunk_1_id(bytes_input):
    id_block = bytes_input[12:]
    id_block = swap32(id_block)
    # id_int = bytes_to_int(id_block)
    return id_block

def find_chunk_2_id(bytes_input):
    id_block = bytes_input[4:]
    id_block = swap32(id_block)
    # id_int = bytes_to_int(id_block)
    return id_block

def split(word): 
    return [bytes for bytes in word]  

###dump chunk parts

with open(os.path.join(os.path.dirname(__file__), input_file), 'rb') as chunk_bin:
    content   = chunk_bin.read()
    block_end = content.index(byte_block)

    #########chunk_1
    chunk_bin.seek(8)                                                                        
    chunk_1   = chunk_bin.read(block_end - 8) 
    with open(os.path.join(os.path.dirname(__file__), ("chunk_1.temp")), 'wb') as chunk_part1:
        chunk_part1.write(chunk_1)

    #########chunk_2
    chunk_bin.seek(block_end)
    content   = chunk_bin.read()  
    new_start = (content.index(part_header))  +  block_end  + 4                               
    chunk_bin.seek(new_start)
    content   = chunk_bin.read()
    block_end = content.index(byte_block)
    chunk_bin.seek(new_start)                                                                
    chunk_2   = chunk_bin.read(block_end) 
    with open(os.path.join(os.path.dirname(__file__), ("chunk_2.temp")), 'wb') as chunk_part2:
        chunk_part2.write(chunk_2)

    #########chunk_3
    chunk_bin.seek(block_end + new_start)
    content   = chunk_bin.read()  
    new_start = (content.index(part_header))  +  block_end + new_start + 4                              
    chunk_bin.seek(new_start)
    content   = chunk_bin.read()
    block_end = content.index(byte_block)
    chunk_bin.seek(new_start)                                                                 
    chunk_2   = chunk_bin.read(block_end) 
    with open(os.path.join(os.path.dirname(__file__), ("chunk_3.temp")), 'wb') as chunk_part2: 
        chunk_part2.write(chunk_2)
        chunk_part2.write(byte_pad)

    #########chunk_4
    chunk_bin.seek(block_end + new_start)
    content   = chunk_bin.read()  
    new_start = (content.index(def_header))  +  block_end + new_start + 4                                
    chunk_bin.seek(new_start)
    content   = chunk_bin.read()
    block_end = content.index(byte_block)
    chunk_bin.seek(new_start)                                                                 
    chunk_2   = chunk_bin.read(block_end) 
    with open(os.path.join(os.path.dirname(__file__), ("chunk_4.temp")), 'wb') as chunk_part2: 
        chunk_part2.write(chunk_2)

##################sort chunk 1
with open(os.path.join(os.path.dirname(__file__), arch_1), 'rb') as f:

    object_count = os.path.getsize(os.path.join(os.path.dirname(__file__), arch_1)) / 20
    object_count = int(object_count)
    print("chunks in 1: ", (object_count))
    chunk_1_count = object_count

    curr_file = f.read()
    # f.seek(489520)
    # test = f.read(16)
    # print(find_chunk_1_id(test))

    i = 0
    part_list = []
    index_list= []

    for _ in itertools.repeat(None, object_count):
        i = i + 1
        f.seek(((i - 1) * 20))
        curr_block = f.read(20)
        a = curr_block[:16]
        a = find_chunk_1_id(a)

        part_list.append(curr_block)
        index_list.append(a)

    sort_list = list(zip(*sorted(zip(index_list,part_list))))[1]

    with open(os.path.join(os.path.dirname(__file__), "chunk_1_sort.bin"), 'wb') as f1:
        sort_list = b''.join(sort_list)
        f1.write(sort_list)
    
    with open(os.path.join(os.path.dirname(__file__), "chunk_1_sort.bin"), 'r+b') as f1:

        i = 0

        for _ in itertools.repeat(None, object_count):
            i = i + 1
            f1.seek(16  + (20 * (i - 1)))
            f1.write(byte_block_2)

##################sort chunk 2 (might not have to do this one)
with open(os.path.join(os.path.dirname(__file__), arch_2), 'rb') as f:

    object_count = os.path.getsize(os.path.join(os.path.dirname(__file__), arch_2)) / 12
    object_count = int(object_count)
    print("chunks in 2: ", (object_count))
    chunk_2_count = object_count

    curr_file = f.read()

    i = 0
    part_list = []
    index_list= []

    for _ in itertools.repeat(None, object_count):
        i = i + 1
        f.seek(((i - 1) * 12))
        curr_block = f.read(12)
        a = curr_block[:8]
        a = find_chunk_2_id(a)

        part_list.append(curr_block)
        index_list.append(a)

    sort_list = list(zip(*sorted(zip(index_list,part_list))))[1]

    with open(os.path.join(os.path.dirname(__file__), "chunk_2_sort.bin"), 'wb') as f1:
        sort_list = b''.join(sort_list)
        f1.write(sort_list)


    ##replaces chunk 2 block footer

    with open(os.path.join(os.path.dirname(__file__), "chunk_2_sort.bin"), 'r+b') as f1:

        i = 0

        for _ in itertools.repeat(None, object_count):
            i = i + 1
            f1.seek(((i - 1) * 12) + 8)
            f1.write(chunk_2_buffer)

##################format chunk 3
with open(os.path.join(os.path.dirname(__file__), arch_3), 'rb') as f:

    object_count = (os.path.getsize(os.path.join(os.path.dirname(__file__), arch_3)) - 12) / 12
    object_count = int(object_count)
    print("chunks in 3: ", (object_count))
    chunk_3_count = object_count + 1

    contentnew = f.read()
    ## contentnew = contentnew[12:] ##uncertain might be essential

    with open(os.path.join(os.path.dirname(__file__), "chunk_3_sort.bin"), 'wb') as f1:
        f1.write(contentnew)

##################format chunk 4
with open(os.path.join(os.path.dirname(__file__), arch_4), 'rb') as f:
    content = f.read()
    n = content
    n = split(n)
    count = n.count(0) + 1

    with open(os.path.join(os.path.dirname(__file__), "chunk_4_sort.bin"), 'wb') as f1:
        f1.write(content)

    chunk_4_count = count
    print("chunks in 4: ", count)

with open(os.path.join(os.path.dirname(__file__), arch_4), 'r') as f:
    content = f.read()
    n = content
    count = n.count('ResourceSync')

    rs_count = count

if rs_count > 0:
    
    print('\n \nThis chunk is corrupt.')
    print("RS Files found. RS file count: ", count)

    with open(os.path.join(os.path.dirname(__file__), "chunk_1_sort.bin"), 'rb') as f:
        a = f.read()
        a = a[: os.path.getsize(os.path.join(os.path.dirname(__file__), 'chunk_1_sort.bin')) - 2040]
    with open(os.path.join(os.path.dirname(__file__), "chunk_1_sort.bin"), 'wb') as f:
        f.write(a)

    with open(os.path.join(os.path.dirname(__file__), "chunk_2_sort.bin"), 'rb') as f:
        a = f.read()
        a = a[: os.path.getsize(os.path.join(os.path.dirname(__file__), 'chunk_2_sort.bin')) - 1044]
    with open(os.path.join(os.path.dirname(__file__), "chunk_2_sort.bin"), 'wb') as f:
        f.write(a)

    with open(os.path.join(os.path.dirname(__file__), "chunk_3_sort.bin"), 'rb') as f:
        a = f.read()
        a = a[: os.path.getsize(os.path.join(os.path.dirname(__file__), 'chunk_3_sort.bin')) - 1464]
    with open(os.path.join(os.path.dirname(__file__), "chunk_3_sort.bin"), 'wb') as f:
        f.write(a)

    with open(os.path.join(os.path.dirname(__file__), "chunk_4_sort.bin"), 'rb') as f:
        a = f.read()
        a = a[: os.path.getsize(os.path.join(os.path.dirname(__file__), 'chunk_4_sort.bin')) - 7001]
    with open(os.path.join(os.path.dirname(__file__), "chunk_4_sort.bin"), 'wb') as f:
        f.write(a)

chunk_header = b'\x41\x52\x43\x48\xDA\x07\x00\x00\x2C\x00\x00\x00\x2C\x00\x00\x00'

with open(os.path.join(os.path.dirname(__file__), 'Chunk0.arc'), 'wb') as c:
    c.write(chunk_header)
    c1_size0 = os.path.getsize(os.path.join(os.path.dirname(__file__), 'chunk_1_sort.bin'))
    c2_size0 = os.path.getsize(os.path.join(os.path.dirname(__file__), 'chunk_2_sort.bin'))
    c3_size0 = os.path.getsize(os.path.join(os.path.dirname(__file__), 'chunk_3_sort.bin'))
    c4_size0 = os.path.getsize(os.path.join(os.path.dirname(__file__), 'chunk_4_sort.bin'))
    c1_size = int_to_bytes_LE(c1_size0)
    c2_size = int_to_bytes_LE(c2_size0)
    c3_size = int_to_bytes_LE(c3_size0)
    c4_size = int_to_bytes_LE(c4_size0)

    c.write(c1_size)
    a = int_to_bytes_LE(44 + c1_size0)
    c.write(a)

    c.write(c2_size)
    a = int_to_bytes_LE(44 + c2_size0 + c1_size0)
    c.write(a)

    c.write(c3_size)
    a = int_to_bytes_LE(44 + c3_size0 + c2_size0 + c1_size0)
    c.write(a)
    c.write(c4_size)

    with open(os.path.join(os.path.dirname(__file__), 'chunk_1_sort.bin'), 'rb') as d:
        read_buffer = d.read()
        c.write(read_buffer)
    with open(os.path.join(os.path.dirname(__file__), 'chunk_2_sort.bin'), 'rb') as d:
        read_buffer = d.read()
        c.write(read_buffer)
    with open(os.path.join(os.path.dirname(__file__), 'chunk_3_sort.bin'), 'rb') as d:
        read_buffer = d.read()
        c.write(read_buffer)
    with open(os.path.join(os.path.dirname(__file__), 'chunk_4_sort.bin'), 'rb') as d:
        read_buffer = d.read()
        c.write(read_buffer)
        c.write(b'\x00'* 159)

os.remove('chunk_1_sort.bin')
os.remove('chunk_2_sort.bin')
os.remove('chunk_3_sort.bin')
os.remove('chunk_4_sort.bin')
os.remove('chunk_1.temp')
os.remove('chunk_2.temp')
os.remove('chunk_3.temp')
os.remove('chunk_4.temp')
os.remove(input_file)

print("Chunk gen'd successfully.")