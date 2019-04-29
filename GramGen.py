#!/usr/bin/python
import xml.etree.ElementTree as ET
import parse

@parse.get_enclosed()
def randStr(string):
    #need a way to specify the file that we want to parse, perhaps we only load the file into memory once?
    #or perhaps we make a generator class?
    #for now we just parse in the given file for quick testing
    root = ET.parse('gen.xml').getroot()
    for node in root.findall('.//' + string):
        if node.text != None:
            return node.text
    return 'NULL'
print(randStr('testing123 [abc] [insect]'))
#tree = ET.parse('list.xml')
#root = tree.getroot()
#for node in root.findall('.//apples'):
#    print(node.tag)
