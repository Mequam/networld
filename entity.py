import random
import make_node
import menu as test
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
			fname = 'players/' + self.name + '.pkl'
		f = open(fname,'wb')
		pickle.dump(self.__dict__,f,pickle.HIGHEST_PROTOCOL)
		f.close()
		return True
	def rand(self):
		Bieng.__init__(self,0,0,2)	
	def prompt(self):
		rolls = []
		for i in range(0,6):
			rolls.append(makeStat())
		print('[new_player] type the stat you want to set folloewd by the index number of your roll')
		print('[new_player] type q to finish and create the new charicter')	
		print(rolls)	
		@test.menu('new_player')
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
	def __init__(self):
		self.x = 1
		self.y = 1
		self.players = []
	def addPlayer(self,player):
		self.players.append(player)
	def addPlayers(self,players):
		self.players += players
test = Party()
test.load('test.pkl')
for player in test.players:
	print(player.name)
	print('-'*20)
	print(player.statStr())
