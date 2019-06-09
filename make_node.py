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
class Culture:
	def __init__(self,f=None):
		if f == None:
			#generate a new culture with the generator
			g = GramGen.generator('gen.xml')
			self.arcs = []
			for i in range(0,random.randrange(1,5)):
				#now this could generate the same style arcitecture more than once,
				#but thats ok, it simply means the culture this represents uses that style more
				#often
				self.arcs.append(g.schema('{tag building || sub building:arc}'))
			self.builds = []
			for i in range(0,random.randrange(2,5)):
				self.builds.append(g.schema('{(tag building || sub building) && !tag shop && !tag manor && !tag school:noun}'))
			self.matts = []
			for i in range(0,random.randrange(2,5)):
				self.matts.append(g.schema('{tag material:equ}'))
			self.nameg = nameGen.generator()
			self.name = self.nameg.makeWord()

			path = 'saves/' + self.name
			
			#write the word lists that we generated to files, the gramer generators
			#dependence on files are quite frusterating	
			f = open(path + '.bld','w')
			for build in self.builds:
				f.write(build + '\n')
			f.close()

			f = open(path + '.mat','w')
			for mat in self.matts:
				f.write(mat + '\n')
			f.close()

			f = open(path + '.arc')
			for arc in self.arcs:
				f.write(arc + '\n')
			f.close()
			
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
		
		#self.towns = []
		#while True:
	#		if random.randrange(0,100) < 30:
#				self.towns.append(town(self.gen))
#			else:
#				break
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

if __name__ == '__main__':
	c = Culture()
	print(c.name)
	print(c.arcs)
	print(c.builds)
	print(c.matts)
