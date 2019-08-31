import parse
import random
import make_node
import menu as Menu 
import pickle
import GramGen
import nameGen
import combat
from math import floor
from statement import makeState
def makeStat():
	roll = 0
	for i in range(0,3):
		roll += random.randrange(1,7)
	return roll

def roll(diceType,adv=0):
#in the future we might want to make cdice parse this for some
#interesting die rolls, but for now well leave it as this
	Dis = False
	if adv < 0:
		#we are disadvantaged
		adv *= -1
		Dis = True

	#this is the "normal" roll, the one that will happen every time regaurdless of advantage
	last_roll = random.randrange(1,diceType)	
	
	#this is the advantage loop roll a dice for each advantage and if that dice is greater (or less than if were dis)
	#than the last roll "topple" the last roll, ensureing that we get the number that best fits the desired advantage
	for i in range(0,int(adv)):
		roll = random.randrange(1,diceType)
		if Dis:
			if roll < last_roll:
				last_roll = roll
		else:
			if roll > last_roll:	
				last_roll = roll

	#return the number now that it ocntains the best roll for what we want
	return last_roll

#what makes a good AI?
#well that depends on the game that you are trying to run
#we will have two types of AI, a person, and a 
class Culture:
	def __init__(self,f=None):
		if f == None:
			
			#generate a new culture with the generator
			g = GramGen.generator('gen.xml')
			arcs = []
			for i in range(0,random.randrange(1,3)):
				#now this could generate the same style arcitecture more than once,
				#but thats ok, it simply means the culture this represents uses that style more
				#often
				arcs.append(g.schema('{tag building || sub building:arc}'))
			builds = []
			for i in range(0,random.randrange(2,5)):
				builds.append(g.schema('{(tag building || sub building) && !tag shop && !tag manor && !tag school:noun}'))
			matts = []
			for i in range(0,random.randrange(2,5)):
				matts.append(g.schema('{tag material:equ}'))
			
			occs = []
			for i in range(0,random.randrange(3,5)):
				occs.append(g.schema('{tag worker:noun}'))	
			
			#store a name generator for the culture and generate the cultures name
			self.nameg = nameGen.generator()
			self.name = self.nameg.makeWord()
			
			self.gen = g
			self.gen.addNode('noun','occ')
			self.gen.addWordList('occ','noun','occ',occs)
			
			self.gen.addNode('noun','build')
			self.gen.addWordList('build','noun','build',builds)
			
			self.gen.addNode('noun','arc')	
			self.gen.addWordList('arc','noun','arc',arcs)	
			
			self.gen.addNode('noun','matt')
			self.gen.addWordList('matt','noun','matt',matts)
			
			#now that the generator is loaded we add schemas to it
			scm = [
'{sub noun || tag noun && !(sub life || tag life):adj} {tag matt:noun} {tag build:noun}',
'{tag matt:noun} {tag arc:noun} {tag build:noun}'
,'{tag arc:noun} style {tag build:noun}',
'{tag build:noun}',
'{tag matt:noun} {tag build:noun}',
'{(tag noun || sub noun) && !(sub life || tag life):adj} {tag build:noun}'
]	
			self.gen.addWordList('build','scm','bscm',scm)
			
			scm = [
'{tag life || sub life || sup life:adj} {tag occ:noun}',
'{tag life || sub life || sup life:adj} {sub sentient:noun}',
]
			self.gen.addWordList('occ','scm','oscm',scm)
	def makeBuilding(self):
		return self.gen.schema('{tag build:scm}')
	def descPerson(self):
		return self.gen.schema('{tag occ:scm}')			

