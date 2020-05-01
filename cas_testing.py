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

os.chdir(sys.path[0])

def bytes_to_int(bytes):
    result = 0
    for b in bytes:
        result = result * 256 + int(b)
    return result

def int_to_bytes(value, length):
    result = []
    for i in range(0, length):
        result.append(value >> (i * 8) & 0xff)
    result.reverse()
    return result

data = open('0000.bin' , errors='ignore').read()

shape_count = os.path.getsize(os.path.join(os.path.dirname(__file__), "shape.pac")) / 32 
model_count = data.count('subobj')

with open(os.path.join(os.path.dirname(__file__), "shape.pac"), 'r') as shape:                  
    model_ID = shape.read(16) , '.yobj'
    model_ID = str(model_ID)
    model_ID = model_ID.replace("\\","")
    model_ID = model_ID.replace("x","")
    model_ID = model_ID.replace("00","")
    model_ID = model_ID.replace("(","")
    model_ID = model_ID.replace(")","")
    model_ID = model_ID.replace(" ","")
    model_ID = model_ID.replace("\'","")
    model_ID = model_ID.replace("\"","")
    model_ID = model_ID.replace(",","")
    
ExportModel = open(model_ID, "w+")
byte_block = b'\xFF\xFF\xFF\xFF'*20
byte_block2= b'\x00\x00\x00\x00'*2

print('Current Model:' , model_ID)
print('')


subobj_current = ''.join(("subobj" , ".pac"))
subobj         = ''.join(("subobj" , "1" , ".pac"))

def yobj_header():
    with open(os.path.join(os.path.dirname(__file__), model_ID), 'ab') as f1:
        pad = b'\x00\x00\x00\x00'*21
        f1.write('JBOY'.encode())
        f1.write(pad)

def currentmodel():
    print(subobj)

def model_writeinfo():
    a = get_mdl_infoheader() 
    with open(os.path.join(os.path.dirname(__file__), ''.join((model_ID , '.headers'))), 'ab') as f0: 
        f0.write(a)
    currentmodel()

def get_mdl_infoheader():
    with open(os.path.join(os.path.dirname(__file__), subobj), 'rb') as modelread:
        model_info = modelread.read(184)
        return model_info

def header_block():
    model_begin = 0
    with open(os.path.join(os.path.dirname(__file__), ''.join((model_ID , '.headers'))), 'r+b') as f0:
        f0.seek(12,0)
        f0.write(byte_block)
        f0.seek(0,0)
        for _ in itertools.repeat(None, int(model_count - 1)):
            model_begin = 0
            model_begin = model_begin + 184
            write_begin = model_begin + 12
            f0.seek(write_begin, 0)
            f0.write(byte_block)

