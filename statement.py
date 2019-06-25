import GramGen
import random
from math import ceil
from cdice import parse as parseDice

def getSides():
	return GramGen.pickRandom([20,12,10,8,6,4])
 
@GramGen.parse.get_enclosed(['(',')'])
def diegen(string,args):	
	if string == 'lvl':
		print('lvl:' + str(args['lvl']))
		lvl = args['lvl']
		if lvl <= 1:
			print('level is less than 1 at ' + str(lvl))
			#make sure that we get a valid lvl to pass to the number generator
			lvl = 2
		#they want us to use the lvl to generate a number
		return str(random.randrange(1,ceil(lvl)))
	elif string == 'dice':
		#they want us to return a dice
		sides = getSides()
		dice = ceil(lvl/sides) + random.randrange(1,3)	
		return str(dice) + 'd' + str(sides)
	else:
		#we assume that they want us to parse out a dice and return the result
		try:
			return str(parseDice(string))
		except:
			return 'None'
def dieSchema(g,lvl,schema='{tag frag:state}'):
	s2 = g.schema(schema) 
	return diegen(s2,['(',')'],lvl=lvl) 

def makeState(lvl):
	#need to load the full generator becuse of objects
	g = GramGen.generator('gen.xml')
	return dieSchema(g,lvl,'{tag frag || tag target:state}')
	
if __name__ == '__main__':	
	print(makeState(20))
