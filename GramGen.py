#!/usr/bin/python
import random
import xml.etree.ElementTree as ET
import parse
def pickRandom(arr):
	#this function returns a random element from an array
	return arr[random.randrange(0,len(arr))]
def getAbs(root,tag,path=''):
    	#need to get it to return none if the path that it follows does not contain the ta
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
def getNodeTag(root,tag):
	#need to get it to return none if the path that it follows does not contain the ta	
	if root.tag == tag:
		return root
	else:
	#their tag is not equal, return any of their childrens tags if they are
		for child in root:
			mbyNode = getNodeTag(child,tag)
			if mbyNode != None:
			#one of the children found the correct path!, return the path that they give us
				return mbyNode
	#none of our children or us have the tag, return None
		return None
def squish(arr,delim):
	ret_val = ''
	for word in arr:
		ret_val += word + delim
	return ret_val[:-1]
def getSup(root,start):
	#this function gets the super class of a given node
	path = getAbs(root,start.tag)	
	split_path = path.split('/')
	superc = []

	wp = split_path[2:]
	i = len(wp)
	while i > 0:
		superc.append(root.find('./' + squish(wp[0:i],'/')))
		i -= 1
	return [root]+superc
def getSub(start):
	#print(f'[getSub] getting the sub of {start.tag}')
	#this function gets the subclass of a given node that contain a node
	#any leaf on the bottom of the tree is ignored
	fa = start.findall('.//')
	i = 0
	while i < len(fa):
		if len(fa[i]) == 0:
			del fa[i]
		else:
			i += 1
	return fa + [start]
#these are wrapper functions that use the above functions but instead of getting passed nodes they get passed tags
#not the most efficient thing in the world to go about getting the sub and supper classes this way as we find the nodes 
def getSubTag(tag):
	node = getNodeTag(root,tag)			
	return getSub(node)
def getSupTag(tag):
	node = getNodeTag(root,tag)
	return getSup(root,node)

#it would be really cool to make a generator class plus it would help with the decorators
#this parser does not clime the xml tree, it only looks for the file specified by {}
@parse.get_enclosed(['[',']'])
def pickSup(string):
	#[attri]
	s = string.split(':')
@parse.get_enclosed(['{','}'])
def make_rand(string):
    words = []
    try:
        f = open(string)
        data = f.readline()
        while data:
            words.append(data)
            data = f.readline()
        f.close()
        return words[random.randrange(0,len(words))][:-1]
    except:
        return 'None'
@parse.get_enclosed(['(',')'])
def make_randWTREE(string):
    return getAbs(root,string)
@parse.get_enclosed()
def randStr(string):
    #need a way to specify the file that we want to parse, perhaps we only load the file into memory once?
    #or perhaps we make a generator class?
    #for now we just parse in the given file for quick testing   
    for node in root.findall('.//' + string):
        return make_rand(node.text)
    return ''
def get_text(fname):
	f = open(fname,'r')
	data = f.readline()[:-1]
	words = [data]
	while data:
		#make sure that we dont read in newlines
		data = f.readline()[:-1]
		if data != '':
			#append the data that we read to the words array
			words.append(data)	
	f.close()
	return words
		
	
@parse.get_enclosed(['{','}'])
def schema(string):
	#this function takes a string and returns a random value from
	#the given node based on the syntax of the string
	#{tag:attr:[sub | sup | sup_e | sub_e]} <- syntax the function uses to find the sup
	
	#default to using the super class and inclusive
	sup = True
	e = False

	split_s = string.split(':')	
	if len(split_s) < 2 or len(split_s) > 3:
		#the programer or user did not supply us with a valid mapping
		#so return an error to the string
		return 'None'
	if len(split_s) == 3:
		#we have one of the optional arguments so use that to parse out our mode
		if split_s[2] == 'sub':
			sup = False
		elif split_s[2] == 'sub_e':
			sup = False
			e = True
		elif split_s[2] == 'sup_e':
			e = True
		elif split_s[2] != 'sup':
			#let them specify the default option if they feel so inclined,
			#even though we dont actualy change anything for it
			print('[ERROR] unrecognised constant!')
			return 'None'

	#this is a code snipit that we are going to use down bellow, its shelterd off as its own function to make our code easier to read
	def removeTag(arr,tag):
		for i in range(0,len(arr)):
			if arr[i].tag == tag:
				del arr[i]
				#we assume each node has no equal in the tree so break off here
				break
		return arr
	if sup and e:
		#exlive super class
		s = getSupTag(split_s[0])
		s = removeTag(s,split_s[0])
	elif sup and not e:
		#inclusive superclass
		s = getSupTag(split_s[0])
	elif not sup and e:
		#exlusive subclass	
		s = getSubTag(split_s[0])
		s = removeTag(s,split_s[0])		
	else:
		#inclusive subclass
		s = getSubTag(split_s[0])	
	words = []
	for node in s:
		#alright we have the node that we want now we just need to use it
		for child in node:
			if child.tag == 'word' and child.attrib['type'] == split_s[1]:
				
				try:	
					words += get_text(child.text)
				except:
					print('[WARNING] unable to load ' + child.text)
	#pick a single word from the pool of random words that we get from the schema value
	return pickRandom(words)

tree = ET.parse('gen.xml')
root = tree.getroot()
print(schema('{noun:color:sub} {bird:noun:sub}s dot the sky, waiting for the perfect oppourtunity to strike unfortionet {animal:noun:sub}, eating below them'))	