def update_offset_0():
    with open(os.path.join(os.path.dirname(__file__), subobj_current), 'rb') as subread:
        readstart = 104

        subread.seek(readstart,0)
        vertice_start = bytes_to_int(subread.read(4)) + readstart

        subread.seek(readstart + 4,0)
        weight_start  = bytes_to_int(subread.read(4)) + readstart + 4

        subread.seek(readstart + 8,0)
        uv_start      = bytes_to_int(subread.read(4)) + readstart + 8

        subread.seek(readstart + 12,0)
        normals_start = bytes_to_int(subread.read(4)) + readstart + 12

        subread.seek(readstart + 44,0)
        parameter_count= bytes_to_int(subread.read(4))
        
        subread.seek(readstart + 48,0)
        shader_offset  = bytes_to_int(subread.read(4)) + readstart + 48
        subread.seek(readstart + 48,0)
        shader_start   = bytes_to_int(subread.read(4)) + readstart + 48

        subread.seek(readstart + 52,0)
        face_start    = bytes_to_int(subread.read(4)) + readstart + 52

        subread.seek(0,0)
        vertice_count = bytes_to_int(subread.read(4))
        vertice_count = vertice_count

        def parameter_update():
            with open(os.path.join(os.path.dirname(__file__), subobj_current), 'r+b') as prm_read:
                prm_read.seek(shader_start,0)
                prm_off = bytes_to_int(prm_read.read(4)) + shader_start
                prm_off = struct.pack(">I", prm_off)
                prm_read.seek(shader_start,0)
                prm_read.write(prm_off)
        
        parameter_update()
        
        for _ in itertools.repeat(None, int(parameter_count - 1)):                                          
            shader_start = shader_start + 4
            parameter_update()
        
        with open(os.path.join(os.path.dirname(__file__), subobj_current), 'r+b') as prm_read0:             
            shader_offset = struct.pack(">I", shader_offset)
            prm_read0.seek(readstart + 48 , 0)
            prm_read0.write(shader_offset)

        with open(os.path.join(os.path.dirname(__file__), subobj_current), 'r+b') as prm_read0:             
            vertice_start = struct.pack(">I", vertice_start)
            prm_read0.seek(readstart , 0)
            prm_read0.write(vertice_start)

        with open(os.path.join(os.path.dirname(__file__), subobj_current), 'r+b') as prm_read0:             
            weight_start = struct.pack(">I", weight_start)
            prm_read0.seek(readstart + 4, 0)
            prm_read0.write(weight_start)
        
        with open(os.path.join(os.path.dirname(__file__), subobj_current), 'r+b') as prm_read0:             
            uv_start = struct.pack(">I", uv_start)
            prm_read0.seek(readstart + 8, 0)
            prm_read0.write(uv_start)
        
        with open(os.path.join(os.path.dirname(__file__), subobj_current), 'r+b') as prm_read0:             
            normals_start = struct.pack(">I", normals_start)
            prm_read0.seek(readstart + 12, 0)
            prm_read0.write(normals_start)

        with open(os.path.join(os.path.dirname(__file__), subobj_current), 'r+b') as prm_read0:             
            face_start = struct.pack(">I", face_start)
            prm_read0.seek(readstart + 52, 0)
            prm_read0.write(face_start)

        with open(os.path.join(os.path.dirname(__file__), subobj_current), 'r+b') as prm_read0:             
            prm_read0.seek(0, 0)
            prm_read0.seek(readstart + 52, 0)
            subface_start = bytes_to_int(prm_read0.read(4)) + 12
            prm_read0.seek(0, 0)
            prm_read0.seek(readstart + 52, 0)
            subheader = bytes_to_int(prm_read0.read(4)) + 8
            prm_read0.seek(0, 0)
            prm_read0.seek(subheader, 0)
            subface_start = struct.pack(">I", subface_start)
            prm_read0.write(subface_start)
            
update_offset_0()

print()

yobj_header()

with open(os.path.join(os.path.dirname(__file__), "subobj.pac"), 'rb') as f:                               
    readsubmodel = f.read()

    shit = 1
    subobj = ''.join(("subobj" , ".pac"))
    model_writeinfo()
    subobj = ''.join(("subobj" , "1" , ".pac"))

    for _ in itertools.repeat(None, int(model_count-1)):
        shit = shit + 1
        shit = eval(str(shit))
        subobj          = ''.join(("subobj" , str(shit) , ".pac"))
        subobj_current  = ''.join(("subobj" , str(shit) , ".pac"))
        update_offset_0()
        model_writeinfo()
    

    print('\nModel Count:' , int(model_count))

header_block()

def delete_subobj_headers():
    with open(os.path.join(os.path.dirname(__file__), subobj_current), 'rb') as in_file:
        with open(''.join((model_ID , '.headerless')), 'ab') as out_file:
            out_file.write(in_file.read()[184:])

subobj_current = ''.join(("subobj" , ".pac"))
delete_subobj_headers()
shit = 1

for _ in itertools.repeat(None, int(model_count-1)):                                                    
        shit = shit + 1
        shit = eval(str(shit))
        subobj          = ''.join(("subobj" , str(shit) , ".pac"))
        subobj_current  = ''.join(("subobj" , str(shit) , ".pac"))
        delete_subobj_headers()

with open(''.join((model_ID , '.headers')), 'rb') as in_file:
    with open(os.path.join(os.path.dirname(__file__), model_ID), 'ab') as out_file:
        out_file.write(in_file.read())

