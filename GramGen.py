#!/usr/bin/python
import random
import xml.etree.ElementTree as ET
import parse
import menu
import sys
import bool_parse
def span_tree(func):
	#this is a recursive function that runs the given function on each of the nodes starting on the first node
	def ret_val(node,args):
		#run the function that we wrapp with the given arguments		
		func(node,args)		
		for child in node:		
			#the given node contains a child, take a recursive step down
			ret_val(child,args)
		#we made it past the for loop, the node does not contain any children so return true on success
		return True
	return ret_val
def pickRandom(arr):
	#this function returns a random element from an array
	return arr[random.randrange(0,len(arr))]
def get_text(filepath):
	f = open(filepath,'r')
	words = []
	line = f.readline()
	while line:
		words.append(line)
		line = f.readline()[0:-1]
	return words
#this function gets the absolute value of a node
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
#this function takes the root of the tree and a tag and returns the node that has that tag
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
#this function take an array and concatanates the values together using delimiter
def squish(arr,delim):
	ret_val = ''
	for word in arr:
		ret_val += word + delim
	return ret_val[:-1]
#this function gets the super class of a given node
def getSup(root,start):
	path = getAbs(root,start.tag)	
	split_path = path.split('/')
	superc = []
	wp = split_path[1:-1]
	for tag in wp:
		superc.append(getNodeTag(root,tag))
	return superc

#this function gets the subclass of a given node that contain a node
def getSub(start):		
	#any leaf on the bottom of the tree is ignored
	fa = start.findall('.//')
	i = 0
	while i < len(fa):
		if len(fa[i]) == 0:
			del fa[i]
		else:
			i += 1
	return fa 

#these are wrapper functions that use the above functions but instead of getting passed nodes they get passed tags
#not the most efficient thing in the world to go about getting the sub and supper classes this way as we find the nodes 
def getSubTag(tag):
	node = getNodeTag(root,tag)			
	return getSub(node)
def getSupTag(tag):
	node = getNodeTag(root,tag)
	return getSup(root,node)
#the following two functions wrap the above two functions to test if a given node is inside of the sub or sup of a given node
#with the same tag
def testSupTag(j,expr,f_arr,default,parenth,args):
	#get the tag that we want to use for the node
	tag = bool_parse.parse(expr[j+3:len(expr)],f_arr,default,parenth,args)	
	#get the target node for the sub or sup classes
	target = getNodeTag(args[0],tag)

	#if the node that we are testing is inside of the set that we are given
	if args[1] in getSup(args[0],target):
		return True
	else:
		return False
def testSubTag(j,expr,f_arr,default,parenth,args):
	#get the tag that we want to test from the recursive function
	tag = bool_parse.parse(expr[j+3:len(expr)],f_arr,default,parenth,args)
	#get the target for the sub or sup class from getNodeTag 
	target = getNodeTag(args[0],tag)
	if args[1] in getSub(target):
		return True
	else:
		return False
def testTag(j,expr,f_arr,default,parenth,args):
	tag = bool_parse.parse(expr[j+3:len(expr)],f_arr,default,parenth,args)
	target = getNodeTag(args[0],tag)
	if target.tag == tag:
		return True
	else:
		return False 
def getTextNode(node,Type):
	#this function returns the text inside of a given node
	#marked by the word tag that has the given type
	#if for some strange reason we are given a word node to begin with we
	#use that instead of searching through the nodes children for the required tag
	if node.tag == 'word' and node.attrib['type'] == Type:
		#the node that we were given was a word file pointer, so use its text	
		return get_text(node.text)
	for child in node:
		if child.tag == 'word' and child.attrib['type'] == Type:
			return get_text(child.text)
	#note technicaly a required statement, but it helps keep things readable
	return None

tree = ET.parse('gen.xml')
root = tree.getroot()

local_arr = [('sub',testSubTag),('sup',testSupTag),('tag',testTag)]

@parse.get_enclosed(['{','}'])
def schema(string):
	split_s = string.split(':')
	words = []
	
	@span_tree
	def loadNodes(node,args):	
		if bool_parse.parse_safe(split_s[0],bool_parse.arr,bool_parse.Default,['(',')'],[root,node]):
			text = getTextNode(node,args[0])
			if text:
				#the given node has text that we can load
				args[1] += text
	loadNodes(root,[split_s[1],words])
	return pickRandom(words)


print(schema('{sup animal:noun}'))

@menu.menu('main')
def main(arr):
	try:
		print(schema(arr))
		return True
	except:
		return False
if __name__ == '__main__':
	if len(sys.argv) == 1:
		main()
	else:
		print(schema(squish(sys.argv[1:],' ')))
