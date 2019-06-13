import random
from uuid import getnode as get_mac
import GramGen
import nameGen
def cat2num(cat):
    if cat == 'insane':
        return 11
    elif cat == 'high':
        return 8
    elif cat == 'medium':
        return 6
    elif cat == 'low':
        return 4
    elif cat == 'scarce':
        return 1
    else:
        print('[*] returning 0!')
        return 0
def get_cat(x=None):
    return roll_mapp([(1,'insane'),(1,'scarce'),(3,'medium'),(2,'high'),(2,'low')]) 

def get_rand(arr):
    return arr[random.randrange(0,len(arr))]

class node:
	def __init__(self,x,y):
		self.x = x
		self.y = y
		self.gen = GramGen.generator('gen.xml')
		#print('the mac is ' + str(int(get_mac())))
		self.seed = (get_mac()-1)*400+(y-1)*20+x
		#init the seed for this node
		#print('seeding with ' + str(self.seed))
		random.seed(self.seed)


		#give the size array four different sizes, one corisponding to each direction
		self.size = [random.randrange(1,8),random.randrange(1,8)]
		self.biome = self.gen.schema('{tag biome:noun_clause}')
		self.gen.addWordList('node_biome','node_noun','node/biome.txt',[self.biome])
		self.hostil = random.randrange(1,101)
		self.animals = []
		for i in range(0,random.randrange(0,11)):
			self.animals.append(self.gen.schema('{tag animal:noun_clause}'))
		self.gen.addWordList('node_animal','node_noun','node/animals.txt',self.animals)

		self.plants = []	
		for i in range(0,random.randrange(0,5)):
			self.plants.append(self.gen.schema('{sub plant:noun_clause}'))
		self.gen.addWordList('node_plant','node_noun','node/plants.txt',self.plants)
		
	#TODO: this function sucks, need to modify it becuse its generation is sloppy to say the least
	def enc(self):
		if len(self.plants) > 0 and len(self.animals) > 0:
			return self.gen.schema('{sub encounter:sent}')
		elif len(self.plants) > 0:
			return self.gen.schema('{tag plant_enc:sent}')
		elif len(self.animals) > 0:
			return self.gen.schema('{tag animal_enc:sent}')
		else:
			return True
	def desc(self):
		return self.gen.schema('{tag node_biome:sent}')
	def getPlant(self):
		return self.gen.schema('{tag node_plant:node_noun}')
	def strPlants(self):
		ret_val = ''
		for plant in self.plants:
			ret_val += plant + '\n'
		return ret_val[:-1]
	def strAnimals(self):
		ret_val = ''
		for animal in self.animals:
			ret_val += animal + '\n'
		return ret_val[:-1]
	def toString(self):
		ret_val = ''
		sep = '-'*20+'\n'
		ret_val += self.biome + '\n'
		ret_val += sep
		ret_val += 'animals\n'
		ret_val += sep
		ret_val	+= self.strAnimals() + '\n\n'
		
		ret_val += 'plants\n'
		ret_val += sep
		ret_val += self.strPlants()
		return ret_val