class Entity:
	#represents somthing that can move around the grid world as it sees fit
	def __init__(self,x=None,y=None):
		if x == None:
			self.x = random.randrange(1,21)
		else:
			self.x = x
		if y == None:
			self.y = random.randrange(1,21)
		else:
			self.y = y
	def move(self,dx,dy):
		#only set the movement if it does not move the entity off of the grid
		#all movement should be done through this function, so as not to move anything off of the mathmaticaly
		#playable grid
		x = self.x + dx
		y = self.y + dy
		
		if (x < 21 and x > 0) and (y < 21 and y > 0):
			self.x = x
			self.y = y
			return True
		return False
	def AI(self,party):
		print('[*] running AI for ' + str(self))
	def load(self,fname):
		try:
			f = open(fname,'rb')
			buff = pickle.load(f)	
			f.close()

			self.__dict__.update(buff)
			return True
		except:
			return False
	def save(self,fname):
		f = open(fname,'wb')
		pickle.dump(self.__dict__,f,pickle.HIGHEST_PROTOCOL)
		f.close()
		return True
class Settler(Entity):
	#this is a type of AI that will explore around the grid and try and settle down to create a new city
	count = 0
	def __init__(self,culture,x=None,y=None):
		Entity.__init__(self,x,y)
		self.culture = culture
		self.name = culture.nameg.makeWord()
		Settler.count += 1
	def AI(self,party):
		#the settler has no idea where home is, so it wanders aimlessly seaching
		#for a place to place a new spawner
		
		#pick a random valid direction to move
		x = random.randrange(-1,2)
		y = random.randrange(-1,2)	
		self.move(x,y)

		#only spawn a new town if there are less than 20 towns
		if random.randrange(1,100) < make_node.node(self.x,self.y).hostil and Town.count < 10:	
			return Town(self.culture,self.x,self.y)
		else:
			#delete ourselfs if we fail our survival check
			if random.randrange(1,101) < 50:
				#remove a count for the settler
				self.count -= 1	
				return -1