with open(''.join((model_ID , '.headerless')), 'rb') as in_file:                                        
    with open(os.path.join(os.path.dirname(__file__), model_ID), 'ab') as out_file:
        out_file.write(in_file.read())

os.remove(''.join((model_ID , '.headers')))
os.remove(''.join((model_ID , '.headerless')))



shit2 = 0

def update_offset_1():

    yobj_start = 88 + (shit2 * 184) + 104

    with open(os.path.join(os.path.dirname(__file__), model_ID), 'rb') as f:                                
        f.seek(yobj_start , 0)
        vertice_start = bytes_to_int(f.read(4)) + ((model_count - 1) * 184) + 88 - 8 + model_size
        vertice_start = struct.pack(">I", int(vertice_start))
        with open(os.path.join(os.path.dirname(__file__), model_ID), 'r+b') as f:  
            f.seek(0,0)
            f.seek(yobj_start,0)
            f.write(vertice_start)

    with open(os.path.join(os.path.dirname(__file__), model_ID), 'rb') as f:           
        f.seek(0 , 0)
        f.seek(yobj_start + 4 , 0)
        weight_start = bytes_to_int(f.read(4)) + ((model_count - 1) * 184) + 88 - 8 + model_size
        weight_start = struct.pack(">I", int(weight_start))
        with open(os.path.join(os.path.dirname(__file__), model_ID), 'r+b') as f:  
            f.seek(0,0)
            f.seek(yobj_start + 4,0)
            f.write(weight_start)

    with open(os.path.join(os.path.dirname(__file__), model_ID), 'rb') as f:  
        f.seek(0 , 0)
        f.seek(yobj_start + 8 , 0)
        uv_start = bytes_to_int(f.read(4)) + ((model_count - 1) * 184) + 88 - 8 + model_size
        uv_start = struct.pack(">I", int(uv_start))
        with open(os.path.join(os.path.dirname(__file__), model_ID), 'r+b') as f: 
            f.seek(0,0)
            f.seek(yobj_start + 8,0)
            f.write(uv_start)

    with open(os.path.join(os.path.dirname(__file__), model_ID), 'rb') as f:
        f.seek(0 , 0)
        f.seek(yobj_start + 12 , 0)
        normals_start = bytes_to_int(f.read(4)) + ((model_count - 1) * 184) + 88 - 8 + model_size
        normals_start = struct.pack(">I", int(normals_start)) 
        with open(os.path.join(os.path.dirname(__file__), model_ID), 'r+b') as f: 
            f.seek(0,0)
            f.seek(yobj_start + 12,0)
            f.write(normals_start)

    with open(os.path.join(os.path.dirname(__file__), model_ID), 'rb') as f:
        f.seek(0 , 0)
        f.seek(yobj_start + 48 , 0)
        shader_start = bytes_to_int(f.read(4)) + ((model_count - 1) * 184) + 88 - 8 + model_size
        shader_start = struct.pack(">I", int(shader_start))
        with open(os.path.join(os.path.dirname(__file__), model_ID), 'r+b') as f:
            f.seek(0,0)
            f.seek(yobj_start + 48,0)
            f.write(shader_start)

    with open(os.path.join(os.path.dirname(__file__), model_ID), 'rb') as f:
        f.seek(0 , 0)
        f.seek(yobj_start + 52 , 0)
        face_start = bytes_to_int(f.read(4)) + ((model_count - 1) * 184) + 88 - 8 + model_size
        face_start = struct.pack(">I", int(face_start))
        with open(os.path.join(os.path.dirname(__file__), model_ID), 'r+b') as f:
            f.seek(0,0)
            f.seek(yobj_start + 52,0)
            f.write(face_start)

    vertice_start     = (bytes_to_int(vertice_start)) + 8
    sub_vertice_start = vertice_start - 4

    face_start        = (bytes_to_int(face_start)) + 16
    sub_face_start    = face_start - 4

    with open(os.path.join(os.path.dirname(__file__), model_ID), 'r+b') as f:  
        sub_vertice_start = struct.pack(">I", int(sub_vertice_start))
        f.seek(0,0)
        f.seek(vertice_start, 0)
        f.write(sub_vertice_start)
    
    with open(os.path.join(os.path.dirname(__file__), model_ID), 'r+b') as f:  
        sub_face_start = struct.pack(">I", int(sub_face_start))
        f.seek(0,0)
        f.seek(face_start, 0)
        f.write(sub_face_start)

    with open(os.path.join(os.path.dirname(__file__), model_ID), 'rb') as f:
        f.seek(0 , 0)
        f.seek(yobj_start + 48 , 0)
        parameter_off = bytes_to_int(f.read(4)) + 8
    
    with open(os.path.join(os.path.dirname(__file__), model_ID), 'rb') as f:
        f.seek(0 , 0)
        f.seek(yobj_start + 44 , 0)
        parameter_count = bytes_to_int(f.read(4))

    yobj_start = 192 * shit

    def parameter_update_0():
        with open(os.path.join(os.path.dirname(__file__), model_ID), 'r+b') as f:
            f.seek(parameter_off,0)
            parameter_ind = bytes_to_int(f.read(4)) + ((model_count - 1) * 184) + 88 - 8 + model_size
            parameter_ind = struct.pack(">I", int(parameter_ind))
            f.seek(parameter_off,0)
            f.write(parameter_ind)

    parameter_update_0()


    for _ in itertools.repeat(None, int(parameter_count - 1)):                                          
        parameter_off = parameter_off + 4
        parameter_update_0()


