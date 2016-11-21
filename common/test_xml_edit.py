# coding: utf-8
import xml.etree.ElementTree as ET
from xml.etree.ElementTree import Element
from xml.etree.ElementTree import SubElement

# 解析文件
text = """<a name="xx">Mr Brouce<Paul>hello kate</Paul><Kate>hello paul</Kate>xxx  <Paul>how are you?</Paul><Kate>fine, thank you, and you?</Kate></a>"""
tree = ET.fromstring(text)

print dir(tree)
print "children():", tree.getchildren()
print "keys():", tree.keys()
print "text:", tree.text

for item in tree.getchildren():
    print item.tag, ":", item.text


def transform(text):
    txt = """<rate speed='-1'/>"""
    template = """<VOICE REQUIRED='NAME=VW {tag}'/>{text}<silence msec='1000'/>"""
    tree = ET.fromstring(text)
    for item in tree.getchildren():
        print item.tag, ":", item.text
        txt += template.format(tag=item.tag, text=item.text)
            
    print  txt

transform(text)