class Town(Entity):
	#each town needs to have a description and a culture
	#what would the culture look like?`
	count = 0
	def __init__(self,culture,x=None,y=None,name=None):
		#steal the entity init for x and y
		Entity.__init__(self,x,y)
		#set name
		if name == None:
			self.name = culture.nameg.makeWord()
		else:
			self.name = name
		#set culture
		self.culture = culture
		
		#set the buildings that exist within the town
		self.buildings = []	
		for i in range(1,11):
			self.buildings.append(culture.makeBuilding())
		self.ppl = []
		for i in range(0,random.randrange(floor(len(self.buildings)/2)+1,len(self.buildings)+2)):
			self.ppl.append(self.culture.nameg.makeWord())
		self.ppl_desc = []
		for name in self.ppl:
			self.ppl_desc.append(self.culture.descPerson())
		self.g = GramGen.generator('gen.xml')
		self.g.addNode('noun','TownG')
		self.g.addNode('TownG','TownsFolk')
		self.g.addNode('TownG','TownBuilding')
		self.g.addNode('TownG','TownEncounter')

		self.g.addWordList('TownsFolk','town_noun','TownsFolk',self.ppl)
		self.g.addWordList('TownBuilding','town_noun','TownBuilding',self.buildings)
			
		encounters = ['theres a {tag noun || sub noun:noun} {tag prep || sub prep:prep} the {tag TownBuilding:town_noun}',
				'{tag TownsFolk:town_noun} is {tag prep || sub prep:prep} a {tag dist:adj} {tag TownBuilding:town_noun}',
				'you {tag sense_far:verb} {tag TownsFolk:town_noun} {sub noun || tag noun:verb_ing} a {tag noun || sub noun:noun}',
				'you {tag sense_far:verb} a {tag TownsFolk:town_noun} {tag noun || sub noun:verb_ing}',
				'you {sub sense:verb} somthing {tag noun || sub noun:adj}']	
		self.g.addWordList('TownEncounter','town_sent','TownEncounter',encounters)

		

		self.g.addNode('TownG','occ')
		self.g.addWordList('occ','town_noun','occ',self.culture.gen.lists['occ'])
		
		self.g.addNode('TownG','TownDesc')
		#this needs to create descriptions of the town
		desc = ['town of {tag occ:town_noun}s',
			'town of {sub sentient:noun}s',
			'{tag noun || sub noun:adj} town',
			'town full of {tag noun || sub noun:noun}s',
			'{sub noun || tag noun:noun} town']	
		self.g.addWordList('TownDesc','town_desc','TownDesc',desc)
				

		self.g.addNode('TownG','TownView')
		self.g.addWordList('TownView','town_desc','TownView',['{tag prep:prep} you you {tag sense_far:verb} a {tag TownDesc:town_desc}'])
		#set the description for the town
		self.desc = self.g.schema('{tag TownView:town_desc}')
		
		#incriment the total of all of the towns, that way the game knows when to STOP spawning towns
		Town.count += 1
	def AI(self,party):
		#have a random chance of spawning a settler based on the hostlity of the node the town finds itself in	

		#there should never be very many settlers on the board at once
		if random.randrange(1,101) < make_node.node(self.x,self.y).hostil and Settler.count < 5:	
			return Settler(self.culture,self.x,self.y)
		if party.x == self.x and party.y == self.y:
			#the party found our town!, tell them whats up
			#this generation could probably use some more work, but for now its ok
			print('[*] ' + self.desc)
	def shell(self,local_arr,party,cultures):
		#this is a menu used to interact with a given town	
		inp = ['a']
		while inp[0] != 'q':
			inp = input('(town)> ').split(' ')
			if inp[0] == 'combat':	
				bieng_arr = []
				for thing in local_arr:
					if type(thing) is Bieng:
						bieng_arr.append(thing)
				for player in party.players:
					bieng_arr.append(player)
				
				combat.combat_wrapper(bieng_arr,party,cultures)
			elif inp[0] == 'list':
				if len(inp) > 1:
					#they gave us somthing to list
					sucess = False
					if 'people' in inp or 'all' in inp:
						sucess = True
						for i in range(0,len(self.ppl)):
							print(str(i+1) + ':' + self.ppl[i])
					if 'all' in inp or ('buildings' in inp and 'people' in inp):
						print('-'*10)
					if 'buildings' in inp or 'all' in inp:
						sucess = True
						for build in self.buildings:
							print(build)
					if not sucess:
						print('[town] ERROR: unrecognised list target')
						print('[town] options are buildings or people')			
				else:
					#they did not tell us what they want to see, complain!
					print('[town] ERROR: somthing to list is required')
					print('[town] options are buildings or people')	
			if inp[0] == 'desc':
				if len(inp) > 1:
					
					#they gave us arguments
					if inp[1] == 'all':
						for i in range(0,len(self.ppl)):
							print(self.ppl[i] + ':' + self.ppl_desc[i])
					else:
						index = 0
						try:
							index = int(inp[1])-1
							if -1 < index < len(self.ppl):
								found = True
						except:
							print('[Debug] searching for name')
							found = False
							for i in range(0,len(self.ppl)):
								if self.ppl[i] == inp[1]:
									index = i
									found = True
									break
						if found:
							print(self.ppl_desc[index])
						else:
							print('[town] ERROR: unable to find ' + str(index))
				else:
					#we were not given any arguments, complain
					print('[town] ERROR: person name or index required')
			else:
				pass
			
