import random
from uuid import getnode as get_mac
from time import time
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
		self.hostil = random.randrange(1,101)	
		
		self.biome = self.gen.schema('{tag biome:noun_clause}')
		self.gen.addWordList('node_biome','node_noun','node/biome.txt',[self.biome])
		

		#create a container node and fill it with node descriptions that have plants and animals each
		self.gen.addNode('node_biome','node_biome_sent')
		self.gen.addNode('node_biome_sent','node_biome_an')
		self.gen.addNode('node_biome_sent','node_biome_pl')

		animal_biome_sent = ['a {tag node_biome:node_noun} teaming with {tag node_animal:node_noun}s',
'a {node_biome:node_noun} full of {tag node_animal:node_noun}s']
		self.gen.addWordList('node_biome_an','node_noun2','node_biome_an',animal_biome_sent)
		
		plant_biome_sent = ['{tag node_biome:node_noun} specled with {tag node_plant:node_noun}s',
'{tag node_plant:node_noun} coverd {tag node_biome:node_noun}']
		self.gen.addWordList('node_biome_pl','node_noun2','node_biome_pl',plant_biome_sent)
			
		self.animals = []
		for i in range(0,random.randrange(0,11)):
			self.animals.append(self.gen.schema('{tag animal:noun_clause}'))
		self.gen.addWordList('node_animal','node_noun','node/animals.txt',self.animals)

		self.plants = []	
		for i in range(0,random.randrange(0,5)):
			self.plants.append(self.gen.schema('{sub plant:noun_clause}'))
		self.gen.addWordList('node_plant','node_noun','node/plants.txt',self.plants)
		
		super_an = ['{tag node_animal:node_noun} {tag life:verb_ing} from a {tag node_plant:node_noun}',
'{tag node_animal:node_noun} {tag life:verb_ing} a {sub noun && !sub animal:noun}',
'{tag life:verb_ing} {tag node_animal:node_noun}',
'{sub life || tag life || sup life:adj} {tag node_animal:node_noun}',
'{tag node_animal:node_noun} in a {tag dist:adj} {tag node_plant:node_noun}',
'{tag node_animal:node_noun}']
		self.gen.addWordList('node_animal','node_noun2','node/super.txt',super_an)
	
		encounters = ['you {sub sense:verb} somthing {sub noun || tag noun:adj}',
'you {sub sense:verb} a {tag node_animal:node_noun2}',
'a {tag node_animal:node_noun} trys to {tag noun:verb_ns} you',
'you see a {tag dist:adj} {tag node_animal:node_noun}',
'you see a {tag dist:adj} {tag node_animal:node_noun2}']	
		self.gen.addWordList('node','encounter','encounter',encounters)
		random.seed(time())
	#TODO: this function sucks, need to modify it becuse its generation is sloppy to say the least
	def enc(self):
		if len(self.plants) > 0 and len(self.animals) > 0:
			return self.gen.schema('{tag node:encounter}')
		elif len(self.plants) > 0:
			return self.gen.schema('{tag plant_enc:sent}')
		elif len(self.animals) > 0:
			return self.gen.schema('{tag animal_enc:sent}')
		else:
			return True
	def desc(self):
		if len(self.plants) > 1 and len(self.animals) > 1:
			return 'you see a ' + self.gen.schema('{sub node_biome_sent:node_noun2}')
		elif len(self.plants) > 1:
			return 'you see a ' + self.gen.schema('{tag node_biome_pl:node_noun2}')
		elif len(self.plants) > 1:
			return 'you see a ' + self.gen.schema('{tag node_biome_an:node_noun2}')
		else:
			return 'a barren ' + self.biome + ' streches out before you'
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
if __name__ == '__main__':
	n = node(1,5)
	print(n.animals)
	print(n.plants)
	print(n.desc())
