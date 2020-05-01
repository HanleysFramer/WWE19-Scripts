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

os.chdir(sys.path[0])

user_model = input("Enter YOBJ: ")
user_model = str(user_model)

model_ID = user_model                                                                      #ID

with open(os.path.join(os.path.dirname(__file__), model_ID), 'rb') as f:                    #gets model count
    f.seek(24 , 0)
    model_count = bytes_to_int(f.read(4))
POF0_Start    = os.path.getsize(os.path.join(os.path.dirname(__file__), model_ID))          #startofpof0
POF0_Header   = b'\x50\x4F\x46\x30\x00\x00\x00\x00'                                         #genericheader
POF0_pad      = b'\x00'                                                                     #struct_pad
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

def int_to_bytes(value, length):
    result = []
    for i in range(0, length):
        result.append(value >> (i * 8) & 0xff)
    result.reverse()
    return result

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
        y += pre           #prepends 0x80
        num1 = y
        return num1

    def sub_pof0_c(num1):
        pre   = num1 - 16640
        pre   = int((pre / 4) + 64)
        pre   = struct.pack(">I", pre)
        pre   = pre.replace(b'\x00',b'')
        y = b'\x90'
        y += pre            #prepends 0x90
        num1 = y
        return num1

    def sub_pof0_d(num1):
        pre   = num1 - 33024
        pre   = int((pre / 4) + 64)
        pre   = struct.pack(">I", pre)
        pre   = pre.replace(b'\x00',b'')
        y = b'\xA0'
        y += pre            #prepends 0xA0
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

with open(os.path.join(os.path.dirname(__file__), model_ID), 'rb') as model:             #appends matrix
    model.seek(84 , 0)
    matrix_off = bytes_to_int(model.read(4)) + 12
    append_to_list(matrix_off)

num_index = 0

def get_offsetlist():

    with open(os.path.join(os.path.dirname(__file__), model_ID), 'rb') as model:

        readbegin = 88 + (num_index * 184)                         #start of modeldata

        model.seek(0,0)                                            #append vertexstart
        model.seek(readbegin + 104, 0)  
        vertice_begin = model.read(4)
        vertice_begin = bytes_to_int(vertice_begin) + 8
        append_to_list(vertice_begin)

        model.seek(readbegin + 148, 0)                             #get parameter count
        parameter_count = model.read(4)
        parameter_count = bytes_to_int(parameter_count)

        model.seek(readbegin + 152, 0)                             #append shaderprm start
        shader_begin = model.read(4)
        shader_begin = bytes_to_int(shader_begin)  + 8
        append_to_list(shader_begin)

        for _ in itertools.repeat(None, int(parameter_count - 1)): #getsparameters
            shader_begin = shader_begin + 4
            prm_off      = shader_begin
            append_to_list(prm_off)

        model.seek(readbegin + 156, 0)                             #appendsfacestart
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

# ---------------------------------------------------------------------

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

# --------------------------------------------------------------------------

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