class Bieng(Entity):
	#this class represents anything that the players can through damage at
	def __init__(self,x,y,lvl):
		self.actions = 2
		self.x = x
		self.y = y

		if lvl <= 1:
			lvl = 2
		stre = makeStat() + random.randrange(1,lvl)
		dex = makeStat() + random.randrange(1,lvl)
		con = makeStat() + random.randrange(1,lvl)
		inte = makeStat() + random.randrange(1,lvl)
		wis = makeStat() + random.randrange(1,lvl)
		cha = makeStat() + random.randrange(1,lvl)	
		
		self.stats = {'str':stre,'dex':dex,'con':con,'int':inte,'wis':wis,'cha':cha}
		
		self.hp = random.randrange(10,lvl*100)
		self.ac = random.randrange(18-lvl,20)-10
		self.thaco = 20 - lvl
		self.name = 'NA'
		self.lvl = lvl
			
		self.adv = {'str':0,'dex':0,'con':0,'int':0,'wis':0,'cha':0}
	def rollHit(self,target):
		if self.check(['hit','attack','str']) >= self.thaco - target.ac:
			return True
		else:
			return False	
	def check(self,given_stats,dieType=20):
		mod = 0
		for stat in self.stats:
			if stat in given_stats:
				mod += floor((self.stats[stat] - 10)/2)
		adv = 0
		for stat in self.stats:
			if stat in given_stats:
				adv += self.adv[stat]
		#now return a disadvantaged/advantaged roll
		return roll(20,adv)+mod
	def loot(self):
		#this function returns a string that represents loot that the players can use
		return makeState(self.lvl)
	
	def ToScreen(self,command=['all']):
		print(self.name)
		print('-'*len(self.name))
		if 'hp' in command or 'all' in command:
			print('hp:' + str(self.hp),end=' ')
		if 'ac' in command or 'all' in command:
			print('ac:' + str(self.ac))
		elif 'hp' in command:
			#make sure that we print a new line after the hp ac line no matter what
			print()
		for stat in self.stats:
			if stat in command or 'all' in command or 'stats' in command:
				print(stat + ':' + str(self.stats[stat]))
		if 'adv' in command or 'all' in command:
			print(self.adv)
	def addAdv(self,stat,num):
		if stat not in self.adv:
			self.adv[stat] = num
			return False
		self.adv[stat] += num
		return True

	#this function is used to roll a stat with the advantages of two different stats
	#it is ment to be a wrapper function ONLY and should not be called outside of the object
	def statStr(self):
		ret_val = ''
		for stat in self.stats:
			ret_val += stat + ':' + str(self.stats[stat]) + '\n'
		return ret_val
	
class Player(Bieng):
	def __init__(self,name=None):
		Bieng.__init__(self,1,1,1)
		if name == None:
			self.name = 'J0hn Doe'
		else:
			self.name = name 	
		
		self.stats = {'str':0,'dex':0,'con':0,'int':0,'wis':0,'cha':0}		
		self.adv = {'str':0,'dex':0,'con':0,'int':0,'wis':0,'cha':0}	
	def load(self,fname=None):
		if fname==None:
			fname = 'players/' + self.name + '.pkl'
		try:
			f = open(fname,'rb')
			buff = pickle.load(f)	
			f.close()

			self.__dict__.update(buff)
			return True
		except:
			return False
	def save(self,fname=None):
		if fname == None:
			fname = 'saves/players/' + self.name + '.pkl'
		f = open(fname,'wb')
		pickle.dump(self.__dict__,f,pickle.HIGHEST_PROTOCOL)
		f.close()
		return True
	def rand(self):
		Bieng.__init__(self,0,0,2)	
	def prompt(self):
		#get the players name before we do anything else
		print('[new_player] what would you like your name to be?')	
		self.name = input('(name)> ')
		print('[new_player] are you sure that you want ' + self.name + ' to be your name?')
		ansr = input('(y/n)> ')

		while ansr != 'y':
			self.name = input('(name)> ')
			print('[new_player] are you sure that you want ' + self.name + ' to be your name?')
			ansr = input('(y/n)> ')
		print('[new_player] set name to ' + self.name)
		print('-'*20+'\n')	
	
		#initilise the rolls of the new player
		rolls = []
		for i in range(0,6):
			rolls.append(makeStat())
		print('[new_player] type the stat you want to set folloewd by the index number of your roll')
		print('[new_player] type q to finish and create the new charicter')	
		print(rolls)	
		
		@Menu.menu('new_player')
		def menu(string):	
			split_s = string.split(' ')


			if split_s[0] == 's':
	 			print(self.statStr())
			#they have given us a command to set one of the stats
			if split_s[0] == 'str' or split_s[0] == 'dex' or split_s[0] == 'con' or split_s[0] == 'int' or split_s[0] == 'wis' or split_s[0] == 'cha':
				if len(split_s) < 2:
					print('[new_player] index required!')	
					return False
				else:
					try:
						x = int(split_s[1])
					except:
						print('[new_player] index not a number!')
						return False
					if x >= len(rolls)+1 or 0 >= x:
						print('[new_player] invalid index!')
					else:
						#we have been given a valid stat, use it to set the target stat	
						index = int(split_s[1]) - 1
						roll = rolls[index]
						print('setting ' + split_s[0] + ' to ' + str(roll))	
						if split_s[0] == 'str':
							if self.stats['str'] != 0:
								#append the old stat to the rolls array so that the user can access it again if they want to
								rolls.append(self.str)
							self.stats['str'] = roll
						elif split_s[0] == 'dex':
							if self.stats['dex'] != 0:
								#append the old stat to the rolls array so that the user can access it again if they want to
								rolls.append(self.stats['dex'])
							self.stats['dex'] = roll
						elif split_s[0] == 'con':
							if self.stats['con'] != 0:
								#append the old stat to the rolls array so that the user can access it again if they want to
								rolls.append(self.stats['con'])
							self.stats['con'] = roll
						elif split_s[0] == 'int':
							if self.stats['int'] != 0:
								#append the old stat to the rolls array so that the user can access it again if they want to
								rolls.append(self.stats['int'])
							self.stats['int'] = roll
						elif split_s[0] == 'wis':
							if self.stats['wis'] != 0:
								#append the old stat to the rolls array so that the user can access it again if they want to
								rolls.append(self.stats['wis'])
							self.stats['wis'] = roll
						elif split_s[0] == 'cha':
							if self.stats['cha'] != 0:
								#append the old stat to the rolls array so that the user can access it again if they want to
								rolls.append(self.stats['cha'])
							self.stats['cha'] = roll
						else:
							print('[new_player] this should never happen, godspeed user')
						del rolls[index]
						print(rolls)
			return True
		menu()
		while len(rolls) != 0:
			print('[new_player] ERROR! not all stats have been set')
			menu()
