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
import argparse
import io
from xml.dom.minidom import parse, parseString
from xml.dom import minidom


os.chdir(sys.path[0])
xml0 = 'custom_data.xml'

files = os.listdir('.')
files = [ x for x in files if ".py" not in x ]
files = [ x for x in files if ".xml" not in x ]
files = [ x for x in files if ".txt" not in x ]

def main_xml_wem(test_file):

    xmldoc = minidom.parse(xml0)             
    namelist = xmldoc.getElementsByTagName('sound')
    nm2 = []
    for s in namelist:
        insert = str(s.attributes['name'].value)
        nm2.append(insert)

    xmldoc1 = minidom.parse(xml0)             
    idlist = xmldoc.getElementsByTagName('sound')    
    id2 = []
    for s in idlist:
        insert = str(s.attributes['id'].value)
        id2.append(insert)

    def search_list_for_id_num(file_input, file_list):

        file_input = file_input.replace('.wem','')
        file_input = file_input.replace('.ogg','')
        file_input = file_input.replace('.flac','')

        id_index = file_list.index(file_input)
        print(id_index)
        return id_index

    a = search_list_for_id_num(test_file, id2)
    name_index= nm2[a]
    print(name_index)
    name_index = name_index.replace('/','_')


    os.rename(str(test_file), ((str(name_index)) + '.wem'))


for file in files:
    try:
        file = str(file)
        main_xml_wem(file)
    except:
        pass