shit2 = 0
model_size  = 0
update_offset_1()

count = model_count

if count > 1:
    shit2 = 1
    subobj_current = ''.join(("subobj" , ".pac"))
    model_size  =  os.path.getsize(os.path.join(os.path.dirname(__file__), subobj_current))
    model_count = model_count - 1
    update_offset_1()

if count > 2:

    shit2 = 2
    subobj         = ''.join(("subobj" , "2" , ".pac"))
    subobj_current = ''.join(("subobj" , ".pac"))
    model_size  =  model_size + os.path.getsize(os.path.join(os.path.dirname(__file__), subobj)) + 184
    model_count =  model_count - 2
    update_offset_1()

if count > 3:

    shit2 = 3
    subobj         = ''.join(("subobj" , "3" , ".pac"))
    model_size  =  model_size + os.path.getsize(os.path.join(os.path.dirname(__file__), subobj)) + 184 + 184
    model_count =  model_count - 3
    update_offset_1()

if count > 4:

    shit2 = 4
    subobj         = ''.join(("subobj" , "4" , ".pac"))
    model_size  =  model_size + os.path.getsize(os.path.join(os.path.dirname(__file__), subobj)) + 184 + 184 + 184
    model_count =  model_count - 4
    update_offset_1()

if count > 5:

    shit2 = 5
    subobj         = ''.join(("subobj" , "5" , ".pac"))
    model_size  =  model_size + os.path.getsize(os.path.join(os.path.dirname(__file__), subobj)) + 184 + 184 + 184 + 184
    model_count =  model_count - 5
    update_offset_1()

if count > 6:

    shit2 = 6
    subobj         = ''.join(("subobj" , "6" , ".pac"))
    model_size  =  model_size + os.path.getsize(os.path.join(os.path.dirname(__file__), subobj)) + 184 + 184 + 184 + 184 + 184
    model_count =  model_count - 6
    update_offset_1()

if count > 7:

    shit2 = 7
    subobj         = ''.join(("subobj" , "7" , ".pac"))
    model_size  =  model_size + os.path.getsize(os.path.join(os.path.dirname(__file__), subobj)) + 184 + 184 + 184 + 184 + 184 + 184
    model_count =  model_count - 7
    update_offset_1()
    
if count > 8:

    shit2 = 8
    subobj         = ''.join(("subobj" , "8" , ".pac"))
    model_size  =  model_size + os.path.getsize(os.path.join(os.path.dirname(__file__), subobj)) + 184 + 184 + 184 + 184 + 184 + 184 + 184
    model_count =  model_count - 8
    update_offset_1()
    
