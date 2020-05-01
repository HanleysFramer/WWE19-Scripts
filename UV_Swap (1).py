import os
import os.path
import re
import itertools
import struct
import sys
import binascii

os.chdir(sys.path[0])

movie_shader = 'yModelMovie'.encode()

print('Input YOBJ file to UV swap:\n')
YOBJ = input()

clear = lambda: os.system('cls')
clear()

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

print('Working on', YOBJ.upper(), '\n\n') 

with open(os.path.join(os.path.dirname(__file__), YOBJ), 'rb') as f:                 
    readmodel   = f.read()
    model_start = 88
    
    f.seek(0,0)
    if f.read(4) != 'JBOY'.encode():
        print('File is not a YOBJ.')
        exit()

    f.seek(24,0)
    model_count = bytes_to_int(f.read(4))

    f.seek(0,0)
    movie_model_count = readmodel.count(('yModelMovie'.encode()))
    if movie_shader in  readmodel:
        print(movie_model_count , 'Movie Model(s) found:\n')
        
        def main_UVswap():                                                                   
            f.seek(model_start, 0)
            vertice_count = bytes_to_int(f.read(4))

            if 'yModelMovie'.encode() in f.read(184):
                print('\nModel Data:')

                f.seek(model_start + 112 , 0)
                UV_Begin = bytes_to_int(f.read(4)) + 8
                f.seek(model_start + 112 + 4 , 0)
                UV_End   = bytes_to_int(f.read(4)) + 8
                print('UV start offset at', UV_Begin, ' (dec)')
                print('UV end offset at',   UV_End,   ' (dec)')
                UV_Size = UV_End - UV_Begin
                print('UV size is' , UV_Size)
                print('Swapping...')

                f.seek(UV_Begin, 0)
                def sub_UVSwap():
                    uv_block = f.read(16)
                    uv_block = binascii.hexlify(bytearray(uv_block))
                    uv_1 = uv_block[:-16]
                    uv_2 = uv_block[16:]
                    stringswap = ''.join((uv_2.decode() , uv_1.decode()))                                       
                    stringswap = ' '.join(stringswap[i:i+2] for i in range(0, len(stringswap), 2))
                    stringswap = 'b' + "\'\\x" + stringswap.replace(" ","\ x") + "\'"
                    stringswap = stringswap.replace(" ","")
                    stringswap = eval(stringswap)
                    swapped_uv_block = stringswap

                    WRITEYOBJ = open(os.path.join(os.path.dirname(__file__), YOBJ), 'r+b')
                    WRITEYOBJ.seek(UV_Begin,0)
                    WRITEYOBJ.write(swapped_uv_block)
                    WRITEYOBJ.close()

                sub_UVSwap() 

                for _ in itertools.repeat(None, vertice_count-1):
                    UV_Begin = UV_Begin + 16
                    sub_UVSwap() 
                    
                print('Swapped Successfully.\n') 
                                                        
            else: 
                print('model shader is not movie')
                
        
        main_UVswap()

        for _ in itertools.repeat(None, int(model_count-1)):                                  
            model_start = model_start + 184
            main_UVswap()             

    else:
        print('No Movie models found in YOBJ. No UVs Swapped.')
        exit()

f.close()

input("\nProcess complete. Press enter to exit.")