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

def int_to_bytes(value, length):
    result = []
    for i in range(0, length):
        result.append(value >> (i * 8) & 0xff)
    result.reverse()
    return result

os.chdir(sys.path[0])


merge_count = 5


# model_1 = input("Enter YOBJ model 1: ")
model_1 = "1.yobj"

if merge_count == 2:

    model_2 = "2.yobj"

if merge_count > 2:
    model_3 = "3.yobj"

    if merge_count > 3:
        model_4 = "4.yobj"

        if merge_count > 4:
            model_5 = "5.yobj"

            if merge_count > 5:
                model_6 = "6.yobj"

                if merge_count > 6:
                    model_7 = "7.yobj"

                    if merge_count > 7:
                        model_8 = "8.yobj"

                        if merge_count > 8:
                            model_9 = "9.yobj"

                            if merge_count > 9:
                                model_10 = "10.yobj"

                                if merge_count > 10:
                                    model_11 = "11.yobj"

                                    if merge_count > 11:
                                        model_12 = "12.yobj"

                                        if merge_count > 12:
                                            model_13 = "13.yobj"



YOBJ_Header = b'\x4A\x42\x4F\x59'
byte_pad    = b'\x00\x00\x00\x00'
byte_pad2   = b'\x00\x00'
byte_pad3   = b'\x00'

def collect_basic_data():

    with open(os.path.join(os.path.dirname(__file__), model_1), 'rb') as model:
        model.seek(40)
        bonestart  = bytes_to_int( model.read(4) ) + 8
        model.seek(32)
        bone_count = bytes_to_int( model.read(4) )
        bone_size  = bone_count * 80
        model.seek(bonestart)
        bones = model.read(bone_size)

        with open("bones.temp", "wb+") as bones_0:
            bones_0.write(bones)

    with open(os.path.join(os.path.dirname(__file__), model_1), 'rb') as model:
        model.seek(44)
        texstart  = bytes_to_int( model.read(4) ) + 8
        model.seek(36)
        tex_count = bytes_to_int( model.read(4) )
        tex_size  = tex_count * 16
        model.seek(texstart)
        tex_name = model.read(tex_size)

        with open("tex_name.temp", "wb+") as tex_0:
            tex_0.write(tex_name)

    with open(os.path.join(os.path.dirname(__file__), model_1), 'rb') as model:
        model.seek(84)
        sk_b_start  = bytes_to_int( model.read(4) ) + 8
        model.seek(sk_b_start)
        skb_count = bytes_to_int( model.read(4) )
        skb_size  = (skb_count * 4) + 8
        model.seek(sk_b_start)
        skb_name = model.read(skb_size)

        with open("matrix_palette.temp", "wb+") as skb_0:
            skb_0.write(skb_name)
        
    bch = bone_count.to_bytes(4, byteorder = 'big')
    tch = tex_count.to_bytes(4, byteorder = 'big')
    mch = merge_count.to_bytes(4, byteorder = 'big')
        
    with open("Merged_Container.YOBJ", "wb+") as new_model:     #sorta blank header
        new_model.write(YOBJ_Header)
        new_model.write(byte_pad)
        new_model.write(b'\x00\x00\x00\x10')
        new_model.write(byte_pad)
        new_model.write(b'\x00\x00\x00\x07')
        new_model.write(byte_pad)
        new_model.write(b'\x00\x00\x00\xFF')                #Todo gen shape list count
        new_model.write(b'\x00\x00\x00\x50')                  
        new_model.write(bch)
        new_model.write(tch)
        new_model.write(byte_pad)       #boneoffset
        new_model.write(byte_pad)       #texoffset
        new_model.write(byte_pad)       #shapeoffset
        new_model.write(mch)
        new_model.write(byte_pad)
        new_model.write(byte_pad)
        new_model.write(byte_pad)
        new_model.write(byte_pad)
        new_model.write(byte_pad)
        new_model.write(byte_pad)
        new_model.write(b'\x00\x00\x00\x01') 
        new_model.write(byte_pad)                              #matrixoffset
    