if count > 9:

    shit2 = 9
    subobj         = ''.join(("subobj" , "9" , ".pac"))
    model_size  =  model_size + os.path.getsize(os.path.join(os.path.dirname(__file__), subobj)) + 184 + 184 + 184 + 184 + 184 + 184 + 184 + 184
    model_count =  model_count - 9
    update_offset_1()
    
with open(os.path.join(os.path.dirname(__file__), model_ID), 'r+b') as f1:
    data = open('0000.bin' , errors='ignore').read()
    model_count = data.count('subobj')
    
    input_model_count = struct.pack(">I", model_count)
    f1.seek(0 , 0)
    f1.seek(24 , 0)
    f1.write(input_model_count)
    f1.seek(52 , 0)
    f1.write(input_model_count)

ysize = os.path.getsize(os.path.join(os.path.dirname(__file__), model_ID)) - 8
ysize = struct.pack(">I", ysize)

with open(os.path.join(os.path.dirname(__file__), "bones.pac"), 'rb') as in_file:                                         
    bone_read = os.path.getsize(os.path.join(os.path.dirname(__file__), "bones.pac")) - 16
    with open(os.path.join(os.path.dirname(__file__), model_ID), 'ab') as out_file:
        out_file.write(in_file.read(bone_read))

fsize0 = os.path.getsize(os.path.join(os.path.dirname(__file__), model_ID)) - 8
fsize0 = struct.pack(">I", fsize0)

with open(os.path.join(os.path.dirname(__file__), "tex_name.pac"), 'rb') as in_file:                                      
    bone_read = os.path.getsize(os.path.join(os.path.dirname(__file__), "tex_name.pac"))
    with open(os.path.join(os.path.dirname(__file__), model_ID), 'ab') as out_file:
        out_file.write(in_file.read(bone_read))

fsize1 = os.path.getsize(os.path.join(os.path.dirname(__file__), model_ID)) - 8
fsize1 = struct.pack(">I", fsize1)

with open(os.path.join(os.path.dirname(__file__), "shape.pac"), 'rb') as in_file:                                         
    bone_read = os.path.getsize(os.path.join(os.path.dirname(__file__), "shape.pac"))
    with open(os.path.join(os.path.dirname(__file__), model_ID), 'ab') as out_file:
        out_file.write(in_file.read(bone_read))

fsize2 = os.path.getsize(os.path.join(os.path.dirname(__file__), model_ID)) - 8
fsize2 = struct.pack(">I", fsize2)

fsize3 = os.path.getsize(os.path.join(os.path.dirname(__file__), model_ID))

with open(os.path.join(os.path.dirname(__file__), "skin_bone_palette.pac"), 'rb') as in_file:                             
    bone_read = os.path.getsize(os.path.join(os.path.dirname(__file__), "skin_bone_palette.pac"))
    with open(os.path.join(os.path.dirname(__file__), model_ID), 'ab') as out_file:
        out_file.write(in_file.read(bone_read))

filesize  = os.path.getsize(os.path.join(os.path.dirname(__file__), model_ID)) - 8
filesize  = struct.pack(">I", filesize)
bonecount = (os.path.getsize(os.path.join(os.path.dirname(__file__), "bones.pac")) - 16) / 80
bonecount = int(bonecount)
bonecount = (os.path.getsize(os.path.join(os.path.dirname(__file__), "bones.pac")) - 16) / 80
bonecount = int(bonecount)
bonecount = struct.pack(">I", bonecount)
texcount  = (os.path.getsize(os.path.join(os.path.dirname(__file__), "tex_name.pac")) / 16)
texcount = int(texcount)
texcount = struct.pack(">I", texcount)

with open(os.path.join(os.path.dirname(__file__), model_ID), 'r+b') as f:                                                  
    f.seek(0,0)
    f.seek(4,0)
    f.write(filesize)
    f.seek(8,0)
    f.write(b'\x00\x00\x00\x10')
    f.seek(12,0)
    f.write(filesize)
    f.seek(16,0)
    f.write(b'\x00\x00\x00\x07')
    f.seek(28,0)
    f.write(b'\x00\x00\x00\x50')
    f.seek(32,0)
    f.write(bonecount)
    f.seek(36,0)
    f.write(texcount)
    f.seek(40,0)
    f.write(ysize)
    f.seek(44,0)
    f.write(fsize0)
    f.seek(48,0)
    f.write(fsize1)
    f.seek(80,0)
    f.write(b'\x00\x00\x00\x01')
    f.seek(84,0)
    f.write(fsize2)
    fsize3 = fsize3 + 4
    f.seek(fsize3 , 0)
    fsize3 = fsize3 - 4
    fsize3 = struct.pack(">I", fsize3)
    f.write(fsize3)



