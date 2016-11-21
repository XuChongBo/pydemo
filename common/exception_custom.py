# coding: utf-8
import xml.etree.ElementTree as ET
from xml.etree.ElementTree import Element
from xml.etree.ElementTree import SubElement
import json
import sys
import os
import requests
import logging

# set logger
logging.basicConfig(
     stream=sys.stdout,
     level=logging.DEBUG,
     format='[%(asctime)s] [%(name)s] [%(levelname)s]:\t%(message)s')

logger = logging.getLogger("utils")

# set BASE_URL
DEPLOY_MODE = os.getenv('DEPLOY_MODE')
assert(DEPLOY_MODE in ['ON-LINE', 'OFF-LINE'])

if DEPLOY_MODE == "ON-LINE":
    BASE_URL = "http://tiku-upload.zuoyetong.com.cn/resource/"
else:
    BASE_URL = "http://tiku-upload-test.zuoyetong.com.cn/resource/"

class TextParseException(Exception):
    def __init__(self, value):
        self.value = value
    def __str__(self):
        return self.value

class HttpException(Exception):
    def __init__(self, value):
        self.value = value
    def __str__(self):
        return "httpcode:%s conent:%s" % (self.value.status_code, self.value.content) 

class NeedAuthException(HttpException):
    pass

class UploadException(HttpException):
    pass


def _getToken():
    data = {"username": "lanbijia", "password": "lanbijia"}
    resp = requests.post(BASE_URL+"token/", data=data)
    if resp.status_code == 200:
        return json.loads(resp.content)['token']
    return None

TOKEN = _getToken()
def needAuth(func):
    def wrapper(*args):
        try:
            return func(*args)
        except NeedAuthException as e:
            logger.warning("************************************" )
            logger.warning("**  %s" % e)
            logger.warning("************************************" )
            logger.info("Current token is invalid. Try to get another." )
            global TOKEN
            TOKEN = _getToken()
            return func(*args)
    return wrapper

@needAuth
def uploadFile(f, is_final, subject):
    f.seek(0) # in case call once more for token retry
    headers = {"Authorization": "JWT %s"%TOKEN}
    if is_final:
        data = { 
                "context": "text2speech",
                "resource.mtype": 2,         #audio
                "resource.subject": subject, #学科.  16:小学英语  24:初中语文  36:高中英语
                "namespace": "universal"
               }
        files = {"resource.media": (f.name, f, "rb")}
        resp = requests.post(BASE_URL+"general/create/", headers=headers, data=data, files=files)
    else:
        data = {}
        files = {"media": (f.name, f, "rb")}
        resp = requests.post(BASE_URL+"tmpfile/create/", headers=headers, data=data, files=files)
    logger.debug("resp from uploadserver. httpcode:%s conent:%s " % (resp.status_code, resp.content))
    if resp.status_code == 201:
        d = json.loads(resp.content)
        if is_final:
            return {"media":d["resource"]["media"], "id":d["resource"]["id"]}
        else:
            return {"media":d["media"], "id":d["id"]}
    elif resp.status_code == 401 or resp.status_code == 403:
        raise NeedAuthException(resp)
    else:
        raise UploadException(resp)



def parse(in_txt):
    """
    in_txt: M:<Paul>hello</Paul>F:<Kate>hello</Kate>M:<Paul>how are you?</Paul>F:<Kate>Fine</Kate>some other thins
    """
    out_txt = """<RATE SPEED='-1'/>"""
    template = """<VOICE REQUIRED='NAME=VW {tag}'/>{text}<SILENCE MSEC='1000'/>"""
    tree = ET.fromstring("<root>"+in_txt+"</root>")
    is_valid = False
    for item in tree.getchildren():
        if item.tag in ["Paul", "Kate"]:
            print item.tag, ":", item.text
            out_txt += template.format(tag=item.tag, text=item.text)
            is_valid = True
    if not is_valid:
        raise TextParseException("Has no valid tags in text.")
    return out_txt

def speak2wav(self, filename):
    self.mem_stream=win32com.client.Dispatch("SAPI.SpMemoryStream")
    self.mem_stream.Format = self.audio_format

    # set mem_stream
    self.speak.AudioOutputStream = self.mem_stream
    text = msg['text']
    print "do speak"
    print text.encode('utf8')

    # speak
    self.speak.Speak(text)

    # get datasize
    datasize=int(self.mem_stream.Seek(0, constants.SSSPTRelativeToEnd))
    print datasize
    self.mem_stream.Seek(0, constants.SSSPTRelativeToStart)
    bitdata = self.mem_stream.Read(None,datasize)[1]
    data = str(bitdata)

    # make format hdr
    wfx=self.mem_stream.Format.GetWaveFormatEx()
    hdr=struct.pack('<4sl4s4slhhllhh4sl', 'RIFF', 36 + datasize,
        'WAVE', 'fmt ', 16,
        wfx.FormatTag, wfx.Channels, wfx.SamplesPerSec,
        wfx.AvgBytesPerSec, wfx.BlockAlign,
        wfx.BitsPerSample, 'data', datasize);
    print len(hdr)
    f = open("c:\\yy.wav",'wb')
    f.write(hdr)
    f.write(data)
    f.close()


if __name__ == "__main__":
    t = "M:<Paul>hello</Paul>F:<Kate>hello</Kate>M:<Paul>how are you?</Paul>F:<Kate>Fine</Kate>some other thins"

    print transform(t)

