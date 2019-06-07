import random
from uuid import getnode as get_mac
import GramGen
import sys
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
def sumD(arr,D=0):
    ret_val=0
    for i in range(0,len(arr)):
        ret_val+=arr[i][D]
    return ret_val
def roll_mapp(mapp,x=None):
    #this function takes a mapp of "tickets"
    #and rolls a dice to see which tickets win, the more tickets you
    #have the more lickely you are to win
    if x == None:
        x=random.randrange(1,sumD(mapp)+1)
    mapp.sort()
    total=1
    for i in range(0,len(mapp)):
        if x < mapp[i][0] + total:
            return mapp[i][1]
        else:

            total+=mapp[i][0]

def get_rand(arr):
    return arr[random.randrange(0,len(arr))]
class node:
	def __init__(self,x,y,g):
		self.x = x
		self.y = y
		self.gen = g
		print('the mac is ' + str(int(get_mac())))
		self.seed = (get_mac()-1)*400+(y-1)*20+x
		#init the seed for this node
		print('seeding with ' + str(self.seed))
		random.seed(self.seed)	
		
		self.biome = self.gen.schema('{tag biome:noun_clause}')
		self.gen.addWordList('node_biome','node/biome.txt','node_noun',[self.biome])

		self.animals = []
		for i in range(0,random.randrange(0,11)):
			self.animals.append(self.gen.schema('{tag animal:noun_clause}'))
		self.gen.addWordList('node_animal','node/animals.txt','node_noun',self.animals)

		self.plants = []	
		for i in range(0,random.randrange(0,5)):
			self.plants.append(self.gen.schema('{sub plant:noun_clause}'))
		self.gen.addWordList('node_plant','node/plants.txt','node_noun',self.plants)
		
		self.towns = []
		while True:
			if random.randrange(0,100) < 30:
				self.towns.append(town(self.gen))
			else:
				break
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
class town:
	def __init__(self,g):
		self.buildings = []
		for i in range(1,11):
			self.buildings.append(g.schema('{tag building:noun_clause}'))	
		self.desc = g.schema('{tag town:noun_clause}')	 
g = GramGen.generator('gen.xml')
test = node(int(sys.argv[1]),int(sys.argv[2]),g)
sep = '-'*20
print('biome')
print(sep)
print(test.biome)
print('\nanimal')
print(sep)
for animal in test.animals:
	print(animal)
print('\nplants')
print(sep)
for plant in test.plants:
	print(plant)
print('\ntowns')
print(sep)
for town in test.towns:
	print(town.desc)
	for building in town.buildings:
		print('\t' + building)
print(test.enc())
print(test.desc())