with open(os.path.join(os.path.dirname(__file__), model_ID), 'rb') as f:                    
    f.seek(24 , 0)
    model_count = bytes_to_int(f.read(4))
    
POF0_Start    = os.path.getsize(os.path.join(os.path.dirname(__file__), model_ID))          
POF0_Header   = b'\x50\x4F\x46\x30\x00\x00\x00\x00'                                         
POF0_pad      = b'\x00'                                                                     
POF0_pad2     = b'\x00\x00'    
POF0_headfill = b'\x45\x43\x41\x41\x49\x5B'
model_data_0  = b'\x41\x41\x41\x49\x41'
next0 = b'\x61'
next1 = b'\x47'

def listToString(s):  
    str1 = ""  
    for ele in s:  
        str1 += ele   
    return str1  

def convert_int_pof0(num1):
    
    def sub_pof0_a(num1):
        y = int((num1 / 4) + 64)
        y = struct.pack(">I", y)
        y = y.replace(b'\x00',b'')
        num1 = y
        return num1
       
    def sub_pof0_b(num1):
        pre   = num1 - 256
        pre   = int((pre / 4) + 64)
        pre   = struct.pack(">I", pre)
        pre   = pre.replace(b'\x00',b'')
        y = b'\x80'
        y += pre           
        num1 = y
        return num1

    def sub_pof0_c(num1):
        pre   = num1 - 16640
        pre   = int((pre / 4) + 64)
        pre   = struct.pack(">I", pre)
        pre   = pre.replace(b'\x00',b'')
        y = b'\x90'
        y += pre            
        num1 = y
        return num1

    def sub_pof0_d(num1):
        pre   = num1 - 33024
        pre   = int((pre / 4) + 64)
        pre   = struct.pack(">I", pre)
        pre   = pre.replace(b'\x00',b'')
        y = b'\xA0'
        y += pre            
        num1 = y
        return num1

    def sub_pof0_e(num1):
        num1 = num1 - 256
        pre     = int((num1 / 4) + 64)
        pre     = struct.pack(">I", pre)
        pre     = pre.replace(b'\x00',b'')
        y = b'\xC0'
        w = b'\x00'
        y += w
        y += pre
        num1 = y
        return num1

    def sub_pof0_f(num1):
        num1 = num1 - 256
        pre     = int((num1 / 4) + 64)
        pre     = struct.pack(">I", pre)
        pre     = pre.replace(b'\x00',b'')
        y = b'\xC0'
        y += pre
        num1 = y
        return num1

    if num1 < 256:
        z = sub_pof0_a(num1)
        z = "".join("\\x%02x" % i for i in z)
        return z

    if 256   <= num1 <= 16380:
        if num1 > 1020:
            z = sub_pof0_b(num1)
            z = "".join("\\x%02x" % i for i in z)
            z = str(z)
            z = z.replace('b\'','')
            z = z.replace('\'','')
            z = z.replace('\\','')
            z = z.replace('x','')
            n = 3
            z = [z[i:i+n] for i in range(0, len(z), n)]
            zone = itemgetter(0)(z)
            ztwo = itemgetter(1)(z)
            zone = str(zone)
            zone = zone.replace('0','')
            ztwo = str(ztwo)
            z = zone + ztwo
            numinterval = 4                                              
            hex_output = [z[i:i+numinterval] for i in range(0, len(z), numinterval)]
            hex_output = list('\ x' + item for item in hex_output)
            hex_output = 'b' + "\'" + (listToString(hex_output)).replace(" ","") + "\'"
            z = eval(hex_output)

            if len(z) == 1:
                pad = b'\x00'
                z += pad

            return z

        z = sub_pof0_b(num1)
        z = "".join("\\x%02x" % i for i in z)
        return z
    
    if 16640 <= num1 <= 32764:
        if num1 > 17404:
            z = sub_pof0_c(num1)
            z = "".join("\\x%02x" % i for i in z)
            z = str(z)
            z = z.replace('b\'','')
            z = z.replace('\'','')
            z = z.replace('\\','')
            z = z.replace('x','')
            n = 3
            z = [z[i:i+n] for i in range(0, len(z), n)]
            zone = itemgetter(0)(z)
            ztwo = itemgetter(1)(z)
            zone = str(zone)
            zone = zone.replace('0','')
            ztwo = str(ztwo)
            z = zone + ztwo
            numinterval = 4                                              
            hex_output = [z[i:i+numinterval] for i in range(0, len(z), numinterval)]
            hex_output = list('\ x' + item for item in hex_output)
            hex_output = 'b' + "\'" + (listToString(hex_output)).replace(" ","") + "\'"
            z = eval(hex_output)

            if len(z) == 1:
                pad = b'\x00'
                z += pad

            return z

        z = sub_pof0_c(num1)
        z = "".join("\\x%02x" % i for i in z)
        return z
    
    if 33024 <= num1 <= 49148:
        if num1 > 33788:
            z = sub_pof0_d(num1)
            z = "".join("\\x%02x" % i for i in z)
            z = str(z)
            z = z.replace('b\'','')
            z = z.replace('\'','')
            z = z.replace('\\','')
            z = z.replace('x','')
            n = 3
            z = [z[i:i+n] for i in range(0, len(z), n)]
            zone = itemgetter(0)(z)
            ztwo = itemgetter(1)(z)
            zone = str(zone)
            zone = zone.replace('0','')
            ztwo = str(ztwo)
            z = zone + ztwo
            numinterval = 4                                          
            hex_output = [z[i:i+numinterval] for i in range(0, len(z), numinterval)]
            hex_output = list('\ x' + item for item in hex_output)
            hex_output = 'b' + "\'" + (listToString(hex_output)).replace(" ","") + "\'"
            z = eval(hex_output)

            if len(z) == 1:
                pad = b'\x00'
                z += pad

            return z

        z = sub_pof0_d(num1)
        z = "".join("\\x%02x" % i for i in z)
        return z

    if 49148 < num1 <= 262140:
        z = sub_pof0_e(num1)
        z = "".join("\\x%02x" % i for i in z)
        return z

    if 262140 < num1 <= 67108860:
        z = sub_pof0_f(num1)
        z = "".join("\\x%02x" % i for i in z)
        return z