collect_basic_data()

n = 0

def extract_model_contents(curr_model):

    with open(os.path.join(os.path.dirname(__file__), curr_model), 'rb') as model:
        model.seek(88)
        subobj_header = model.read(184)

        with open(((curr_model) + ("_header")), "wb+") as submodel_header:
            submodel_header.write(subobj_header)
        
        model.seek(88)
        model_vertices = bytes_to_int(model.read(4))
        model.seek(192)
        vertice_start  = bytes_to_int(model.read(4)) + 8
        vertice_size   = (model_vertices * 28) + 4
        model.seek(vertice_start)
        subobj_vert = model.read(vertice_size)

        with open(((curr_model) + ("_vertices")), "wb+") as submodel_vert:
            submodel_vert.write(subobj_vert)

        model.seek(180)
        weight_count = bytes_to_int(model.read(4))
        model.seek(196)
        weight_start  = bytes_to_int(model.read(4)) + 8
        weight_size   = model_vertices * (8 * weight_count)
        model.seek(weight_start)
        subobj_weights_0 = model.read(weight_size)

        with open(((curr_model) + ("_weights")), "wb+") as submodel_weights:
            submodel_weights.write(subobj_weights_0)

        model.seek(204)
        normals_start  = bytes_to_int(model.read(4)) + 8
        normals_size   = model_vertices * 12
        model.seek(normals_start)
        subobj_normals = model.read(normals_size)

        with open(((curr_model) + ("_normals")), "wb+") as submodel_nrm:
            submodel_nrm.write(subobj_normals)

        model.seek(200)
        uv_start  = bytes_to_int(model.read(4)) + 8
        uv_size   = model_vertices * 8
        model.seek(uv_start)
        subobj_uvs = model.read(uv_size)

        with open(((curr_model) + ("_uv")), "wb+") as submodel_uv:
            submodel_uv.write(subobj_uvs)
        
        model.seek(236)
        prm_count  = bytes_to_int(model.read(4))
        model.seek(240)
        prm_start  = bytes_to_int(model.read(4)) + 8
        prm_0      = (prm_count * 4)
        model.seek(prm_start)
        prm_2      = bytes_to_int(model.read(4)) + 8
        model.seek(prm_start + prm_0)
        prm_1      = bytes_to_int(model.read(4))
        prm_size2  = (prm_1 - prm_2) + 8
        model.seek(prm_start)
        subobj_prms = model.read(prm_0)
        model.seek(prm_2)
        subobj_prms2 = model.read(prm_size2)

        with open(((curr_model) + ("_parameters")), "wb+") as submodel_prm:
            submodel_prm.write(subobj_prms)
            submodel_prm.write(subobj_prms2)

        model.seek(244)
        face_start  = bytes_to_int(model.read(4)) + 8
        model.seek(face_start + 4)
        face_size = (bytes_to_int(model.read(4)) * 2)
        model.seek(face_start)
        subobj_faces = model.read(face_size + 12)

        with open(((curr_model) + ("_faces")), "wb+") as submodel_face:
            submodel_face.write(subobj_faces)

        model.seek(48)
        shape_start  = bytes_to_int(model.read(4)) + 8
        shape_size   = 32
        model.seek(shape_start)
        subobj_shape = model.read(shape_size)

        with open(((curr_model) + ("_shape")), "wb+") as submodel_shape:
            submodel_shape.write(subobj_shape)

for _ in itertools.repeat(None, merge_count):
    n = n + 1
    model_x = (str(n)) + (".yobj")
    extract_model_contents(model_x)

n = 0

