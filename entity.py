import parse
import random
import make_node
import menu as Menu 
import pickle

def makeStat():
	roll = 0
	for i in range(0,3):
		roll += random.randrange(1,7)
	return roll

#what makes a good AI?
#well that depends on the game that you are trying to run
#we will have two types of AI, a person, and a 
class Entity:
	#represents somthing that can move around the grid world as it sees fit
	def __init__(self,x,y):
		self.x = x
		self.y = y
	def move(self,dx,dy):
		self.x += dx
		self.y += dy
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
class Town(Entity):
	#each town needs to have a description and a culture
	#what would the culture look like?
	def __init__(self,culture):
		self.buildings = []
		for i in range(1,11):
			self.buildings.append(g.schema('{tag building:noun_clause}'))	
		self.desc = g.schema('{tag town:noun_clause}')	 
class Culture:
	def __init__(self):
		#generate a list of traits that the culture uses
		#this will be used when creating Towns
		
		#need a list of common profesions
		#need a description
		#need a list of common arcitectures
		#need a list of allowed adj
		print('fake')
class Bieng(Entity):
	#this class represents anything that the players can through damage at
	def __init__(self,x,y,lvl):
		self.x = x
		self.y = y
		self.str = makeStat() + random.randrange(1,lvl)
		self.dex = makeStat() + random.randrange(1,lvl)
		self.con = makeStat() + random.randrange(1,lvl)
		self.int = makeStat() + random.randrange(1,lvl)
		self.wis = makeStat() + random.randrange(1,lvl)
		self.cha = makeStat() + random.randrange(1,lvl)	
		self.hp = random.randrange(10,lvl*100)
		self.ac = random.randrange(18-lvl,20)-10

		#this array contains all of the effects placed on the bieng 
		self.eff = []	
	def statStr(self):
		ret_val = ''
		ret_val += 'str:' + str(self.str) + '\n'
		ret_val += 'dex:' + str(self.dex) + '\n'
		ret_val += 'con:' + str(self.con) + '\n'
		ret_val += 'int:' + str(self.int) + '\n'
		ret_val += 'wis:' + str(self.wis) + '\n'	
		ret_val += 'cha:' + str(self.cha)
		return ret_val
	
class Player(Bieng):
	def __init__(self,name=None):
		if name == None:
			self.name = 'J0hn Doe'
		else:
			self.name = name 	
		self.str = 0
		self.dex = 0
		self.con = 0
		self.int = 0
		self.wis = 0
		self.cha = 0	
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
							if self.str != 0:
								#append the old stat to the rolls array so that the user can access it again if they want to
								rolls.append(self.str)
							self.str = roll
						elif split_s[0] == 'dex':
							if self.dex != 0:
								#append the old stat to the rolls array so that the user can access it again if they want to
								rolls.append(self.dex)
							self.dex = roll
						elif split_s[0] == 'con':
							if self.con != 0:
								#append the old stat to the rolls array so that the user can access it again if they want to
								rolls.append(self.con)
							self.con = roll
						elif split_s[0] == 'int':
							if self.int != 0:
								#append the old stat to the rolls array so that the user can access it again if they want to
								rolls.append(self.int)
							self.int = roll
						elif split_s[0] == 'wis':
							if self.wis != 0:
								#append the old stat to the rolls array so that the user can access it again if they want to
								rolls.append(self.wis)
							self.wis = roll
						elif split_s[0] == 'cha':
							if self.cha != 0:
								#append the old stat to the rolls array so that the user can access it again if they want to
								rolls.append(self.cha)
							self.cha = roll
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
		if name == None:
			self.name = 'potato_party'
		else:
			self.name = name
		if players == None:
			self.players = []
		else:
			self.players = players
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
			self.save('saves/parties/'+self.name)
		except:
			print('[new party] OH NO, unable to save the party :(')	
	def addPlayer(self,player):
		self.players.append(player)
	def addPlayers(self,players):
		self.players += players
if __name__ == '__main__':
	#p = Party('TeamAvatar')
	
	#ang = Player('Ang')
	#ang.rand()
	#katara = Player('Katara')
	#katara.rand()
	#soka = Player('Soka')
	#soka.rand

	#p.addPlayers([ang,katara,soka])

	#p.save('saves/parties/' + p.name)
	
	p = Party()
	p.load('saves/parties/Venturians')
	print(p.name)
	for player in p.players:
		print(player.name)
		print('-'*20)
		print(player.statStr())
	#test = Player()
	#test.prompt()