def append_to_list(input):
    f = open(os.path.join(os.path.dirname(__file__), 'input_list.temp'), 'a')
    input = str(input)
    input = ''.join((input , ','))
    f.write(input)

with open(os.path.join(os.path.dirname(__file__), model_ID), 'rb') as model:             
    model.seek(84 , 0)
    matrix_off = bytes_to_int(model.read(4)) + 12
    append_to_list(matrix_off)

num_index = 0

def get_offsetlist():

    with open(os.path.join(os.path.dirname(__file__), model_ID), 'rb') as model:

        readbegin = 88 + (num_index * 184)                         

        model.seek(0,0)                                            
        model.seek(readbegin + 104, 0)  
        vertice_begin = model.read(4)
        vertice_begin = bytes_to_int(vertice_begin) + 8
        append_to_list(vertice_begin)

        model.seek(readbegin + 148, 0)                             
        parameter_count = model.read(4)
        parameter_count = bytes_to_int(parameter_count)

        model.seek(readbegin + 152, 0)                             
        shader_begin = model.read(4)
        shader_begin = bytes_to_int(shader_begin)  + 8
        append_to_list(shader_begin)

        for _ in itertools.repeat(None, int(parameter_count - 1)): 
            shader_begin = shader_begin + 4
            prm_off      = shader_begin
            append_to_list(prm_off)

        model.seek(readbegin + 156, 0)                             
        face_begin  = model.read(4)
        face_begin  = bytes_to_int(face_begin) + 16
        append_to_list(face_begin)