with open("Merged_Container.YOBJ", "ab+") as new_model:

    for _ in itertools.repeat(None, merge_count):
        n = n + 1

        model_x = (str(n)) + (".yobj") + ("_header")
        
        with open(model_x, "rb+") as new_model1:
            new_model2 = new_model1.read()
            new_model.write(new_model2)
    
    n = 0
    
    for _ in itertools.repeat(None, merge_count):
        time.sleep(2)

        n = n + 1

        model_x = (str(n)) + (".yobj")

        # with open("YOBJ_metadata.txt", "a+") as data:
        #         statinfo = os.stat("Merged_Container.YOBJ")
        #         curr_size= statinfo.st_size
        #         data.write((str(curr_size)) + (","))

        fh = open("Merged_Container.YOBJ", "r+b")
        statinfo     = os.stat("Merged_Container.YOBJ")
        curr_size    = statinfo.st_size

        if n == 1:
            curr_size= curr_size + (184 * merge_count)

        curr_size    = (curr_size - 8).to_bytes(4, byteorder = 'big')
        verticebegin = (88 + (184 * (n - 1)) + 104)
        fh.seek(verticebegin)
        fh.write(curr_size)
        
        with open(model_x + ("_vertices"), "rb+") as new_model1: #write_vert
            new_model2 = new_model1.read()
            new_model.write(new_model2)
        
        fh  = open("Merged_Container.YOBJ", "r+b")
        vert= (88 + (184 * (n - 1)) + 104)
        fh.seek(vert)
        vbeg = bytes_to_int(fh.read(4))
        vnew = vbeg + 4
        vbeg = vbeg + 8
        fh.seek(vbeg)
        vnew = vnew.to_bytes(4, byteorder = 'big')  
        fh.write(vnew)

        def align_bytes():

            fh  = open("Merged_Container.YOBJ", "ab")
            statinfo     = os.stat("Merged_Container.YOBJ")
            curr_size    = statinfo.st_size
            
            if curr_size % 2 != 0:
                fh.write(byte_pad3)
            
            fh  = open("Merged_Container.YOBJ", "ab")
            statinfo     = os.stat("Merged_Container.YOBJ")
            curr_size    = statinfo.st_size

            byte_check = str((curr_size / 4))

            if ".5" in byte_check:
                fh.write(byte_pad2)
                fh.write(byte_pad)
            
            fh  = open("Merged_Container.YOBJ", "ab")
            statinfo     = os.stat("Merged_Container.YOBJ")
            curr_size    = statinfo.st_size

            byte_check = str((curr_size / 8))

            if ".5" in byte_check:
                fh.write(byte_pad)
        
        align_bytes()

        fh = open("Merged_Container.YOBJ", "r+b")
        statinfo     = os.stat("Merged_Container.YOBJ")
        curr_size    = statinfo.st_size
        curr_size    = (curr_size - 8).to_bytes(4, byteorder = 'big')
        begin = (88 + (184 * (n - 1)) + 108)
        fh.seek(begin)
        fh.write(curr_size)    

        with open(model_x + ("_weights"), "rb+") as new_model1:  #write_weights
            new_model2 = new_model1.read()
            new_model.write(new_model2)
        
        fh = open("Merged_Container.YOBJ", "r+b")
        statinfo     = os.stat("Merged_Container.YOBJ")
        curr_size    = statinfo.st_size
        curr_size    = (curr_size - 8).to_bytes(4, byteorder = 'big')
        begin = (88 + (184 * (n - 1)) + 112)
        fh.seek(begin)
        fh.write(curr_size) 
        fh.close()  

        with open(model_x + ("_uv"), "rb+") as new_model1:
            new_model2 = new_model1.read()
            one = str((model_x + ("_uv")))
            fh = open(one ,  "r+b")
            statinfo2     = os.stat((model_x + ("_uv")))
            curr_size3   = statinfo2.st_size
            new_model.write(new_model2)
        
        with open(((model_x) + ("_header")), "rb+") as submodel_header:
            submodel_header.seek(0)
            model_vertices = bytes_to_int(submodel_header.read(4))

        if model_vertices < 500:

            fh = open("Merged_Container.YOBJ", "r+b")
            statinfo     = os.stat("Merged_Container.YOBJ")
            curr_size    = statinfo.st_size + curr_size3
            curr_size    = (curr_size - 8).to_bytes(4, byteorder = 'big')
            begin = (88 + (184 * (n - 1)) + 116)
            fh.seek(begin)
            fh.write(curr_size) 
            fh.close() 

        else:
            fh = open("Merged_Container.YOBJ", "r+b")
            statinfo     = os.stat("Merged_Container.YOBJ")
            curr_size    = statinfo.st_size
            curr_size    = (curr_size - 8).to_bytes(4, byteorder = 'big')
            begin = (88 + (184 * (n - 1)) + 116)
            fh.seek(begin)
            fh.write(curr_size) 
            fh.close() 

        
        with open(model_x + ("_normals"), "rb+") as new_model1:
            new_model2 = new_model1.read()
            fh = open(one ,  "r+b")
            statinfo2     = os.stat((model_x + ("_normals")))
            curr_size4   = statinfo2.st_size
            new_model.write(new_model2)
        
        if model_vertices < 500:

            fh = open("Merged_Container.YOBJ", "r+b")
            statinfo     = os.stat("Merged_Container.YOBJ")
            curr_size    = statinfo.st_size + curr_size4
            curr_size    = (curr_size - 8).to_bytes(4, byteorder = 'big')
            begin = (88 + (184 * (n - 1)) + 152)
            fh.seek(begin)
            fh.write(curr_size) 
            fh.close() 

        else:
            fh = open("Merged_Container.YOBJ", "r+b")
            statinfo     = os.stat("Merged_Container.YOBJ")
            curr_size    = statinfo.st_size
            curr_size    = (curr_size - 8).to_bytes(4, byteorder = 'big')
            begin = (88 + (184 * (n - 1)) + 152)
            fh.seek(begin)
            fh.write(curr_size) 
            fh.close() 

        with open(model_x + ("_parameters"), "rb+") as new_model1:
            new_model2 = new_model1.read()
            one = str((model_x + ("_parameters")))
            fh = open(one ,  "r+b")
            statinfo2     = os.stat((model_x + ("_parameters")))
            curr_size3   = statinfo2.st_size
            new_model.write(new_model2)


        if model_vertices < 500:
            c1 = os.path.getsize(os.path.join(os.path.dirname(__file__), "Merged_container.YOBJ"))
            print(c1)
            curr_size    = c1 + curr_size3 + curr_size4 + 24
            curr_size    = (curr_size - 8).to_bytes(4, byteorder = 'big')
            begin = (88 + (184 * (n - 1)) + 156)
            fh = open("Merged_Container.YOBJ", "r+b")
            fh.seek(begin)
            fh.write(curr_size) 
            fh.close() 
            
        else:
            c1 = os.path.getsize(os.path.join(os.path.dirname(__file__), "Merged_container.YOBJ"))
            print(c1)
            curr_size    = c1 + curr_size3
            curr_size    = (curr_size - 8).to_bytes(4, byteorder = 'big')
            begin = (88 + (184 * (n - 1)) + 156)
            fh = open("Merged_Container.YOBJ", "r+b")
            fh.seek(begin)
            fh.write(curr_size) 
            fh.close() 

        with open(model_x + ("_faces"), "rb+") as new_model1:
            new_model2 = new_model1.read()
            new_model.write(new_model2)

        align_bytes()  

        
        os.remove(model_x + ("_vertices"))
        os.remove(model_x + ("_weights"))
        os.remove(model_x + ("_normals"))
        os.remove(model_x + ("_uv"))
        os.remove(model_x + ("_parameters"))
        os.remove(model_x + ("_faces"))
        os.remove(model_x + ("_header"))
    
    fh  = open("Merged_Container.YOBJ", "ab")
    fh.write(byte_pad)
    fh.write(byte_pad)

    statinfo     = os.stat("Merged_Container.YOBJ")
    curr_size    = statinfo.st_size

    byte_check = str((curr_size / 16))


    if ".5" in byte_check:
        fh.write(byte_pad)
        fh.write(byte_pad)

        fh.close()

        fh  = open("Merged_Container.YOBJ", "ab")

        statinfo     = os.stat("Merged_Container.YOBJ")
        curr_size    = statinfo.st_size

        byte_check = str((curr_size / 16))


        if ".5" in byte_check:
            fh.write(byte_pad)


    fh    = open("bones.temp", "rb")
    bones = fh.read()
    fh.close()

    fh    = open("tex_name.temp", "rb")
    tex = fh.read()
    fh.close()

    fh = open("Merged_Container.YOBJ", "r+b")
    statinfo     = os.stat("Merged_Container.YOBJ")
    print(curr_size)
    curr_size    = statinfo.st_size
    curr_size    = (curr_size - 8).to_bytes(4, byteorder = 'big')
    begin = (40)
    fh.seek(begin)
    fh.write(curr_size)
    fh.close()

    new_model.write(bones)
    new_model.write(tex)

    new_model.seek(40)
    bone_start = bytes_to_int(new_model.read(4))

    new_model.seek(32)
    bone_count = bytes_to_int(new_model.read(4))

    bone1 = ((bone_count * 80) + bone_start)
    bone1 = bone1.to_bytes(4, byteorder = 'big')

    fh = open("Merged_Container.YOBJ", "r+b")
    fh.seek(44)
    fh.write(bone1)
    fh.close()

    n = 0
    
    for _ in itertools.repeat(None, merge_count):
        n = n + 1

        model_x = (str(n)) + (".yobj")

        with open(model_x + ("_shape"), "rb+") as a: 
            new_model4 = a.read()
        
        new_model.write(new_model4)
    
        os.remove(model_x + ("_shape"))

    fh = open("Merged_Container.YOBJ", "r+b")
    statinfo     = os.stat("Merged_Container.YOBJ")
    curr_size    = statinfo.st_size
    curr_size    = (curr_size - 8).to_bytes(4, byteorder = 'big')
    begin = (48)
    fh.seek(begin)
    fh.write(curr_size)
    fh.close()

