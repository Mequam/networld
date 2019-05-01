#!/usr/bin/python
import xml.etree.ElementTree as ET
import parse

@parse.get_enclosed()
def randStr(string):
    #need a way to specify the file that we want to parse, perhaps we only load the file into memory once?
    #or perhaps we make a generator class?
    #for now we just parse in the given file for quick testing
   
    return 'POTATO'
    #tree = ET.parse('gen.xml')
    #root = tree.getroot()
    #for node in root.findall('.//' + string):
    #    if node.text != None:
    #        return tree.xpath
    #return 'NULL'

def getAbs(root,tag,path=''):
    #need to get it to return none if the path that it follows does not contain the tag
    path += '/' + root.tag
    if root.tag == tag:
        return path
    else:
        #their tag is not equal, return any of their childrens tags if they are
        for child in root:
            lowpath = getAbs(child,tag,path)
            if lowpath != None:
                #one of the children found the correct path!, return the path that they give us
                return lowpath
        #none of our children or us have the tag, return None
        return None

tree = ET.parse('gen.xml')
root = tree.getroot()

print(getAbs(root,'insect'))
print(root.findall('.//insect')[0].tag)
print(randStr('testing123 [abc] [insect]'))

