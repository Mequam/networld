import GramGen
import random
from math import ceil
def getSides():
	return GramGen.pickRandom([20,12,10,8,6,4])
def diegen(string,lvl): 
	@GramGen.parse.get_enclosed(['(',')'])
	def dice(string):
		if string == 'number':
			return str(random.randrange(1,ceil(lvl/2)))
		else:
			sides = getSides()
			dice = ceil(lvl/sides) + random.randrange(1,3)	
			return str(dice) + 'd' + str(sides)
	return dice(string)
def dieSchema(g,lvl,schema='{tag frag:state}'):
	return diegen(g.schema(schema),lvl) 
#def parse(statement)

if __name__ == '__main__':
	g = GramGen.generator('gen.xml')
	print(dieSchema(g,20))