fh = open("Merged_Container.YOBJ", "r+b")
statinfo     = os.stat("Merged_Container.YOBJ")
curr_size    = statinfo.st_size
curr_size    = (curr_size - 8).to_bytes(4, byteorder = 'big')
begin = (84)
fh.seek(begin)
fh.write(curr_size)
fh.close()

with open("matrix_palette.temp", "rb+") as b: 
    new_model4 = b.read()

fh = open("Merged_Container.YOBJ", "ab")
fh.write(new_model4)
fh.close()
    
    # with open( "bones.temp", "rb+") as new_model1:
    #     new_model2 = new_model1.read()
    #     new_model.write(new_model2)

    # with open( "tex_name.temp", "rb+") as new_model1:
    #     new_model2 = new_model1.read()
    #     new_model.write(new_model2)

fh = open("Merged_Container.YOBJ", "r+b")
statinfo     = os.stat("Merged_Container.YOBJ")
curr_size    = statinfo.st_size
curr_size    = (curr_size - 8).to_bytes(4, byteorder = 'big')
begin = (4)
fh.seek(begin)
fh.write(curr_size)
fh.close()

fh = open("Merged_Container.YOBJ", "r+b")
statinfo     = os.stat("Merged_Container.YOBJ")
curr_size    = statinfo.st_size
curr_size    = (curr_size - 8).to_bytes(4, byteorder = 'big')
begin = (12)
fh.seek(begin)
fh.write(curr_size)
fh.seek(24)
merge_count2 = merge_count.to_bytes(4, byteorder = 'big')
fh.write(merge_count2)
fh.close()