def appwrite_to_model(insert):
    with open(os.path.join(os.path.dirname(__file__), model_ID), 'ab') as f: 
        f.write(insert) 

get_offsetlist()

for _ in itertools.repeat(None, int(model_count - 1)):
    num_index = num_index + 1
    get_offsetlist()



with open('input_list.temp', 'rb+') as filehandle:
    filehandle.seek(-1, os.SEEK_END)
    filehandle.truncate()

with open('input_list.temp') as f:            
    lines = f.read()
    lines = lines.split(",")
    lines = list(map(int, lines))
    y = list(set(lines))
    y = sorted(y)
    y = [x - y[i - 1] for i, x in enumerate(y)][1:]

def write_pof0():

    output = []

    for i in y:
        output.append(convert_int_pof0(i))
    
    output = [str(i) for i in output]
    output = [i[2:]  for i in output]


    s = ' '

    output = s.join(str(output))
    output = output.replace('b\'\\','')
    output = output.replace('"','')
    output = output.replace(' ','')
    output = output.replace('\\','')
    output = output.replace('x','')
    output = output.replace(',','')
    output = output.replace('\'','')
    output = output.replace('[','')
    output = output.replace(']','')

    numinterval = 2                                              
    hex_output = [output[i:i+numinterval] for i in range(0, len(output), numinterval)]
    hex_output = list('\ x' + item for item in hex_output)
    hex_output = 'b' + "\'" + (listToString(hex_output)).replace(" ","") + "\'"
    output = eval(hex_output)

    a = open("pof0.temp", "x")
    a = open(os.path.join(os.path.dirname(__file__), 'pof0.temp'), 'ab')
    a.write(output)
    a.close()

write_pof0()

os.remove('input_list.temp')

temppof0_size = os.path.getsize(os.path.join(os.path.dirname(__file__), 'pof0.temp'))

with open(os.path.join(os.path.dirname(__file__), 'pof0.temp'), 'rb') as hex_read:
    pof0_data = hex_read.read()



appwrite_to_model(POF0_Header)
appwrite_to_model(POF0_headfill)

if model_count > 1:
    appwrite_to_model(model_data_0)
    appwrite_to_model(next0)

if model_count - 2 != 0:
    for _ in itertools.repeat(None, model_count - 2):
        appwrite_to_model(model_data_0)
        appwrite_to_model(next0)

appwrite_to_model(model_data_0)
appwrite_to_model(next1)

appwrite_to_model(pof0_data)

os.remove('pof0.temp')

full_size = os.path.getsize(os.path.join(os.path.dirname(__file__), model_ID)) 

POF0_size = (full_size - POF0_Start) + 8

if POF0_size % 2 != 0:
    appwrite_to_model(POF0_pad)
    full_size = os.path.getsize(os.path.join(os.path.dirname(__file__), model_ID))

POF0_size = (full_size - POF0_Start) 

if POF0_size % 4 != 0:
    appwrite_to_model(POF0_pad2)
    full_size = os.path.getsize(os.path.join(os.path.dirname(__file__), model_ID)) 

POF0_size = (full_size - POF0_Start) + 8
POF0_size  = POF0_size - 16
POF0_size  = struct.pack(">I", POF0_size)
POF0_Start = POF0_Start + 4

with open(os.path.join(os.path.dirname(__file__), model_ID), 'r+b') as f:
    f.seek(POF0_Start,0)
    f.write(POF0_size)
    f.close()

with open(os.path.join(os.path.dirname(__file__), model_ID), 'r+b') as f:
    f.seek(52,0)
    shape_write = int(shape_count)
    shape_write = struct.pack(">I", shape_write)
    f.write(shape_write)

def fix_pads():
    with open(os.path.join(os.path.dirname(__file__), model_ID), 'r+b') as f:
        byte_block = b'\xFF\xFF\xFF\xFF'*20
        pad_start = 100 + (184 * n)
        f.seek(pad_start,0)
        f.write(byte_block)

n = 0
fix_pads()

n = 0
for _ in itertools.repeat(None, int(model_count - 1)):
    n = n + 1
    fix_pads()