class Party(Entity):
	def __init__(self,name=None,players=None):
		self.x = 1
		self.y = 1
		self.subx = 0
		self.suby = 0
		if name == None:
			self.name = 'potato_party'
		else:
			self.name = name
		if players == None:
			self.players = []
		else:
			self.players = players
	def save(self,fname=None):
		if fname == None:
			fname = 'saves/parties/' + self.name + '.pkl'
		Entity.save(self,fname)
	def prompt(self):
		#the user wants to start a new party, so prompt them for the desired information
	
	#get the parties name, make absolutly sure that the name is one the user wants
		self.name = input('what should the parties name be?\n(name)> ')
		inp = parse.selectPrompt('[new party] are you sure thats what you want the parties name to be?\n(y/n)> ',['y','n'])
		while inp != 'y':
			self.name = input('what should the parties name be?\n(name)> ')
			inp = parse.selectPrompt('[new party] are you sure thats what you want the parties name to be?(y/n)> \n(y/n)',['y','n'])
		
		print('[new party] set party name to ' + self.name)
		print('\n[new party] now we add players to the party!')
		while True:
			charic = Player()
			charic.prompt()
			self.addPlayer(charic)
			print('-'*20+'\n')
			if parse.selectPrompt('[new party] want to stop making charicters?\n(y/n)> ',['y','n']) == 'y':
				break
		print('[new party] saving the party!')
		try:
			self.save()
		except:
			print('[new party] OH NO, unable to save the party :(')	
	def addPlayer(self,player):
		self.players.append(player)
	def addPlayers(self,players):
		self.players += players
	def move(self,x,y,careSub=False):
		if not Entity.move(self,x,y):
			print('[*] you see a pulsating wall of energy in front of you')
			print('[*] it seems to buzz as you touch it, preventing you from moving in this direction')
			if careSub:
				#we dont want any of the sub x and sub y values to indicate movement, so figure out which one to decriment or incriment
				if self.subx < 0:
					print('resetting subx')
					self.subx += 1
				elif self.suby < 0:
					self.suby += 1
				elif x+self.x > 20:
					self.subx -= 1
				elif y+self.y > 20:
					self.suby -= 1 
			return False
		return True
if __name__ == '__main__':
	c = Culture()
	t = Town(c)
	print(t.desc)
	a = Bieng(1,1,1)
	b = Bieng(1,1,1)
	p = Party()
	t.shell([a,b],p)