os.remove("bones.temp")
os.remove("tex_name.temp")
os.remove("matrix_palette.temp")

def update_prm():

    n = n1
    n2= n1
    

    with open("Merged_Container.YOBJ", "rb+") as model:

        model.seek(88 + (184 * n) + 152)
        prm_start = bytes_to_int(model.read(4)) + 8
        model.seek(88 + (184 * n) + 148)
        prm_count = bytes_to_int(model.read(4))
        prm_begin = prm_start + (4 * prm_count)

        model.seek(prm_start + (4 * n))
        prm1_start  = bytes_to_int(model.read(4)) + 8
        model.seek(prm_start + (4 * n) + 4)

        prm2_start  = bytes_to_int(model.read(4)) + 8

        prm_displace=prm2_start - prm1_start

        fh = open("Merged_Container.YOBJ", "r+b")
        fh.seek(prm_start)
        prm_2 = (prm_begin - 8).to_bytes(4, byteorder = 'big')
        fh.write(prm_2)

        a = 0

        for _ in itertools.repeat(None, int(prm_count - 2)):

            a = a + 1
            n = a

            model.seek(prm_start + (4 * n))
            prm1_start  = bytes_to_int(model.read(4)) + 8
            model.seek(prm_start + (4 * n) + 4)
            prm2_start  = bytes_to_int(model.read(4)) + 8
            prm_displace =prm2_start - prm1_start
            model.seek(prm_start + (4 * n) - 4)
            prm_begin = prm_begin + prm_displace
            prm_3 = (prm_begin - 8).to_bytes(4, byteorder = 'big')
            fh.seek(prm_start + (4 * n))
            fh.write(prm_3)

    model.close()
    fh.close()

    with open("Merged_Container.YOBJ", "rb+") as model:

        prm_prel = prm_start + (4 * (prm_count - 2))
        prm_last = prm_start + (4 * (prm_count - 1))

        model.seek(prm_prel)
        prm_off2      = bytes_to_int(model.read(4)) + 8
        model.seek(prm_off2 + 19)
        prm_ind_size  = bytes_to_int(model.read(1))
        prm_off3      = (prm_off2 + prm_ind_size) - 8
        prm_new       = prm_off3.to_bytes(4, byteorder = 'big')
        model.seek(prm_last)
        model.write(prm_new)
    
