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
from google.cloud import speech_v1p1beta1
from google.cloud.speech_v1p1beta1 import enums
import argparse
import io

from google.cloud import speech_v1
from google.cloud.speech_v1 import enums

#rename function>>
##[os.rename(f, f.replace('00 - ogg_dump - ', '')) for f in os.listdir('.') if not f.startswith('.')]

os.chdir(sys.path[0])
os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = r"C:/Users/wauke/Desktop/sound_stuff/2k20_ra_m/ogg_dump/My First Project-e9e643c15b69.json"

def create_xml(xml_name):
    xml_header = str('<?xml version="1.0" encoding="utf-8"?>')
    xml_2 = str('<data>')
    xml_3 = str('  <sounds>')

    with io.open(xml_name, "a") as xml_file:
        insert = (xml_header + '\n' + xml_2 + '\n' + xml_3 + '\n')
        xml_file.write(insert)

xml = 'list_output.xml'
test_file =  '1073702644.flac' #file_input

create_xml(xml)

def transcribe_file(local_file_path):

    client = speech_v1.SpeechClient()

    language_code = "en-US"                    #audio_settings
    sample_rate_hertz = 48000
    encoding = enums.RecognitionConfig.AudioEncoding.FLAC
    config = {
        "language_code": language_code,
        "sample_rate_hertz": sample_rate_hertz,
        "encoding": encoding,
    }

    with io.open(local_file_path, "rb") as f:   #file_read
        content = f.read()
    audio = {"content": content}

    response = client.recognize(config, audio)

    for result in response.results:
        # First alternative is the most probable result
        alternative = result.alternatives[0]
        trans_output = (u"{}".format(alternative.transcript))
        print(trans_output)

        output_path_2 = ('GH_') + ((trans_output) + (".flac"))

        if ' ' in output_path_2:
            output_path_2 = output_path_2.replace(' ','_')
        if '/' in output_path_2:
            output_path_2 = output_path_2.replace('/','')
        if '\'' in output_path_2:
            output_path_2 = output_path_2.replace('\'','')

        with io.open(output_path_2, "ab") as a:
            a.write(content)

        def append_to_xml(file_input, xml_file):
            file_input = file_input.replace('.flac','')
            a = '\n' + '    <sound id=' + '"' + file_input + '"' + ' name=' + '"' + trans_output + '"' + " />"

            with io.open(xml_file, "a") as xml_file0:
                xml_file0.write(a)
        
        append_to_xml(local_file_path, xml)
        

files = os.listdir('.')
files = [ x for x in files if ".py" not in x ]
files = [ x for x in files if ".xml" not in x ]
files = [ x for x in files if ".txt" not in x ]

# files = files[6592:]  #bc errors

with io.open("log_list.txt", "a") as xml_file0:  #appends xml end
    xml_file0.write(str(files))

for i in files:
    try: 
        print(i)
        str(i)
        transcribe_file(i)
    except:
        pass

with io.open(xml, "a") as xml_file0:  #appends xml end
    a1 = ('\n' + '  </sounds>' + '\n' + '</data>')
    xml_file0.write(a1)
