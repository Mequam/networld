#TODO:need to make an inventory system for the players
#TODO:need to add more entities to the game that can spawn
#TODO:need to work on the network aspect of the game and allow for pcs to travel computers
#TODO:need to work on the corruption
import random
import menu
import GramGen
import make_node
import entity
import pickle
import parse
import combat
import entity
from math import floor
from uuid import getnode as get_mac

#this is a wrapper function for the game menu that is actualy the main loop of the game
#this function contains variables that can be used inside of the game loop
def updateArrs(grid_arr,entity_arr,player):
	try:
		#TODO: need to make it so the program can delete entities without
		#making the index that its targeting go over the length of the given array
		appended = 0
		for i in range(0,len(entity_arr)):
			if entity_arr[i].x != player.x and entity_arr[i].y != player.y:
				#somthing in the entity array is not on the same grid as the players, move it to the other array
				grid_arr.append(entity_arr[i])
				del entity_arr[i]
				appended += 1
		print('[Debug] party pos ' + str(player.x) + ' ' + str(player.y))
		for i in range(0,len(grid_arr)-appended):
			print('[Debug] checking entity at ' + str(grid_arr[i].x) + ' ' + str(grid_arr[i].y))
			if grid_arr[i].x == player.x and grid_arr[i].y == player.y:
				print('[*] found a matching entity!')
				entity_arr.append(grid_arr[i])
				#remove the entity from the grid array after placing it into the entity array
				del grid_arr[i]
		return True
	except:
		return False	
def game(partyname):	
	#the grid array represents any entity not on the same node as the players
	#load the grid and the partyname
	grid_arr = parse.loadArr('saves/grid.pkl')
	if not grid_arr:
		#we need to make cultures and then populate the world with cities
		print('[*] GENERATING THE GRID *^*')	
		grid_arr = []
		offset = 1

		random.seed(get_mac())
		cultures = []
		for i in range(2,5):
			cultures.append(entity.Culture())
		for culture in cultures:
			grid_arr.append(entity.Town(culture,random.randrange(1,21),random.randrange(1,21)))
		for town in grid_arr:
			print('[*] Town at ' + str(town.x) + ' ' + str(town.y))
	#the entity array represents entities in the same cords as the players
	entity_arr = parse.loadArr('saves/entity.pkl')
	if not entity_arr:
		print('no entities found, eh')
		entity_arr = []

	party = entity.Party() 
	party.load('saves/parties/'+partyname + '.pkl')


	#this variable stores the node that the party is currently at, so that way we dont have to re-compute the node EVERY
	#time we need to access a variable inside of it


	node = make_node.node(1,1)
	print(grid_arr)

	@menu.menu('networld')
	def game_menu(inputs,args):
		import entity
		split_i = inputs.split(' ')
		
		#this is where we actualy runn the game
		if split_i[0] == 'list' and len(split_i) > 1:
			if split_i[1] == 'members':
				print('[networld] listing party members')
				for player in party.players:
					print(player.name)
			if split_i[1] == 'towns':
				print('[networld] listing towns in your node')
				print(args[2])
				for e in args[2]:	
					if type(e) is type(entity.Town()):
						print(e.name + ', a ' + e.culture.name + ' town')
		elif split_i[0] in ['w','a','s','d']:	
			#TODO:make a movement function that takes wasd as inputs and spits out
			#really directions as outputs
			if split_i[0] == 'w':
				party.suby += 1
			elif split_i[0] == 'a':
				party.subx -= 1
			elif split_i[0] == 's':
				party.suby -= 1
			elif split_i[0] == 'd':
				#this could be an else statement, but were going to leave it as elif for readability
				party.subx += 1
			
			#they have performed a movement action, now see if that action is enough to move them out of the node that
			#they are in
			moved = False
			if party.subx > args[0].size[0]:
				moved = party.move(1,0,True)	
			elif party.subx < 0:
				moved = party.move(-1,0,True)
			elif party.suby > args[0].size[1]:
				moved = party.move(0,1,True)
			elif party.suby < 0:
				moved = party.move(0,-1,True)
			if moved:
				#first update the loaded node
				args[0] = make_node.node(party.x,party.y)
				print(args[0].desc())
				#set the parties sub x and y to the middle of that node
				party.suby = floor(args[0].size[1]/2)
				party.subx = floor(args[0].size[0]/2)
				
				#update the entity arrays to load all of the entities from the grid array that match the players current poss
				#are loaded correctly
				updateArrs(args[1],args[2],party)

				#update entitiys in the grids node only if the players leave their current node
				i = 0
				while i < len(args[1]):
					spawn = args[1][i].AI(party)
					if spawn == -1:
						del args[1][i]
						#avoid incrimenting i when we delete an entity so that way we dont go over the desired index
						continue
					elif spawn != None:
						args[1].append(spawn)
					i += 1
			else:
				#we didnt leave the node that we are in, there is a chance that we will spawn an encounter
				#roll for that chance
				if random.randrange(1,101) < 45:
					print('[*] ' + args[0].enc())
				else:
					print('[*] you move onwards unobscured')
			#update entities in the players node no matter what	
			for i in range(0,len(args[2])):
				#print(entity)
				spawn = args[2][i].AI(party)
				if spawn == -1:
					del args[2][i]
				elif spawn != None:
					args[2].append(spawn)
		elif split_i[0] == 'show' and len(split_i) > 1:
			if split_i[1] == 'all':
				print(args[0].toString())
			elif split_i[1] == 'plants':
				print(args[0].strPlants())
			elif split_i[1] == 'animals':
				print(args[0].strAnimals())
			elif split_i[1] == 'biome':
				print(args[0].biome)
		elif split_i[0] == 'tp' and len(split_i) > 2:
			#this command is for development ONLY
			try:
				party.x = int(split_i[1])
				party.y = int(split_i[2])
				args[0] = make_node.node(party.x,party.y)
				print('you see a ' + args[0].desc())
			except:
				return False
		elif split_i[0] == 'combat':
			#load all of the entites that are on the parties current grid and are biengs
			#into the bieng arr, as well as all of the players
			bieng_arr = []
			for entity in args[2]:
				if type(entity) is entity.Bieng:
					bieng_arr.append(Bieng)
			for player in party.players:	
				bieng_arr.append(player)
			#send the party and the loaded bieng array to the combat menu
			combat.combat_wrapper(bieng_arr,party)
		return True	
	
	print(grid_arr)	
	game_menu('main_menu',[node,grid_arr,entity_arr])
	#exit the main loop of the game
	parse.saveArr(grid_arr,'saves/grid.pkl')
	parse.saveArr(entity_arr,'saves/entity.pkl')	

@menu.menu('main menu')
def main(inputs):
	split_i = inputs.split(' ')
	if split_i[0].lower() == 'h':
		print('[main menu] list of commands')
		print('\t"start"		start the game')
		print('\t"party"   		enter the the party management menu')
		print('\t"q"       		exit the game')
	elif split_i[0] == 'new':
		i = parse.selectPrompt('[main menu] are you sure that you would like to start a new party?\n(y/n)> ',['y','n'])
		if i == 'y':
			p = entity.Party()
			p.prompt()
	elif split_i[0] == 'party':
		party()
	elif len(split_i) > 1 and split_i[0] == 'start':
		game(split_i[1])
	else:
		return False
	return True
print('[*] welcome to networld, at any time type \'?\' for a list of commands')
main()	