n1 = 0
update_prm()

n1 = 0

for _ in itertools.repeat(None, int(merge_count - 1)):
    n1 = n1 + 1
    update_prm()

def face_update():

    n = n1

    fh = open("Merged_Container.YOBJ", "r+b")
    fh.seek(156 + (n * 184) + 88)
    face_start = fh.read(4)
    face_1     = bytes_to_int(face_start) + 16
    face_start = bytes_to_int(face_start) + 12

    face_start = face_start.to_bytes(4, byteorder = 'big')

    fh.seek(face_1)
    fh.write(face_start)

n1 = 0
face_update()

for _ in itertools.repeat(None, int(merge_count - 1)):
    n1 = n1 + 1
    face_update()

fh = open("Merged_Container.YOBJ", "r+b")
statinfo     = os.stat("Merged_Container.YOBJ")
curr_size    = statinfo.st_size
curr_size    = (curr_size - 8).to_bytes(4, byteorder = 'big')
begin = (12)
fh.seek(begin)
fh.write(curr_size)
fh.seek(24)
merge_count2 = merge_count.to_bytes(4, byteorder = 'big')
fh.write(merge_count2)
fh.close()

def pofo_gen(input_model):

    user_model = input_model

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

pofo_gen("Merged_Container.YOBJ") 

fh = open("Merged_Container.YOBJ", "r+b")
fh.seek(84)

matrix_start = bytes_to_int(fh.read(4)) + 8
matrix_start2= matrix_start + 4

insert = matrix_start.to_bytes(4, byteorder = 'big')
fh.seek(matrix_start2)
fh.write(insert)
fh.close()

input("Models merged. please kill yourself now. k bye.")